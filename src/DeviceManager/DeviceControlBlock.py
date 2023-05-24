from utils.logger import logger
from queue import Queue
# 设备控制块类
class DeviceControlBlock:
    def __init__(self, dev_type, dev_id):
        self.dev_type = dev_type  # 设备类型
        self.dev_id = dev_id  # 设备编号
        self.status = "idle"  # 设备状态
        self.queue = Queue()  # 设备队列，存储等待该设备资源的进程信息
        logger.info('Successfully initialized device:'+str(dev_id)+' '+dev_type+'.')

    def get_dcb_queue(self):
        if not self.queue.empty():
            return self.queue.get()
        else:
            return None