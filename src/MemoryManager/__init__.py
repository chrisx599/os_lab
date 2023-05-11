import random

PAGE_TABLE_LEVEL = 2 # 四级页表
PAGE_ITEM_SIZE = 8 # 一个页表里可以储存1024个页表项
PAGE_SIZE = 4 # 一个页的大小为4B
PROGRAM_CNT = 0 #程序计数器，创建一个程序，计数器+1
INSTRCUTION_MAX_NUM = 1000 # 程序最多指令条数

# 生成一个随机数列表，size为列表大小，start和end为随机数最小值和最大值
def create_random_list(size,start,end):
    list = []
    for i in range(size):
        list.append(random.randint(start,end))
    return list


# 物理内存类，memory_size代表物理内存大小,frame_size代表一个帧(页)的大小,memory_space则是一个二维的列表，64个页,每页又有4B
class PhysicalMemory:
    memory_size = pow(2, 8)
    frame_size = pow(2, 2)
    frame_num = memory_size / frame_size
    memory_space = list()

    # 初始化一个内存列表，抽象成二维列表
    def _init_memory_space(self):
        self.memory_space = [list() for i in range(self.frame_num)]
        for i in range(self.frame_num):
            memory_space[i] = [list() for i in range(self.frame_size)]
        for i in range(self.frame_num):
            for j in range(self.frame_size):
                memory_space[i][j] = 0

    # 从未分配的页中选择一页分配,返回分配的块号给虚拟内存的分配，虚拟内存将其存储到对应的页中,完成从虚拟内存到物理内存的映射
    def allocate_physical_memory(self):

        #一个死循环,只有找到一个未被使用的页,将其页号记录下来之后,存储到列表中返回,否则一直循环
        while(1):
            block_num = create_random_list(1,0,self.frame_num)
            if(len(self.memory_space[block_num[0]][0]) == 0):
                self.memory_space[block_num[0]][0] = 1
                self.load_memory(instruction_list, list_location,block_num[0])
                return block_num

    def load_memory(self,instruction_list,location,block_num):

        for i in range(PAGE_SIZE):
            self.memory_space[block_num[0]][i] = instruction_list[location]
            location = location + 1


# 创建一个物理内存的实际对象用于后续的使用
real_memory = PhysicalMemory()

# 创建一个指令列表，每当一个程序运行时，将指令读入列表中，一个程序暂停时，记录指令执行的位置，以便重新运行。一个程序终止后，清空该列表。
instruction_list = [list() for i in range (INSTRCUTION_MAX_NUM)]
list_location = 0

# 程序类,每有一个程序创建,就创建一个程序类,其属性有程序id,以及其页表
class Program:

    program_table = 0

    def __init__(self):
        program_id = PROGRAM_CNT
        PROGRAM_CNT = PROGRAM_CNT + 1
        program_table = PageTable()

    def end_program(self):
        self.program_table.recycle_physical_memory()

# 页表类，每个程序都一有一个相应的页表


class PageTable:

    page_table_list = ()
    page_allocated_list = []
    read_list = ()
    write_list = ()

    # 初始化页表列表
    def __init__(self):
        # 一个页表列表里放着各级页表
        page_table_list = [list() for i in range(PAGE_ITEM_SIZE)]

        for i in range(PAGE_ITEM_SIZE):
            page_table_list[i] = [list() for i in range(PAGE_ITEM_SIZE)]

        for i in range(PAGE_ITEM_SIZE):
            for j in range (PAGE_ITEM_SIZE):
                page_table_list[i][j] = PageTableItem

    # 给程序分配虚拟内存页的的函数，need_space代表其一共需要的空间，key_space代表核心部分所需要的空间，用于按需调页，只有key_space大小的页才会实际分配物理内存空间
    def allocate_virtual_memory(self, need_space, key_space):
        offset = 0

        # 计算需要分配的页数,分为整除和不能整除两种情况
        if (need_space % PAGE_SIZE != 0):
            page_count = need_space / PAGE_SIZE + 1
        else:
            page_count = need_space / PAGE_SIZE

        offset = page_count #一共分配了几页，相当于偏移量。
        self.page_allocated_list = [list() for i in range(page_count)]

        # 虚拟内存连续分配
        for i in range(PAGE_ITEM_SIZE):
            for j in range(PAGE_ITEM_SIZE):
                if (self.page_table_list[i][j].state == 0):
                    allocate_list = real_memory.allocate_physical_memory()
                    self.page_table_list[i][j].item_state = 1
                    self.page_table_list[i][j].item_num1 = i;
                    self.page_table_list[i][j].item_num2 = j;
                    self.page_table_list[i][j].physical_block_num = allocate_list[0]
                    page_count = page_count - 1;
                    if(page_count == 0):
                        break
            if(page_count == 0):
                break
        return offset


    def recycle_physical_memory(self):
        for i in range(PAGE_ITEM_SIZE):
            for j in range(PAGE_ITEM_SIZE):
                for k in range(PAGE_SIZE):
                    real_memory[self.page_table_list[i][j].physiccal_block_num][k] = 0
                    self.page_table_list[i][j].item_state = 0
                    self.page_table_list[i][j].item_num1 = 0
                    self.page_table_list[i][j].item_num2 = 0
                    self.page_table_list[i][j].physical_block_num = 0
        # 分配n页循环n次，进行随机分配，将n页存放在n级页表的各个地方
        # for i in range(page_count):
        #     while(1):
        #         page_num = create_random_list(1,0,1023)
        #         if(self.get_item_state(0, page_num[0]) and self.get_item_state(1, page_num[1]) and self.get_item_state(2, page_num[2]) and self.get_item_state(3, page_num[3])):
        #             self.add_item(real_memory.allocate_physical_memory(),page_num,i)
        #             break


    # def add_item(self,physcial_blocknum_list,page_num_list,page_allocated_list_num):
    #
    #     self.page_table_list[PAGE_TABLE_LEVEL - 1].page_table_item_list[page_num_list[3]].num = page_num_list[3]
    #     self.page_table_list[PAGE_TABLE_LEVEL - 1].page_table_item_list[page_num_list[3]].state = 1
    #     self.page_table_list[PAGE_TABLE_LEVEL - 1].page_table_item_list[page_num_list[3]].physical_block0_num = physcial_blocknum_list[0]
    #     self.page_table_list[PAGE_TABLE_LEVEL - 1].page_table_item_list[page_num_list[3]].physical_block1_num = physcial_blocknum_list[1]
    #     for i in range(PAGE_TABLE_LEVEL):
    #         self.page_allocated_list[page_allocated_list_num].append(page_num_list[i])
    #
    # def item_not_used(self,page_num,item_num):
    #
    #     if(self.page_table_list[page_num].page_table_item_list[item_num].item_state == 0):
    #
    #         return true

# class PageTable:
#
#     def __init__(self):
#         page_table_item_list = list(PageTableItem for i in range(PAGE_ITEM_SIZE))


class PageTableItem:

    def __init__(self):

        item_num1 = 0
        item_num2 = 0
        item_state = 0
        physical_block_num = 0
        is_write = 0
        is_read = 0
