cmake_minimum_required(VERSION 3.16)

set(target test_session)

set(headers test_session.h)
set(sources test_session.cpp)

add_executable(${target} ${headers} ${sources})
target_link_libraries(${target} PRIVATE Qt5::Test PRIVATE framework_network PRIVATE cutemockserver)
