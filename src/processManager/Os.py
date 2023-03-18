# -*- coding:utf-8 -*-
# @FileName : Os.py
# @Time     : 2023/3/18 14:02
# @Author   : qingyao

from Timer import *
import threading

class Os:
    __timer = Timer()
    launch = False

    def is_launch(self):
        return self.launch

    def timing(self):
        while self.is_launch():
            self.__timer.__run__()

    def start(self):
        system_timer_th = threading.Thread(target=self.timing)
        system_timer_th.start()

    def set_launch(self, launch):
        self.launch = launch

if __name__ == "__main__":
    run_code = 0
