from glob import glob
from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension

shared_memory = Pybind11Extension(
    "shared_memory",
    ["src/shared_memory.cpp", "src/SharedMemory.cpp", "src/ShmMessageQueue.cpp"],  # Sort source files for reproducibility
    cxx_std=14,
)
ext_modules = [
    shared_memory,
]

setup(name="shared_memory",
      packages=["shared_memory"],
      ext_package="shared_memory",
      ext_modules=ext_modules,
)
