# -*- coding:utf-8 -*-
# @FileName : Timer.py
# @Time     : 2023/5/22 16:47
# @Author   : qingyao
import threading
from utils.Container import *
import time
class Timer(threading.Thread):

    system_time = 0
    timeout_event = None

    @inject("os_timer_messager", "timeout_event", "running_event", "process_over_event")
    def __init__(self, os_timer_messager, timeout_event, running_event, process_over_event):
        self.os_timer_messager = os_timer_messager
        self.timeout_event = timeout_event
        self.running_event = running_event
        self.process_over_event = process_over_event

    def run(self) -> None:
        while True:
            if (not self.running_event.is_set()) or self.timeout_event.is_set():
                if not self.running_event.is_set():
                    self.running_event.wait()
                else:
                    continue
            time_slice = self.os_timer_messager.get()
            self.process_over_event.wait(time_slice * 0.005)
            self.timeout_event.set()



if __name__ == "__main__":
    run_code = 0