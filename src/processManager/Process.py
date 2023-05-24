# -*- coding:utf-8 -*-
# @FileName : Process.py
# @Time     : 2023/5/11 11:26
# @Author   : qingyao
from PCB import PCB
from utils.Container import *
from queue import Queue
class Process:
    __ready_pcb_queue = []
    __block_pcb_queue = None
    __exit_pcb_queue = None


    @inject("ready_pcb_queue", "block_pcb_queue", "exit_pcb_queue", "new_pcb_event")
    def __init__(self, ready_pcb_queue, block_pcb_queue, exit_pcb_queue, new_pcb_event):
        self.__ready_pcb_queue = ready_pcb_queue
        self.__block_pcb_queue = block_pcb_queue
        self.__exit_pcb_queue = exit_pcb_queue
        self.new_pcb_event = new_pcb_event

    # 进程调度
    def dispatch_process(self, pcb):
        # 由于进程运行完成或者进程阻塞引起调度
        if pcb.get_state() == PCB.PROCESS_EXIT or pcb.get_state() == PCB.PROCESS_BLOCK:
            # 如果是由于进程运行完成
            if pcb.get_state == PCB.PROCESS_EXIT:
                if pcb.get_release():
                    self.del_process(pcb)
                else:
                    self.__exit_pcb_queue.put(pcb)
                return self.multi_feedback_dispatch(None)
        # 正常调度
        else:
            return self.multi_feedback_dispatch(pcb)

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
            self.new_pcb_event.set()
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

    # 获取下一个pcb
    def get_next_pcb(self):
        for i in range(3):
            if not self.__ready_pcb_queue[i].empty():
                return self.__ready_pcb_queue[i].get()
        return None

    # 将pcb添加到正确的队列中
    def move_to_next_queue(self, pcb):
        if pcb.get_priority() < 2:
            self.__ready_pcb_queue[pcb.get_priority() + 1].put(pcb)
            pcb.set_priority(pcb.get_priority() + 1)
        else:
            self.__ready_pcb_queue[2].put(pcb)

    # 多级反馈算法
    def multi_feedback_dispatch(self, pcb):
        if pcb != None:
            self.move_to_next_queue(pcb)
        next_pcb = self.get_next_pcb()
        return next_pcb

    # 进程状态切换
    def to_ready(self, pcb):
        pcb.set_state(PCB.PROCESS_READY)

    def to_running(self, pcb):
        pcb.set_state(PCB.PROCESS_RUNNING)

    def to_block(self, pcb):
        pcb.set_state(PCB.PROCESS_BLOCK)

    def to_exit(self, pcb):
        pcb.set_state(PCB.PROCESS_EXIT)

    def get_block_pcb_queue(self):
        return self.__block_pcb_queue

    def get_ready_pcb_queue(self):
        return self.__ready_pcb_queue



if __name__ == "__main__":
    run_code = 1


