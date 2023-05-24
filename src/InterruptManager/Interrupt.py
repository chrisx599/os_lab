# -*- coding:utf-8 -*-
# @FileName : Interrupt.py
# @Time     : 2023/5/18 10:39
# @Author   : qingyao
from processManager.PCB import PCB
interrupt_vector = []
class Interrput:
    def __init__(self):
        file = open("interrupt_vector_table")
        for line in file:
            interrupt_vector.append(line)
        file.close()
    def interrupt_handling(self):
        type = self.interrupt_pcb.get_event()
        func_name = interrupt_vector[type]
        eval(func_name + '()')

def do_divide_error():
    # 保存上下文环境，释放所有临界资源
    # 日志记录
    # 通过进程树获取父进程
    pass

def do_page_fault():
    '''
    当程序请求访问某个虚拟地址时，若该地址尚未在内存中，则会触发缺页中断。

    操作系统内核会检查该地址是否属于合法的虚拟地址空间，并且是否有相应的页表项。

    如果有相应的页表项，则操作系统会将该页表项读入内存，并设置对应的物理页框。

    如果没有相应的页表项，则会发生页表项缺失，需要操作系统进行相应的处理。

    操作系统会选择一个空闲的物理页框，并将其分配给该虚拟页面，同时更新该页的页表项。

    如果物理页框已被占用，则需要进行页面置换，选择一个合适的物理页框并将其内容替换出去。

    替换出去的页面需要进行保存，可以写入磁盘或者其他存储介质。

    如果某个页已经被修改，则需要将其写回磁盘，以保证数据的一致性。

    处理完缺页中断后，操作系统会重新执行之前被中断的指令，程序可以继续运行。
    :param address:
    :return:
    '''
    pass

def do_syscall_64():
    pass


def do_IRQ(device:int):
    if device == 1:
        pass
    elif device == 2:
        pass
    elif device == 3:
        pass
    elif device == 4:
        pass

