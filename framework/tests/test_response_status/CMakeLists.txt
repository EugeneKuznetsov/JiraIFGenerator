cmake_minimum_required(VERSION 3.16)

set(target test_restponse_status)

set(headers test_response_status.h)
set(sources test_response_status.cpp)

add_executable(${target} ${headers} ${sources})
target_link_libraries(${target} PRIVATE Qt5::Test PRIVATE framework_types PRIVATE cutemockserver)
