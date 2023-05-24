# -*- coding:utf-8 -*-
# @FileName : CPU.py
# @Time     : 2023/5/18 21:11
# @Author   : qingyao
import threading
from utils.Container import *
class CPU(threading.Thread):
    # 程序计数器
    PC = 0

    # 指令寄存器
    IR = 0

    # 4个通用寄存器， 4个地址寄存器
    gen_reg = []

    # 基址寄存器
    base_mem_reg = 0

    # 标志寄存器
    flag_reg = 0

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


    @inject("atom_lock", "running_event", "process_over_event")
    def __init__(self, atom_lock, running_event, process_over_event):
        self.atom_lock = atom_lock
        self.running_event = running_event
        self.process_over_event = process_over_event

    def run(self):
        while True:
            if (not self.running_event.is_set()) or self.process_over_event.is_set():
                if not self.running_event.is_set():
                    self.running_event.wait()
                else:
                    continue
            with self.atom_lock:
                self.fetch_instruction()
                self.analysis_and_execute_instruction()


    def fetch_instruction(self):
        pass

    def analysis_and_execute_instruction(self):
        opt = int(self.IR[:8])
        front_obj = int(self.IR[8:12])
        back_obj = int(self.IR[12:16])
        immvalue = int(self.IR[16:32])
        if front_obj >= 4 or back_obj >= 4:
            # get from mem
            get_value = 0
        if opt == 0:
            self.process_over_event.set()
        elif opt == 1:
            # 立即数放到寄存器中
            if back_obj == 0:
                self.gen_reg[front_obj] = immvalue
            # 地址数据 -> 寄存器
            elif front_obj < 4:
                self.gen_reg[front_obj] = get_value
            # 寄存器数据 -> 内存
            else:
                # 写入， write2mem(self.gen_reg[front_obj], self.gen_reg[back_obj])
                pass
        elif opt == 2:
            # 立即数加寄存器
            if back_obj == 0:
                self.gen_reg[front_obj] += immvalue
            else:
                self.gen_reg[front_obj] += get_value
        elif opt == 3:
            # 寄存器 - 立即数
            if back_obj == 0:
                self.gen_reg[front_obj] -= immvalue
            else:
                self.gen_reg[front_obj] -= get_value
        elif opt == 4:
            # 寄存器 * 立即数
            if back_obj == 0:
                self.gen_reg[front_obj] *= immvalue
            else:
                self.gen_reg[front_obj] *= get_value
        elif opt == 5:
            # 寄存器 / 立即数
            if back_obj == 0:
                self.gen_reg[front_obj] //= immvalue
            else:
                self.gen_reg[front_obj] //= get_value
        elif opt == 6:
            if back_obj == 0:
                self.gen_reg[front_obj] = 1 if self.gen_reg[front_obj] and immvalue else 0
            else:
                self.gen_reg[front_obj] = 1 if self.gen_reg[front_obj] and get_value else 0
        elif opt == 7:
            if back_obj == 0:
                self.gen_reg[front_obj] = 1 if self.gen_reg[front_obj] or immvalue else 0
            else:
                self.gen_reg[front_obj] = 1 if self.gen_reg[front_obj] or get_value else 0
        elif opt == 8:
            if front_obj == 0:
                self.gen_reg[back_obj] = 1 if not self.gen_reg[back_obj] else 0
            else:
                # write2mem(self.gen_reg[back_obj], 1 if not get_value else 0)
                pass
        elif opt == 9:
            if back_obj == 0:
                if self.gen_reg[front_obj] == immvalue:
                    self.flag_reg = 0
                elif self.gen_reg[front_obj] < immvalue:
                    self.flag_reg = -1
                else:
                    self.flag_reg = 1
            else:
                if self.gen_reg[front_obj] == get_value:
                    self.flag_reg = 0
                elif self.gen_reg[front_obj] < get_value:
                    self.flag_reg = -1
                else:
                    self.flag_reg = 1
        elif opt == 10:
            if back_obj == 0:
                self.PC += immvalue
            elif back_obj == 1:
                if self.flag_reg == 0:
                    self.PC += immvalue
            elif back_obj == 2:
                if self.flag_reg == 1:
                    self.PC += immvalue
            elif back_obj == 3:
                if self.flag_reg == -1:
                    self.PC += immvalue
        elif opt == 11:
            # 触发IO中断 此处为input
            pass
        elif opt == 12:
            # 触发IO中断， 此处为output
            pass


    def set_gen_reg(self, AX, BX, CX, DX):
        self.AX = AX
        self.BX = BX
        self.CX = CX
        self.DX = DX

    def get_gen_reg(self):
        return self.AX, self.BX, self.CX, self.DX

    def set_PC(self, PC):
        self.PC = PC

    def get_PC(self):
        return self.PC

    def set_event(self, event):
        self.event = event

    def get_event(self):
        return self.event

    def set_device_id(self, id):
        self.device_id = id

    def get_device_id(self):
        return self.device_id

    def set_IR(self, IR):
        self.IR = IR

    def get_IR(self):
        return self.IR

    def set_gen_reg(self, index, value):
        self.gen_reg[index] = value

    def get_gen_reg(self, index,):
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
        return self.gen_reg[0],self.gen_reg[1],self.gen_reg[2],self.gen_reg[3],\
               self.gen_reg[4],self.gen_reg[5],self.gen_reg[6],self.gen_reg[7]

    def set_flag_reg(self, flag):
        self.flag_reg = flag

    def get_flag_reg(self):
        return self.flag_reg