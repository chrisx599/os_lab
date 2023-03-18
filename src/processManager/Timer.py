# -*- coding:utf-8 -*-
# @FileName : Timer.py
# @Time     : 2023/3/17 19:06
# @Author   : qingyao

import time
class Timer:
    __TIMESLICE_UNIT = 1
    __TIMESLICE_NUM = 5
    __system_time = 0
    __rest_time = 0

    def __init__(self):
        self.__rest_time = self.__TIMESLICE_NUM

    def __run__(self):
        time.sleep(self.__TIMESLICE_UNIT)
        self.__system_time = self.__system_time + self.__TIMESLICE_UNIT
        self.__rest_time = (self.__rest_time - self.__TIMESLICE_UNIT) % self.__TIMESLICE_NUM
        if self.__rest_time == 0:
            print('aaaa')

    def set_system_time(self, system_time):
        self.__system_time = system_time

    def get_system_time(self):
        return self.__system_time



if __name__ == "__main__":
    run_code = 0