# -*- coding:utf-8 -*-
# @FileName : Timer.py
# @Time     : 2023/5/22 16:47
# @Author   : qingyao
import threading
from utils.Container import *
import time
import ctypes
class Timer(threading.Thread):

    system_time = 0
    timeout_event = None

    @inject("os_timer_messager", "timeout_event", "running_event", "process_over_event", "interrupt_event", "exit_event")
    def __init__(self, os_timer_messager, timeout_event, running_event, process_over_event, interrupt_event, exit_event):
        threading.Thread.__init__(self, name="timer")
        self.os_timer_messager = os_timer_messager
        self.timeout_event = timeout_event
        self.running_event = running_event
        self.process_over_event = process_over_event
        self.interrupt_event = interrupt_event
        self.exit_event = exit_event

    def run(self) -> None:
        print("Timer thread start")
        while True:
            if (not self.running_event.is_set()) or self.timeout_event.is_set():
                if not self.running_event.is_set():
                    print("timer: waiting running_event set")
                    self.running_event.wait()
                    if self.exit_event.is_set():
                        print("Timer thread end")
                        return
                else:
                    continue
            print("timer: time_slice start")
            time_slice = self.os_timer_messager.get()
            i = 0
            while i < time_slice * 5 and not self.process_over_event.is_set():
                if not self.interrupt_event.is_set():
                    i += 1
                    self.process_over_event.wait(0.001)
            self.os_timer_messager.put(i)
            self.timeout_event.set()
            print("timer:timeout_event is set now need dispatch")


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
    #     self.running_event.set()
    #     res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
    #                                                      ctypes.py_object(SystemExit))
    #     if res > 1:
    #         ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
    #         print('Exception raise failure')

if __name__ == "__main__":
    run_code = -1
