cmake_minimum_required(VERSION 3.16)

set(target framework_types)

set(headers responsestatus.h definitions.h)
set(sources responsestatus.cpp)

add_library(${target} OBJECT ${headers} ${sources})
target_include_directories(${target} INTERFACE $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>)
target_link_libraries(${target} PUBLIC Qt5::Qml)
