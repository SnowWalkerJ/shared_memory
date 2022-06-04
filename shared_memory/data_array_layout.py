from .struct_layout import StructLayout
from .pickle_layout import PickleLayout
from .ndarray_layout import NdArrayLayout

import xarray as xr


class DataArrayLayout(StructLayout):
    sign = b"x"

    def __init__(self, dims, coords, dtype, shape, init_value=None):
        super().__init__({
            "dims": PickleLayout(dims),
            "coords": PickleLayout(coords),
            "data": NdArrayLayout(dtype, shape)
        })
        self.init_value = init_value

    def dump(self, mem: memoryview):
        super().dump(mem)
        if self.init_value is not None:
            array = self.load(mem)
            array.data[:] = self.init_value

    @classmethod
    def load(cls, mem: memoryview):
        data = super().load(mem)
        return xr.DataArray(data["data"], dims=data["dims"], coords=data["coords"])

    @classmethod
    def from_data(cls, array: xr.DataArray):
        return cls(array.dims, array.coords, array.dtype, array.shape, init_value=array)
