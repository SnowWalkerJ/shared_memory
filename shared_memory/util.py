from .shared_memory import SharedMemory, unlink
from .layout import Layout

import struct
from typing import Optional, Type


__all__ = ["create", "load"]


def create(name, layout: Layout):
    shm = SharedMemory.create(name, layout.size())
    mem = memoryview(shm)
    layout.dump(mem)
    return layout.load(mem)


def load(name, layout: Optional[Type[Layout]]=None):
    shm = SharedMemory.open(name)
    mem = memoryview(shm)
    return load_mem(mem, layout)


def load_mem(mem: memoryview, layout: Optional[Type[Layout]]=None):
    if layout is None:
        sign = struct.unpack_from("c", mem, 0)[0]
        layout = Layout.get_layout_cls(sign)
    return layout.load(mem)
