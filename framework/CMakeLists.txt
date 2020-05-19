cmake_minimum_required(VERSION 3.16)

find_package(Qt5 REQUIRED COMPONENTS Qml Network Test)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)

set(target ${PROJECT_NAME})

add_subdirectory(network)
add_subdirectory(types)
add_subdirectory(tests)

set(headers endpoint.h)
set(sources endpoint.cpp)

add_library(${target} OBJECT ${headers} ${sources})
target_include_directories(${target} INTERFACE $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>)
target_link_libraries(${target} PUBLIC Qt5::Qml PUBLIC framework_network PUBLIC framework_types)
