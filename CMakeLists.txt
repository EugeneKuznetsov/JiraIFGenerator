cmake_minimum_required(VERSION 3.16)

project(ifgenerator VERSION 0.4)

set(generator_work_dir ${CMAKE_CURRENT_LIST_DIR}
    CACHE INTERNAL "Working directory for JiraIFGenerator")

function(generate_endpoints wadl_file output_dir class_prefix)
    find_package(Python3 REQUIRED COMPONENTS Interpreter)
    if(class_prefix STREQUAL "")
    else()
        set(class_prefix "--prefix=${class_prefix}")
    endif()
    message(STATUS "Generating Jira endpoints from ${wadl_file}")
    message(STATUS "   Output directory for endpoints: ${output_dir}")
    execute_process(COMMAND ${Python3_EXECUTABLE} "-m"
        "generator" ${wadl_file} ${output_dir} ${class_prefix}
        WORKING_DIRECTORY ${generator_work_dir}
        RESULT_VARIABLE generator_result
        OUTPUT_VARIABLE generator_output)
    if(generator_result)
        message(FATAL_ERROR "JiraIFGenerator failure")
    endif()
endfunction()

add_subdirectory(framework)
