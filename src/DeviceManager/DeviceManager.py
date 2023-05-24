import sys
import threading
sys.path.append('..')
from DeviceControlBlock import *
from DeviceStatusTable import *
from DeviceRequestQueue import *
import time
from utils.logger import logger
from utils.Container import *
from processManager import PCB

def run(dcb):
    #参数interrupt_event, interrupt_pcb_queue
    while True:
        if dcb.status == "idle":
            dcb_request = dcb.get_dcb_queue()
            pcb,dev_type,dev_num = dcb_request
            if pcb != None:
                execute_operation(pcb, dev_type, dev_num)
                time.sleep(3)
                pcb.set_event = 1
                interrupt_pcb_queue.put(pcb)
                interrupt_event.set()

#t=threading.Thread(target=run, name=name)

#处理请求，调用设备
def use_dev(drq,dst):
    # 获取设备请求
    request = drq.get_request()
    if request is not None:
        pcb, dev_type, dev_num = request
        dcb = dst.get_dev(dev_num)
        if dcb is not None:
            dcb.queue.append(request)  # 将进程加入设备队列
    else:
        time.sleep(1)  # 暂停一段时间，等待下一次设备请求

#执行设备操作
def execute_operation(pcb,dev_type,dev_num):
    print("Device" + dev_type + "is using by " + pcb.get_PID())
    if dev_num == 1:
        input_tmp = input("请在键盘上输入\n")
        # 确认input长度，写入内存
        pcb.set_buffer_size()
        pcb.set_buffer_adderss()
    elif dev_num == 2:
        print("***模拟操作系统打印机***")
        print(pcb.get_buffer_content())
    else:
        pass


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



if __name__ == "__main__":
    #************测试************

    # 初始化设备状态表和设备请求队列
    dst = DeviceStatusTable()
    drq = DeviceRequestQueue()

    # 添加设备到设备状态表
    dst.add_dev("keyboard",1)
    dst.add_dev("printer", 2)
    t = threading.Thread(target=run,args=[dst.get_dev(1)],name="keyboard")
    t.start()

    #查看所有设备
    dst.print_all_devs()

    #删除指定设备
    dst.del_dev("disk",1)

    dst.print_all_devs()

    #添加设备申请
    pcb = PCB
    drq.add_request(pcb,"printer",2)

    # 处理设备请求
    while True:
        use_dev()