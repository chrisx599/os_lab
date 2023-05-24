"""""
文件权限：
    Default = 0
    ReadOnly = 1
    WriteOnly = 2
"""
import os


class Folder:
    def __init__(self, folder_name: str, parent_folder, child_nodes: list):
        """
        文件夹数据结构，文件夹为逻辑结构，因此不会占用物理磁盘空间
        :param folder_name:文件夹名
        :param parent_folder:父节点，一定是文件夹，注意，根节点没有父节点，该属性为None
        :param child_nodes:子节点。可能有多个，且可能是文件夹，也可能是文件
        """
        self.folder_name = folder_name
        self.parent_node = parent_folder
        self.child_nodes = child_nodes

    def __str__(self):
        return self.folder_name


class UserFile:
    def __init__(self, file_name: str, parent_folder, data, authority: int = 0):
        """
        文件数据结构
        :param file_name:文件名
        :param parent_folder:父节点文件夹，每个文件该属性必须有值
        :param data:文件数据
        :param authority:文件权限
        """
        self.file_name = file_name
        self.parent_node = parent_folder
        self.data = data
        self.size = len(data)
        """
        size是文件占据的磁盘空间，为了方便前端表示，单位为1字节，一个英文字符一个字节，
        注意每次更改file内容时应当要更新该值
        """
        self.disk_position = 'x'  # 文件在磁盘中的位置
        self.authority = authority

    def __str__(self):
        return self.file_name


def contiguousAllocation(file_to_allocated: UserFile, Disk: list):
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


def creatFileOrFolder(is_folder: bool, name: str, parent_folder: Folder, file_table: list,
                      Disk: list, data, child_nodes=None):
    """
    创建文件或文件夹

    :param Disk: 文件系统磁盘
    :param file_table: 文件表
    :param is_folder:是否是文件夹
    :param name:文件/文件夹名称
    :param parent_folder:父文件夹对象
    :param child_nodes:文件夹内容
    :param data:文件数据
    :return:文件/文件夹对象。若同路径存在重名返回-1，磁盘分配错误返回-2
    """
    if child_nodes is None:
        child_nodes = []
    if is_folder:
        if parent_folder is not None:
            for node in parent_folder.child_nodes:
                if str(node) == name and isinstance(node, Folder):  # 判断是否已存在
                    return -1

        new_folder = Folder(name, parent_folder, child_nodes)
        if not name == 'root':
            parent_folder.child_nodes.append(new_folder)
        return new_folder
    else:

        for node in parent_folder.child_nodes:
            if str(node) == name and isinstance(node, UserFile):
                # 同路径重名
                return -1

        new_file = UserFile(name, parent_folder, data)
        file_table.append(new_file)
        new_file.disk_position = contiguousAllocation(new_file, Disk)
        if new_file.disk_position == 'x':
            print('磁盘空间分配错误')
            return -2
        parent_folder.child_nodes.append(new_file)

        return new_file


def getPath(is_folder: bool, target_folder: Folder = None, target_file: UserFile = None):
    """
    利用递归获取文件/文件夹的路径

    :param is_folder:欲获取路径的对象是否是文件夹
    :param target_folder:目标文件夹
    :param target_file:目标文件
    :return:目标对象的路径
    """
    if is_folder and target_folder.folder_name == 'root':
        return '/root'

    if not is_folder:
        path_now = target_file.file_name
        parent_node = target_file.parent_node
    else:
        path_now = target_folder.folder_name
        parent_node = target_folder.parent_node

    path = getPath(True, target_folder=parent_node) + '/' + path_now
    return path


"""
路径的格式为： /root/aaa/w
以上路径表示root文件夹下的aaa文件夹的名为w的文件/文件夹
"""


def pathToObj(path: str, IR: dict, file_table: list, Disk: list, root: Folder):
    """
    通过路径找到文件/文件夹

    :param root:文件系统根节点
    :param Disk: 文件系统磁盘
    :param file_table: 文件表
    :param IR: 直接执行指令
    :param path:文件字符串
    :return:文件/文件夹对象。若查找错误，返回0
    """
    path = path.replace(" ", "")
    path_node_list = path.split('/')
    if path_node_list[0] == "":
        path_node_list = path_node_list[1:]
    if len(path_node_list) < 1 or path_node_list[0] != 'root':
        return 0
    # 从root出发
    parent_node = root
    # 每次都会更新子节点们
    child_node_names = list(map(str, parent_node.child_nodes))
    for i in range(1, len(path_node_list)):
        if i == len(path_node_list) - 1:  # 最后一层
            # 单纯的查询文件目录树
            if IR is None:
                return parent_node.child_nodes[child_node_names.index(path_node_list[i])]
            elif IR["operator"] == "createFile":
                return creatFileOrFolder(False, path_node_list[i], parent_node, data=IR['content'], Disk=Disk,
                                         file_table=file_table)
            elif IR["operator"] == "createFolder":
                return creatFileOrFolder(True, path_node_list[i], parent_node, data=None, Disk=Disk,
                                         file_table=file_table)
            else:
                # 不存在问题
                if not path_node_list[i] in child_node_names:
                    return 0
                target = parent_node.child_nodes[child_node_names.index(path_node_list[i])]

                # 读文件
                if IR["operator"] == "readFile":
                    # 权限不够
                    if target.authority == 2:
                        return -1
                    # 读数据
                    else:
                        return target.data

                # 写文件
                elif IR["operator"] == "writeFile":
                    print(target.authority)
                    # 权限不够
                    if target.authority == 1:
                        return -1
                    # 写数据
                    else:
                        clearFileInDisk(target, Disk)
                        target.data = IR["content"]
                        target.size = len(IR["content"])
                        target.disk_position = contiguousAllocation(target, Disk)
                        return 1

                elif IR["operator"] == "delFile":
                    if isinstance(target, Folder):
                        return 0
                    else:
                        clearFileInDisk(target, Disk)
                        file_table.remove(target)
                        target.parent_node.child_nodes.remove(target)
                        return 1

                elif IR["operator"] == "renameFile":
                    if IR["newName"] in child_node_names:
                        print('新名称在同路径下冲突')
                        return -1
                    else:
                        target.file_name = IR["newName"]
                        return 1

                elif IR["operator"] == "renameFolder":
                    if IR["newName"] in child_node_names:
                        print('新名称在同路径下冲突')
                        return -1
                    else:
                        target.folder_name = IR["newName"]
                        return 1

                elif IR["operator"] == "changeFileAuthority":
                    if isinstance(target, Folder):
                        return 0
                    else:
                        target.authority = int(IR["newAuthority"])
                        print(target.authority)
                        return 1

        elif path_node_list[i] in child_node_names:
            parent_node = parent_node.child_nodes[child_node_names.index(path_node_list[i])]
            child_node_names = list(map(str, parent_node.child_nodes))
        else:
            return 0


def clearFileInDisk(target_file: UserFile, Disk: list):
    """
    在物理磁盘中删除文件信息
    :param Disk: 文件系统磁盘
    :param target_file:欲删除的文件
    """
    for i in range(target_file.disk_position, target_file.disk_position + target_file.size):
        Disk[i] = 'x'


def findObjByName(name: str, parent_node):
    """
    利用递归，查找除了root文件夹以外的文件系统对象

    :param name:文件/文件夹名称
    :param parent_node:该参数用于递归，调用时必须传入root文件系统节点
    :return:None表示没有该对象，否则返回文件系统对象
    """

    if not parent_node.child_nodes:
        return None

    child_node_names = list(map(str, parent_node.child_nodes))
    if name in child_node_names:
        return parent_node.child_nodes[child_node_names.index(name)]
    else:
        for child_node in parent_node.child_nodes:
            if isinstance(child_node, Folder):
                result = findObjByName(name, child_node)
                if result is not None:
                    return result
        return None


def initFileSystem(DiskSize: int = 256, state: bool = False):
    """
    文件系统初始化

    :param DiskSize:文件系统磁盘大小
    :param state:状态标志
    :return:状态标志，文件根节点，文件系统磁盘，文件表
    """
    is_Disk_exist = os.path.exists('Disk.txt')
    if is_Disk_exist:
        with open("Disk.txt", "r") as tf:
            disk = tf.read().split(' ')  # 磁盘文件存在 读入磁盘
    else:
        disk = ['x' for _ in range(DiskSize)]  # 磁盘不存在 新建磁盘

    f_table = []  # 文件表，存储所有已经建立的文件

    root_node = creatFileOrFolder(True, 'root', None, data=None, Disk=disk, file_table=f_table)

    if not state:
        state = True
        default_folder_1 = creatFileOrFolder(True, 'folder1', root_node, data=None, Disk=disk,
                                             file_table=f_table)
        default_folder_2 = creatFileOrFolder(True, 'folder2', root_node, data=None, Disk=disk,
                                             file_table=f_table)
        default_folder_3 = creatFileOrFolder(True, 'folder3', root_node, data=None, Disk=disk,
                                             file_table=f_table)
        creatFileOrFolder(False, 'test', default_folder_1, data='test_content', Disk=disk,
                          file_table=f_table)
        root_node.child_nodes = [default_folder_1, default_folder_2, default_folder_3]
    return state, root_node, disk, f_table


def FileTree(parent_node):
    # 是目录
    if isinstance(parent_node, Folder):
        data = []
        child_nodes = list(parent_node.child_nodes)
        for child in child_nodes:
            data.append(FileTree(child))
        return {parent_node.__str__(): data}
    elif isinstance(parent_node, UserFile):
        return {parent_node.__str__(): 0}
