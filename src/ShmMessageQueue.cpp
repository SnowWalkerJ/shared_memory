#include "ShmMessageQueue.h"

#ifndef _unlikely
#define _unlikely(x) __builtin_expect((x), 1)
#endif


struct block_control {
  std::atomic_flag ready;
  std::atomic_uint64_t size;
};


namespace shm_array {
ShmMessageQueue::ShmMessageQueue(SharedMemory &&shm, long safe_buffer) : shm_(std::move(shm)), safe_buffer_(safe_buffer) {
  control_ = static_cast<control *>(shm_.Address());
  buffer_ = reinterpret_cast<volatile char *>(shm_.Address()) + std::max(sizeof(control), hardwareInterferenceSize);
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
  block_control &bc = *reinterpret_cast<block_control *>(const_cast<char *>(block));
  bc.ready.clear();
  bc.size = data.size();
  char *buffer = const_cast<char *>(block) + sizeof(block_control);
  std::copy(data.begin(), data.end(), buffer);
  bc.ready.test_and_set();
}

std::string ShmMessageQueue::Get() {
  auto block = GetBlock(GetHeadId());
  IncHead();
  block_control &bc = *reinterpret_cast<block_control *>(const_cast<char *>(block));
  while (!bc.ready.test());
  char *buffer = const_cast<char *>(block) + sizeof(block_control);
  return {buffer, bc.size};
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

ShmMessageQueue ShmMessageQueue::Create(const std::string &name, long itemsize, long count, long safe_buffer) {
    auto shm = SharedMemory::Create(name, sizeof(control) + itemsize * count);
    auto ctrl = static_cast<control *>(shm.Address());
    ctrl->count = count;
    ctrl->itemsize = itemsize;
    ctrl->tail_id_.store(0);
    return ShmMessageQueue(std::move(shm), safe_buffer);
}

ShmMessageQueue ShmMessageQueue::Open(const std::string &name, long safe_buffer) {
    auto shm = SharedMemory::Open(name, Permission::READWRITE);
    return ShmMessageQueue(std::move(shm), safe_buffer);
}
} // shm_array