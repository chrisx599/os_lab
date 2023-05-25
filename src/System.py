"""
Writen by Liang Zhengyang
"""
from DeviceManager.DeviceStatusTable import *
from DeviceManager.DeviceRequestQueue import *
from FileManager.FileOperation import *
import threading
from queue import Queue
from utils import Container
from ProcessManager.IDGenerator import *
from MemoryManager.Memory import *
from TimeManager.Timer import *
from ProcessManager.Process import *
from HardWareManager.CPU import *
from OS import OS


class System():
    def __init__(self) -> None:
        self.device_st = DeviceStatusTable() # 初始化设备表
        self.device_queue = DeviceRequestQueue() # 初始化设备请求队列
        self.file_manager = FileSystem() # 初始化文件系统
        # self.memory = Memory()
        #################################################################
        # 初始化CPU和进程
        self.container = Container()
        timeout_event = threading.Event()
        running_event = threading.Event()
        atom_lock = threading.Lock()
        process_over_event = threading.Event()
        new_process_event = threading.Event()
        os_timer_messager = Queue()
        interrupt_pcb_queue = Queue()
        ready_pcb_queue = []
        for i in range(3):
            ready_pcb_queue.append(Queue())
        block_pcb_queue = Queue()
        exit_pcb_queue = Queue()
        interrupt_event = threading.Event()
        interrupt_message_queue = Queue()
        id_generator = IDGenerator()
        self.container.register("timeout_event", timeout_event)
        self.container.register("running_event", running_event)
        self.container.register("atom_lock", atom_lock)
        self.container.register("interrupt_event", interrupt_event)
        self.container.register("process_over_event", process_over_event)
        self.container.register("new_process_event", new_process_event)
        self.container.register("os_timer_messager", os_timer_messager)
        self.container.register("interrupt_pcb_queue", interrupt_pcb_queue)
        self.container.register("interrupt_message_queue", interrupt_message_queue)
        self.container.register("id_generator", id_generator)
        self.container.register("ready_pcb_queue", ready_pcb_queue)
        self.container.register("block_pcb_queue", block_pcb_queue)
        self.container.register("exit_pcb_queue", exit_pcb_queue)
        memory = Memory()
        self.container.register("memory", memory)
        timer = Timer()
        self.container.register("timer", timer)
        process = Process()
        self.container.register("process", process)
        cpu = CPU()
        self.container.register("cpu", cpu)
        self.os = OS()
        cpu.start()
        timer.start()


        