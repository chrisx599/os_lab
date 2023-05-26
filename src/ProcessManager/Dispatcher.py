# -*- coding:utf-8 -*-
# @FileName : Dispatcher.py
# @Time     : 2023/5/11 11:27
# @Author   : qingyao

from PCB import *
from queue import *
from utils.Container import *
class Dispatcher:

    __ready_pcb_queue = []
    __block_pcb_queue = None

    __LEVEL = 3

    # @inject("ready_pcb_queue", "block_pcb_queue")
    def __init__(self, ready_pcb_queue, block_pcb_queue):
        self.__ready_pcb_queue = ready_pcb_queue
        self.__block_pcb_queue = block_pcb_queue


    def add_ready_PCB(self, pcb):
        self.__ready_pcb_queue[0].put(pcb)

    # 获取下一个pcb
    def get_next_pcb(self):
        for i in range(self.__LEVEL):
            if not self.__ready_pcb_queue[i].empty():
                return self.__ready_pcb_queue[i].get()
        return None

    # 将pcb添加到正确的队列中
    def move_to_next_queue(self, pcb):
        if pcb.get_priority() < self.__LEVEL - 1:
            self.__ready_pcb_queue[pcb.get_priority() + 1].put(pcb)
            pcb.set_priority(pcb.get_priority() + 1)
        else:
            self.__ready_pcb_queue[self.__LEVEL - 1].put(pcb)

    # 多级反馈算法
    def multi_feedback_dispatch(self, pcb):
        if pcb != None:
            self.move_to_next_queue(pcb)
        next_pcb = self.get_next_pcb()
        return next_pcb



    # 进程状态切换
    def to_ready(self, pcb):
        pcb.set_state(pcb.PROCESS_READY)

    def to_running(self, pcb):
        pcb.set_state(pcb.PROCESS_RUNNING)

    def to_block(self, pcb):
        pcb.set_state(pcb.PROCESS_BLOCK)

    def to_exit(self, pcb):
        pcb.set_state(pcb.PROCESS_EXIT)

    def get_block_pcb_queue(self):
        return self.__block_pcb_queue

    def get_ready_pcb_queue(self):
        return self.__ready_pcb_queue

    def get_level(self):
        return self.__LEVEL










if __name__ == "__main__":
    run_code = 0
