import sys
sys.path.append('..')
from DeviceControlBlock import *
from DeviceStatusTable import *
from DeviceRequestQueue import *
import time
from ...lib.logger import logger
from utils.Container import *

#处理请求，调用设备
def use_dev():
    # 获取设备请求
    request = drq.get_request()
    print(request)
    if request is not None:
        pid, dev_type, dev_num = request
        dcb = dst.get_dev(dev_num)
        if dcb is not None and dcb.status == "idle":
            dcb.status = "busy"  # 更新设备状态为忙碌
            # 执行设备操作
            execute_operation(pid, dev_type, dev_num)
        else:
            dcb.queue.append(request)  # 将进程加入设备队列
    else:
        time.sleep(1)  # 暂停一段时间，等待下一次设备请求

#执行设备操作
@inject("interrupt_event","interrupt_type_queue","interrupt_ack_event")
def execute_operation(pid,dev_type,dev_num,interrupt_event,interrupt_type_queue,interrupt_ack_event):
    time.sleep(5)
    interrupt_event.set()
    if dev_type == "printer":
        interrupt_ack_event.wait()
        print("***模拟操作系统打印机***")
        interrupt_type_queue.put(4)
        print(interrupt_type_queue.get())
    elif dev_type == "keyboard":
        input_tmp = input("请在键盘上输入\n")
        interrupt_type_queue.put(3)
        interrupt_type_queue.put(input_tmp)

    interrupt_event.clear()
    interrupt_ack_event.clear()

#释放设备
def release_dev(dev_type,dev_num):
    dcb = dst.get_dev(dev_type)
    if dcb is not None:
        dcb.status = "idle"

# 中断处理程序
def interrupt_handler(dev_id):
    dcb = dst.get_dev(dev_id)
    if dcb is not None:
        dcb.status = "idle"  # 更新设备状态为闲置
        # 唤醒等待该设备资源的进程
        while len(dcb.queue) > 0:
            pid, dev_type, dev_num = dcb.queue.pop(0)
            ready_queue.append((pid, dev_type, dev_num))




#************测试************

# 初始化设备状态表和设备请求队列
dst = DeviceStatusTable()
drq = DeviceRequestQueue()

# 添加设备到设备状态表
dst.add_dev("disk", 1)
dst.add_dev("printer", 2)

#查看所有设备
dst.print_all_devs()

#删除指定设备
dst.del_dev("dsik",1)

dst.print_all_devs()

#添加设备申请
drq.add_request(1,"printer",2)

# 处理设备请求
while True:
    use_dev()