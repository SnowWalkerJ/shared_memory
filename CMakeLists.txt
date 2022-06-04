cmake_minimum_required(VERSION 3.10)
project(shm_array)

set(CMAKE_CXX_FLAGS_DEBUG "-g -ggdb -O0")
set(CMAKE_CXX_FLAGS_RELEASE -O3)
set(CMAKE_CXX_STANDARD 14)
set(PYTHON_EXECUTABLE "/Users/snowwalkerj/opt/anaconda3/bin/python")

include_directories($ENV{HOME}/opt/anaconda3/include)
find_package(pybind11 REQUIRED)
pybind11_add_module(shared_memory src/shared_memory.cpp src/SharedMemory.cpp src/SharedMemory.h src/Common.h src/ShmMessageQueue.cpp)
