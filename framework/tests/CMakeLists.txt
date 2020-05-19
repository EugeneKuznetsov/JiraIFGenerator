cmake_minimum_required(VERSION 3.16)

set(BUILD_CUTE_MOCK_SERVER_TESTS OFF)
add_subdirectory(mockserver)

add_subdirectory(test_reply)
add_subdirectory(test_session)
add_subdirectory(test_response_status)

