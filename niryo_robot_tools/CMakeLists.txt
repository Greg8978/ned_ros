cmake_minimum_required(VERSION 2.8.3)
project(niryo_robot_tools)

find_package(catkin REQUIRED
  COMPONENTS
  actionlib_msgs
  message_generation
  std_msgs
)

add_message_files(
  FILES
  ToolCommand.msg
)

add_action_files(
  DIRECTORY action
  FILES
  Tool.action
)

generate_messages(
  DEPENDENCIES
  actionlib_msgs
  std_msgs
)

catkin_package(
  CATKIN_DEPENDS
  message_runtime)

include_directories(
  ${catkin_INCLUDE_DIRS}
)
