from .struct_layout import StructLayout
from .pickle_layout import PickleLayout
from .ndarray_layout import NdArrayLayout

import xarray as xr


class DataArrayLayout(StructLayout):
    sign = b"x"

    def __init__(self, array: xr.DataArray):
        super().__init__({
            "dims": PickleLayout(array.dims),
            "coords": PickleLayout(array.coords),
            "data": NdArrayLayout(array.dtype, array.shape)
        })

    @classmethod
    def load(cls, mem: memoryview):
        data = super().load(mem)
        return xr.DataArray(data["data"], dims=data["dims"], coords=data["coords"])
