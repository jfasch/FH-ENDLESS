cmake_minimum_required(VERSION 3.20)
project(MC-SysFSTemperature)

if ("${CMAKE_C_COMPILER_ID}" STREQUAL GNU)
  string(APPEND CMAKE_C_FLAGS "-Wall -Werror")
endif()

add_executable(MC-SysFSTemperature 
  main.cpp

  sensor.h
  sensor.cpp
  can-bus.h
  can-bus.cpp
  error.h
  error.cpp
)
