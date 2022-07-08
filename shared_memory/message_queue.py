from struct import calcsize
import numpy as np
from .shared_memory import SharedMemory
from .layout import Layout, align
from .util import load_mem
from .pickle_layout import PickleLayout


class MQLayout(Layout):
    sign = b"q"

    def __init__(self, itemsize: int, count: int):
        self.itemsize = itemsize
        self.count = count

    @align(8)
    def size(self) -> int:
        return calcsize("3l") + self.itemsize * self.count

    def dump(self, mem: memoryview):
        index = np.ndarray((3, ), "int64", mem)
        index[0] = self.itemsize
        index[1] = self.count
        index[2] = 0

    @classmethod
    def load(cls, mem: memoryview):
        return MessageQueue(mem)


class DefaultSerializer:
    @staticmethod
    def load(mem: memoryview):
        obj, layout = load_mem(mem)
        return obj

    @staticmethod
    def dump(obj, mem: memoryview):
        PickleLayout(obj).dump(mem)


class MessageQueue:
    def __init__(self, mem: memoryview, safe_buffer: int = 2, serializer=DefaultSerializer):
        # itemsize, total count, tail_id
        self.index = np.ndarray((3, ), "int64", mem)
        self.buffer = mem[calcsize("3l"):]
        self._safe_buffer = safe_buffer
        self._head_id = self.tail_id - 1
        self.serializer = serializer

    @property
    def itemsize(self):
        return self.index[0].item()

    @property
    def total_count(self):
        return self.index[1].item()

    @property
    def tail_id(self):
        return self.index[2].item()

    @tail_id.setter
    def tail_id(self, id):
        self.index[2] = id

    @property
    def head_id(self):
        tail_id = self.tail_id
        if self._head_id < 0 < tail_id:
            self._head_id = 0
        if tail_id > self.total_count:
            safe_front_bound = tail_id - self.total_count + self._safe_buffer
        else:
            safe_front_bound = max(tail_id - self.total_count, 0)
        self._head_id = max(safe_front_bound, self._head_id)
        return self._head_id

    def put(self, obj):
        slot_id = self.tail_id % self.total_count
        address = self.buffer[slot_id * self.itemsize:]
        self.serializer.dump(obj, address)
        self.tail_id = self.tail_id + 1

    def get(self):
        slot_id = self.head_id % self.total_count
        address = self.buffer[slot_id * self.itemsize:]
        obj = self.serializer.load(address)
        self._head_id += 1
        return obj

    def empty(self):
        return self.head_id >= self.tail_id

    @classmethod
    def create(cls, name: str, item_size: int, count: int, safe_buffer: int = 2, serializer=DefaultSerializer):
        layout = MQLayout(item_size, count)
        shm = SharedMemory.create(name, layout.size())
        mem = memoryview(shm)
        layout.dump(mem)
        return cls(mem, safe_buffer=safe_buffer, serializer=serializer)

    @classmethod
    def load(cls, name: str, safe_buffer: int = 2, serializer=DefaultSerializer):
        shm = SharedMemory.open(name)
        mem = memoryview(shm)
        return cls(mem, safe_buffer=safe_buffer, serializer=serializer)
