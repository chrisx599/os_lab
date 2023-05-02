import queue

class Device:
    def __init__(self, device_id, device_type): #初始化设备类，包括设备的ID、类型等信息
        self.device_id = device_id
        self.device_type = device_type
        self.is_busy = False

    def get_id(self):   #获取设备的ID
        return self.device_id

    def get_type(self): #获取设备的类型
        return self.device_type

    def is_available(self): #判断设备是否可用
        return not self.is_busy

    def use(self):  #使用设备
        self.is_busy = True

    def release(self):  #释放设备
        self.is_busy = False

class DeviceManager:
    def __init__(self): #初始化设备管理类，包括初始化设备列表、设备队列
        self.devices = []
        self.device_queue = queue.Queue()

    def add_device(self, device):   #向设备管理类中添加一个设备
        self.devices.append(device)
        self.device_queue.put(device)

    def remove_device(self, device):    #从设备管理类中移除一个设备
        self.devices.remove(device)
        if not device.is_busy:
            self.device_queue.get()

    def request_device(self, device_type):  #请求一个指定类型的设备，并返回该设备的引用
        while True:
            for device in self.devices:
                if device.get_type() == device_type and device.is_available():
                    device.use()
                    self.device_queue.get()
                    return device
            else:
                # 如果没有可用设备，则等待
                self.wait_for_device()

    def release_device(self, device):   #释放一个设备，并将该设备重新加入设备队列
        device.release()
        self.device_queue.put(device)

    def wait_for_device(self):  # 等待设备可用
        pass
