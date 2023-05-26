# -*- coding:utf-8 -*-
# @FileName : PCB.py
# @Time     : 2023/3/17 19:00
# @Author   : qingyao
import random


from utils.Container import *


class PCB:



    # 进程唯一标识
    PID = 0

    # 进程名
    name = ""

    # 进程优先级
    priority = -1
    # 进程状态
    state = ""
    # 进程程序计数器
    PC = 0

    # 指令寄存器
    IR = 0

    # 4个通用寄存器,4个地址寄存器
    gen_reg = [0, 0, 0, 0, 0, 0, 0, 0]

    # 标志寄存器
    flag_reg = 0

    # 基址寄存器
    base_mem_reg = 0

    # code_size
    code_size = 0

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

    # IO内容
    buffer_content = ""

    # 缓冲区首地址
    buffer_address = 0

    # 需要使用的设备的逻辑号
    device_id = -1

    # 调度参数:到达时间
    arrive_time = -1

    # 进程运行完毕是否立即被释放
    release = 0

    # page_num
    page_num = 0

    # 累计运行时间
    total_time = 0

    @inject("id_generator")
    def __init__(self, name, id_generator):
        self.PID = id_generator.create_id()
        self.name = name
        self.priority = 1
        self.state = ""
        self.gen_reg = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.event = 0
        self.device_id = -1
        self.arrive_time = -1
        self.page_num = 0
        self.total_time = 0
        self.buffer_address = 0
        self.buffer_size = 0
        self.PC = 0
        self.IR = ""
        self.flag_reg = 0
        self.base_mem_reg = 0
        self.code_size = 0
        self.data_start_location = 0
        self.limit_mem_reg = 0
        self.size = 0
        self.IO_reg = 0
        self.PROCESS_READY = 'ready'
        self.PROCESS_RUNNING = 'running'
        self.PROCESS_BLOCK = 'block'
        self.PROCESS_EXIT = 'exit'

    def get_PID(self):
        return self.PID

    def set_PID(self, PID):
        self.PID = PID

    def set_IO_reg(self, reg):
        self.IO_reg = reg

    def get_IO_reg(self):
        return self.IO_reg

    def set_code_size(self, code_size):
        self.code_size = code_size

    def get_code_size(self):
        return self.code_size

    def set_IR(self, IR):
        self.IR = IR

    def get_IR(self):
        return self.IR


    def get_page_num(self):
        return self.page_num

    def set_page_num(self, page_num):
        return self.page_num

    def set_buffer_address(self, address):
        self.buffer_address = address

    def get_buffer_address(self):
        return self.buffer_address

    def set_buffer_content(self, content):
        self.buffer_content = content

    def get_buffer_content(self):
        return self.buffer_content

    def get_total_time(self):
        return self.total_time

    def set_total_time(self, total_time):
        self.total_time = total_time

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

    def set_gen_reg_all(self, value1, value2, value3,
                        value4, value5, value6, value7, value8):
        self.gen_reg[1] = value1
        self.gen_reg[2] = value2
        self.gen_reg[3] = value3
        self.gen_reg[4] = value4
        self.gen_reg[5] = value5
        self.gen_reg[6] = value6
        self.gen_reg[7] = value7
        self.gen_reg[8] = value8

    def get_gen_reg_all(self):
        return self.gen_reg[1], self.gen_reg[2], self.gen_reg[3], self.gen_reg[4], \
               self.gen_reg[5], self.gen_reg[6], self.gen_reg[7], self.gen_reg[8]

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
