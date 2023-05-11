# -*- coding:utf-8 -*-
# @FileName : Process.py
# @Time     : 2023/5/11 11:26
# @Author   : qingyao
from PCB import PCB
from Dispatcher import Dispatcher
from utils.Container import *
from queue import Queue
class Process:
    __dispatcher = None
    __running_pcb = None
    __ready_pcb_queue = []
    __block_pcb_queue = None


    @inject("dispatcher", "ready_pcb_queue", "block_pcb_queue")
    def __init__(self, dispatcher, ready_pcb_queue, block_pcb_queue):
        self.__dispatcher = dispatcher
        self.__ready_pcb_queue = ready_pcb_queue
        self.__block_pcb_queue = block_pcb_queue

    # 进程调度
    def dispatch_process(self):
        # 保存现场
        next_running_pcb = self.__dispatcher.multi_feedback_dispatch(self.__running_pcb)
        self.__running_pcb = next_running_pcb
        # 恢复现场

    # 创建新进程
    def create_process(self, name):
        new_pcb = PCB(name)
        # 申请内存
        # 根据申请内存API的返还值修改new_pcb内容
        # if apply_memory is OK:
        # new_pcb.set_state(PCB.PROCESS_READY)
        # new_pcb.set_base_mem_reg()
        # new_pcb.set_limit_mem_reg()
        # else:
        # 抛异常
        if self.__running_pcb == None:
            new_pcb.set_state(PCB.PROCESS_RUNNING)
            self.__running_pcb = new_pcb
        else:
            self.__ready_pcb_queue[0].put(new_pcb)

    # 销毁进程
    def del_process(self, pcb):
        # 释放内存
        del pcb


    def get_running_pcb(self):
        return self.__running_pcb

    def set_running_pcb(self, pcb):
        self.__running_pcb = pcb


if __name__ == "__main__":
    container = Container()
    a = []
    for i in range(3):
        a.append(Queue())
    b = Queue()
    container.register("ready_pcb_queue", a)
    container.register("block_pcb_queue", b)
    dispatcher = Dispatcher()
    container.register("dispatcher", dispatcher)
    process = Process()
    process.create_process("aa")
    process.create_process("bb")
    process.create_process("cc")
    process.dispatch_process()
    i = 0
    while i < 10:
        print(process.get_running_pcb().get_name())
        print(process.get_running_pcb().get_priority())
        process.dispatch_process()
        i += 1


