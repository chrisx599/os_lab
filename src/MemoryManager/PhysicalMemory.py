# 物理内存类，memory_size代表物理内存大小,block_size代表一个块(页)的大小，64B,memory_space则是一个二维的列表,256个块(页),每页又有64B/4,16条指令
class PhysicalMemory:
    memory_size = pow(2, 14)  # 物理内存总大小
    block_size = pow(2, 6)  # 一个块的大小
    block_num = memory_size / block_size  # 一共有多少块
    core_block_num = block_num / 4  # 系统区的大小，块数
    used_block_num = 0  # 使用了多少物理块
    block_threshold_num = block_num / 8  # 设定的是剩余块阈值
    memory_space = list()
    interrupt_vector_list = list()  # 分配第0页
    buffer_list = list()  # 分配第1页

    # 初始化一个内存列表，抽象成二维列表,一个数组元素储存
    def __init__(self):
        # 一维为块号，代表有这么多物理内存块
        self.memory_space = [list() for i in range(self.block_num)]
        # 二维代表一个物理内存块是多少字节，block_size是64，列表有64个元素，一个元素代表着一个字节(byte)
        for j in range(self.block_num):
            self.memory_space[j] = [list() for j in range(self.block_size)]
        # 每个块都初始化一下，置0
        for i in range(self.block_num):
            for j in range(self.block_size):
                self.memory_space[i][j] = 0
        self.memory_space[0][0] = ('vector')
        self.memory_space[1][0] = ('buffer')

    # 从未分配的页中选择一页分配,返回分配的块号给虚拟内存的分配，虚拟内存将其存储到对应的页中,完成从虚拟内存到物理内存的映射
    def allocate_physical_memory(self):

        # 一个死循环,只有找到一个未被使用的页,将其页号记录下来之后,存储到列表中返回,否则一直循环
        while (1):
            temp_block_num = create_random_list(1, self.core_block_num, self.block_num)
            if (len(self.memory_space[temp_block_num[0]][0]) == 0):
                self.memory_space[temp_block_num[0]][0] = 1
                return temp_block_num[0]

    # 把指令装入对应的内存中
    def load_memory(self, instruction_list, location, block_num):

        for i in range(PAGE_SIZE):
            self.memory_space[block_num[0]][i] = instruction_list[location]
            location = location + 1

    # 检测物理内存中是否还有空闲块
    def exist_available_page(self):

        # 用户区还有多大
        avai_page = self.block_num - self.core_block_num - self.used_block_num
        if (avai_page > self.block_threshold_num):
            return 1
        else:
            return 0

    # 清空对应物理块中的内存
    def unload_block(self, block_num):

        for i in range(self.block_size / INSTRCUTION_LENGTH):
            self.memory_space[block_num][i] = 0
