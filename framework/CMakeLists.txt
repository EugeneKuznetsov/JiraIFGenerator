cmake_minimum_required(VERSION 3.16)

find_package(Qt5 REQUIRED COMPONENTS Core Gui Qml Network Test QuickTest)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)

set(target framework)

add_subdirectory(network)
add_subdirectory(types)
add_subdirectory(tests)
