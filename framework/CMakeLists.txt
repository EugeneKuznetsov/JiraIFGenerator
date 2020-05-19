cmake_minimum_required(VERSION 3.16)

find_package(Qt5 REQUIRED COMPONENTS Qml Network Test)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)

set(target framework)

add_subdirectory(network)
add_subdirectory(types)
add_subdirectory(tests)

set(headers endpoint.h)
set(sources endpoint.cpp)

add_library(${target} STATIC ${headers} ${sources})
target_include_directories(${target} INTERFACE $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>)
target_link_libraries(${target} PRIVATE Qt5::Qml PRIVATE framework_network PRIVATE framework_types)
