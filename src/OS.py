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
            "atom_lock", "running_event", "process_over_event", "os_timer_messager", "new_process_event", "exit_event")
    def __init__(self, cpu, process, timeout_event,
                 atom_lock, running_event, process_over_event, os_timer_messager,  new_process_event, exit_event):
        self.cpu = cpu
        self.process = process
        self.system_time = 0
        self.process_tree = treelib.Tree()
        self.timeout_event = timeout_event
        self.atom_lock = atom_lock
        self.running_event = running_event
        self.process_over_event = process_over_event
        self.new_process_event = new_process_event
        self.os_timer_messager = os_timer_messager
        self.exit_event = exit_event
        self.dispatch_thread = threading.Thread(target=self.dispatch_process)
        self.dispatch_thread.start()


    def dispatch_func(self):
        # 保存上下文环境
        ax, bx, cx, dx, axm, bxm, cxm, dxm = self.cpu.get_gen_reg_all()
        self.running_pcb.set_gen_reg_all(ax, bx, cx, dx, axm, bxm, cxm, dxm)
        pc = self.cpu.get_PC()
        self.running_pcb.set_PC(pc)
        ir = self.cpu.get_IR()
        self.running_pcb.set_IR(ir)
        # 修改进程状态
        if self.running_pcb.get_state == PCB.PROCESS_RUNNING:
            self.running_pcb.set_state(PCB.PROCESS_READY)
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
        while True:
            if not self.timeout_event.is_set():
                self.timeout_event.wait()
            print("dispatch start")
            self.running_event.clear()
            self.last_run_time = self.os_timer_messager.get()
            self.cpu_time += self.last_run_time
            self.running_pcb.set_total_time(self.running_pcb.get_total_time() + self.last_run_time)
            if self.process_over_event.is_set():
                self.running_pcb.set_state(PCB.PROCESS_EXIT)
            with self.atom_lock:
                self.dispatch_func()
            self.timeout_event.clear()
            self.process_over_event.clear()
            self.running_event.set()
            self.update_timer()

    def create_process(self, name, parent_pid):
        pcb = self.process.create_process(name)
        if self.running_pcb == None:
            self.new_process_event.set()
        if self.process_tree.size() == 0:
            self.process_tree.create_node(name, pcb.get_PID(), data=pcb)
        else:
            self.process_tree.create_node(name, pcb.get_PID(), parent=parent_pid, data=pcb)

    def update_timer(self):
        pid = self.process.get_running_pcb().get_PID()
        self.process_pid.append(pid)
        start_time = self.cpu_time - self.last_run_time
        self.process_start_timer.append(start_time)
        self.process_running_timer.append(self.last_run_time)

    def get_process_tree(self):
        return self.process_tree

    @inject("cpu", "timer")
    def process_exit(self, cpu, timer):
        cpu.stop()
        timer.stop()
        time.sleep(1)




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
    memory = Memory()
    container.register("memory", memory)
    timer = Timer()
    container.register("timer", timer)
    process = Process()
    container.register("process", process)
    cpu = CPU()
    container.register("cpu", cpu)
    os = OS()
    cpu.start()
    timer.start()
    pcb = PCB("bbb")
    os.running_pcb = pcb
    os.create_process("aaa", 0)
    timeout_event.set()
    os_timer_messager.put(5)