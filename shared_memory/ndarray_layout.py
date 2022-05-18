import itertools

from .shared_memory import SharedMemory
from .layout import Layout, align

import functools
import operator
import struct
from typing import Tuple

import numpy as np


class NdArrayLayout(Layout):
    sign = b"a"

    def __init__(self, dtype: np.dtype, shape: Tuple[int]):
        self.dtype = np.dtype(dtype)
        self.shape = shape

    @align(8)
    def size(self) -> int:
        header_size = struct.calcsize("cci{size}i".format(size=len(self.shape)))
        data_size = functools.reduce(operator.mul, self.shape, self.dtype.itemsize)
        return align(self.dtype.alignment, header_size) + data_size

    def dump(self, mem: memoryview):
        format = "cci{size}i".format(size=len(self.shape))
        values = [self.sign, self.dtype.char.encode(), len(self.shape)] + list(self.shape)
        struct.pack_into(format, mem, 0, *values)

    @classmethod
    def load(cls, mem: memoryview):
        sign, dtype_char, dims = struct.unpack_from("cci", mem, 0)
        if sign != cls.sign:
            raise TypeError("unknown data type")
        dtype = np.dtype(dtype_char)
        shape = struct.unpack_from(f"{dims}i", mem, 8)
        buffer = mem[align(dtype.alignment, struct.calcsize(f"cci{dims}i")):]
        return np.ndarray(shape, dtype, buffer)

    @classmethod
    def from_data(cls, array: np.ndarray):
        dtype = array.dtype
        shape = array.shape
        return cls(dtype, shape)
