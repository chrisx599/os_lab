from DeviceControlBlock import *

# 设备状态表类
class DeviceStatusTable:
    def __init__(self):
        self.table = {}  # 设备状态表，用字典实现

    # 添加设备控制块
    def add_dev(self, dev_type, dev_id):
        self.table[dev_id] = DeviceControlBlock(dev_type, dev_id)

    #删除设备控制块
    def del_dev(self,dev_type,dev_id):
        self.table.pop(dev_id)

    # 获取设备控制块
    def get_dev(self, dev_id):
        return self.table.get(dev_id)

    #查看所有设备，打印设备状态表
    def print_all_devs(self):
        lis=sorted(self.table.items(),key=lambda d:d[0])
        for i in self.table:
            print(i)
            print("设备编号：",self.table[i].dev_id)
            print("设备类型：",self.table[i].dev_type)
            print("设备状态：",self.table[i].status)
            print("设备队列：",self.table[i].queue,"\n")

