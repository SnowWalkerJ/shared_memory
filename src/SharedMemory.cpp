#include "SharedMemory.h"
#include <cassert>

namespace shm_array {
SharedMemory SharedMemory::Create(const std::string &name, size_t size) {
  bi::shared_memory_object shm(bi::create_only, name.c_str(), bi::read_write);
  shm.truncate(size);
  bi::mapped_region region(shm, bi::read_write);
  return SharedMemory(std::move(region));
}

SharedMemory SharedMemory::Open(const std::string &name, Permission permission) {
  if (permission == READONLY) {
    bi::shared_memory_object shm(bi::open_only, name.c_str(), bi::read_only);
    bi::mapped_region region(shm, bi::read_only);
    return SharedMemory(std::move(region));
  } else {
    bi::shared_memory_object shm(bi::open_only, name.c_str(), bi::read_write);
    bi::mapped_region region(shm, bi::read_write);
    return SharedMemory(std::move(region));
  }
}

SharedMemory::SharedMemory(bi::mapped_region &&region) : region_(std::move(region)) {}

size_t SharedMemory::Size() const {
  return region_.get_size();
}
void *SharedMemory::Address() {
  return region_.get_address();
}
const void *SharedMemory::Address() const {
  return region_.get_address();
}
} // shm_array