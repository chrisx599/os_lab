import random
from utils.Container import *
from utils.logger import *
from PageTableItem import *
from PhysicalMemory import *
from Program import *
from constant import *
from ProgramVirtualMem import *
from FileManager.FileOperation import *
from FileManager.FileCore import *
from DeviceManager.DeviceManager import *

# PAGE_TABLE_LEVEL = 2  # 四级页表
# PAGE_ITEM_SIZE = 32  # 一个页表里可以储存32个页表项
# PAGE_SIZE = 64  # 一个页的大小为64B
# PROGRAM_CNT = 0  # 程序计数器，创建一个程序，计数器+1
# MAX_PROGRAM = 100 # 最大程序个数
# INSTRCUTION_MAX_NUM = 1000  # 程序最多指令条数
# INSTRCUTION_LENGTH = 4




class Memory:

    def __init__(self):
        self.physical_memory = real_memory
        self.program_list = [Program() for i in range(MAX_PROGRAM)]
        self.program_num = None

    def get_memory_size(self):
        return self.physical_memory.memory_size
    def get_block_size(self):
        return self.physical_memory.block_size
    def get_all_block_num(self):
        return self.physical_memory.block_num
    def get_core_block_num(self):
        return self.physical_memory.core_block_num
    def used_block_list(self):
        block_list = [list() for i in range (16)]
        for i in range(16):
            for j in range(16):
                block_list[i].append(0)
        block_num = self.physical_memory.block_num
        count = 0
        for i in range(16):
            for j in range(16):
                if(self.physical_memory.memory_space[count][0] != 0):
                    block_list[i][j] = 1
                else:
                    block_list[i][j] = 0
                count = count + 1
        return block_list
    def used_block_num(self):
        count = 0
        block_num = self.physical_memory.block_num
        for i in range(block_num):
            if (self.physical_memory.memory_space[i][0] != 0):
                count = count + 1
        return count

    def create_program(self,program_num):
        self.program_list[program_num].program_id = program_num
        return len(self.program_list[program_num].program_page_table.instruction_list) * 4
    def load_program(self,program_num,instruction_list):
        self.program_list[program_num].program_page_table.__init__()
        self.program_list[program_num].program_page_table.instruction_list = instruction_list
        self.program_list[program_num].program_page_table.allocate_virtual_memory(len(instruction_list), 1)

    def program_get_instruction(self,addr,program_num):
        ins_list = []
        page_num = addr // PAGE_SIZE
        page_offset = addr % PAGE_SIZE
        # self.program_list[program_num].program_page_table.check_page_interruption(page_num)
        #处理完了，可以用了
        physical_block = self.program_list[program_num].program_page_table.page_table_list[page_num].physical_block_num
        for i in range(4):
            ins_list.append(self.physical_memory.memory_space[physical_block][page_offset + i])
        return ins_list


    def program_read_memory(self,program_num,addr,offset):
        data_list = []
        page_num = addr // PAGE_SIZE
        page_offset = addr % PAGE_SIZE
        # self.program_list[program_num].program_page_table.check_page_interruption(page_num)
        #处理完了，可以用了
        physical_block = self.program_list[program_num].program_page_table.page_table_list[page_num].physical_block_num
        for i in range(offset):
            count = 0
            data_list.append(self.physical_memory.memory_space[physical_block][page_offset + count])
            count = count + 1
        #todo: 此处要处理一下列表
        return data_list


    def program_check_page_fault(self,page_num,program_num):
        out_page = self.program_list[program_num].program_page_table.check_page_interruption(page_num)
        return out_page

    def program_deal_page_fault(self,page_num,program_num,out_page):
        if(out_page >= 0):
            self.program_replace_vm_page(page_num,program_num,out_page)
        else:#分配的情况
            if(self.program_list[program_num].program_page_table.used_block_num != 1):
                self.program_lru_allocate_page(page_num,program_num)

    def program_replace_vm_page(self,page_num,program_num,out_page):
        self.program_list[program_num].program_page_table.replace_page(page_num,out_page)

    def program_lru_allocate_page(self,page_num,program_num):
        self.program_list[program_num].program_page_table.lru_allocate_page(page_num)


    def program_recycle_physcial_memory(self,program_num):
        for i in range(self.program_list[program_num].program_page_table.page_num):
            if(self.program_list[program_num].program_page_table.page_table_list[i].item_state == 1):
                block_num = self.program_list[program_num].program_page_table.page_table_list[i].physical_block_num
                self.physical_memory.unload_block(block_num)
                self.program_list[program_num].program_page_table.page_table_list[i].item_state = 0
                self.program_list[program_num].program_page_table.page_table_list[i].physical_block_num = None
            elif(self.program_list[program_num].program_page_table.page_table_list[i].item_state == 2):
                self.program_list[program_num].program_page_table.page_table_list[i].item_state = 0
                self.program_list[program_num].program_page_table.page_table_list[i].page_num = None

    def write_buffer(self,write_str):
        buffer_page = 0
        temp_list = []
        for i in range(PAGE_SIZE):
            if(self.physical_memory[buffer_page][i] == 0):
                self.physical_memory[buffer_page][i] = write_str
                temp_list.append(i)
                temp_list.append(1)
                break
        return temp_list


    def program_write_memory(self, program_num, addr, write_str):
        page_num = addr // PAGE_SIZE
        page_offset = addr % page_num
        block_num = self.program_list[program_num].program_page_table.page_table_list[page_num].physical_block_num
        self.physical_memory.memory_space[block_num][page_offset] = write_str
        return 1


# 1.运行一个程序从，文件系统返回一个代码
# 2.把代码放入内存中
# 3.CPU开始执行代码，通过地址取指令

#CPU调用检查中断函数 check
#若有缺页中断，则进行换页 replace or allocate
#CPU调用换页函数之后再读或写内存 read or write
# 666