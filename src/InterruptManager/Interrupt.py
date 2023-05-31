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
            "interrupt_message_queue", "process_over_event", "memory", "block_pcb_queue", "exit_event", "os", "force_dispatch_event")
    def __init__(self, ready_pcb_queue, interrupt_pcb_queue, interrupt_event,
                 interrupt_message_queue, process_over_event, memory, block_pcb_queue, exit_event, os, force_dispatch_event):
        super().__init__(name="interrupt")
        self.ready_pcb_queue = ready_pcb_queue
        self.interrupt_event = interrupt_event
        self.interrupt_pcb_queue = interrupt_pcb_queue
        self.interrupt_message_queue = interrupt_message_queue
        self.process_over_event = process_over_event
        self.memory = memory
        self.block_pcb_queue = block_pcb_queue
        self.exit_event = exit_event
        self.force_dispatch_event = force_dispatch_event
        self.os = os


    def run(self):
        # print("interrupt thread new ok")
        while True:
            if not self.interrupt_event.is_set():
                # print("interrupt: now waiting interrupt_event")
                self.interrupt_event.wait()
                # print("收到中断")
                if self.exit_event.is_set():
                    # print("interrupt thread end")
                    return
                type = 0
                if not self.interrupt_pcb_queue.empty():
                    self.interrupt_pcb = self.interrupt_pcb_queue.get()
                    type = self.interrupt_pcb.get_event()
                    # print(type)
                if type == 1:# ok
                    self.os.wakeup(self.interrupt_pcb)
                    self.interrupt_event.clear()
                elif type == 2:
                    do_IRQ(pcb=self.interrupt_pcb, device=self.interrupt_pcb.get_device_id())
                    self.os.block()
                    # print("中断set了force")
                    self.interrupt_event.clear()
                else:
                    # page_num = self.interrupt_message_queue.get()
                    # program_num = self.interrupt_message_queue.get()
                    # out_page = self.interrupt_message_queue.get()
                    message = self.interrupt_message_queue.get()
                    page_num = message["page_num"]
                    program_num = message["PID"]
                    out_page = message["flag"]
                    # print("interrupt_get: page_num" + str(page_num)+ "program_num:"+ str(program_num) + "out_page:" + str(out_page))
                    self.memory.program_deal_page_fault(page_num, program_num, out_page)
                    self.interrupt_event.clear()

                # print("中断结束")


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

@inject("device_queue", "device_st")
def do_IRQ(device_queue, device_st, pcb=None, device=0):
    if device == 1:
        device_queue.add_request(pcb=pcb, dev_type="keyboard", dev_num=1)
    elif device == 2:
        device_queue.add_request(pcb=pcb, dev_type="print", dev_num=2)
    elif device == 3:
        device_queue.add_request(pcb=pcb, dev_type="A", dev_num=3)
        # print("申请设备3")
    elif device == 4:
        device_queue.add_request(pcb=pcb, dev_type="B", dev_num=4)
    elif device == 5:
        device_queue.add_request(pcb=pcb, dev_type="C", dev_num=5)
    use_dev(device_queue, device_st)
