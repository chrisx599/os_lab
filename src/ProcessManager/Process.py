# -*- coding:utf-8 -*-
# @FileName : Process.py
# @Time     : 2023/5/11 11:26
# @Author   : qingyao
from PCB import PCB
from utils.Container import *
import threading
from queue import Queue
class Process:
    ready_pcb_queue = []
    block_pcb_queue = None
    exit_pcb_queue = None
    running_pcb = None


    @inject("ready_pcb_queue", "block_pcb_queue", "exit_pcb_queue", "memory")
    def __init__(self, ready_pcb_queue, block_pcb_queue, exit_pcb_queue, memory):
        self.ready_pcb_queue = ready_pcb_queue
        self.block_pcb_queue = block_pcb_queue
        self.exit_pcb_queue = exit_pcb_queue
        self.memory = memory

    # 进程调度
    def dispatch_process(self, pcb):
        # 由于进程运行完成或者进程阻塞引起调度
        if pcb.get_state() == pcb.PROCESS_EXIT or pcb.get_state() == pcb.PROCESS_BLOCK:
            # 如果是由于进程运行完成
            if pcb.get_state == pcb.PROCESS_EXIT:
                if pcb.get_release():
                    self.del_process(pcb)
                else:
                    self.exit_pcb_queue.put(pcb)
                return self.multi_feedback_dispatch(None)
        # 正常调度
        else:
            return self.multi_feedback_dispatch(pcb)

    # 创建新进程
    def create_process(self, name):
        new_pcb = PCB(name)
        new_pcb.set_code_size(self.memory.create_program(new_pcb.get_PID()))
        # new_pcb.set_size((self.memory.program_list[new_pcb.get_PID()].program_page_table.allocated_block_num) * 64)
        new_pcb.set_state(new_pcb.PROCESS_READY)
        if new_pcb.PID != 0:
            self.move_to_next_queue(new_pcb)
        return new_pcb

    # 销毁进程
    def del_process(self, pcb):
        # 释放内存
        self.memory.program_list[pcb.get_PID()].program_page_table.recycle_physical_memory()
        del pcb


    def get_running_pcb(self):
        return self.running_pcb

    def set_running_pcb(self, pcb):
        self.running_pcb = pcb

    # 获取下一个pcb
    def get_next_pcb(self):
        for i in range(3):
            if not self.ready_pcb_queue[i].empty():
                return self.ready_pcb_queue[i].get()
        return None

    # 将pcb添加到正确的队列中
    def move_to_next_queue(self, pcb):
        if pcb.get_priority() < 2:
            self.ready_pcb_queue[pcb.get_priority() + 1].put(pcb)
            pcb.set_priority(pcb.get_priority() + 1)
        else:
            self.ready_pcb_queue[2].put(pcb)

    # 多级反馈算法
    def multi_feedback_dispatch(self, pcb):
        if pcb != None:
            self.move_to_next_queue(pcb)
        next_pcb = self.get_next_pcb()
        self.running_pcb = next_pcb
        return next_pcb

    # 进程状态切换
    def to_ready(self, pcb):
        pcb.set_state(pcb.PROCESS_READY)

    def to_running(self, pcb):
        pcb.set_state(pcb.PROCESS_RUNNING)

    def to_block(self, pcb):
        pcb.set_state(pcb.PROCESS_BLOCK)
        self.block_pcb_queue.put(pcb)

    def to_exit(self, pcb):
        pcb.set_state(pcb.PROCESS_EXIT)

    def get_block_pcb_queue(self):
        return self.block_pcb_queue

    def get_ready_pcb_queue(self):
        return self.ready_pcb_queue

    def get_running_pcb(self):
        return self.running_pcb



if __name__ == "__main__":
    run_code = 1


