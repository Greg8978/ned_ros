Niryo Robot Poses Handlers Package
======================================================

This package is in charge of dealing with transforms, workspace, grips and
trajectories.


Poses Handlers Node
--------------------------

Description - Poses Handlers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ROS Node is made of several services to deal with transforms, workspace, grips and
trajectories.

The namespace used is : |namespace_emphasize|

Workspaces
"""""""""""""

A workspace is defined by 4 markers that form a rectangle. With the help of the robot's calibration
tip, the marker positions are learnt. The camera returns poses (x, y, yaw) relative to the workspace.
We can then infer the absolute object pose in robot coordinates.

Grips
"""""""""

When we know the object pose in robot coordinates, we can't directly send this pose to the robot because
we specify the target pose of the tool_link and not of the actual TCP (tool center point). Therefore
we introduce the notion of grip. Each end effector has its own grip that specifies where to place the
robot with respect to the object. Currently, the notion of grip is not part of the python/tcp/blockly
interface because it would add an extra layer of complexity that is not really necessary for the moment.
Therefore we have a default grip for all tools that is selected automatically based on the current
tool id. However, everything is ready if you want to define custom grips, e.g. for custom tools or
for custom grip positions.

The vision pick loop
""""""""""""""""""""""""""""""

1. Camera detects object relative to markers and sends x<sub>rel</sub>, y<sub>rel</sub>, yaw<sub>rel</sub>
2. The object is placed on the workspace, revealing the object pose in robot coordinates x, y, z, roll, pitch, yaw
3. The grip is applied on the absolute object pose and gives the pose the robot should move to.

Poses & Trajectories
""""""""""""""""""""""""""""""""""

List of Poses

Parameters - Poses Handlers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. list-table:: Poses Handlers' Parameters
   :header-rows: 1
   :widths: auto
   :stub-columns: 0
   :align: center

   *  -  Name
      -  Description
   *  -  ``workspace_dir``
      -  Path to the Workspace storage mother folder
   *  -  ``grip_dir``
      -  Path to the Grip storage mother folder
   *  -  ``poses_dir``
      -  Path to the Poses storage mother folder
   *  -  ``trajectories_dir``
      -  Path to the Trajectory storage mother folder

Services - Poses Handlers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table:: Poses Handlers' Services
   :header-rows: 1
   :widths: auto
   :stub-columns: 0
   :align: center

   *  -  Name
      -  Message Type
      -  Description

   *  -  ``manage_workspace``
      -  :ref:`ManageWorkspace<ManageWorkspace (Service)>`
      -  Save/Delete a workspace
   *  -  ``get_workspace_ratio``
      -  :ref:`GetWorkspaceRatio<GetWorkspaceRatio (Service)>`
      -  Get ratio of a workspace
   *  -  ``get_workspace_list``
      -  :ref:`GetNameDescriptionList`
      -  Get list of workspaces' name & description
   *  -  ``get_workspace_poses``
      -  :ref:`GetWorkspaceRobotPoses<GetWorkspaceRobotPoses (Service)>`
      -  Get workspace's robot poses

   *  -  ``get_target_pose``
      -  :ref:`GetTargetPose<GetTargetPose (Service)>`
      -  Get saved programs' name

   *  -  ``manage_pose``
      -  :ref:`ManagePose<ManagePose (Service)>`
      -  Save/Delete a Pose
   *  -  ``get_pose``
      -  :ref:`GetPose<GetPose (Service)>`
      -  Get Pose
   *  -  ``get_pose_list``
      -  :ref:`GetNameDescriptionList`
      -  Get list of poses' name & description

   *  -  ``manage_trajectory``
      -  :ref:`ManageTrajectory<ManageTrajectory (Service)>`
      -  Save/Delete a Trajectory
   *  -  ``get_trajectory``
      -  :ref:`GetTrajectory<GetTrajectory (Service)>`
      -  Get Trajectory
   *  -  ``get_trajectory_list``
      -  :ref:`GetNameDescriptionList`
      -  Get list of trajectories' name & description


All these services are available as soon as the node is started

Dependencies - Poses Handlers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- :msgs_index:`geometry_msgs`
- :msgs_index:`moveit_msgs`
- :ref:`niryo_robot_msgs <Niryo Robot Messages Package>`
- :wiki_ros:`tf`


Services & Messages files - Poses Handlers
----------------------------------------------

GetPose (Service)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../../niryo_robot_poses_handlers/srv/GetPose.srv
   :language: rostype


GetTargetPose (Service)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../../niryo_robot_poses_handlers/srv/GetTargetPose.srv
   :language: rostype


GetTrajectory (Service)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../../niryo_robot_poses_handlers/srv/GetTrajectory.srv
   :language: rostype


GetWorkspaceRatio (Service)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../../niryo_robot_poses_handlers/srv/GetWorkspaceRatio.srv
   :language: rostype


GetWorkspaceRobotPoses (Service)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../../niryo_robot_poses_handlers/srv/GetWorkspaceRobotPoses.srv
   :language: rostype


ManagePose (Service)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../../niryo_robot_poses_handlers/srv/ManagePose.srv
   :language: rostype


ManageTrajectory (Service)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../../niryo_robot_poses_handlers/srv/ManageTrajectory.srv
   :language: rostype


ManageWorkspace (Service)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../../niryo_robot_poses_handlers/srv/ManageWorkspace.srv
   :language: rostype


NiryoPose (Message)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../../niryo_robot_poses_handlers/msg/NiryoPose.msg
   :language: rostype


Trajectory (Message)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../../niryo_robot_poses_handlers/msg/Trajectory.msg
   :language: rostype


Workspace (Message)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../../niryo_robot_poses_handlers/msg/Workspace.msg
   :language: rostype



.. |namespace| replace:: /niryo_robot_poses_handlers/
.. |namespace_emphasize| replace:: ``/niryo_robot_poses_handlers/``
.. |package_path| replace:: ../../../niryo_robot_poses_handlers
