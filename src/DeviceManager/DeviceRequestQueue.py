# 设备请求队列类
class DeviceRequestQueue:
    def __init__(self):
        self.queue = []  # 设备请求队列，用列表实现

    # 添加设备请求
    def add_request(self, pid, dev_type, dev_num):
        self.queue.append((pid, dev_type, dev_num))

    # 获取设备请求
    def get_request(self):
        if len(self.queue) > 0:
            return self.queue.pop(0)
        else:
            return None

