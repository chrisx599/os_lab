import threading

# from src.ProcessManager.Semaphore import Semaphore
from time import sleep

# #初始化信号量
# sign = Semaphore(3)

# def task(id):
#     # 请求信号量
#     sign.wait()
#     print(f"任务 {id} 开始执行")
#     # 模拟任务执行
#     for i in range(10):
#         print(f"任务 {id} 正在执行{i}部分")
#         sleep(0.5)
#     # 释放信号量
#     sign.signal()




# 创建一个信号量，初始值为2
semaphore = threading.Semaphore(3)

# 定义一个任务函数
def task(id):
    # 请求信号量
    semaphore.acquire()
    print(f"任务 {id} 开始执行")
    # 模拟任务执行时间
    for i in range(5):
        print(f"任务 {id} 正在执行{i}部分")
        sleep(0.5)
    # 释放信号量
    semaphore.release()
    print(f"任务 {id} 执行完成")

# 创建并启动多个线程执行任务
threads = []
for i in range(5):
    t = threading.Thread(target=task, args=(i,))
    threads.append(t)
    t.start()

# 等待所有线程执行完毕
for t in threads:
    t.join()
