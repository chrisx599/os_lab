# -*- coding:utf-8 -*-
# @FileName : Interrupt.py
# @Time     : 2023/5/18 10:39
# @Author   : qingyao
import threading
from lib.logger import logger
from processManager.PCB import PCB
from utils.Container import *
from DeviceManager.DeviceManager import *
interrupt_vector = []
class Interrput(threading.Thread):

    @inject("ready_pcb_queue")
    def __init__(self, interrupt_event, ready_pcb_queue):
        self.interrupt_event = interrupt_event
        self.ready_pcb_queue = ready_pcb_queue
        file = open("interrupt_vector_table")
        for line in file:
            interrupt_vector.append(line)
        file.close()
    def interrupt_handling(self):
        type = self.interrupt_pcb.get_event()
        func_name = interrupt_vector[type]
        eval(func_name + '()')

    def run(self):
        while True:
            if not self.interrupt_event.is_set():
                self.interrupt_event.wait()
                type = self.interrupt_type_queue.get()
                if type == 1:# ok
                    pcb = self.interrupt_type_queue.get()
                    self.ready_pcb_queue.put(pcb)
                elif type == 2:# page fault
                    pass
                else:
                    do_IRQ()
                # diaodu


def do_page_fault():
    pass


def do_IRQ(device: int):
    if device == 1:
        DeviceRequestQueue.add_request("", "keyboard", 1)
    elif device == 2:
        DeviceRequestQueue.add_request("", "print", 2)
    elif device == 3:
        DeviceRequestQueue.add_request("", "A", 3)
    elif device == 4:
        DeviceRequestQueue.add_request("", "B", 4)
    elif device == 5:
        DeviceRequestQueue.add_request("", "C", 5)
