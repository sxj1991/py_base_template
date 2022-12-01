import logging
import random
import threading
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import os
from time import sleep

# 初始化线程池
pool = ThreadPoolExecutor(max_workers=5, thread_name_prefix="base_thread")

logger = logging.getLogger('full_logger')

# 创建锁
lock = threading.Lock()


def log_message(message: str):
    # 加锁 lock.acquire(timeout=1) 可设超市时间
    lock.acquire()
    print(f"打印信息:{message}-pid:{os.getpid()}")
    sleep(random.randint(1, 5))
    print(f"done-{message}")
    # 解锁
    lock.release()


def start_thread(message: str):
    pool.submit(log_message, message)


def process_thread(message: str):
    with ProcessPoolExecutor(max_workers=10) as executor:
        executor.map(log_message, range(100))


if __name__ == '__main__':
    for num in range(0, 3):
        start_thread(f"test{num}")
