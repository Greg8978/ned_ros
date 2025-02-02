Niryo Robot Programs Manager Package
======================================================

This package is in charge of interpreting/running/saving programs.
It is used by Niryo Studio.


Programs Manager Node
--------------------------
The ROS Node is made of several services to deal with the storage and running of
programs

Call are not available from the Python ROS Wrapper, as it made to run its programs
with the Python ROS Wrapper

The namespace used is : |namespace_emphasize|

Parameters - Programs Manager
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. list-table:: Programs Manager's Parameters
   :header-rows: 1
   :widths: auto
   :stub-columns: 0
   :align: center

   *  -  Name
      -  Description
   *  -  ``autorun_file_name``
      -  Name of the file containing auto run infos
   *  -  ``programs_dir``
      -  Path to the Program storage mother folder

Services - Programs Manager
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table:: Programs manager Services
   :header-rows: 1
   :widths: auto
   :stub-columns: 0
   :align: center

   *  -  Name
      -  Message Type
      -  Description
   *  -  ``execute_program``
      -  :ref:`ExecuteProgram<ExecuteProgram (Service)>`
      -  Execute a program
   *  -  ``execute_program_autorun``
      -  :ref:`Trigger`
      -  Execute autorun program
   *  -  ``get_program``
      -  :ref:`GetProgram<GetProgram (Service)>`
      -  Retrieve saved program
   *  -  ``get_program_autorun_infos``
      -  :ref:`GetProgramAutorunInfos<GetProgramAutorunInfos (Service)>`
      -  Get autorun settings
   *  -  ``get_program_list``
      -  :ref:`GetProgramList<GetProgramList (Service)>`
      -  Get saved programs' name
   *  -  ``manage_program``
      -  :ref:`ManageProgram<ManageProgram (Service)>`
      -  Save and Delete programs
   *  -  ``set_program_autorun``
      -  :ref:`SetProgramAutorun<SetProgramAutorun (Service)>`
      -  Set autorun settings
   *  -  ``stop_program``
      -  :ref:`Trigger`
      -  Stop the current running program


All these services are available as soon as the node is started
whereas on standalone mode or not

Dependencies - Programs Manager
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- :ref:`niryo_robot_commander <Niryo Robot Commander Package>`
- :ref:`niryo_robot_msgs <Niryo Robot Messages Package>`
- `python-yaml <https://pyyaml.org/wiki/PyYAMLDocumentation/>`_
- :msgs_index:`std_msgs`


Services & Messages files - Programs Manager
----------------------------------------------

ExecuteProgram (Service)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../../niryo_robot_programs_manager/srv/ExecuteProgram.srv
   :language: rostype


GetProgram (Service)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../../niryo_robot_programs_manager/srv/GetProgram.srv
   :language: rostype


GetProgramAutorunInfos (Service)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../../niryo_robot_programs_manager/srv/GetProgramAutorunInfos.srv
   :language: rostype


GetProgramList (Service)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../../niryo_robot_programs_manager/srv/GetProgramList.srv
   :language: rostype


ManageProgram (Service)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../../niryo_robot_programs_manager/srv/ManageProgram.srv
   :language: rostype


SetProgramAutorun (Service)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../../niryo_robot_programs_manager/srv/SetProgramAutorun.srv
   :language: rostype


ProgramLanguage (Message)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../../niryo_robot_programs_manager/msg/ProgramLanguage.msg
   :language: rostype


ProgramLanguageList (Message)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../../niryo_robot_programs_manager/msg/ProgramLanguageList.msg
   :language: rostype


ProgramList (Message)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../../niryo_robot_programs_manager/msg/ProgramList.msg
   :language: rostype



.. |namespace| replace:: /niryo_robot_programs_manager/
.. |namespace_emphasize| replace:: ``/niryo_robot_programs_manager/``
.. |package_path| replace:: ../../../niryo_robot_programs_manager
