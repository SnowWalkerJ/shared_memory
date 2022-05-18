from .layout import Layout, align
from .util import load_mem

import struct
from typing import Dict


class StructLayout(Layout):
    sign = b"s"

    def __init__(self, layout: Dict[str, Layout]):
        self.layout = layout

    @align(8)
    def size(self) -> int:
        size = 16
        for key in self.layout:
            size += 8 + 8 + align(8, len(key))
        for layout in self.layout.values():
            size += layout.size()
        return size

    def dump(self, mem: memoryview):
        struct.pack_into("cL", mem, 0, self.sign, len(self.layout))
        entry_offset = 16

        offset = 16
        for key in self.layout:
            offset += 16 + align(8, len(key))

        for key, layout in self.layout.items():
            struct.pack_into("LL", mem, entry_offset, len(key), offset)
            entry_offset += 16
            for i, b in enumerate(key.encode()):
                mem[entry_offset + i] = b
            entry_offset += align(8, len(key))
            layout.dump(mem[offset:])
            offset += layout.size()

        assert offset == self.size()

    @classmethod
    def load(cls, mem: memoryview):
        sign, entries = struct.unpack_from("cL", mem, 0)
        if sign != cls.sign:
            raise TypeError("unknown data type")

        result = {}

        entry_offset = 16
        for i in range(entries):
            key_size, data_offset = struct.unpack_from("LL", mem, entry_offset)
            entry_offset += 16
            key = mem[entry_offset: entry_offset + key_size].tobytes().decode()
            result[key] = load_mem(mem[data_offset:])
            entry_offset += align(8, key_size)

        return result
