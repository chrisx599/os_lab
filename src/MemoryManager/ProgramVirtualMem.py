from constant import *
from linklist import *
from PageTableItem import *
# 页表类，每个程序都一有一个相应的页表
real_memory = PhysicalMemory()
class PageTable:
    page_table_list = ()  # 页表管理虚拟内存
    page_allocated_list = []  # 已分配的页的列表
    read_list = ()  # 用于存放读取内存的结果的列表
    write_list = ()  # 用于存放写入内存结果的列表
    allocated_block_num = None  # 记录要给该程序分配多少物理块
    used_block_num = None  # 记录该程序已经实际使用了多少物理块
    lru_list = None  # lru的列表，是一个链表，其中每个节点代表一个页
    page_num = PAGE_ITEM_SIZE * PAGE_ITEM_SIZE  # 一共有多少页
    interrupt_event = None
    # 创建一个指令列表，每当程序运行时，将指令读入列表中，程序暂停时，记录指令执行的位置，以便重新运行。程序终止后，清空该列表。
    instruction_list = [list() for i in range(INSTRCUTION_MAX_NUM)]
    list_location = 0

    # 初始化页表列表
    # @inject("interrupt_event", "interrupt_type_queue")
    def __init__(self):
        # 一个页表列表里存放所有页表项，一个页表项对应着一个页面
        self.page_table_list = [PageTableItem() for i in range(self.page_num)]
        self.lru_list = linklist()
        # self.interrupt_event = interrupt_event
        # self.interrupt_type_queue = interrupt_type_queue
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
            page_count = need_space // PAGE_SIZE + 1
        else:
            page_count = need_space // PAGE_SIZE
        # 需要放入内存的核心页的数量(key_page)
        key_page = 1
        # 一共分配了几页，相当于偏移量,后续可能用于计算
        offset = page_count
        end_addr = page_count * PAGE_SIZE
        # 给这个程序分配的物理块的总数，先暂定为其需要的总页数的一般
        self.allocated_block_num = page_count // 2 + 1
        # 实际使用了多少物理块
        self.used_block_num = 0
        # 可以把分配的物理快的块号记录下
        self.page_allocated_list = [list() for i in range(page_count)]

        # 虚拟内存连续分配
        # 循环中控制先分配n页，i=0，j<n，然后剩下的再判断。
        for i in range(self.page_num):
            if (i < key_page):
                if (self.page_table_list[i].item_state == 0):
                    # 有空闲的物理页，可以选择一个进行分配。
                    if (real_memory.exist_available_page() == 1):
                        # 说明已经用了一个物理页
                        self.used_block_num = self.used_block_num + 1
                        # 修改该页的状态，已经映射到物理内存中
                        self.page_table_list[i].item_state = 1
                        # 保存页号
                        self.page_table_list[i].page_num = i
                        # 指令准备好了，可以装入内存了，先分配一块空闲的内存，然后把指令装入对应的物理块中，instrution_list是指令列表,list_location是用来控制装入位置的指针
                        if (self.load_instrution() == 1):
                            self.page_table_list[i].physical_block_num = real_memory.allocate_physical_memory()
                            real_memory.load_memory(self.instruction_list, self.list_location,
                                                    self.page_table_list[i].physical_block_num)
                            page_count = page_count - 1
                            self.lru_list.head.value = self.page_table_list[i].page_num
                    else:
                        # 检查内存，发现用户区已经没有空闲内存块了，无法进行分配，停止分配
                        print('申请失败,没有空闲块')
                        error = 1
                        break
            # 对要求的几页装入内存，剩下的只在页表中留下痕迹，说明要用到，但并不映射到物理块
            else:
                self.page_table_list[i].item_state = 2
                self.page_table_list[i].page_num = i
                page_count = page_count - 1
            # 申请内存失败，或者分配结束
            if (page_count == 0 or error == 1):
                break

        return offset

    # 回收内存，遍历页表，找到已经映射和分配但未映射的页
    def recycle_physical_memory(self):
        for i in range(self.page_num):
            # 已分配的页，把到物理页的映射取消了，根据页表项中存储的物理页号，调用对应的函数，将物理内存中的内容清空。
            if (self.page_table_list[i].item_state == 1):
                block_num = self.page_table_list[i].physical_block_num
                real_memory.unload_block(block_num)
                self.page_table_list[i].item_state = 0
                self.page_table_list[i].physical_block_num = None
            # 使用但未映射的页，将其状态置0即可
            elif (self.page_table_list[i].item_state == 2):
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
    def lru_switch(self, visited_page_list, page_num):  # 当前页不在page_num = i * 32 + j，多级页号做一个变换
        out_page = None
        # 查找需要的页是否在LRU链表中
        if (visited_page_list.search_value(page_num) == 0):
            # 若不在LRU链表中
            if (visited_page_list.get_length() < self.allocated_block_num):
                # 若已分配的物理块未用完，LRU链表未满
                if(visited_page_list.get_length() != 0):
                    new_node = Node()
                    new_node.next = visited_page_list.head
                    visited_page_list.head = new_node
                    visited_page_list.head.value = page_num
                    return -1
            elif (visited_page_list.get_length() == self.allocated_block_num):
                # 若已分配的物理块已经用完，LRU链表满了
                temp_node = visited_page_list.head
                if(visited_page_list.get_length() != 1):
                    while (temp_node.next.next != None):
                        temp_node = temp_node.next
                        temp_node.next.next = visited_page_list.head
                        out_value = temp_node.next.value
                        visited_page_list.head = temp_node.next
                        temp_node.next = None
                        visited_page_list.head.value = page_num
                        return out_value
                else:
                    temp_value = visited_page_list.head.value
                    visited_page_list.head.value = page_num
                    return temp_value
        else:
            # 需要的页在LRU链表中，只需要将其放在链表头部即可
            # location为目标页在链表中的位置,prev_node为目标页节点的前驱节点，goal_node为目标页节点
            # 只有不是头结点或只有一个节点时才需要特殊处理
            if (not (visited_page_list.get_length == 1 or visited_page_list.head.value == page_num)):
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
                goal_node.next = visited_page_list.head
                visited_page_list.head = goal_node
                return -2
            else:
                visited_page_list.head.value = page_num
                return -2
    # 处理访存,若out_page为1，即需要缺页中断，否则只是更新LRU链表

    def check_page_interruption(self, page_num):
        out_page = self.lru_switch(self.lru_list, page_num)
        return out_page
        # 访问页替代淘汰页，占用其物理块，并且重新映射
        # if (out_page >= 0):
        #     return out_page
        #     # self.interrupt_event.set()
        #     # self.interrupt_type_queue.put(2)
        #     # self.replace_page(page_num,out_page)
        #     # self.interrupt_event.clear()
        # elif (out_page == -2):
        #     print('update LRU')
        # elif (out_page == -1):
        #     # 还要分配一个页,给页号为page_num的页表项分配一个物理页
        #     return out_page
            # self.interrupt_event.set()
            # self.interrupt_type_queue.put(2)
            # self.interrupt_event.clear()

    def load_instrution(self):
        # 检查instrution_list的状态,通过磁盘接口把命令都读入了，这里检查并确认一下,可以的话,返回1
        return 1

    def read_memomry(self, addr, offset):
        page_num = addr / 8
        offset = addr % (PAGE_SIZE * 8)

    # 清空out_page对应的物理块，并取消out_page到物理块的映射,将page_num对应的页映射到刚才释放的物理块，并且修改其页表项信息。
    def replace_page(self, page_num, out_page):
        block_num = self.page_table_list[out_page].physical_block_num
        real_memory.unload_block(block_num)
        self.page_table_list[out_page].physical_block_num = 0
        self.page_table_list[out_page].item_state = 2
        self.page_table_list[page_num].physical_block_num = block_num
        self.page_table_list[page_num].item_state = 1
        self.page_table_list[page_num].page_num = page_num
        real_memory.load_memory(self.instruction_list, self.list_location, self.page_table_list[page_num].physical_block_num)

    def lru_allocate_page(self, page_num):
        new_page = real_memory.allocate_physical_memory()
        self.page_table_list[page_num].physical_block_num = new_page
        self.page_table_list[page_num].item_state = 1
        self.page_table_list[page_num].page_num = page_num
        real_memory.load_memory(self.instruction_list, self.list_location, page_num)
        return page_num
