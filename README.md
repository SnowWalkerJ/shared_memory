# shared_memory

为Python封装的SharedMemory结构

## 解决痛点

- Python自带的SharedMemory会在创建它的进程结束后强制删除共享内存，这在有些场景下是不好的。我们的SharedMemory不会主动为你删除内存，需要手动删除
- 封装了`numpy.ndarray`和`xarray.DataArray`的共享内存版本，方便在进程间共享这些高级数据结构

## TODO

- 封装pandas结构

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

### 创建基于共享内存的`xarray.DataArray`

```python
import shared_memory as shm
import xarray as xr
# 定义一个模板数据
template_data = xr.DataArray(0, dims=["x", "y"], coords={"x": [1, 2, 3], "y": ["a", "b", "c"]})
layout = shm.DataArrayLayout(template_data)
array = shm.create("array2", layout)

# 读取创建的array
same_array = shm.load("array2")
```