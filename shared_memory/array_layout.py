from .layout import Layout, align
from .util import load_mem

import struct


class ArrayLayout(Layout):
    sign = b"a"

    def __init__(self, layout: Layout, count: int):
        self.layout = layout
        self.count = count

    @align(8)
    def size(self) -> int:
        return struct.calcsize("cL") + self.layout.size() * self.count

    def dump(self, mem: memoryview):
        struct.pack_into("cL", mem, 0, self.sign, self.count)
        offset = struct.calcsize("cL")

        for _ in range(self.count):
            self.layout.dump(mem[offset:])
            offset += self.layout.size()

        assert offset == self.size()

    @classmethod
    def load(cls, mem: memoryview):
        sign, entries = struct.unpack_from("cL", mem, 0)
        if sign != cls.sign:
            raise TypeError("unknown data type")

        result = []

        offset = struct.calcsize("cL")
        for _ in range(entries):
            data, layout = load_mem(mem[offset:])
            result.append(data)
            offset += layout.size()

        return result
