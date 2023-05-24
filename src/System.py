from DeviceManager.DeviceManager import *
from FileManager.FileOperation import *

class System():
    def __init__(self) -> None:
        self.device_st = DeviceStatusTable() # 初始化设备表
        # self.file_manager = FileSystem() # 初始化文件系统
        