import pickle
from FileCore import *


class FileSystem:
    def __init__(self) -> None:
        self.state = False
        self.root = None
        self.disk = []
        self.filecore = FileCore()
        self.disk = self.filecore.initFileSystem()

    # 创建文件
    def create_File(self, name, content):
        message = self.filecore.pathToObj(name, {"operator": "createFile", "content": content},self.disk)
        if isinstance(message, int):
            # 同目录文件重名
            if message == -1:
                return -1
            # 磁盘读写错误
            elif message == -2:
                return -2
        # 成功
        else:
            return 1

    # 读文件
    def read_File(self, name):
        message = self.filecore.pathToObj(name, {"operator": "readFile"},self.disk)
        if isinstance(message, int):
            # 文件不存在
            if message == 0:
                print('read_File Failed!File Does Not Exist!')
            # 同目录文件重名
            if message == -1:
                print('read_File Failed!Permission Denied!')
        # 成功,返回对象是文件内容
        else:
            print(message)

    # 读命令
    def read_Order(self, name):
        message = self.filecore.pathToObj(name, {"operator": "readOrder"}, self.disk)
        if isinstance(message, int):
            # 文件不存在
            if message == 0:
                return 0
            # 同目录文件重名
            if message == -1:
                return -1
        # 成功,返回对象是文件内容
        else:
            message_list = message.split("\n")
            return message_list

    # # 读设备
    # def read_Device(self, name):
    #     message = self.filecore.pathToObj(name, {"operator": "readDevice"}, self.disk)
    #     if isinstance(message, int):
    #         # 文件不存在
    #         if message == 0:
    #             return 0
    #         # 同目录文件重名
    #         if message == -1:
    #             return -1
    #     # 成功,返回对象是文件内容
    #     else:
    #         message_list = message.split("\n")
    #         return message_list

    def read_instruction(self, name:str='all'):
        """
        name:需要读入的指令集名称,默认为all读入所有\n
        从pkl文件中读入指令\n
        writen by Liang Zhengyang
        """
        if os.path.exists('instruction.pkl'):
            with open('instruction.pkl', 'rb') as file:
                instruction = pickle.load(file)
            if name == "all":
                # print(instruction)
                return instruction
            else:
                # print(instruction[name])
                return instruction[name]
        else:
            print("please init instruction system")

        return None
    
    def write_instruction(self):
        """
        向pkl文件中写入指令\n
        writen by Liang Zhengyang
        """
        if os.path.exists('instruction.pkl'):
            ins_file = self.read_instruction()
        else:
            ins_file = dict()
        ins_save = []
        with open('instruction.pkl', 'wb') as file:
            print("use command exit to exit")
            print("please input instruction, use space each 8 bits:")
            while True:
                ins = input()
                if ins == "exit":
                    break
                ins_list = ins.split(' ')
                ins_save.append(ins_list[0])
                ins_save.append(ins_list[1])
                ins_save.append(ins_list[2])
                ins_save.append(ins_list[3])
            name = input("please input instruction file name:")
            if name not in ins_file:
                ins_file[name] = []
            ins_file[name].append(ins_save)
            pickle.dump(ins_file, file)
        print("Instructions write successfully!")
            
            



    # 写文件
    def write_File(self, name, content):
        message = self.filecore.pathToObj(name, {"operator": "writeFile", "content": content},
                                          self.disk)
        # 文件不存在
        if message == 0:
            print('write_File Failed!File Does Not Exist!')
        # 同目录文件重名
        elif message == -1:
            print('write_File Failed!Permission Denied!')
        # 成功,返回对象是文件内容
        else:
            print('write_File Success!')

    # 写入命令
    def write_Order(self, name):
        with open("sample.txt") as f:
            content = f.read()
        message = self.filecore.pathToObj(name, {"operator": "writeFile", "content": content}, self.disk)
        # 文件不存在
        if message == 0:
            print('write_Order Failed!File Does Not Exist!')
        # 同目录文件重名
        elif message == -1:
            print('write_Order Failed!Permission Denied!')
        # 成功,返回对象是文件内容
        else:
            print('write succuessful!')

    # # 写入设备
    # def write_Device(self, name):
    #     with open("Device.txt") as f:
    #         content = f.read()
    #     message = self.filecore.pathToObj(name, {"operator": "writeFile", "content": content},self.disk)
    #     # 文件不存在
    #     if message == 0:
    #         return 0
    #     # 同目录文件重名
    #     elif message == -1:
    #         return -2
    #     # 成功,返回对象是文件内容
    #     else:
    #         return 1

    # 重命名文件
    def rename_File(self, name, newName):
        message = self.filecore.pathToObj(name, {"operator": "renameFile", "newName": newName},self.disk)
        # 文件不存在
        if message == 0:
            return 0
        # 同目录文件重名
        elif message == -1:
            return -1
            # 成功,返回对象是文件内容
        else:
            return 1

    # 删文件
    def del_File(self, filePath):
        message = self.filecore.pathToObj(filePath, {"operator": "delFile"}, self.disk)
        # 文件不存在
        if message == 0:
            return 0
        else:
            return 1

    # 查看磁盘占比
    def check_Disk(self, DiskSize: int = 256):
        full = 0
        for i in range(DiskSize):
            if self.disk[i] != 'x':
                full = full + 1
        rate = full / DiskSize
        print('Disk rate:{:.2%}'.format(rate))

    # 打印磁盘
    def print_disk(self):
        print(self.disk)

    # 将磁盘保存到文件
    def saveDisk(self):
        f = open("Disk.txt", "w")
        for line in self.disk:
            f.write(" " + str(line))

    # 将目录树保存到文件
    def save(self):
        with open('tree.pkl', 'wb') as file:
            pickle.dump(self.filecore.tree, file)
