"""
Writen by Liang Zhengyang
"""
from DeviceManager.DeviceManager import *
from FileManager.FileOperation import *

class System():
    def __init__(self) -> None:
        self.device_st = DeviceStatusTable() # 初始化设备表
        self.device_queue = DeviceRequestQueue() # 初始化设备请求队列
        self.file_manager = FileSystem() # 初始化文件系统
        