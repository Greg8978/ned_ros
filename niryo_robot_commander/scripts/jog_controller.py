#!/usr/bin/env python
"""
The Jog Controller allows to easily command the robot manually. It means that you can use
mouse input, Leap Motion, Wii Controller or even Image processing to calculate determine
where the robot should go
This controller can be used :
- directly by using ROS Topic | ROS Low Level (see the file client_jog_interface_mouse.py which shows how to use
a mouse to control the robot)
- with Python ROS Wrapper | "Medium" Level
- through the TCP server | High Level
"""

import rospy
import math
from niryo_robot_commander.command_enums import ArmCommanderException

# Command Status
from niryo_robot_msgs.msg import CommandStatus

# Messages
from geometry_msgs.msg import Quaternion
from sensor_msgs.msg import JointState
from std_msgs.msg import Bool
from trajectory_msgs.msg import JointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint

from niryo_robot_msgs.msg import HardwareStatus
from niryo_robot_msgs.msg import RobotState

# Services
from niryo_robot_commander.srv import GetIK
from niryo_robot_commander.srv import JogShift, JogShiftRequest
from niryo_robot_msgs.srv import SetBool
from niryo_robot_msgs.srv import GetBool


class JogController:
    def __init__(self, parameters_validator):
        # - Publisher which publishes if JogController is enabled
        self._enabled = False
        self._jog_enabled_publisher = rospy.Publisher('/niryo_robot/jog_interface/is_enabled',
                                                      Bool, queue_size=1)
        rospy.Timer(rospy.Duration(1.0 / rospy.get_param("~jog_enable_publish_rate")),
                    self._publish_jog_enabled)
        self._check_disable_jog_timer = None
        self._last_command_timer = rospy.get_time()

        self._publish_jog_enabled()

        # Service to enable Jog Controller
        rospy.Service('/niryo_robot/jog_interface/enable',
                      SetBool, self.__callback_enable_jog)

        # - Direct publisher to joint controller
        self._joint_trajectory_publisher = rospy.Publisher(
            rospy.get_param("~joint_controller_name") + '/command', JointTrajectory,
            queue_size=3)
        # Publishing rate
        self._timer_rate = rospy.get_param("~jog_timer_rate_sec")
        self._publisher_joint_trajectory_timer = None

        # - Subscribers
        self._joint_states = None
        rospy.Subscriber('/joint_states', JointState,
                         self.__callback_joint_states)

        self._robot_state = None
        rospy.Subscriber('/niryo_robot/robot_state', RobotState,
                         self.__callback_sub_robot_state)

        self.__learning_mode_on = None
        rospy.Subscriber('/niryo_robot/learning_mode/state', Bool,
                         self.__callback_sub_learning_mode)

        self.__hardware_status = None
        rospy.Subscriber('/niryo_robot_hardware_interface/hardware_status', HardwareStatus,
                         self.__callback_hardware_status)

        # - Service
        rospy.Service('/niryo_robot/jog_interface/jog_shift_commander', JogShift,
                      self.__callback_jog_commander)

        # - Kinematics
        self._new_robot_state = RobotState()
        self._last_robot_state_published = RobotState()
        self._service_ik = rospy.ServiceProxy('/niryo_robot/kinematics/inverse', GetIK)

        # - Values Init
        self._shift_mode = None
        self._last_target_values = [0.0 for _ in range(6)]
        self._target_values = None

        # Validation
        self.__parameters_validator = parameters_validator
        jog_limits = rospy.get_param("~jog_limits")
        self.__pose_translation_max = jog_limits["translation"]
        self.__pose_rotation_max = jog_limits["rotation"]
        self.__joints_rotation_max = jog_limits["joints"]

        # - Others param
        self.__time_without_jog_limit = rospy.get_param("~time_without_jog_limit")

    # - Callbacks

    def __callback_sub_robot_state(self, robot_state):
        self._robot_state = robot_state

    def __callback_joint_states(self, joint_states_msg):
        self._joint_states = joint_states_msg.position[:6]

    def __callback_sub_learning_mode(self, learning_mode):
        self.__learning_mode_on = learning_mode.data

    def __callback_hardware_status(self, msg):
        self.__hardware_status = msg

    def __callback_enable_jog(self, req):
        if req.value:
            return self.enable()
        else:
            return self.disable()

    def __callback_jog_commander(self, msg):
        if self.__hardware_status.calibration_needed or self.__hardware_status.calibration_in_progress:
            return CommandStatus.ABORTED, "Cannot send command cause Jog because calibration is not done"
        if self.__learning_mode_on:
            try:
                rospy.wait_for_service('/niryo_robot/learning_mode/activate', 2)
                service = rospy.ServiceProxy('/niryo_robot/learning_mode/activate', SetBool)
                result = service(True)
                if result.status != CommandStatus.SUCCESS:
                    return CommandStatus.ABORTED, "Cannot send command cause Jog because learning mode is on and" \
                                                  " cannot be disabled"
                rospy.sleep(0.1)
            except (rospy.ROSException, rospy.ServiceException):
                return CommandStatus.ABORTED, "Error while trying to turn Off learning mode"

        if not self._enabled:
            ret, str_msg = self.enable()
            if ret == CommandStatus.ABORTED:
                return CommandStatus.ABORTED, "Cannot send command cause Jog is not activated and cannot be"
        self._last_command_timer = rospy.get_time()

        shift_mode = msg.cmd
        if shift_mode != self._shift_mode:
            self._reset_last_pub()
            self._shift_mode = shift_mode

        shift_command = list(msg.shift_values)
        if shift_mode == JogShiftRequest.POSE_SHIFT:
            shift_command[:3] = [min([v, math.copysign(self.__pose_translation_max, v)], key=abs) for v in
                                 shift_command[:3]]
            shift_command[3:] = [min([v, math.copysign(self.__pose_rotation_max, v)], key=abs) for v in
                                 shift_command[3:]]
            try:
                success, potential_target_values = self._get_new_joints_w_ik(shift_command)
            except ArmCommanderException as e:
                return e.status, "Error while validating pose : {}".format(e.message)
            if not success:
                return CommandStatus.NO_PLAN_AVAILABLE, "Unable to find on invert kinematics for the target position"
            else:
                self._target_values = potential_target_values
        else:
            # Accumulate multiple commands if they come faster than the publish rate
            shift_command = [min([v, math.copysign(self.__joints_rotation_max, v)], key=abs) for v in shift_command]
            target_values = [actual + shift for actual, shift in
                             zip(self._last_target_values, shift_command)]

            target_values = self.__limit_params_joints(target_values)

            try:
                self.__validate_params_joints(target_values)
            except ArmCommanderException as e:
                return e.status, "Error while validating joints : {}".format(e.message)

            self._target_values = target_values
            self._new_robot_state = RobotState()
        return CommandStatus.SUCCESS, "Command send"

    # - Publishers

    def _publish_jog_enabled(self, *_):
        msg = Bool()
        msg.data = self._enabled
        try:
            self._jog_enabled_publisher.publish(msg)
        except rospy.ROSException:
            return

    def _publish_joint_trajectory(self, *_):
        if not self._enabled:
            return
        if self._target_values is None:
            return
        msg = JointTrajectory()
        msg.header.stamp = rospy.Time.now()
        msg.joint_names = ['joint_1', 'joint_2', 'joint_3', 'joint_4', 'joint_5', 'joint_6']

        point = JointTrajectoryPoint()
        point.positions = self._target_values
        point.time_from_start = rospy.Duration(self._timer_rate)

        msg.points = [point]

        self._joint_trajectory_publisher.publish(msg)

        # Reset Target
        self._target_values = None

        # Save state for next time
        self._last_target_values = point.positions
        self._last_robot_state_published = self._new_robot_state

    # - Setters & Getters
    @staticmethod
    def can_be_enable():
        """
        Check if Jog Controller can be enabled
        Basically, it checks if commander is running

        :return: Bool indicating if Controller can be enabled
        :rtype: bool
        """
        try:
            rospy.wait_for_service('/niryo_robot_commander/is_active')
            is_active_service = rospy.ServiceProxy('/niryo_robot_commander/is_active', GetBool)
            response = is_active_service()
            return not response.value
        except rospy.ServiceException:
            return False

    def enable(self):
        """
        Enable jog controller if possible

        :return: status, message
        :rtype: (GoalStatus, str)
        """
        if not self.can_be_enable():
            msg_str = "Jog Controller - Wait for the end of command to enable Jog Controller"
            rospy.logwarn(msg_str)
            return CommandStatus.ABORTED, msg_str

        rospy.wait_for_message('/niryo_robot/robot_state', RobotState, timeout=2)
        rospy.wait_for_message('/joint_states', JointState, timeout=2)
        self._enabled = True
        self._reset_last_pub()
        self._last_command_timer = rospy.get_time()
        self._publisher_joint_trajectory_timer = rospy.Timer(rospy.Duration(self._timer_rate),
                                                             self._publish_joint_trajectory)
        self._check_disable_jog_timer = rospy.Timer(rospy.Duration(1.0 / rospy.get_param("~jog_enable_publish_rate")),
                                                    self._check_for_disable)
        msg_str = "Jog Controller - Enabled"
        rospy.loginfo(msg_str)
        return CommandStatus.SUCCESS, msg_str

    def disable(self):
        """
        Disable jog controller

        :return: status, message
        :rtype: (GoalStatus, str)
        """
        if not self._enabled:
            msg_str = "Jog Controller - Already Disabled"
            rospy.loginfo(msg_str)
            return CommandStatus.SUCCESS, msg_str

        self._enabled = False
        self._shift_mode = None
        self._target_values = None
        # Shutdown timer (Only launched when jog enabled)
        self._publisher_joint_trajectory_timer.shutdown()
        self._publisher_joint_trajectory_timer = None
        self._check_disable_jog_timer.shutdown()
        self._check_disable_jog_timer = None

        msg_str = "Jog Controller - Disabled"
        rospy.loginfo(msg_str)
        return CommandStatus.SUCCESS, msg_str

    def is_enabled(self):
        """
        Return the if Jog Controller is enable

        :return: True if enable else False
        :rtype: bool
        """
        return self._enabled

    # - Useful Functions
    def _check_for_disable(self, *_):
        if not self.is_enabled():
            return
        delta_time = rospy.get_time() - self._last_command_timer
        if delta_time > self.__time_without_jog_limit:
            self.disable()

    def _reset_last_pub(self):
        self._last_target_values = self._joint_states
        self._last_robot_state_published = self._robot_state

    def _get_new_joints_w_ik(self, shift_command):
        self._new_robot_state = RobotState()
        self._new_robot_state.position.x = self._last_robot_state_published.position.x + shift_command[0]
        self._new_robot_state.position.y = self._last_robot_state_published.position.y + shift_command[1]
        self._new_robot_state.position.z = self._last_robot_state_published.position.z + shift_command[2]
        self._new_robot_state.rpy.roll = self._last_robot_state_published.rpy.roll + shift_command[3]
        self._new_robot_state.rpy.pitch = self._last_robot_state_published.rpy.pitch + shift_command[4]
        self._new_robot_state.rpy.yaw = self._last_robot_state_published.rpy.yaw + shift_command[5]
        self._new_robot_state.orientation = Quaternion()

        self.__validate_params_pose(self._new_robot_state)

        response = self._service_ik(self._new_robot_state)
        return response.success, response.joints

    def __validate_params_pose(self, new_robot_state):
        self.__parameters_validator.validate_position(new_robot_state.position)
        self.__parameters_validator.validate_orientation(new_robot_state.rpy)

    def __validate_params_joints(self, joints):
        self.__parameters_validator.validate_joints(joints)

    def __limit_params_joints(self, joints):
        joints_limits = self.__parameters_validator.get_joints_limits()
        for j, joint_value in enumerate(joints):
            joints[j] = max(joints_limits[j].lower, min(joints_limits[j].upper, joint_value))
        return joints


if __name__ == '__main__':
    pass
