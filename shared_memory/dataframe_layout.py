from typing import Any, Iterable, List, Tuple

import numpy as np
import pandas as pd
from pandas.core.internals.blocks import get_block_type
from pandas.core.internals import create_block_manager_from_blocks

from .pickle_layout import PickleLayout
from .ndarray_layout import NdArrayLayout
from .struct_layout import StructLayout


__all__ = ["DataFrameLayout"]


class DataFrameLayout(StructLayout):
    sign = b"D"

    def __init__(self, dtypes: List[Tuple[str, np.dtype]], index: Iterable[Any]):
        meta = {"index": index, "columns": [col for (col, _) in dtypes], "blocks": {}}
        blocks = meta["blocks"]
        for idx, (name, dtype) in enumerate(dtypes):
            dtype = np.dtype(dtype)
            if dtype not in blocks:
                blocks[dtype] = []
            blocks[dtype].append(idx)

        layouts = {"meta": PickleLayout(meta)}
        for dtype, idxs in blocks.items():
            layouts[dtype.name] = NdArrayLayout(dtype, (len(idxs), len(index)))
        super().__init__(layouts)

    @classmethod
    def from_data(cls, df: pd.DataFrame):
        dtypes = list(df.dtypes.to_dict().items())
        index = df.index
        return cls(dtypes, index)

    @classmethod
    def load(cls, mem: memoryview) -> pd.DataFrame:
        data = super().load(mem)
        meta = data["meta"]
        blocks = []
        for dtype, block_locs in meta["blocks"].items():
            block_value = data[dtype.name]
            block_type = get_block_type(block_value)
            block = block_type(block_value, block_locs, 2)
            blocks.append(block)
        mgr = create_block_manager_from_blocks(blocks, [meta["columns"], meta["index"]])
        return pd.DataFrame(mgr)
