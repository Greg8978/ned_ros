cmake_minimum_required(VERSION 2.8.3)
project(niryo_robot_python_ros_wrapper)

find_package(catkin REQUIRED COMPONENTS
)
catkin_python_setup()

catkin_package()

include_directories(
  ${catkin_INCLUDE_DIRS}
)

#############
## Testing ##
#############
find_package(rostest REQUIRED)

add_rostest(launch/rpi_python_wrapper.test)
add_rostest(launch/simulation_python_wrapper.test)
