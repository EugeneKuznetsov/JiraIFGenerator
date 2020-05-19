cmake_minimum_required(VERSION 3.16)

set(target framework_network)

set(headers reply.h session.h)
set(sources reply.cpp session.cpp)

add_library(${target} OBJECT ${headers} ${sources})
target_include_directories(${target} INTERFACE $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>)
target_link_libraries(${target} PUBLIC Qt5::Network PUBLIC framework_types)
