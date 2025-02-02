Niryo Robot Joints Interface Package
====================================

| This package handles packages related to the robot's joints controller.
| It provides an interface to :wiki_ros:`ros_control` 

Joints Interface Node
--------------------------
The ROS Node is made to :
 - Interface robot's motors to joint trajectory controller, from :wiki_ros:`ros_control` package
 - Create a controller manager, from :wiki_ros:`controller_manager` package, to provides the infrastructure to load, unload, start and stop controllers.
 - Interface with motors calibration
 - Initialize motors parameters


Parameters - Joints Interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table:: Joint Interface's Parameters 
   :header-rows: 1
   :widths: auto
   :stub-columns: 0
   :align: center

   *  -  Name
      -  Description
   *  -  ``ros_control_loop_frequency``
      -  | control loop frequency.
         | Default : '100.0'
   *  -  ``publish_learning_mode_frequency``
      -  | Publish rate for learning mode state.
         | Default : '2.0'
   *  -  ``calibration_timeout``
      -  | Waiting time in ms between 2 commands during the calibration process.
         | Default : '30'
   *  -  ``calibration_file``
      -  | File directory where is saved motors calibration value.
         | Default : '/home/niryo/niryo_robot_saved_files/stepper_motor_calibration_offsets.txt'

Published Topics - Joints Interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table:: Joint Interface's Published Topics
   :header-rows: 1
   :widths: auto
   :stub-columns: 0
   :align: center

   *  -  Name
      -  Message Type
      -  Description
   *  -  ``/niryo_robot/learning_mode/state``
      -  :std_msgs:`Bool`
      -  Learning mode state

Services - Joints Interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table:: Joint Interface Package Services
   :header-rows: 1
   :widths: auto
   :stub-columns: 0
   :align: center

   *  -  Name
      -  Message Type
      -  Description
   *  -  ``/niryo_robot/joints_interface/calibrate_motors``
      -  :ref:`SetInt`
      -  Start motors calibration - value can be 1 for auto calibration, 2 for manual
   *  -  ``/niryo_robot/joints_interface/request_new_calibration``
      -  :ref:`Trigger`
      -  Unset motors calibration
   *  -  ``niryo_robot/learning_mode/activate``
      -  :ref:`Trigger`
      -  Either activate or deactivate learning mode

Dependencies - Joints Interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- :wiki_ros:`hardware_interface <hardware_interface>`
- :wiki_ros:`controller_manager <controller_manager>`
- :ref:`dynamixel_driver <Niryo Robot Dynamixel Driver Package>`
- :ref:`stepper_driver <Niryo Robot Stepper Driver Package>`
- :ref:`niryo_robot_msgs <Niryo Robot Messages Package>`
