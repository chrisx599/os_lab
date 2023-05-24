from DeviceManager.DeviceManager import *

class System():
    def __init__(self) -> None:
        self.device_st = DeviceStatusTable() # 初始化设备表
        