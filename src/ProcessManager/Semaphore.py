"""
Writen by Liang Zhengyang
"""

import sys
import os
current_path = os.getcwd()
sys.path.append(current_path + "\src")
import queue
from utils.logger import logger
from Process import Process
import threading
from time import sleep

class Semaphore():
    def __init__(self, initial:int) -> None:
        """
        initial:the initial value of Semaphore
        return a bool value, False represent failed to init semaphore, True represent successfully
        init semaphore
        """
        if initial <= 0:
            logger.error("the input number of initial value is wrong")
            # return False
        logger.info("successfully init semaphore")
        # self.value = initial
        self.lock = threading.Lock()
        self.queue = threading.Condition(self.lock)
        self.value = initial
        # self.queue = queue.Queue()
        # return True

    def wait(self):
        with self.lock:
            self.value -= 1
            if self.value < 0:
                # add this process to queue and block()
                self.queue.wait()
            
    
    def signal(self):
        with self.lock:
            self.value += 1
            if self.value <= 0:
                # remove a process P from queue and wakeup(P)
                self.queue.notify()
                

if __name__ == "__main__":
    semaphore = Semaphore(3)

    def worker(id):
        print(f'Worker {id} 正在执行')
        semaphore.wait()
        for i in range(5):
            print(f'Worker {id} 正在执行{i}部分')
            sleep(5)
        # 这里可以添加需要执行的代码
        semaphore.signal()
        print(f'Worker {id} 释放信号量')

    # 创建多个线程进行测试
    threads = []
    for i in range(5):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    # 等待所有线程执行完成
    for t in threads:
        t.join()