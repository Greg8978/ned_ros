Niryo Robot Dynamixel Driver Package
=====================================

| This package handles dynamixel motors communication through dynamixel sdk 
| It provides an interface to :wiki_ros:`dynamixel_sdk` 

Dynamixel Driver Node
--------------------------
The ROS Node is made to :
 - Send commands to dynamixel motor
 - Receive dynamixel motors data

Parameters - Dynamixel Driver
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table:: Dynamixel Driver's Parameters 
   :header-rows: 1
   :widths: auto
   :stub-columns: 0
   :align: center

   *  -  Name
      -  Description
   *  -  ``dxl_hardware_control_loop_frequency``
      -  | control loop frequency.
         | Default : '100.0'
   *  -  ``dxl_hardware_write_frequency``
      -  | Write frequency.
         | Default : '50.0'
   *  -  ``dxl_hardware_read_data_frequency``
      -  | Read frequency.
         | Default : '15.0'
   *  -  ``dxl_hardware_read_status_frequency``
      -  | Read dynmixels status frequency.
         | Default : '0.5'
   *  -  ``dxl_hardware_check_connection_frequency``
      -  | Check dynmixels connection frequency.
         | Default : '2.0'
   *  -  ``dxl_motor_id_list``
      -  | list of dynmixels ID
         | Default : '[2,3,6]'
   *  -  ``dxl_motor_type_list``
      -  | list of dynmixels type
         | Default : '["xl430","xl430","xl320"]'

Services - Dynamixel Driver
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table:: Dynmixel Driver Package Services
   :header-rows: 1
   :widths: auto
   :stub-columns: 0
   :align: center

   *  -  Name
      -  Message Type
      -  Description
   *  -  ``niryo_robot/dynamixel_driver/set_dxl_leds``
      -  :ref:`SetInt`
      -  Control dynmixel LED
   *  -  ``niryo_robot/dynamixel_driver/send_custom_dxl_value``
      -  :ref:`dynamixel_driver/SendCustomDxlValue<SendCustomDxlValue (Service)>`
      -  Send a custom dynamixel command

Dependencies - Dynamixel Driver
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- :wiki_ros:`dynamixel_sdk` 
- :ref:`niryo_robot_msgs <Niryo Robot Messages Package>`

Services & Messages files - Dynamixel Driver
--------------------------------------------------

SendCustomDxlValue (Service)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../../niryo_robot_hardware_stack/dynamixel_driver/srv/SendCustomDxlValue.srv
   :language: rostype

DxlMotorHardwareStatus (Message)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../../niryo_robot_hardware_stack/dynamixel_driver/msg/DxlMotorHardwareStatus.msg
   :language: rostype

DxlMotorCommand (Message)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../../niryo_robot_hardware_stack/dynamixel_driver/msg/DxlMotorCommand.msg
   :language: rostype

DxlArrayMotorHardwareStatus (Message)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../../niryo_robot_hardware_stack/dynamixel_driver/msg/DxlArrayMotorHardwareStatus.msg
   :language: rostype
