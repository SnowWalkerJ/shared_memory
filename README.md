# shared_memory

[中文](README_CN.md)

A shared memory encapsulated for Python

## Why should I use it

- The `multiprocessing.shared_memory.SharedMemory` carried by Python itself has the annoying behavior that it forces deleting the shared memory once the process that created (or opened) it exits, which is not always a wanted feature. So we make a SharedMemory that give you the flexibility to choose when you free the memory.
- We encapsulate shared memory-version of some handful data structs such as:
  - numpy.ndarray
  - pandas.Series
  - pandas.DataFrame
  - xarray.DataArray
- We offer a simple API for users to extend it and create more shared objects of their own

## Warning

`pandas.DataFrame` is a complex class that it often copies its data at suprising timing. Modifications on the copy won't apply to the shared memory, therefore out encapsulation might fail suprisingly.

## Usage

### create a `SharedMemory`

```python
import shared_memory as shm

# a shared memory named `name` with the size of 100 bytes
memory = shm.SharedMemory.create("name", 100)

# open the memory we just created
same_memory = shm.SharedMemory.open("name")
```

### create a shared `numpy.ndarray`

```python
import shared_memory as shm
# define the memory layout：dtype=float32, shape=(3, 5)
layout = shm.NdArrayLayout("float32", (3, 5))
array = shm.create("array", layout)

# load the array we just created
same_array = shm.load("array")
```

### create a shared `pandas.Series`

```python
import shared_memory as shm
layout = shm.SeriesLayout(dtype="float32", index=["a", "b", "c"])
series = shm.create("series", layout)

# read the series we just created
same_series = shm.load("series")
```

### 创建一个基于共享内存的`pandas.DataFrame`

```python
import shared_memory as shm
# two columns `a` and `b`, with dtypes `float32` and `int32` respectively
# index are ["a", "b", "c"]
layout = shm.DataFrameLayout(dtypes=[("a", "float32"), ("b", "int32")], index=["a", "b", "c"])
frame = shm.create("frame", layout)

# read the datafrmae we just created
same_frame = shm.load("frame")
```

### create a shared`xarray.DataArray`

```python
import shared_memory as shm
import xarray as xr
# define a template data
template_data = xr.DataArray(0, dims=["x", "y"], coords={"x": [1, 2, 3], "y": ["a", "b", "c"]})
layout = shm.DataArrayLayout.from_data(template_data)
array = shm.create("array2", layout)

same_array = shm.load("array2")
```

### remove an existing shared memory

```python
import shared_memory as shm
shm.unlink("name")
```