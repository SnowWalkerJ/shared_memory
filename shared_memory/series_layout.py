import pandas as pd
from .ndarray_layout import NdArrayLayout
from .pickle_layout import PickleLayout
from .struct_layout import StructLayout


__all__ = ["SeriesLayout"]


class SeriesLayout(StructLayout):
    sign = b"d"

    def __init__(self, dtype, index):
        shape = (len(index), )
        super().__init__({
            "index": PickleLayout(index),
            "values": NdArrayLayout(dtype, shape),
        })

    @classmethod
    def load(cls, mem: memoryview) -> pd.Series:
        data = super().load(mem)
        return pd.Series(data["values"], index=data["index"])

    @classmethod
    def from_data(cls, data: pd.Series):
        return cls(data.dtype, data.index)
