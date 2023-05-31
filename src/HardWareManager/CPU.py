# -*- coding:utf-8 -*-
# @FileName : CPU.py
# @Time     : 2023/5/18 21:11
# @Author   : qingyao
import threading
from utils.Container import *
from MemoryManager.Memory import *
import ctypes
import time
class CPU(threading.Thread):
    # processId

    PID = 0

    # process
    running_pcb = None

    # 程序计数器
    PC = 0

    # 指令寄存器
    IR = 0

    # 4个通用寄存器， 4个地址寄存器
    gen_reg = [0, 0, 0, 0, 0, 0, 0, 0, 0]

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

    buffer_content = 0

    buffer_address = 0

    # 需要使用的设备的逻辑号
    device_id = -1


    @inject("atom_lock", "running_event", "process_over_event", "memory",
            "interrupt_event", "interrupt_pcb_queue", "interrupt_message_queue", "exit_event", "force_dispatch_event")
    def __init__(self, atom_lock, running_event, process_over_event, memory,
                 interrupt_event, interrupt_pcb_queue, interrupt_message_queue, exit_event, force_dispatch_event):
        super().__init__(name="cpu")
        self.atom_lock = atom_lock
        self.running_event = running_event
        self.process_over_event = process_over_event
        self.memory = memory
        self.interrupt_event = interrupt_event
        self.interrupt_message_queue = interrupt_message_queue
        self.interrupt_pcb_queue = interrupt_pcb_queue
        self.exit_event = exit_event
        self.force_dispatch_event = force_dispatch_event

    def get_PID(self):
        return self.PID

    def set_PID(self, PID):
        self.PID = PID

    def run(self):
        while True:
            if self.force_dispatch_event.is_set():
                if self.exit_event.is_set():
                    return
                continue
            # 如果进程正在运行并且进程结束信号没有发出并且中断信号没有发出
            if (not self.running_event.is_set()) or self.interrupt_event.is_set():
                if not self.running_event.is_set():
                    # print("cpu: now waiting running_event")
                    self.running_event.wait()
                    # print("cpu: running_event get")
                    if self.exit_event.is_set():
                        # print("CPU thread ended")
                        return
                else:
                    continue


            self.atom_lock.acquire()
            self.fetch_instruction()
            time.sleep(0.003)
            # print(str(self.running_pcb.get_PID()) +" now is " + str(self.IR))
            self.analysis_and_execute_instruction()
            # print(str(self.PID) + ": " + self.IR)
            self.atom_lock.release()
            time.sleep(0.1)


    def fetch_instruction(self):
        if self.PC > self.running_pcb.code_size:
            self.running_pcb.state(self.running_pcb.PROCESS_EXIT)
            self.force_dispatch_event.set()
            return

        address = self.base_mem_reg + self.PC
        # print("cpU:::::::::::::::base_mem_reg:" + str(self.base_mem_reg) + " PC:" + str(self.PC))
        flag = self.memory.program_check_page_fault(address // 64, self.PID)
        if flag == -2:
            pass
            # print("update LRU")
        else:
            message = {"page_num": address // 64, "PID": self.PID, "flag": flag}
            self.interrupt_message_queue.put(message)
            self.interrupt_event.set()
        while self.interrupt_event.is_set():
            pass
        IRs = self.memory.program_get_instruction(self.base_mem_reg + self.PC, self.PID)
        self.IR = IRs[0] + IRs[1] +IRs[2] + IRs[3]
        # print(self.IR)
        self.PC += 4

    def analysis_and_execute_instruction(self):
        if self.force_dispatch_event.is_set():
            return
        opt = int(self.IR[:8], 2)
        front_obj = int(self.IR[8:12], 2)
        back_obj = int(self.IR[12:16], 2)
        immvalue = int(self.IR[16:32], 2)


        if opt == 0:
            print(self.gen_reg)
            self.running_pcb.state = self.running_pcb.PROCESS_EXIT
            self.force_dispatch_event.set()
            # print("cpu set force")
            time.sleep(1)
        elif opt == 1:
            # 立即数放到寄存器中
            if back_obj == 0:
                self.gen_reg[front_obj] = immvalue
            # 地址数据 -> 寄存器
            elif front_obj < 4:
                address = self.gen_reg[back_obj]
                flag = self.memory.program_check_page_fault(address // 64, self.PID)
                if flag == -2:
                    pass
                    # print("update LRU")
                else:
                    message = {"page_num" : address // 64, "PID" :self.PID, "flag": flag}
                    self.interrupt_message_queue.put(message)
                    self.interrupt_event.set()
                while self.interrupt_event.is_set():
                    continue
                get_value = self.memory.program_read_memory(self.get_PID(), address, 1)
                self.gen_reg[front_obj] = get_value
            # 寄存器数据 -> 内存
            else:
                address = self.gen_reg[front_obj]
                flag = self.memory.program_check_page_fault(address // 64, self.PID)
                if flag == -2:
                    pass
                    # print("update LRU")
                else:
                    # print("address:" + str(address))
                    # print("front_obj" + str(front_obj))
                    message = {"page_num" : address // 64, "PID" :self.PID, "flag": flag}
                    self.interrupt_message_queue.put(message)
                    # self.interrupt_message_queue.put(address // 64)
                    # self.interrupt_message_queue.put(self.get_PID())
                    # self.interrupt_message_queue.put(flag)
                    self.interrupt_event.set()
                while self.interrupt_event.is_set():
                    continue
                self.memory.program_write_memory(self.running_pcb.get_PID(), address, self.gen_reg[back_obj])
        elif opt == 2:
            # 立即数加寄存器
            if back_obj == 0:
                self.gen_reg[front_obj] += immvalue
            elif back_obj < 5:
                self.gen_reg[front_obj] += self.gen_reg[back_obj]
            else:
                address = self.gen_reg[back_obj]
                flag = self.memory.program_check_page_fault(address // 64, self.PID)
                if flag == -2:
                    pass
                    # print("update LRU")
                else:
                    message = {"page_num": address // 64, "PID": self.PID, "flag": flag}
                    # print("cpu::::::flag:" + str(flag))
                    self.interrupt_message_queue.put(message)
                    self.interrupt_event.set()
                while self.interrupt_event.is_set():
                    continue
                # print("address:" + str(address))
                # print("back_obj:" + str(back_obj))
                get_value = self.memory.program_read_memory(self.get_PID(), address, 1)
                # print("test: get_value" + str(get_value))
                # print("test: reg " + str(self.gen_reg[front_obj]))
                self.gen_reg[front_obj] += int(get_value[0])
        elif opt == 3:
            # 寄存器 - 立即数
            if back_obj == 0:
                self.gen_reg[front_obj] += immvalue
            else:
                address = self.gen_reg[back_obj]
                flag = self.memory.program_check_page_fault(address // 64, self.PID)
                if flag == -2:
                    pass
                    # print("update LRU")
                else:
                    message = {"page_num": address // 64, "PID": self.PID, "flag": flag}
                    # print("cpu::::::flag:" + str(flag))
                    self.interrupt_message_queue.put(message)
                    self.interrupt_event.set()
                while self.interrupt_event.is_set():
                    continue
                # print("address:" + str(address))
                # print("back_obj:" + str(back_obj))
                get_value = self.memory.program_read_memory(self.get_PID(), address, 1)
                # print("test: get_value" + str(get_value))
                # print("test: reg " + str(self.gen_reg[front_obj]))
                self.gen_reg[front_obj] -= int(get_value[0])
        elif opt == 4:
            # 寄存器 * 立即数
            if back_obj == 0:
                self.gen_reg[front_obj] += immvalue
            else:
                address = self.gen_reg[back_obj]
                flag = self.memory.program_check_page_fault(address // 64, self.PID)
                if flag == -2:
                    pass
                    # print("update LRU")
                else:
                    message = {"page_num": address // 64, "PID": self.PID, "flag": flag}
                    # print("cpu::::::flag:" + str(flag))
                    self.interrupt_message_queue.put(message)
                    self.interrupt_event.set()
                while self.interrupt_event.is_set():
                    continue
                # print("address:" + str(address))
                # print("back_obj:" + str(back_obj))
                get_value = self.memory.program_read_memory(self.get_PID(), address, 1)
                # print("test: get_value" + str(get_value))
                # print("test: reg " + str(self.gen_reg[front_obj]))
                self.gen_reg[front_obj] *= int(get_value[0])
        elif opt == 5:
            # 寄存器 / 立即数
            if back_obj == 0:
                self.gen_reg[front_obj] //= immvalue
            else:
                address = self.gen_reg[back_obj]
                flag = self.memory.program_check_page_fault(address // 64, self.PID)
                if flag == -2:
                    pass
                    # print("update LRU")
                else:
                    message = {"page_num": address // 64, "PID": self.PID, "flag": flag}
                    self.interrupt_message_queue.put(message)
                    self.interrupt_event.set()
                while self.interrupt_event.is_set():
                    continue
                get_value = self.memory.program_read_memory(self.get_PID(), address, 1)
                self.gen_reg[front_obj] //= get_value
        elif opt == 6:
            if back_obj == 0:
                self.gen_reg[front_obj] = 1 if self.gen_reg[front_obj] and immvalue else 0
            else:
                address = self.gen_reg[back_obj]
                flag = self.memory.program_check_page_fault(address // 64, self.PID)
                if flag == -2:
                    pass
                    # print("update LRU")
                else:
                    message = {"page_num": address // 64, "PID": self.PID, "flag": flag}
                    self.interrupt_message_queue.put(message)
                    self.interrupt_event.set()
                while self.interrupt_event.is_set():
                    continue
                get_value = self.memory.program_read_memory(self.get_PID(), address, 1)
                self.gen_reg[front_obj] = 1 if self.gen_reg[front_obj] and get_value else 0
        elif opt == 7:
            if back_obj == 0:
                self.gen_reg[front_obj] = 1 if self.gen_reg[front_obj] or immvalue else 0
            else:
                address = self.gen_reg[back_obj]
                flag = self.memory.program_check_page_fault(address // 64, self.PID)
                if flag == -2:
                    pass
                    # print("update LRU")
                else:
                    message = {"page_num": address // 64, "PID": self.PID, "flag": flag}
                    self.interrupt_message_queue.put(message)
                    self.interrupt_event.set()
                while self.interrupt_event.is_set():
                    continue
                get_value = self.memory.program_read_memory(self.get_PID(), address, 1)
                self.gen_reg[front_obj] = 1 if self.gen_reg[front_obj] or get_value else 0
        elif opt == 8:
            if back_obj == 0:
                self.gen_reg[front_obj] = 1 if not self.gen_reg[front_obj] else 0
            else:
                address = self.gen_reg[back_obj]
                flag = self.memory.program_check_page_fault(address // 64, self.PID)
                if flag == -2:
                    pass
                    # print("update LRU")
                else:
                    message = {"page_num": address // 64, "PID": self.PID, "flag": flag}
                    self.interrupt_message_queue.put(message)
                    self.interrupt_event.set()
                while self.interrupt_event.is_set():
                    continue
                # write2mem(self.gen_reg[back_obj], 1 if not get_value else 0)
                get_value = self.memory.program_read_memory(self.get_PID(), address, 1)
                self.memory.program_write_memory(self.running_pcb.get_PID(), address, 1 if not get_value else 0)
        elif opt == 9:
            if back_obj == 0:
                if self.gen_reg[front_obj] == immvalue:
                    self.flag_reg = 0
                elif self.gen_reg[front_obj] < immvalue:
                    self.flag_reg = -1
                else:
                    self.flag_reg = 1
            else:
                address = self.gen_reg[back_obj]
                flag = self.memory.program_check_page_fault(address // 64, self.PID)
                if flag == -2:
                    pass
                    # print("update LRU")
                else:
                    message = {"page_num": address // 64, "PID": self.PID, "flag": flag}
                    self.interrupt_message_queue.put(message)
                    self.interrupt_event.set()
                while self.interrupt_event.is_set():
                    continue
                get_value = self.memory.program_read_memory(self.get_PID(), address, 1)
                if self.gen_reg[front_obj] == get_value:
                    self.flag_reg = 0
                elif self.gen_reg[front_obj] < get_value:
                    self.flag_reg = -1
                else:
                    self.flag_reg = 1
        elif opt == 10:
            if immvalue > 32767:
                immvalue -= 65536
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
        elif opt == 11 or opt == 12:
            ax, bx, cx, dx, axm, bxm, cxm, dxm = self.get_gen_reg_all()
            self.running_pcb.set_gen_reg_all(ax, bx, cx, dx, axm, bxm, cxm, dxm)
            pc = self.get_PC()
            self.running_pcb.set_PC(pc)
            ir = self.get_IR()
            self.running_pcb.set_IR(ir)
            self.running_pcb.buffer_address = self.buffer_address
            self.running_pcb.set_event(2)
            # 如果是输出的话，就把寄存器的值送到content中。
            if opt == 12:
                self.running_pcb.buffer_content = self.gen_reg[front_obj]
            self.running_pcb.set_device_id(1 if opt == 11 else 2)
            self.running_pcb.set_state(self.running_pcb.PROCESS_BLOCK)
            self.interrupt_pcb_queue.put(self.running_pcb)
            self.interrupt_event.set()
        elif opt == 13:
            item = self.memory.read_buffer(self.buffer_address)
            self.gen_reg[front_obj] = item
        elif opt == 14:
            # apply device
            dev_num = immvalue
            self.running_pcb.set_event(2)
            self.running_pcb.set_device_id(immvalue)
            self.interrupt_pcb_queue.put(self.running_pcb)
            self.interrupt_event.set()
        # print(self.gen_reg[1], self.gen_reg[2],self.gen_reg[3],self.gen_reg[4],
            #   self.gen_reg[5], self.gen_reg[6],self.gen_reg[7],self.gen_reg[8])







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
        return self.gen_reg[1],self.gen_reg[2],self.gen_reg[3],self.gen_reg[4],\
               self.gen_reg[5],self.gen_reg[6],self.gen_reg[7],self.gen_reg[8]

    def set_flag_reg(self, flag):
        self.flag_reg = flag

    def get_flag_reg(self):
        return self.flag_reg

