cmake_minimum_required(VERSION 3.10)
project(mqtt_demo_cpp)

set(CMAKE_CXX_STANDARD 17)

find_package(PahoMqttC REQUIRED)
find_package(PahoMqttCpp REQUIRED)

add_executable(robot robot.cpp)
target_link_libraries(robot PahoMqttC::paho-mqtt3c PahoMqttCpp::paho-mqttpp3)

add_executable(control control.cpp)
target_link_libraries(control PahoMqttC::paho-mqtt3c PahoMqttCpp::paho-mqttpp3)
