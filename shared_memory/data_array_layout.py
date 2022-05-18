from .struct_layout import StructLayout
from .pickle_layout import PickleLayout
from .ndarray_layout import NdArrayLayout

import xarray as xr


class DataArrayLayout(StructLayout):
    sign = b"x"

    def __init__(self, dims, coords, dtype, shape):
        super().__init__({
            "dims": PickleLayout(dims),
            "coords": PickleLayout(coords),
            "data": NdArrayLayout(dtype, shape)
        })

    @classmethod
    def load(cls, mem: memoryview):
        data = super().load(mem)
        return xr.DataArray(data["data"], dims=data["dims"], coords=data["coords"])

    @classmethod
    def from_data(cls, array: xr.DataArray):
        return cls(array.dims, array.coords, array.dtype, array.shape)
