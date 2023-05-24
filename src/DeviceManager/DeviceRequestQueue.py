from utils.logger import logger

# 设备请求队列类
class DeviceRequestQueue:
    def __init__(self):
        self.queue = []  # 设备请求队列，用列表实现
        logger.info('Successfully initialized device_request_queue.')

    # 添加设备请求
    def add_request(self, pcb, dev_type, dev_num):
        self.queue.append((pcb, dev_type, dev_num))
        logger.info('Successfully added device request to queue:'+str(pcb.get_PID())+' '+str(dev_num)+' '+dev_type+'.')

    # 获取设备请求
    def get_request(self):
        if len(self.queue) > 0:
            return self.queue.pop(0)
        else:
            return None

