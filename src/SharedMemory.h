#ifndef SHM_ARRAY__SHAREDMEMORY_H_
#define SHM_ARRAY__SHAREDMEMORY_H_
#include <memory>
#include <string>
#include <boost/interprocess/shared_memory_object.hpp>
#include <boost/interprocess/mapped_region.hpp>
#include "Common.h"
namespace shm_array {
namespace bi = boost::interprocess;


 class SharedMemory {
 public:
  SharedMemory(const SharedMemory &) = delete;
  SharedMemory(SharedMemory &&) = default;
  static SharedMemory Create(const std::string &name, size_t size);
  static SharedMemory Open(const std::string &name, Permission permission);
  SharedMemory &operator=(const SharedMemory &) = delete;
  SharedMemory &operator=(SharedMemory &&) = default;
  size_t Size() const;
  void *Address();
  const void *Address() const;
 protected:
  explicit SharedMemory(bi::mapped_region &&region);
 private:
  bi::mapped_region region_;
};

} // shm_array

#endif //SHM_ARRAY__SHAREDMEMORY_H_
