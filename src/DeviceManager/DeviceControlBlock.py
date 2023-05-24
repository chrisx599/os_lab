from utils.logger import logger

# 设备控制块类
class DeviceControlBlock:
    def __init__(self, dev_type, dev_id):
        self.dev_type = dev_type  # 设备类型
        self.dev_id = dev_id  # 设备编号
        self.status = "idle"  # 设备状态
        self.queue = []  # 设备队列，存储等待该设备资源的进程信息
        logger.info('Successfully initialized device:'+str(dev_id)+' '+dev_type+'.')

    def get_dcb_queue(self):
        if len(self.queue) > 0:
            return self.queue.pop(0)
        else:
            return None