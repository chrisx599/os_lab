PAGE_TABLE_LEVEL = 4
PAGE_ITEM_SIZE = 1024
PAGE_SIZE = 4096


class PhysicalMemory:
    memory_size = pow(2, 32)
    frame_size = pow(2, 12)
    memory_space = list()

    # def __init__(self):

    def __init_memory_space(self):
        self.memory_space = [list() for i in range(1024)]
        for i in range(1024):
            memory_space[i] = [list() for i in range(1024)]
        for i in range(4096):
            memory_space[i][j] = [str for i in range(4096)]

    def allocate_physical_memory(self,need_space,pid,program_data):

        if need_space <= pow(2, 12):
            for i in range (1024):
                for j in range (1024):
                    for k in range (4096):
                        if self.memory_space[i][j][k] == '':
                            self.memory_space[i][j][k] = program_data

        physical_addr = i * pow(2, 22) + j * pow(2, 12) + k



# 程序类
class Program:

    def __init__(self, start_addr, length, table):
        program.id = 0
        program.start_addr = start_addr
        program.length = length
        program.table = table

# 页表类，每个程序都一有一个相应的页表


class PageTableList:

    # 初始化页表列表
    def __init__(self, depth):
        # 一个页表里面
        page_table_list = list(PageTable for i in range(PAGE_TABLE_LEVEL))


class PageTable:
    def __init__(self):
        page_table_item_list = list(PageTableItem for i in range(PAGE_ITEM_SIZE))


class PageTableItem:

    def __init__(self):
        item_num = 0
        item_state = 0
        item_level = 0
        next_table = 0
        is_write = 0
        is_read = 0
