#include "ShmMessageQueue.h"

#ifndef _unlikely
#define _unlikely(x) __builtin_expect((x), 1)
#endif

namespace shm_array {
ShmMessageQueue::ShmMessageQueue(SharedMemory &&shm, long safe_buffer) : shm_(std::move(shm)), safe_buffer_(safe_buffer) {
  control_ = static_cast<control *>(shm_.Address());
  buffer_ = reinterpret_cast<volatile char *>(shm_.Address()) + sizeof(control);
  head_id_ = GetTailId() - 1;
}

bool ShmMessageQueue::Empty() {
  return GetHeadId() < 0 || GetHeadId() == GetTailId();
}

volatile char *ShmMessageQueue::GetBlock(long id) {
  long slot_id = id % GetCount();
  return buffer_ + slot_id * GetItemSize();
}

void ShmMessageQueue::Put(const std::string &data) {
  auto block = GetBlock(GetAndIncTail());
  *reinterpret_cast<volatile unsigned long *>(block) = data.size();
  std::copy(data.begin(), data.end(), block+sizeof(long));
}

std::string ShmMessageQueue::Get() {
  auto block = GetBlock(GetHeadId());
  IncHead();
  unsigned long size = *reinterpret_cast<volatile unsigned long *>(block);
  return {const_cast<char *>(block+sizeof(long)), size};
}

long ShmMessageQueue::GetHeadId() {
  long tail_id = GetTailId();
  if (_unlikely(head_id_ < 0 && tail_id > 0)) {
    head_id_ = 0;
  }
  long safe_front_bound;
  if (tail_id > GetCount()) {
    safe_front_bound = tail_id - GetCount() + safe_buffer_;
  } else {
    safe_front_bound = std::max<long>(tail_id - GetCount(), 0);
  }
  head_id_ = std::max(safe_front_bound, head_id_);
  return head_id_;
}
} // shm_array