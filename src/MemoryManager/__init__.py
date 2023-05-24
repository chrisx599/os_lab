import random

PAGE_TABLE_LEVEL = 2 # 四级页表
PAGE_ITEM_SIZE = 32 # 一个页表里可以储存32个页表项
PAGE_SIZE = 64 # 一个页的大小为64B
PROGRAM_CNT = 0 #程序计数器，创建一个程序，计数器+1
INSTRCUTION_MAX_NUM = 1000 # 程序最多指令条数
INSTRCUTION_LENGTH = 4

# 生成一个随机数列表，size为列表大小，start和end为随机数最小值和最大值
def create_random_list(size,start,end):
    list = []
    for i in range(size):
        list.append(random.randint(start,end))
    return list

class Node:
    value = 0
    next = None

class linklist:
    head = None

    def __init__(self):
        head = Node()

    def get_length(self):
        count = 0
        cur_node = self.head
        while(cur_node != None):
            count = count + 1
            cur_node = curNode.next
        return count


    def insert_head(self,value):
        new_node = Node()
        new_node.value = value
        new_node.next = self.head
        self.head = new_node

    def insert_tail(self,value):
        new_node = Node()
        new_node.value = value
        cur_node = self.head
        while(cur_node.next != None):
            cur_node = cur_node.next
        cur_node.next = new_node
        new_node.next = None

    def search_value(self,value):
        cur_node = self.head
        count = 0
        while(cur_node != None):
            if(cur_node.value == value):
                return count + 1
            cur_node = cur_node.next
            count = count + 1
        return 0


    # 物理内存类，memory_size代表物理内存大小,block_size代表一个块(页)的大小，64B,memory_space则是一个二维的列表,256个块(页),每页又有64B/4,16条指令
class PhysicalMemory:
    memory_size = pow(2, 14) #物理内存总大小
    block_size = pow(2, 6) #一个块的大小
    block_num = memory_size / block_size #一共有多少块
    used_block_num = 0 # 使用了多少物理块
    block_threshold_num = block_num / 8 #设定的是剩余块阈值
    memory_space = list()

    # 初始化一个内存列表，抽象成二维列表,一个数组元素储存
    def _init_memory_space(self):
        #一维为块号，代表有这么多物理内存块
        self.memory_space = [list() for i in range(self.block_num)]
        #二维代表一个物理内存块是多少字节，block_size是64，列表有64个元素，一个元素代表着一个字节(byte)
        for j in range(self.block_num):
            memory_space[j] = [list() for i in range(self.block_size)]
        #每个块都初始化一下，置0
        for i in range(self.block_num):
            for j in range(self.block_size):
                memory_space[i][j] = 0

    # 从未分配的页中选择一页分配,返回分配的块号给虚拟内存的分配，虚拟内存将其存储到对应的页中,完成从虚拟内存到物理内存的映射
    def allocate_physical_memory(self):

        #一个死循环,只有找到一个未被使用的页,将其页号记录下来之后,存储到列表中返回,否则一直循环
        while(1):
            temp_block_num = create_random_list(1,0,self.block_num)
            if(len(self.memory_space[temp_block_num[0]][0]) == 0):
                self.memory_space[temp_block_num[0]][0] = 1
                return temp_block_num[0]

    #把指令装入对应的内存中
    def load_memory(self,instruction_list,location,block_num):

        for i in range(PAGE_SIZE):
            self.memory_space[block_num[0]][i] = instruction_list[location]
            location = location + 1

    #检测物理内存中是否还有空闲块
    def exist_available_page(self):

        avai_page = self.block_num - self.used_block_num
        if(avai_page > self.block_threshold_num):
            return 1
        else:
            return 0

    # 清空对应物理块中的内存
    def unload_block(self,block_num):

        for i in range(self.block_size / INSTRCUTION_LENGTH):
            self.memory_space[block_num][i] = 0

# 创建一个物理内存的实际对象用于后续的使用
real_memory = PhysicalMemory()

# 程序类,每有一个程序创建,就创建一个程序类,其属性有程序id,以及其页表
class Program:

    program_table = 0
    program_page_table = PageTable()

    def __init__(self):
        program_id = PROGRAM_CNT
        PROGRAM_CNT = PROGRAM_CNT + 1
        program_table = PageTable()

    def end_program(self):
        self.program_table.recycle_physical_memory()

# 页表类，每个程序都一有一个相应的页表


class PageTable:

    page_table_list = () # 页表管理虚拟内存
    page_allocated_list = [] # 已分配的页的列表
    read_list = () # 用于存放读取内存的结果的列表
    write_list = () # 用于存放写入内存结果的列表
    allocated_block_num = None # 记录要给该程序分配多少物理块
    used_block_num = None # 记录该程序已经实际使用了多少物理块
    lru_list = None # lru的列表，是一个链表，其中每个节点代表一个页
    page_num = PAGE_ITEM_SIZE * PAGE_ITEM_SIZE # 一共有多少页
    # 创建一个指令列表，每当程序运行时，将指令读入列表中，程序暂停时，记录指令执行的位置，以便重新运行。程序终止后，清空该列表。
    instruction_list = [list() for i in range(INSTRCUTION_MAX_NUM)]
    list_location = 0
    # 初始化页表列表
    def __init__(self):
        # 一个页表列表里存放所有页表项，一个页表项对应着一个页面
        page_table_list = [PageTableItem() for i in range(self.page_num)]

        # for j in range(PAGE_ITEM_SIZE):
        #     page_table_list[j] = PageTableItem()
        # for i in range(PAGE_ITEM_SIZE):
        #     page_table_list[i] = [list() for i in range(PAGE_ITEM_SIZE)]
        #
        # for i in range(PAGE_ITEM_SIZE):
        #     for j in range (PAGE_ITEM_SIZE):
        #         page_table_list[i][j] = PageTableItem()

    # 给程序分配虚拟内存页的的函数，need_space代表其一共需要的空间，key_space代表核心部分所需要的空间,用于按需调页，只有key_space大小的页才会实际分配物理内存空间
    # 通过分析，获得程序需要占多少空间，至少分配一页
    def allocate_virtual_memory(self, need_space, key_space):
        offset = 0
        error = None
        # 计算需要分配的页数,分为整除和不能整除两种情况
        if (need_space % PAGE_SIZE != 0):
            page_count = need_space / PAGE_SIZE + 1
        else:
            page_count = need_space / PAGE_SIZE
        #需要放入内存的核心页的数量(key_page)
        key_page = 1
        # 一共分配了几页，相当于偏移量,后续可能用于计算
        offset = page_count
        end_addr = page_count * PAGE_SIZE
        # 给这个程序分配的物理块的总数，先暂定为其需要的总页数的一般
        self.allocated_block_num = page_count / 2
        # 实际使用了多少物理块
        self.used_block_num = 0
        # 可以把分配的物理快的块号记录下
        self.page_allocated_list = [list() for i in range(page_count)]

        # 虚拟内存连续分配
        # 循环中控制先分配n页，i=0，j<n，然后剩下的再判断。
        for i in range(self.page_num):
            if(i < key_page):
                if (self.page_table_list[i].state == 0):
                    #有空闲的物理页，可以选择一个进行分配。
                    if(real_memory.exist_available_page() == 1):
                        #说明已经用了一个物理页
                        self.used_block_num = self.used_block_num + 1
                        #修改该页的状态，已经映射到物理内存中
                        self.page_table_list[i].item_state = 1
                        #保存页号
                        self.page_table_list[i].page_num = i
                        #指令准备好了，可以装入内存了，先分配一块空闲的内存，然后把指令装入对应的物理块中，instrution_list是指令列表,list_location是用来控制装入位置的指针
                        if(self.load_instrution() == 1):
                            self.page_table_list[i].physical_block_num = real_memory.allocate_physical_memory()
                            real_memory.load_memory(self.instruction_list, self.list_location,self.page_table_list[i].physical_block_num)
                            page_count = page_count - 1;
                    else:
                    #检查内存，发现用户区已经没有空闲内存块了，无法进行分配，停止分配
                        print(申请失败,没有空闲块)
                        error = 1
                        break
            #对要求的几页装入内存，剩下的只在页表中留下痕迹，说明要用到，但并不映射到物理块
            else:
                self.page_table_list[i].item_state = 2
                self.page_table_list[i].page_num = i
                page_count = page_count - 1
            #申请内存失败，或者分配结束
            if (page_count == 0 or error == 1):
                break

        return offset


    #回收内存，遍历页表，找到已经映射和分配但未映射的页
    def recycle_physical_memory(self):
        for i in range(self.page_num):
            #已分配的页，把到物理页的映射取消了，根据页表项中存储的物理页号，调用对应的函数，将物理内存中的内容清空。
            if(self.page_table_list[i].item_state == 1):
                block_num = self.page_table_list[i].physical_block_num
                real_memory.unload_block(block_num)
                self.page_table_list[i].item_state = 0
                self.page_table_list[i].physical_block_num = None
            #使用但未映射的页，将其状态置0即可
            elif(self.page_table_list[i].item_state == 2):
                self.page_table_list[i].item_state = 0
                self.page_table_list[i].page_num = None

    # 访问一个页之前时调用
    # 此函数用于对lru链表进行操作、访问页号为page_num的页,共有三种情况
    # 前两种情况才是真正意义是的缺页，第三种情况只是更新当前LRU链表，把最近访问的页面放在链表的头部
    # 若是前两种情况，函数返回一个物理块号，把需要换入的页的内容装入对应的物理块号即可
    # 若是第三种情况，返回-1说明不需要重新装入
    # 1.需要访问的这个页不在链表之中，且链表未满，只需把新的页节点放在链表头部即可
    # 2.需要访问的这个页不在链表之中，但链表已满，这时就需要淘汰链表尾部的页，将其给需要访问的这个页使用
    # 3.需要访问的这个页在链表之中，不管链表满或者不满，只需将需要访问的页放在链表的头部即可
    def lru_switch(self,visited_page_list,page_num):# 当前页不在page_num = i * 32 + j，多级页号做一个变换
        out_page = None
        #查找需要的页是否在LRU链表中
        if(visited_page_list.search_value(page_num) == 0):
            #若不在LRU链表中
            if(visited_page_list.get_length < self.allocated_block_num):
                #若已分配的物理块未用完，LRU链表未满
                new_node = Node()
                new_node.next = visited_page_list.head
                visited_page_list.head = new_node
                visited_page_list.head.value = page_num
                return -2
            elif(visited_page_list.get_length == self.allocated_block_num):
                #若已分配的物理块已经用完，LRU链表满了
                temp_node = visited_page_list.head
                while (temp_node.next.next != None):
                    temp_node = temp_node.next
                temp_node.next.next = visited_page_list.head
                out_value = temp_node.next.value
                visited_page_list.head = temp_node.next
                temp_node.next = None
                head.value = page_num
                return out_value
        else:
            #需要的页在LRU链表中，只需要将其放在链表头部即可
            #location为目标页在链表中的位置,prev_node为目标页节点的前驱节点，goal_node为目标页节点
            #只有不是头结点或只有一个节点时才需要特殊处理
            if(not(visited_page_list.get_length == 1 or visited_page_list.head.value == page_num)):
                location = visited_page_list.search_value(page_num)
                prev_node = None
                goal_node = None
                cur_node = visited_page_list.head
                for i in range(location - 1):
                    if (i == location - 2):
                        prev_node = cur_node
                    cur_node = cur_node.next
                goal_node = cur_node
                prev_node.next = goal_node.next
                goal_node.next = head
                head = goal_node
                return -1

    #处理访存,若out_page为1，即需要缺页中断，否则只是更新LRU链表

    def check_page_interruption(self,page_num):
        out_page = lru_switch(lru_list,page_num)
        #访问页替代淘汰也，占用其物理块，并且重新映射
        if(out_page > 0):
            self.replace_page(page_num,out_page)
        elif(out_page == -1):
            print('update LRU')
        elif(out_page == -2):
            # 还要分配一个页,给页号为page_num的页表项分配一个物理页
            send_interruption

    def load_instrution(self):
        #检查instrution_list的状态,通过磁盘接口把命令都读入了，这里检查并确认一下,可以的话,返回1
        return 1

    def read_memomry(self,addr):
        page_num = addr / PAGE_SIZE * 8
        offset =  addr % (PAGE_SIZE * 8)

    #清空out_page对应的物理块，并取消out_page到物理块的映射,将page_num对应的页映射到刚才释放的物理块，并且修改其页表项信息。
    def replace_page(self,page_num,out_page):
        block_num = self.page_table_list[out_page].physical_block_num
        real_memory.unload_block(block_num)
        self.page_table_list[out_page].physical_block_num = 0
        self.page_table_list[out_page].item_state = 2
        self.page_table_list[page_num].physical_block_num = block_num
        self.page_table_list[page_num].item_state = 1
        self.page_table_list[page_num].page_num = page_num
        real_memory.load_memory(self.instruction_list,self.list_location,page_num)



class PageTableItem:
    page_num = 0 #0级页表
    # page1_num = 0 #1级页号
    out_address = 0 # 磁盘交换
    physical_block_num = 0#映射到的物理块号
    item_state = 0 #(页表项状态，0空，1已映射，2已分配但未映射到物理帧)
    write = 0 #该页的内容是否可写
    read = 0 #该页的内容是否可读
    access = 0 #访问位
    modify = 0 #修改位
    interrupt = 0 #中断位

    # def __init__(self):

        # item_num
        # item_num2 = 0
        # item_state = 0
        # physical_block_num = 0
        # is_write = 0
        # is_read = 0
