from FileCore import *

class FileSystem():
    def __init__(self) -> None:
        self.state = False  # 
        self.root = None
        self.disk = []
        self.f_table = []

        self.tree = tree

        self.state, self.root, self.disk, self.f_table = initFileSystem()
        self.message = FileTree(self.root)

    # 创建目录
    def create_Folder(self, filePath):
        message = pathToObj(filePath, {"operator": "createFolder"}, self.f_table
                            , self.disk, self.root)
        if message == -1:
            # 目录重名
            return False
            # print('create_Folder Failed!Folder Already Exists!')
        # 成功
        else:
            return True
            # print('create_Folder Success!Folder Created!')

    # 创建文件
    def create_File(self, filePath):
        message = pathToObj(filePath, {"operator": "createFile", "content": ""}
                            , self.f_table, self.disk, self.root)

        if isinstance(message, int):
            # 同目录文件重名
            if message == -1:
                return -1
                # print('create_File Failed!Folder Already Exists!')
            # 磁盘读写错误
            elif message == -2:
                return -2
                # print('create_File Failed!Disk Allocation Fault!')
        # 成功
        else:
            return 1
            # print('create_File Success!File Created!')

    # 读文件
    def read_File(self, filePath):
        message = pathToObj(filePath, {"operator": "readFile"}
                            , self.f_table, self.disk, self.root)
        if isinstance(message, int):
            # 文件不存在
            if message == 0:
                return 0
                # print('read_File Failed!File Does Not Exist!')
            # 同目录文件重名
            if message == -1:
                return -1
                # print('read_File Failed!Permission Denied!')
        # 成功,返回对象是文件内容
        else:
            return 1
            # print('read_File Success!', message)

    # 读命令
    def read_Order(self, filePath):
        message = pathToObj(filePath, {"operator": "readFile"}, self.f_table, self.disk, self.root)
        if isinstance(message, int):
            # 文件不存在
            if message == 0:
                return 0
                # print('read_Order Failed!File Does Not Exist!')
            # 同目录文件重名
            if message == -1:
                return -1
                # print('read_Order Failed!Permission Denied!')
        # 成功,返回对象是文件内容
        else:
            message_list = message.split("\n")
            return message_list
            # print('read_Order Success!')

    # 读设备
    def read_Device(self, filePath):
        message = pathToObj(filePath, {"operator": "readFile"}, self.f_table, self.disk, self.root)
        if isinstance(message, int):
            # 文件不存在
            if message == 0:
                return 0
                # print('read_Device Failed!File Does Not Exist!')
            # 同目录文件重名
            if message == -1:
                return -1
                # print('read_Device Failed!Permission Denied!')
        # 成功,返回对象是文件内容
        else:
            message_list = message.split("\n")
            return message_list
            # print('read_Device Success!')

    # 写文件
    def write_File(self, filePath, content):
        message = pathToObj(filePath, {"operator": "writeFile", "content": content},
                            self.f_table, self.disk, self.root)
        # 文件不存在
        if message == 0:
            return 0
            # print('write_File Failed!File Does Not Exist!')
        # 同目录文件重名
        elif message == -1:
            return -1
            # print('write_File Failed!Permission Denied!')
        # 成功,返回对象是文件内容
        else:
            return 1
            # print('write_File Success!')

    # 写入命令
    def write_Order(self, filePath):
        with open("sample.txt") as f:
            content = f.read()
        message = pathToObj(filePath, {"operator": "writeFile", "content": content},
                            self.f_table, self.disk, self.root)
        # 文件不存在
        if message == 0:
            return 0
            # print('write_Order Failed!File Does Not Exist!')
        # 同目录文件重名
        elif message == -1:
            return -1
            # print('write_Order Failed!Permission Denied!')
        # 成功,返回对象是文件内容
        else:
            return 1
            # print('write_Order Success!')

    # 写入设备
    def write_Device(self, filePath):
        with open("Device.txt") as f:
            content = f.read()
        message = pathToObj(filePath, {"operator": "writeFile", "content": content},
                            self.f_table, self.disk, self.root)
        # 文件不存在
        if message == 0:
            return 0
            # print('write_Device Failed!File Does Not Exist!')
        # 同目录文件重名
        elif message == -1:
            return -2
            # print('write_Device Failed!Permission Denied!')
        # 成功,返回对象是文件内容
        else:
            return 1
            # print('write_Device Success!')

    # 重命名目录
    def rename_Folder(self, filePath,newName):
        message = pathToObj(filePath, {"operator": "renameFolder", "newName": newName},
                            self.f_table, self.disk, self.root)
        # 文件不存在
        if message == 0:
            return 0
            # print('rename_Folder Failed!File Does Not Exist!')
        # 同目录文件重名
        elif message == -1:
            return -1
            # print('rename_Folder Failed!Permission Denied!')
            # 成功,返回对象是文件内容
        else:
            return 1
            # print('rename_Folder Success!')

    # 重命名文件
    def rename_File(self, filePath,newName):
        message = pathToObj(filePath, {"operator": "renameFile", "newName": newName},
                            self.f_table, self.disk, self.root)
        # 文件不存在
        if message == 0:
            return 0
            # print('rename_File Failed!File Does Not Exist!')
        # 同目录文件重名
        elif message == -1:
            return -1
            # print('rename_File Failed!Permission Denied!')
            # 成功,返回对象是文件内容
        else:
            return 1
            # print('Rename File Success!')

    # 删文件
    def del_File(self, filePath):
        message = pathToObj(filePath, {"operator": "delFile"}, self.f_table, self.disk, self.root)
        # 文件不存在
        if message == 0:
            return 0
            # print('Delete File Failed!File Does Not Exist!')
        else:
            return 1
            # print('Delete File Success!')

    # 更改权限
    def change_Authority(self,filePath,newAuthority):
        message = pathToObj(filePath, {"operator": "changeFileAuthority", "newAuthority": newAuthority},
                            self.f_table, self.disk, self.root)
        # 文件不存在
        if message == 0:
            return 0
            # print('change File Authority Failed!File Does Not Exist!')
        else:
            return 1
            # print('change File Authority Success!')

    # 查看磁盘占比
    def check_Disk(self, DiskSize: int = 256):
        full = 0
        for i in range(DiskSize):
            if self.disk[i] != 'x':
                full = full + 1
        rate = full / DiskSize
        print('Disk rate:{:.2%}'.format(rate))

    # 查找文件路径
    def find_file(self, name):
        a = findObjByName(name, self.root)
        print(getPath(False, None, a))

    # 查找文件夹路径
    def find_folder(self, name):
        a = findObjByName(name, self.root)
        print(getPath(True, a, None))

    # 打印文件树
    def print_filetree(self):
        return FileTree(self.root)

    # 打印磁盘
    def print_disk(self):
        print(self.disk)

    # 将磁盘保存到文件
    def saveDisk(self):
        f = open("Disk.txt", "w")
        for line in self.disk:
            f.write(" " + str(line))

    # 将文件树保存到文件
    def saveTree(self):
        self.tree.save2file("tree.txt")

