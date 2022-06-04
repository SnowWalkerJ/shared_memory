class SharedMemory:
    def size(self) -> int:
        pass

    @classmethod
    def create(cls, name: str, size: int):
        pass

    @classmethod
    def open(cls, name: str, read_only: bool=False):
        pass


class ShmMessageQueue:
    def get(self):
        pass

    def put(self, obj):
        pass

    @classmethod
    def open(cls, name: str, safe_buffer: int = 2):
        pass

    @classmethod
    def create(cls, name: str, itemsize: int, count: int, safe_buffer: int = 2):
        pass


def unlink(name: str):
    pass
