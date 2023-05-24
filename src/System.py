import sys
sys.path.append('..')
sys.path.append('../DeviceManager/')
from DeviceManager.DeviceManager import *

class System():
    def __init__(self) -> None:
        self.device_st = DeviceStatusTable() # 初始化设备表
        