import pickle

import DeviceManager.DeviceManager
from DeviceControlBlock import *
from utils.logger import logger
from FileManager.FileOperation import FileSystem
import os
import threading
from DeviceManager import *

# 设备状态表类
class DeviceStatusTable:
    def __init__(self):
        self.table = {}  # 设备状态表，用字典实现
        if os.path.exists('Device.pkl'):
            with open('Device.pkl', 'rb') as file:
                dict = pickle.load(file)
                for key in dict.keys():
                    self.add_dev(dict[key], int(key))
        # FileSystem.read_Device()
        # self.add_dev("daw", 1)
        logger.info('Successfully initialized device_status_table.')

    # 添加设备控制块
    def add_dev(self, dev_type:str, dev_id):
        self.table[dev_id] = DeviceControlBlock(dev_type, dev_id)
        t = threading.Thread(target=DeviceManager.run, args=[self.table.get_dev(dev_id)], name=dev_type)
        t.start()
        logger.info('Successfully added device:'+str(dev_id)+' '+dev_type+'.')

    #删除设备控制块
    def del_dev(self, dev_id):
        self.table.pop(dev_id)
        logger.info('Successfully deleted device:'+str(dev_id)+'.')

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
        logger.info('Successfully viewed devices.')

    def save(self):
        new_dict = {}
        for key in self.table.keys():
            new_dict[key] = self.table[key].dev_type
        with open('Device.pkl', 'wb') as file:
            pickle.dump(new_dict, file)