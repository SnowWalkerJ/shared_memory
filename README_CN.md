# shared_memory

[English](README.md)

为Python封装的SharedMemory结构

## 解决痛点

- Python自带的SharedMemory会在创建它的进程结束后强制删除共享内存，这在有些场景下是不好的。我们的SharedMemory不会主动为你删除内存，需要手动删除
- 封装了一些数据结构的的共享内存版本，方便在进程间共享这些高级数据结构
  - numpy.ndarray
  - pandas.Series
  - pandas.DataFrame
  - xarray.DataArray
- 提供了易用的API供用户创建自己的基于共享内存的数据结构

## 警告

`pandas.DataFrame`是一个非常复杂的数据结构，在修改`DataFrame`的时候，它可能出其不意地对自己的数据做了拷贝，而对拷贝的修改就不会再应用到
共享内存上。

## 用法

### 创建一块共享内存

```python
import shared_memory as shm

# 共享内存名字叫"name"，大小是100字节
memory = shm.SharedMemory.create("name", 100)
# 打开刚才创建的内存
same_memory = shm.SharedMemory.open("name")
```

### 创建一个基于共享内存的`numpy.ndarray`

```python
import shared_memory as shm
# 定义内存布局：dtype=float32, shape=(3, 5)
layout = shm.NdArrayLayout("float32", (3, 5))
array = shm.create("array", layout)

# 读取创建的array
same_array = shm.load("array")
```

### 创建一个基于共享内存的`pandas.Series`

```python
import shared_memory as shm
layout = shm.SeriesLayout(dtype="float32", index=["a", "b", "c"])
series = shm.create("series", layout)

# 读取创建的series
same_series = shm.load("series")
```

### 创建一个基于共享内存的`pandas.DataFrame`

```python
import shared_memory as shm
layout = shm.DataFrameLayout(dtypes=[("a", "float32"), ("b", "int32")], index=["a", "b", "c"])
frame = shm.create("frame", layout)

# 读取创建的frame
same_frame = shm.load("frame")
```

### 创建基于共享内存的`xarray.DataArray`

```python
import shared_memory as shm
import xarray as xr
# 定义一个模板数据
template_data = xr.DataArray(0, dims=["x", "y"], coords={"x": [1, 2, 3], "y": ["a", "b", "c"]})
layout = shm.DataArrayLayout.from_data(template_data)
array = shm.create("array2", layout)

# 读取创建的array
same_array = shm.load("array2")
```

### 删除已经存在的共享内存

```python
import shared_memory as shm
shm.unlink("name")
```