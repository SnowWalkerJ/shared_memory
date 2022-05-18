from glob import glob
from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension

extension = Pybind11Extension(
    "shared_memory",
    sorted(glob("src/*.cpp")),  # Sort source files for reproducibility
    cxx_std=14,
)

ext_modules = [
    extension
]

setup(name="shared_memory",
      packages=["shared_memory"],
      ext_package="shared_memory",
      ext_modules=ext_modules,
)
