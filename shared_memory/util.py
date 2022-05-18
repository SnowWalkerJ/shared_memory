from .shared_memory import SharedMemory, unlink
from .layout import Layout

import struct
from typing import Optional, Type


__all__ = ["create", "load", "get_layout"]


def create(name, layout: Layout):
    unlink(name)
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
        layout = get_layout(sign)
    return layout.load(mem)


def get_layout(sign):
    from .ndarray_layout import NdArrayLayout
    from .pickle_layout import PickleLayout
    from .struct_layout import StructLayout
    from .data_array_layout import DataArrayLayout
    layouts = {
        b"a": NdArrayLayout,
        b"p": PickleLayout,
        b"s": StructLayout,
        b"x": DataArrayLayout,
    }
    return layouts[sign]
