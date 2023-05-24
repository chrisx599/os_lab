from FileCore import *

state, root, disk, f_table = False, None, [], []


def init_FileSystem():  # 初始化文件系统 地址是根目录，创建一个新的资源
    global state, root, disk, f_table

    state, root, disk, f_table = initFileSystem()
    message = FileTree(root)
    print(message)


# 创建目录
def create_Folder():
    filePath = input("Create Folder,Please input path:")
    message = pathToObj(filePath, {"operator": "createFolder"}, f_table, disk, root)
    if message == -1:
        # 目录重名
        print('create_Folder Failed!Folder Already Exists!')
    # 成功
    else:
        print('create_Folder Success!Folder Created!')


# 创建文件
def create_File():
    filePath = input("Create File,Please input path:")
    message = pathToObj(filePath, {"operator": "createFile", "content": ""}, f_table, disk, root)

    if isinstance(message, int):
        # 同目录文件重名
        if message == -1:
            print('create_File Failed!Folder Already Exists!')
        # 磁盘读写错误
        elif message == -2:
            print('create_File Failed!Disk Allocation Fault!')
    # 成功
    else:
        print('create_File Success!File Created!')


# 读文件
def read_File():
    filePath = input("Read File,Please input path:")
    message = pathToObj(filePath, {"operator": "readFile"}, f_table, disk, root)
    if isinstance(message, int):
        # 文件不存在
        if message == 0:
            print('read_File Failed!File Does Not Exist!')
        # 同目录文件重名
        if message == -1:
            print('read_File Failed!Permission Denied!')
    # 成功,返回对象是文件内容
    else:
        print('read_File Success!', message)


# 读命令
def read_Order():
    filePath = input("Read Order,Please input path:")
    message = pathToObj(filePath, {"operator": "readFile"}, f_table, disk, root)
    if isinstance(message, int):
        # 文件不存在
        if message == 0:
            print('read_Order Failed!File Does Not Exist!')
        # 同目录文件重名
        if message == -1:
            print('read_Order Failed!Permission Denied!')
    # 成功,返回对象是文件内容
    else:
        message_list = message.split("\n")
        print('read_Order Success!', message_list)


# 读设备
def read_Device():
    filePath = input("Read Device,Please input path:")
    message = pathToObj(filePath, {"operator": "readFile"}, f_table, disk, root)
    if isinstance(message, int):
        # 文件不存在
        if message == 0:
            print('read_Device Failed!File Does Not Exist!')
        # 同目录文件重名
        if message == -1:
            print('read_Device Failed!Permission Denied!')
    # 成功,返回对象是文件内容
    else:
        message_list = message.split("\n")
        print('read_Device Success!', message_list)


# 写文件
def write_File():
    filePath = input("Write File,Please input path:")
    content = input("input Content")
    message = pathToObj(filePath, {"operator": "writeFile", "content": content}, f_table, disk, root)
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
def write_Order():
    filePath = input("Write Order,Please input path:")
    with open("sample.txt") as f:
        content = f.read()
    message = pathToObj(filePath, {"operator": "writeFile", "content": content}, f_table, disk, root)
    # 文件不存在
    if message == 0:
        print('write_Order Failed!File Does Not Exist!')
    # 同目录文件重名
    elif message == -1:
        print('write_Order Failed!Permission Denied!')
    # 成功,返回对象是文件内容
    else:
        print('write_Order Success!')


# 写入设备
def write_Device():
    filePath = input("Write Device,Please input path:")
    with open("Device.txt") as f:
        content = f.read()
    message = pathToObj(filePath, {"operator": "writeFile", "content": content}, f_table, disk, root)
    # 文件不存在
    if message == 0:
        print('write_Device Failed!File Does Not Exist!')
    # 同目录文件重名
    elif message == -1:
        print('write_Device Failed!Permission Denied!')
    # 成功,返回对象是文件内容
    else:
        print('write_Device Success!')


# 重命名目录
def rename_Folder():
    filePath = input("Rename Folder,Please input path:")
    newName = input("input newName:")
    message = pathToObj(filePath, {"operator": "renameFolder", "newName": newName}, f_table, disk, root)
    # 文件不存在
    if message == 0:
        print('rename_Folder Failed!File Does Not Exist!')
    # 同目录文件重名
    elif message == -1:
        print('rename_Folder Failed!Permission Denied!')
        # 成功,返回对象是文件内容
    else:
        print('rename_Folder Success!')


# 重命名文件
def rename_File():
    filePath = input("Rename File,Please input path:")
    newName = input("input newName:")
    message = pathToObj(filePath, {"operator": "renameFile", "newName": newName}, f_table, disk, root)
    # 文件不存在
    if message == 0:
        print('rename_File Failed!File Does Not Exist!')
    # 同目录文件重名
    elif message == -1:
        print('rename_File Failed!Permission Denied!')
        # 成功,返回对象是文件内容
    else:
        print('Rename File Success!')


# 删文件
def del_File():
    filePath = input("Delete File,Please input path:")
    message = pathToObj(filePath, {"operator": "delFile"}, f_table, disk, root)
    # 文件不存在
    if message == 0:
        print('Delete File Failed!File Does Not Exist!')
    else:
        print('Delete File Success!')


# 更改权限
def change_Authority():
    filePath = input("change File Authority,Please input path:")
    newAuthority = input("input newAuthority:")
    message = pathToObj(filePath, {"operator": "changeFileAuthority", "newAuthority": newAuthority}, f_table, disk, root)
    # 文件不存在
    if message == 0:
        print('change File Authority Failed!File Does Not Exist!')
    else:
        print('change File Authority Success!')


# 查看磁盘占比
def check_Disk(DiskSize: int = 256):
    full = 0
    for i in range(DiskSize):
        if disk[i] != 'x':
            full = full+1
    rate = full/DiskSize
    print('Disk rate:{:.2%}'.format(rate))


# 查找文件路径
def find_file():
    name = input("Find file,Please input file name:")
    a = findObjByName(name, root)
    print(getPath(False, None, a))


# 查找文件夹路径
def find_folder():
    name = input("Find folder,Please input folder name:")
    a = findObjByName(name, root)
    print(getPath(True, a, None))


# 打印文件树
def print_filetree():
    print(FileTree(root))


# 打印磁盘
def print_disk():
    print(disk)


# 将磁盘保存到文件
def saveDisk():
    f = open("Disk.txt", "w")
    for line in disk:
        f.write(" "+str(line))


# 将文件树保存到文件
def saveTree():
    f = open("FileTree.txt", "w")
    f.writelines(str(FileTree(root)))
    f.close()
