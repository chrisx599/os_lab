"""""
文件权限：
    Default = 0
    ReadOnly = 1
    WriteOnly = 2
"""
import os
import pickle
from treelib import Tree, Node


class File:
    def __init__(self, data):
        self.data = data
        self.size = len(data)
        self.disk_position = -1  # 文件在磁盘中的位置


class FileCore:
    def __init__(self) -> None:
        if os.path.exists('tree.pkl'):
            with open('tree.pkl', 'rb') as file:
                self.tree = pickle.load(file)
        else:
            self.tree = Tree()

    def contiguousAllocation(self, file_to_allocated: File, Disk: list):
        """
        磁盘文件连续分配
        :param Disk: 文件系统磁盘
        :param file_to_allocated:需要分配磁盘空间的文件
        :return:返回文件所存储的磁盘位置（起始下标），若返回-1说明磁盘空间不足
        """
        start_index = 'x'  # 文件首地址
        space_counter = 0  # 空间计算器
        for i in range(len(Disk)):
            # 主要思想是，找到磁盘中连续且符合文件大小的几个块，且从磁盘头部遍历查找，这样有利于减少外部碎片
            if Disk[i] == 'x':  # 搜索到一个空位
                if start_index == 'x':  # 首位空
                    start_index = i
                space_counter += 1

                if space_counter >= file_to_allocated.size:  # 情况符合
                    i = 0
                    for j in range(start_index, start_index + file_to_allocated.size):
                        Disk[j] = file_to_allocated.data[i]  # 填满磁盘
                        i = i + 1
                    return start_index
            else:
                start_index = 'x'
                space_counter = 0
        return -1

    def creatFileOrFolder(self, name: str, parent_name: str, Disk: list, data):
        """
        创建文件或文件夹
        :param parent_name: 父节点名称
        :param Disk: 文件系统磁盘
        :param name:文件/文件夹名称
        :param data:文件数据
        :return:文件/文件夹对象。若同路径存在重名返回-1，磁盘分配错误返回-2
        """
        if name == 'root':
            root_node = Node(identifier="root", data=data)
            self.tree.add_node(root_node)

        if not name == 'root':
            child_node = Node(identifier=name, data=data)
            parent_node = self.tree.get_node(parent_name)
            self.tree.add_node(child_node, parent=parent_node)  # 创建子节点

        new_file = File(data)
        self.contiguousAllocation(new_file, Disk)

    def pathToObj(self, name: str, IR: dict, Disk: list):
        """
        找到文件/文件夹执行操作
        :param name: 文件名
        :param Disk: 文件系统磁盘
        :param IR: 直接执行指令
        :return:文件/文件夹对象。若查找错误，返回0
        """
        node = self.tree.get_node(name)
        file = File(None)

        if IR is None:
            return -1
        elif IR["operator"] == "createFile":
            return self.creatFileOrFolder(IR['content'], name, Disk, None)

        elif IR["operator"] == "createFolder":
            return self.creatFileOrFolder(IR['content'], name, Disk, None)

        else:
            # 读文件
            if IR["operator"] == "readFile":
                return node.data

            # 写文件
            elif IR["operator"] == "writeFile":
                self.clearFileInDisk(file, Disk)
                node.data = IR["content"]
                file.data = IR["content"]
                file.size = len(IR["content"])
                file.disk_position = self.contiguousAllocation(file, Disk)
                return 1

            elif IR["operator"] == "delFile":
                self.clearFileInDisk(file, Disk)
                self.tree.remove_node(node)
                return 1

            # 重命名
            elif IR["operator"] == "renameFile":
                self.tree.update_node(node, nid=IR["newName"])
                return 1

            elif IR["operator"] == "renameFolder":
                self.tree.update_node(node, nid=IR["newName"])
                return 1

            else:
                return 0

    def clearFileInDisk(self, target_file: File, Disk: list):
        """
        在物理磁盘中删除文件信息
        :param Disk: 文件系统磁盘
        :param target_file:欲删除的文件
        """
        for i in range(target_file.disk_position, target_file.disk_position + target_file.size):
            Disk[i] = 'x'

    def initFileSystem(self, DiskSize: int = 256):
        """
        文件系统初始化
        :param DiskSize:文件系统磁盘大小
        """
        is_Disk_exist = os.path.exists('Disk.txt')
        if is_Disk_exist:
            with open("Disk.txt", "r") as tf:
                disk = tf.read().split(' ')  # 磁盘文件存在 读入磁盘
        else:
            disk = ['x' for _ in range(DiskSize)]  # 磁盘不存在 新建磁盘

        if not os.path.exists('tree.pkl'):
            self.creatFileOrFolder('root', None, Disk=disk, data=None)
            self.creatFileOrFolder('folder1', 'root', Disk=disk, data=None)
            self.creatFileOrFolder('folder2', 'root', Disk=disk, data=None)

        return disk
