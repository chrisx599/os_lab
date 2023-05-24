from __init__ import *
# 程序类,每有一个程序创建,就创建一个程序类,其属性有程序id,以及其页表
class Program:

    program_table = None

    def __init__(self):
        program_id = PROGRAM_CNT
        PROGRAM_cnt = PROGRAM_CNT + 1
        program_table = PageTable()

    def end_program(self):
        self.program_table.recycle_physical_memory()