import struct

from .layout import Layout, align

import pickle


class PickleLayout(Layout):
    sign = b"p"

    def __init__(self, item):
        self.data = pickle.dumps(item)

    @align(8)
    def size(self) -> int:
        return len(self.data) + struct.calcsize("cL")

    def dump(self, mem: memoryview):
        size = len(self.data)
        struct.pack_into(f"cL{size}s", mem, 0, self.sign, size, self.data)

    @classmethod
    def load(cls, mem: memoryview):
        sign, size = struct.unpack_from("cL", mem, 0)
        if sign != cls.sign:
            raise TypeError("unknown data type")
        return pickle.loads(mem[16:16+size].tobytes())
