# -*- coding:utf-8 -*-
# @FileName : PCB.py
# @Time     : 2023/3/17 19:00
# @Author   : qingyao
import random

from IDGenerator import *


class PCB:

    PROCESS_READY = 'ready'
    PROCESS_RUNNING = 'running'
    PROCESS_BLOCK = 'block'
    PROCESS_NEW = 'new'
    PROCESS_EXIT = 'exit'

    # 进程唯一标识
    __PID = 0

    # 进程名
    __name = ""

    # 进程优先级
    __priority = 0
    # 进程状态
    __state = ""
    # 进程程序计数器
    __PC = 0

    # 4个通用寄存器
    __AX = 0
    __BX = 0
    __CX = 0
    __DX = 0

    # 基址寄存器
    __base_mem_reg = 0
    # 界限寄存器
    __limit_mem_reg = 0

    def __init__(self, name):
        self.__PID = IDGenerator.create_id(IDGenerator)
        self.__name = name

    def set_state(self, state):
        self.__state = state

    def get_state(self):
        return self.__state

    def set_PC(self, pc):
        self.__PC = pc

    def get_PC(self):
        return self.__PC

    def set_AX(self, AX):
        self.__AX = AX

    def get_AX(self):
        return self.__AX

    def set_BX(self, BX):
        self.__BX = BX

    def get_BX(self):
        return self.BX

    def set_CX(self, CX):
        self.__CX = CX

    def get_CX(self):
        return self.CX

    def set_DX(self, DX):
        self.__DX = DX

    def get_DX(self):
        return self.BD

    def set_base_mem_reg(self, base_mem):
        self.__base_mem_reg = base_mem

    def get_base_mem_reg(self):
        return self.__base_mem_reg

    def set_limit_mem_reg(self, limit_mem):
        self.__limit_mem_reg = limit_mem

    def get_limit_reg(self):
        return self.__limit_mem_reg

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_priority(self):
        return self.__priority

    def set_priority(self, priority):
        self.__priority = priority


if __name__ == "__main__":
    run_code = 0