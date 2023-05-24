# -*- coding:utf-8 -*-
# @FileName : PCB.py
# @Time     : 2023/3/17 19:00
# @Author   : qingyao
import random

from IDGenerator import *
from utils.Container import *


class PCB:

    PROCESS_READY = 'ready'
    PROCESS_RUNNING = 'running'
    PROCESS_BLOCK = 'block'
    PROCESS_EXIT = 'exit'

    # 进程唯一标识
    PID = 0

    # 进程名
    name = ""

    # 进程优先级
    priority = 0
    # 进程状态
    state = ""
    # 进程程序计数器
    PC = 0

    # 指令寄存器
    IR = 0

    # 4个通用寄存器,4个地址寄存器
    gen_reg = []

    # 标志寄存器
    flag_reg = 0

    # 基址寄存器
    base_mem_reg = 0

    # 数据区起始地址
    data_start_location = 0

    # 界限寄存器
    limit_mem_reg = 0

    # 进程大小
    size = 0

    # IO相关参数, 1表示input， 2表示output
    event = 0

    # IO传输的数据量大小
    buffer_size = 0

    # 需要使用的设备的逻辑号
    device_id = -1

    # 调度参数:到达时间
    arrive_time = -1

    # 进程运行完毕是否立即被释放
    release = 0

    # 累计运行时间
    total_time = 0

    def __init__(self, name):
        self.PID = IDGenerator.create_id(IDGenerator)
        self.name = name

    def get_PID(self):
        return self.PID

    def set_PID(self, PID):
        self.PID = PID

    def set_data_start_location(self, location):
        self.data_start_location = location

    def get_data_start_location(self):
        return self.data_start_location

    def get_size(self):
        return self.size

    def set_size(self, size):
        self.size = size

    def set_event(self, event):
        self.event = event

    def get_event(self):
        return self.event

    def set_buffer_size(self, buffer_size):
        self.buffer_size = buffer_size

    def get_buffer_size(self):
        return self.buffer_size

    def set_device_id(self, device_id):
        self.device_id = device_id

    def get_device_id(self):
        return self.device_id

    def set_arrive_time(self, arrive_time):
        self.arrive_time = arrive_time

    def get_arrive_time(self):
        return self.arrive_time


    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_PC(self, pc):
        self.PC = pc

    def get_PC(self):
        return self.PC

    def set_gen_reg(self, index, value):
        self.gen_reg[index] = value

    def get_gen_reg(self, index):
        return self.gen_reg[index]

    def set_gen_reg_all(self, value0, value1, value2, value3,
                        value4, value5, value6, value7):
        self.gen_reg[0] = value0
        self.gen_reg[1] = value1
        self.gen_reg[2] = value2
        self.gen_reg[3] = value3
        self.gen_reg[4] = value4
        self.gen_reg[5] = value5
        self.gen_reg[6] = value6
        self.gen_reg[7] = value7

    def get_gen_reg_all(self):
        return self.gen_reg[0], self.gen_reg[1], self.gen_reg[2], self.gen_reg[3], \
               self.gen_reg[4], self.gen_reg[5], self.gen_reg[6], self.gen_reg[7]

    def set_base_mem_reg(self, base_mem):
        self.base_mem_reg = base_mem

    def get_base_mem_reg(self):
        return self.base_mem_reg

    def set_limit_mem_reg(self, limit_mem):
        self.limit_mem_reg = limit_mem

    def get_limit_reg(self):
        return self.limit_mem_reg

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_priority(self):
        return self.priority

    def set_priority(self, priority):
        self.priority = priority

    def set_release(self, release):
        self.release = release

    def get_release(self):
        return self.release

    def set_flag_reg(self, flag):
        self.flag_reg = flag

    def get_flag_reg(self):
        return self.flag_reg
