import sys
import os
current_path = os.getcwd()
print(current_path)
sys.path.append(current_path + "\..")
sys.path.append(current_path + "\..\ProcessManager")
sys.path.append(current_path + "\..\DeviceManager")
sys.path.append(current_path + "\..\\UIManager")
sys.path.append(current_path + "\..\MemoryManager")
sys.path.append(current_path + "\..\FileManager")
sys.path.append(current_path + "\..\InterruptManager")
sys.path.append(current_path + "\..\TimeManager")
sys.path.append(current_path + "\..\HardWareManager")
sys.path.append(current_path + "\..\\utils")

import threading
from DeviceControlBlock import *
from DeviceStatusTable import *
from DeviceRequestQueue import *
import time
from utils.logger import logger
from utils.Container import *
from ProcessManager.PCB import PCB
from MemoryManager.Memory import *

#@inject("interrupt_event","interrupt_pcb_queue")
def run(dcb):
    #参数interrupt_event, interrupt_pcb_queue
    while True:
        if dcb.status == "idle":
            pcb = dcb.get_dcb_queue()
            if pcb != None:
                dcb.status = "busy"
                execute_operation(pcb, dcb.dev_type, dcb.dev_id)
                time.sleep(3)
                release_dev(dcb.dev_type,dcb.dev_id)
                pcb.set_event = 1
                # interrupt_pcb_queue.put(pcb)
                # interrupt_event.set()

#处理请求，调用设备
def use_dev(drq,dst):
    # 获取设备请求
    request = drq.get_request()
    if request is not None:
        pcb, dev_type, dev_num = request
        dcb = dst.get_dev(dev_num)
        if dcb is not None:
            dcb.queue.put(pcb)  # 将进程加入设备队列
    else:
        time.sleep(1)  # 暂停一段时间，等待下一次设备请求

#执行设备操作
@inject("memory")
def execute_operation(pcb,dev_type,dev_num, memory):
    print("Device" + str(dev_type) + "is using by " + str(pcb.get_PID()))
    if dev_num == 1:
        input_tmp = input("请在键盘上输入\n")
        buffer_list = memory.write_buffer(input_tmp)
        # 确认input长度，写入内存
        pcb.set_buffer_size(buffer_list[1])
        pcb.set_buffer_adderss(buffer_list[0])
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

if __name__ == "__main__":
    #************测试************

    # 初始化设备状态表和设备请求队列
    dst = DeviceStatusTable()
    drq = DeviceRequestQueue()

    dev_list = ['1 keyboard','2 printer']
    for dev in dev_list:
        d_id = int(dev.split()[0])
        d_type = dev.split()[1]
        dst.add_dev(d_type,d_id)

    # 添加设备到设备状态表
    # dst.add_dev("keyboard",1)
    # dst.add_dev("printer", 2)


    #查看所有设备
    dst.print_all_devs()

    #删除指定设备
    #dst.del_dev("disk",2)

    dst.print_all_devs()

    #添加设备申请
    pcb = PCB("aaa")
    drq.add_request(pcb,"printer",2)
    use_dev(drq, dst)
    drq.add_request(pcb, "printer", 2)
    use_dev(drq, dst)
    drq.add_request(pcb, "keyboard", 1)
    use_dev(drq, dst)
    t = threading.Thread(target=run, args=[dst.get_dev(1)], name="keyboard")
    t.start()
    t = threading.Thread(target=run, args=[dst.get_dev(2)], name="printer")
    t.start()
    # 处理设备请求
    #while True:
        #use_dev()