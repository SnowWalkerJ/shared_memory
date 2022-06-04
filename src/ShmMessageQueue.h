#ifndef SHM_ARRAY_SRC_SHMMESSAGEQUEUE_H_
#define SHM_ARRAY_SRC_SHMMESSAGEQUEUE_H_
#include <cstring>
#include <string>
#include "SharedMemory.h"

namespace shm_array {

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
  long GetTailId() const { return *tail_id_; }
  long GetCount() const { return count_; }
  long GetItemSize() const { return *itemsize_; }
  long GetHeadId();
  volatile char *GetBlock(long id);
  void IncHead() { ++head_id_; }
  void IncTail() { ++(*tail_id_); }
  volatile long *itemsize_;
  long count_;
  long safe_buffer_;
  volatile long *tail_id_;
  volatile char *buffer_;
  long head_id_;
  SharedMemory shm_;
};

} // shm_array

#endif //SHM_ARRAY_SRC_SHMMESSAGEQUEUE_H_
