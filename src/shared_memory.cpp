#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include "SharedMemory.h"
#include "ShmMessageQueue.h"
#include <boost/interprocess/shared_memory_object.hpp>

namespace py = pybind11;
using namespace shm_array;
using namespace pybind11::literals;


PYBIND11_MODULE(shared_memory, m) {
  py::class_<SharedMemory>(m, "SharedMemory", py::buffer_protocol())
      .def_property_readonly_static("create", [](const py::object&) {
        return py::cpp_function(&SharedMemory::Create, "name"_a, "size"_a);
      })
      .def_property_readonly_static("open", [](const py::object&) {
        return py::cpp_function([](const std::string &name, bool read_only) {
          Permission permission = read_only ? shm_array::READONLY : shm_array::READWRITE;
          return SharedMemory::Open(name, permission);
        }, "name"_a, "read_only"_a = false);
      })
      .def("size", &SharedMemory::Size)
      .def_buffer([](SharedMemory &shm) {
        return py::buffer_info(
            shm.Address(),
            1,
            py::format_descriptor<unsigned char>::format(),
            1,
            {shm.Size()},
            {1}
            );
      })
      ;
  m.def("unlink", [](const std::string &name) {
    boost::interprocess::shared_memory_object::remove(name.c_str());
  });

  py::class_<ShmMessageQueue>(m, "ShmMessageQueue")
//      .def(py::init<SharedMemory &&, long>(), "buf"_a, "safe_buffer"_a=2, py::return_value_policy::move)
      .def("get", [](ShmMessageQueue &mq) {
        auto pickle = py::module::import("pickle");
        py::bytes data = mq.Get();
        return pickle.attr("loads")(data);
      })
      .def("put", [](ShmMessageQueue &mq, const py::object &obj) {
        auto pickle = py::module::import("pickle");
        py::bytes data = pickle.attr("dumps")(obj);
        mq.Put(data);
      })
      .def("empty", &ShmMessageQueue::Empty)
      .def_property_readonly_static("create", [](const py::object &self) {
        return py::cpp_function([](const std::string &name, long itemsize, long count, long safe_buffer) {
          auto shm = SharedMemory::Create(name, sizeof(control) + itemsize * count);
          auto ctrl = static_cast<control *>(shm.Address());
          ctrl->count = count;
          ctrl->itemsize = itemsize;
          ctrl->tail_id_.store(0);
          return ShmMessageQueue(std::move(shm), safe_buffer);
        }, "name"_a, "itemsize"_a, "count"_a, "safe_buffer"_a=2l, py::return_value_policy::move);
      })
      .def_property_readonly_static("open", [](const py::object &self) {
        return py::cpp_function([](const std::string &name, long safe_buffer) {
          auto shm = SharedMemory::Open(name, Permission::READWRITE);
          return ShmMessageQueue(std::move(shm), safe_buffer);
        }, "name"_a, "safe_buffer"_a=2l, py::return_value_policy::move);
      })
  ;
}