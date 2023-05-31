import threading
import time
import queue

from src.ProcessManager.Semaphore import Semaphore

# 初始化信号量
sign = Semaphore(5)

# 生产者线程
class ProducerThread(threading.Thread):
    def run(self):
        numbers = range(1, 6)
        global task_queue
        while True:
            # 获取队列锁
            queue_lock.acquire()
            if task_queue.full():
                # 如果队列已满，释放队列锁并等待
                queue_lock.release()
                time.sleep(1)
            else:
                # 如果队列未满，将数据放入队列中
                for number in numbers:
                    task_queue.put(number)
                    print("生产者生产数据:", number)
                # 释放队列锁
                queue_lock.release()
                time.sleep(2)


# 消费者线程
class ConsumerThread(threading.Thread):
    def run(self):
        global task_queue
        while True:
            # 获取队列锁
            queue_lock.acquire()
            if task_queue.empty():
                # 如果队列为空，释放队列锁并等待
                queue_lock.release()
                time.sleep(1)
            else:
                # 如果队列不为空，从队列中取出数据并进行消费
                number = task_queue.get()
                print("消费者消费数据:", number)
                # 释放队列锁
                queue_lock.release()
                time.sleep(2)




# 创建一个线程安全的队列
queue_lock = threading.Lock()
task_queue = queue.Queue(maxsize=5)




# 生产者线程
class ProducerThread(threading.Thread):
    def run(self):
        numbers = range(1, 6)
        global task_queue
        while True:
            # 获取队列锁
            queue_lock.acquire()
            if task_queue.full():
                # 如果队列已满，释放队列锁并等待
                queue_lock.release()
                time.sleep(1)
            else:
                # 如果队列未满，将数据放入队列中
                for number in numbers:
                    task_queue.put(number)
                    print("生产者生产数据:", number)
                # 释放队列锁
                queue_lock.release()
                time.sleep(2)


# 消费者线程
class ConsumerThread(threading.Thread):
    def run(self):
        global task_queue
        while True:
            # 获取队列锁
            queue_lock.acquire()
            if task_queue.empty():
                # 如果队列为空，释放队列锁并等待
                queue_lock.release()
                time.sleep(1)
            else:
                # 如果队列不为空，从队列中取出数据并进行消费
                number = task_queue.get()
                print("消费者消费数据:", number)
                # 释放队列锁
                queue_lock.release()
                time.sleep(2)


# 创建并启动生产者和消费者线程
producer_thread = ProducerThread()
consumer_thread = ConsumerThread()
producer_thread.start()
consumer_thread.start()
