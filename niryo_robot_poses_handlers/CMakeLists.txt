cmake_minimum_required(VERSION 2.8.3)
project(niryo_robot_poses_handlers)

find_package(catkin REQUIRED
  COMPONENTS
  geometry_msgs
  message_generation
  moveit_msgs
  niryo_robot_msgs
)

add_message_files(
  FILES
  NiryoPose.msg
  Trajectory.msg
  Workspace.msg
)

add_service_files(
  DIRECTORY srv
  FILES
  GetPose.srv
  GetTargetPose.srv
  GetTrajectory.srv
  GetWorkspaceRatio.srv
  GetWorkspaceRobotPoses.srv
  ManagePose.srv
  ManageTrajectory.srv
  ManageWorkspace.srv
)

catkin_python_setup()

generate_messages(
  DEPENDENCIES
  geometry_msgs
  moveit_msgs
  niryo_robot_msgs
)

catkin_package()

include_directories(
  ${catkin_INCLUDE_DIRS}
)

#############
## Testing ##
#############
find_package(rostest REQUIRED)

add_rostest(launch/rpi_poses_handlers.test)
add_rostest(launch/simulation_poses_handlers.test)
