# 设备控制块类
class DeviceControlBlock:
    def __init__(self, dev_type, dev_id):
        self.dev_type = dev_type  # 设备类型
        self.dev_id = dev_id  # 设备编号
        self.status = "idle"  # 设备状态
        self.queue = []  # 设备队列，存储等待该设备资源的进程信息