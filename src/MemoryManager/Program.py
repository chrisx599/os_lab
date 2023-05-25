from Memory import *
from ProgramVirtualMem import *
# 程序类,每有一个程序创建,就创建一个程序类,其属性有程序id,以及其页表
class Program:
    program_page_table = None

    def __init__(self):
        self.program_id = None
        self.PROGRAM_cnt = None
        self.program_page_table = PageTable()

    def end_program(self):
        self.program_page_table.recycle_physical_memory()