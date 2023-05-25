# -*- coding:utf-8 -*-
# @FileName : test.py
# @Time     : 2023/5/23 21:14
# @Author   : qingyao
import threading
import ctypes


class A(threading.Thread):

    def __init__(self, event):
        super().__init__()
        self.event = event

    def run(self) -> None:
        try:
            while True:
                self.event.wait()
        finally:
            print("end")
    def get_id(self):

        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def stop(self):
        thread_id = self.get_id()
        self.event.set()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
                                                         ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')


if __name__ == "__main__":
    event = threading.Event()
    a = A(event)
    a.start()
    a.stop()
