# -*- coding:utf-8 -*-
# @FileName : Interrupt.py
# @Time     : 2023/5/18 10:39
# @Author   : qingyao
import threading
from utils.logger import logger
from processManager.PCB import PCB
from utils.Container import *
from DeviceManager.DeviceManager import *
from processManager import PCB
interrupt_vector = []
class Interrput(threading.Thread):

    @inject("ready_pcb_queue", "interrupt_pcb_queue", "interrupt_event", "interrupt_message_queue", "process_over_event")
    def __init__(self,ready_pcb_queue, interrupt_pcb_queue, interrupt_event, interrupt_message_queue, process_over_event):
        self.ready_pcb_queue = ready_pcb_queue
        self.interrupt_event = interrupt_event
        self.interrupt_pcb_queue = interrupt_pcb_queue
        self.interrupt_message_queue = interrupt_message_queue
        self.process_over_event = process_over_event
        file = open("interrupt_vector_table")
        for line in file:
            interrupt_vector.append(line)
        file.close()

    def run(self):
        while True:
            if not self.interrupt_event.is_set():
                self.interrupt_event.wait()
                self.interrupt_pcb = self.interrupt_pcb_queue.get()
                type = self.interrupt_pcb.get_event()
                if type == 1:# ok
                    self.interrupt_pcb.set_state(PCB.PROCESS_READY)
                    self.ready_pcb_queue.put(self.interrupt_pcb)
                    self.interrupt_event.clear()
                elif type == 2:# page fault
                    do_page_fault()
                    address = self.interrupt_message_queue.get()
                    page_num = self.interrupt_message_queue.get()

                elif type == 3:# page fault
                    do_page_fault()
                else:
                    do_IRQ(self.interrupt_pcb.get_device_id())
                    self.interrupt_pcb.set_state(PCB.PROCESS_BLOCK)
                    self.process_over_event.set()
                    self.interrupt_event.clear()

def do_page_fault():
    pass

@inject("device_request_queue", "device_status_table")
def do_IRQ(pcb, device: int, device_request_queue, device_status_table):
    if device == 1:
        DeviceRequestQueue.add_request(pcb, "keyboard", 1)
    elif device == 2:
        DeviceRequestQueue.add_request(pcb, "print", 2)
    elif device == 3:
        DeviceRequestQueue.add_request(pcb, "A", 3)
    elif device == 4:
        DeviceRequestQueue.add_request(pcb, "B", 4)
    elif device == 5:
        DeviceRequestQueue.add_request(pcb, "C", 5)
    use_dev(device_request_queue, device_status_table)
