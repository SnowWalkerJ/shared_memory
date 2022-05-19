class SharedMemory:
    def size(self) -> int:
        pass

    @classmethod
    def create(cls, name: str, size: int):
        pass

    @classmethod
    def open(cls, name: str, read_only: bool=False):
        pass
