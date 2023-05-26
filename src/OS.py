# -*- coding:utf-8 -*-
# @FileName : OS.py
# @Time     : 2023/5/18 21:11
# @Author   : qingyao
import threading
import sys
sys.path.append("D:\\pythonCode\\final\\os_lab\\src\\MemoryManager")
sys.path.append("D:\\pythonCode\\final\\os_lab\\src\\FileManager")
sys.path.append("D:\\pythonCode\\final\\os_lab\\src\\ProcessManager")
sys.path.append("D:\\pythonCode\\final\\os_lab\\src\\InterruptManager")
sys.path.append("D:\\pythonCode\\final\\os_lab\\src\\TimeManager")
sys.path.append("D:\\pythonCode\\final\\os_lab\\src\\HardWareManager")
sys.path.append("D:\\pythonCode\\final\\os_lab\\src\\DeviceManager")
print(sys.path)
from utils.Container import *
from ProcessManager.PCB import *
import treelib
from utils.Container import *

import threading
from MemoryManager.Memory import *
from ProcessManager.Process import *
from ProcessManager.IDGenerator import *
from TimeManager.Timer import *
from HardWareManager.CPU import *
from ProcessManager.PCB import *
from InterruptManager.Interrupt import *

class OS:
    cpu = None
    process = None
    running_pcb = None
    cpu_time = 0
    last_run_time = 0
    dispatch_thread = None

    process_tree = None
    process_pid = []
    process_start_timer = []
    process_running_timer = []


    @inject("cpu", "process", "timeout_event",
            "atom_lock", "running_event", "process_over_event", "os_timer_messager", "new_process_event", "exit_event", "interrupt_event")
    def __init__(self, cpu, process, timeout_event,
                 atom_lock, running_event, process_over_event, os_timer_messager,  new_process_event, exit_event, interrupt_event):
        self.cpu = cpu
        self.process = process
        self.system_time = 0
        self.process_tree = treelib.Tree()
        self.timeout_event = timeout_event
        self.atom_lock = atom_lock
        self.exit_event = exit_event
        self.interrupt_event = interrupt_event
        self.running_event = running_event
        self.process_over_event = process_over_event
        self.new_process_event = new_process_event
        self.os_timer_messager = os_timer_messager
        self.dispatch_thread = threading.Thread(target=self.dispatch_process, name="dispatch")
        self.dispatch_thread.start()
        self.create_process("init")


    def dispatch_func(self):
        # 保存上下文环境
        ax, bx, cx, dx, axm, bxm, cxm, dxm = self.cpu.get_gen_reg_all()
        self.running_pcb.set_gen_reg_all(ax, bx, cx, dx, axm, bxm, cxm, dxm)
        pc = self.cpu.get_PC()
        self.running_pcb.set_PC(pc)
        ir = self.cpu.get_IR()
        self.running_pcb.set_IR(ir)
        # 修改进程状态
        if self.running_pcb.get_state() == self.running_pcb.PROCESS_RUNNING:
            self.running_pcb.set_state(self.running_pcb.PROCESS_READY)
        # 进程调度
        next_running_pcb = self.process.dispatch_process(self.running_pcb)
        if next_running_pcb == None:
            self.new_process_event.wait()
            next_running_pcb = self.process.get_next_pcb()
            self.cpu.running_pcb = next_running_pcb
            self.new_process_event.clear()
        self.running_pcb = next_running_pcb
        # 恢复上下文环境
        ax, bx, cx, dx, axm, bxm, cxm, dxm = self.running_pcb.get_gen_reg_all()
        self.cpu.set_gen_reg_all(ax, bx, cx, dx, axm, bxm, cxm, dxm)
        pc = self.running_pcb.get_PC()
        self.cpu.set_PC(pc)
        ir = self.running_pcb.get_IR()
        self.cpu.set_IR(ir)
        self.cpu.set_PID(self.running_pcb.get_PID())

    def dispatch_process(self):
        print("dispatch_process")
        if not self.new_process_event.is_set():
            self.new_process_event.wait()
            self.new_process_event.clear()
            print("dispatch: new_process_event get")
            self.running_pcb = self.process.get_next_pcb()
            ax, bx, cx, dx, axm, bxm, cxm, dxm = self.running_pcb.get_gen_reg_all()
            self.cpu.set_gen_reg_all(ax, bx, cx, dx, axm, bxm, cxm, dxm)
            pc = self.running_pcb.get_PC()
            self.cpu.set_PC(pc)
            ir = self.running_pcb.get_IR()
            self.cpu.set_IR(ir)
            self.cpu.set_PID(self.running_pcb.get_PID())
            self.os_timer_messager.put(self.running_pcb.get_priority())
            self.cpu.running_pcb = self.running_pcb
            self.running_event.set()
            print("dispatch: now running_event set")
        while True:
            if not self.timeout_event.is_set():
                print("dispatch: now waiting timeout_event")
                self.timeout_event.wait()
                print("dispatch: get timeout_event now ")
                if self.exit_event.is_set():
                    return
            self.running_event.clear()
            self.last_run_time = self.os_timer_messager.get()
            self.cpu_time += self.last_run_time
            self.running_pcb.set_total_time(self.running_pcb.get_total_time() + self.last_run_time)
            if self.process_over_event.is_set():
                self.running_pcb.set_state(self.running_pcb.PROCESS_EXIT)

            self.atom_lock.acquire()
            print("dispatch: dispatch start")
            self.dispatch_func()
            self.cpu.running_pcb = self.running_pcb
            self.atom_lock.release()
            self.timeout_event.clear()
            self.process_over_event.clear()
            self.running_event.set()
            self.update_timer()

    def create_process(self, *args):
        pcb = self.process.create_process(args[0])
        if self.running_pcb == None and pcb.PID != 0:
            self.new_process_event.set()
        if self.process_tree.size() == 0:
            self.process_tree.create_node(args[0], pcb.get_PID(), data=pcb)
        else:
            self.process_tree.create_node(args[0], pcb.get_PID(), parent=args[1], data=pcb)

    def update_timer(self):
        pid = self.process.get_running_pcb().get_PID()
        self.process_pid.append(pid)
        start_time = self.cpu_time - self.last_run_time
        self.process_start_timer.append(start_time)
        self.process_running_timer.append(self.last_run_time)

    def get_process_tree(self):
        return self.process_tree

    def process_exit(self):
        self.exit_event.set()
        self.interrupt_event.set()
        self.running_event.set()
        self.new_process_event.set()
        self.timeout_event.set()





if __name__ == "__main__":
    print(sys.path)
    container = Container()
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
    exit_event = threading.Event()
    interrupt_message_queue = Queue()
    id_generator = IDGenerator()
    container.register("timeout_event", timeout_event)
    container.register("running_event", running_event)
    container.register("atom_lock", atom_lock)
    container.register("interrupt_event", interrupt_event)
    container.register("process_over_event", process_over_event)
    container.register("new_process_event", new_process_event)
    container.register("os_timer_messager", os_timer_messager)
    container.register("interrupt_pcb_queue", interrupt_pcb_queue)
    container.register("interrupt_message_queue", interrupt_message_queue)
    container.register("id_generator", id_generator)
    container.register("ready_pcb_queue", ready_pcb_queue)
    container.register("block_pcb_queue", block_pcb_queue)
    container.register("exit_pcb_queue", exit_pcb_queue)
    container.register("exit_event", exit_event)
    memory = Memory()
    container.register("memory", memory)
    timer = Timer()
    container.register("timer", timer)
    process = Process()
    container.register("process", process)
    cpu = CPU()
    container.register("cpu", cpu)
    device_status_table = DeviceStatusTable()
    device_request_queue = DeviceRequestQueue()
    container.register("device_status_table", device_status_table)
    container.register("device_request_queue", device_request_queue)

    interrupt = Interrput()
    interrupt.start()
    os = OS()
    instructions = ["00000001", "01010000", "10000000","00000000","00000001","00010000","00000000","00000011",
                    "00000001", "01010001", "00000000","00000000","00000001","00010000","00000000","00001100",
                    "00000010", "00010100", "00000000","00000000","00000000","00000000","00000000","00000000"]
    memory.load_program(1, instructions)
    cpu.start()
    timer.start()
    os.create_process("aaa", 0)