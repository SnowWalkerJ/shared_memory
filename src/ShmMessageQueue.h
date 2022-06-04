#ifndef SHM_ARRAY_SRC_SHMMESSAGEQUEUE_H_
#define SHM_ARRAY_SRC_SHMMESSAGEQUEUE_H_
#include <atomic>
#include <cstring>
#include <string>
#include "SharedMemory.h"

namespace shm_array {

#if defined(__cpp_lib_hardware_interference_size) && !defined(__APPLE__)
static constexpr size_t hardwareInterferenceSize =
    std::hardware_destructive_interference_size;
#else
static constexpr size_t hardwareInterferenceSize = 64;
#endif

struct control {
  long itemsize;
  long count;
  alignas(hardwareInterferenceSize) std::atomic_int64_t tail_id_;
};

class ShmMessageQueue {
 public:
  ShmMessageQueue() = delete;
  explicit ShmMessageQueue(SharedMemory &&shm, long safe_buffer=2);
  ShmMessageQueue(const ShmMessageQueue &) = delete;
  ShmMessageQueue(ShmMessageQueue &&) = default;
  ShmMessageQueue &operator=(const ShmMessageQueue &) = delete;
  ShmMessageQueue &operator=(ShmMessageQueue &&) = default;
  void Put(const std::string &);
  std::string Get();
  bool Empty();
 private:
  long GetTailId() const { return control_->tail_id_.load(); }
  long GetCount() const { return control_->count; }
  long GetItemSize() const { return control_->itemsize; }
  long GetHeadId();
  volatile char *GetBlock(long id);
  void IncHead() { ++head_id_; }
  long GetAndIncTail() { return control_->tail_id_.fetch_add(1); }
  long safe_buffer_;
  control *control_;
  volatile char *buffer_;
  long head_id_;
  SharedMemory shm_;
};

} // shm_array

#endif //SHM_ARRAY_SRC_SHMMESSAGEQUEUE_H_
