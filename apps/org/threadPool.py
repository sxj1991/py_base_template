import logging
import random
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import os
from time import sleep

# 初始化线程池
pool = ThreadPoolExecutor(max_workers=5, thread_name_prefix="base_thread")

logger = logging.getLogger('full_logger')


def log_message(message: str):
    print(f"打印信息:{message}-pid:{os.getpid()}")
    sleep(random.randint(1, 5))
    print(f"done-{message}")


def start_thread(message: str):
    pool.submit(log_message, message)


def process_thread(message: str):
    with ProcessPoolExecutor(max_workers=10) as executor:
        executor.map(log_message, range(100))


if __name__ == '__main__':
    start_thread("test1")

