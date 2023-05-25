# -*- coding:utf-8 -*-
# @FileName : constant.py.py
# @Time     : 2023/5/25 4:10
# @Author   : qingyao
PAGE_TABLE_LEVEL = 2  # 四级页表
PAGE_ITEM_SIZE = 32  # 一个页表里可以储存32个页表项
PAGE_SIZE = 64  # 一个页的大小为64B
PROGRAM_CNT = 0  # 程序计数器，创建一个程序，计数器+1
MAX_PROGRAM = 100 # 最大程序个数
INSTRCUTION_MAX_NUM = 1000  # 程序最多指令条数
INSTRCUTION_LENGTH = 4
if __name__ == "__main__":
    run_code = 0
