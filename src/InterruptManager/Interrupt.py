# -*- coding:utf-8 -*-
# @FileName : Interrupt.py
# @Time     : 2023/5/18 10:39
# @Author   : qingyao
import threading
from utils.logger import logger
from ProcessManager.PCB import PCB
from utils.Container import *
from DeviceManager.DeviceManager import *
from ProcessManager import PCB
import ctypes
class Interrput(threading.Thread):

    @inject("ready_pcb_queue", "interrupt_pcb_queue", "interrupt_event",
            "interrupt_message_queue", "process_over_event", "memory", "block_pcb_queue", "exit_event")
    def __init__(self, ready_pcb_queue, interrupt_pcb_queue, interrupt_event,
                 interrupt_message_queue, process_over_event, memory, block_pcb_queue, exit_event):
        super().__init__(name="interrupt")
        self.ready_pcb_queue = ready_pcb_queue
        self.interrupt_event = interrupt_event
        self.interrupt_pcb_queue = interrupt_pcb_queue
        self.interrupt_message_queue = interrupt_message_queue
        self.process_over_event = process_over_event
        self.memory = memory
        self.block_pcb_queue = block_pcb_queue
        self.exit_event = exit_event


    def run(self):
        print("interrupt thread new ok")
        while True:
            if not self.interrupt_event.is_set():
                print("interrupt: now waiting interrupt_event")
                self.interrupt_event.wait()
                if self.exit_event.is_set():
                    print("interrupt thread end")
                    return
                type = 0
                if not self.interrupt_pcb_queue.empty():
                    self.interrupt_pcb = self.interrupt_pcb_queue.get()
                    type = self.interrupt_pcb.get_event()
                if type == 1:# ok
                    self.interrupt_pcb.set_state(self.interrupt_pcb.PROCESS_READY)
                    self.ready_pcb_queue.put(self.interrupt_pcb)
                    self.interrupt_event.clear()
                elif type == 2:
                    do_IRQ(pcb=self.interrupt_pcb, device=self.interrupt_pcb.get_device_id())
                    self.interrupt_pcb.set_state(self.interrupt_pcb.PROCESS_BLOCK)
                    self.block_pcb_queue.put(self.interrupt_pcb)
                    self.process_over_event.set()
                    self.interrupt_event.clear()
                else:
                    page_num = self.interrupt_message_queue.get()
                    program_num = self.interrupt_message_queue.get()
                    out_page = self.interrupt_message_queue.get()
                    self.memory.program_deal_page_fault(page_num, program_num, out_page)
                    self.interrupt_event.clear()


    # def get_id(self):
    #
    #     # returns id of the respective thread
    #     if hasattr(self, '_thread_id'):
    #         return self._thread_id
    #     for id, thread in threading._active.items():
    #         if thread is self:
    #             return id
    #
    # def stop(self):
    #     thread_id = self.get_id()
    #     self.interrupt_event.set()
    #     res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
    #                                                      ctypes.py_object(SystemExit))
    #     if res > 1:
    #         ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
    #         print('Exception raise failure')

@inject("device_request_queue", "device_status_table")
def do_IRQ(device_request_queue, device_status_table, pcb=None, device=0):
    if device == 1:
        device_request_queue.add_request(pcb=pcb, dev_type="keyboard", dev_num=1)
    elif device == 2:
        device_request_queue.add_request(pcb=pcb, dev_type="print", dev_num=2)
    elif device == 3:
        device_request_queue.add_request(pcb=pcb, dev_type="A", dev_num=3)
    elif device == 4:
        device_request_queue.add_request(pcb=pcb, dev_type="B", dev_num=4)
    elif device == 5:
        device_request_queue.add_request(pcb=pcb, dev_type="C", dev_num=5)
    use_dev(device_request_queue, device_status_table)
