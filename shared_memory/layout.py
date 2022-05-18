import abc
import functools
import inspect


class Layout(abc.ABC):
    @abc.abstractmethod
    def size(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def dump(self, mem: memoryview):
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def load(cls, mem: memoryview):
        raise NotImplementedError


def align(alignment, target=None):
    if target is None:
        return functools.partial(align, alignment)
    if inspect.isfunction(target):
        @functools.wraps(target)
        def wrapped(*args, **kwargs):
            return align(alignment, target(*args, **kwargs))
        return wrapped
    if isinstance(target, int):
        if target % alignment != 0:
            target += alignment - target % alignment
        return target
    raise TypeError
