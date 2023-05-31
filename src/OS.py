# -*- coding:utf-8 -*-
# @FileName : OS.py
# @Time     : 2023/5/18 21:11
# @Author   : qingyao
import threading
import sys
import os
sys.path.append("D:\\pythonCode\\os_labv2\\os_lab\\src\\ProcessManager")
sys.path.append("D:\\pythonCode\\os_labv2\\os_lab\\src\\MemoryManager")
sys.path.append("D:\\pythonCode\\os_labv2\\os_lab\\src\\HardWareManager")
sys.path.append("D:\\pythonCode\\os_labv2\\os_lab\\src\\TimeManager")
sys.path.append("D:\\pythonCode\\os_labv2\\os_lab\\src\\InterruptManager")
sys.path.append("D:\\pythonCode\\os_labv2\\os_lab\\src\\DeviceManager")
sys.path.append("D:\\pythonCode\\os_labv2\\os_lab\\src\\FileManager")
sys.path.append("D:\\pythonCode\\os_labv2\\os_lab\\src\\utils")
# print(sys.path)
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
from DeviceManager.DeviceManager import *
from DeviceManager.DeviceStatusTable import *
from DeviceManager.DeviceRequestQueue import *
from DeviceManager.DeviceControlBlock import *

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
            "atom_lock", "running_event", "process_over_event", "os_timer_messager", "new_process_event", "exit_event", "interrupt_event", "force_dispatch_event")
    def __init__(self, cpu, process, timeout_event,
                 atom_lock, running_event, process_over_event, os_timer_messager,  new_process_event, exit_event, interrupt_event, force_dispatch_event):
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
        self.force_dispatch_event = force_dispatch_event
        self.dispatch_thread = threading.Thread(target=self.dispatch_process, name="dispatch")
        self.dispatch_thread.start()
        self.create_process("init")



    def dispatch_func(self):
        # 保存上下文环境
        ax, bx, cx, dx, axm, bxm, cxm, dxm = self.cpu.get_gen_reg_all()
        self.running_pcb.set_gen_reg_all(ax, bx, cx, dx, axm, bxm, cxm, dxm)
        # print("寄存器正常")
        pc = self.cpu.get_PC()
        self.running_pcb.set_PC(pc)
        # print("pc yes")
        ir = self.cpu.get_IR()
        self.running_pcb.set_IR(ir)
        # print("ir yes")
        # 修改进程状态
        if self.running_pcb.get_state() == self.running_pcb.PROCESS_RUNNING:
            # print(self.running_pcb.state)
            self.running_pcb.set_state(self.running_pcb.PROCESS_READY)
        # 进程调度
        next_running_pcb = self.process.dispatch_process(self.running_pcb)
        if next_running_pcb == None:
            self.new_process_event.wait()
            if self.exit_event.is_set():
                return
            next_running_pcb = self.process.get_next_pcb()
            self.cpu.running_pcb = next_running_pcb
            self.new_process_event.clear()
        self.running_pcb = next_running_pcb
        self.running_pcb.set_state(self.running_pcb.PROCESS_RUNNING)
        # print("调度了， 现在进程id为" + str(self.running_pcb.get_PID()))
        # 恢复上下文环境
        time.sleep(0.001)
        if self.exit_event.is_set():
            return
        ax, bx, cx, dx, axm, bxm, cxm, dxm = self.running_pcb.get_gen_reg_all()
        self.cpu.set_gen_reg_all(ax, bx, cx, dx, axm, bxm, cxm, dxm)
        pc = self.running_pcb.get_PC()
        self.cpu.set_PC(pc)
        ir = self.running_pcb.get_IR()
        self.cpu.set_IR(ir)
        self.cpu.set_PID(self.running_pcb.get_PID())

    def dispatch_process(self):
        # print("dispatch_process")
        if not self.new_process_event.is_set():
            self.new_process_event.wait()
            if self.exit_event.is_set():
                return
            self.new_process_event.clear()
            # print("dispatch: new_process_event get")
            self.running_pcb = self.process.get_next_pcb()
            self.running_pcb.set_state(self.running_pcb.PROCESS_RUNNING)
            ax, bx, cx, dx, axm, bxm, cxm, dxm = self.running_pcb.get_gen_reg_all()
            self.cpu.set_gen_reg_all(ax, bx, cx, dx, axm, bxm, cxm, dxm)
            pc = self.running_pcb.get_PC()
            self.cpu.set_PC(pc)
            ir = self.running_pcb.get_IR()
            self.cpu.set_IR(ir)
            buffer_address = self.running_pcb.buffer_address
            self.cpu.buffer_address = buffer_address
            self.cpu.set_PID(self.running_pcb.get_PID())
            self.os_timer_messager.put(self.running_pcb.get_priority())
            self.cpu.running_pcb = self.running_pcb
            self.running_event.set()
            # print("dispatch: now running_event set")
        while True:
            if not self.timeout_event.is_set():
                # print("dispatch: now waiting timeout_event")
                self.timeout_event.wait()
                # print("dispatch: get timeout_event now ")
                if self.exit_event.is_set():
                    self.update_timer()
                    return
            self.last_run_time = self.os_timer_messager.get()
            self.cpu_time += self.last_run_time
            self.running_pcb.set_total_time(self.running_pcb.get_total_time() + self.last_run_time)
            self.atom_lock.acquire()
            # print("dispatch: dispatch start")
            self.update_timer()
            # print("dispatch: update timer成功")
            self.dispatch_func()
            if self.exit_event.is_set():
                return
            self.cpu.running_pcb = self.running_pcb
            self.os_timer_messager.put(self.running_pcb.get_priority())
            if self.exit_event.is_set():
                self.update_timer()
                return
            # print("dispatch: dispatch ok")
            self.atom_lock.release()
            self.timeout_event.clear()
            self.force_dispatch_event.clear()
            self.running_event.set()

    def create_process(self, *args):
        # self.interrupt_event.set()
        pcb = self.process.create_process(args[0])
        if self.running_pcb == None and pcb.PID != 0:
            self.new_process_event.set()
        if self.process_tree.size() == 0:
            self.process_tree.create_node(args[0], pcb.get_PID(), data=pcb)
        else:
            self.process_tree.create_node(args[0], pcb.get_PID(), parent=args[1], data=pcb)
        self.new_process_event.clear()
        # self.interrupt_event.clear()

    def update_timer(self):
        if self.running_pcb == None:
            return
        pid = self.running_pcb.PID
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

    def del_process(self, PID):
        pcb = self.process_tree.get_node(PID).data
        self.process_tree.remove_node(PID)
        if pcb.get_state() == pcb.PROCESS_READY:
            pcb = self.process.get_ready_pcb_by_PID(PID)
            pcb.set_state(pcb.PROCESS_EXIT)
            del pcb

    def wakeup(self, pcb):
        pcb.set_state(pcb.PROCESS_READY)
        self.process.move_to_next_queue(pcb)
        for i in range(self.process.block_pcb_queue.qsize()):
            get_pcb = self.process.block_pcb_queue.get()
            if get_pcb.PID != pcb.PID:
                self.process.block_pcb_queue.put(get_pcb)

    def block(self):
        pcb = self.running_pcb
        pcb.set_state(pcb.PROCESS_BLOCK)
        self.process.block_pcb_queue.put(pcb)
        self.force_dispatch_event.set()
        # print("block set event")


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
    force_dispatch_event = threading.Event()
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
    container.register("force_dispatch_event", force_dispatch_event)
    memory = Memory()
    container.register("memory", memory)
    timer = Timer()
    container.register("timer", timer)
    process = Process()
    container.register("process", process)
    cpu = CPU()
    container.register("cpu", cpu)
    dst = DeviceStatusTable()
    drq = DeviceRequestQueue()
    container.register("device_queue", drq)
    container.register("device_st", dst)
    # dst.add_dev("A", 3)
    os = OS()
    container.register("os", os)
    interrupt = Interrput()
    interrupt.start()

    instructions1 = ["00000001","00010000","00000000","00000011",
                     "00000001","01010000","10000000","00000000",
                     "00000001","01010001","00000000","00000000",
                     "00000001","00010000","00000000","00001100",
                     "00000001","00100000","00000000","00001100",
                     "00000001","00110000","00000000","00001100",
                     "00000010","00010101","00000000","00000000",
                     "00000011","00100101","00000000","00000000",
                     "00000100","00110101","00000000","00000000",
                     "00000000","00000000","00000000","00000000"]
    instructions2 = ["00000001", "00010000", "00000000", "00000000",
                     "00000001", "00100000", "00000000", "00000000",
                     "00001001", "00010000", "00000000", "00001010",
                     "00000010", "00100001", "00000000", "00000000",
                     "00000010", "00010000", "00000000", "00000001",
                     "00001010", "00000011", "11111111", "11110000",
                     "00000000", "00000000", "00000000", "00000000", ]
    # instructions3 = ["00000001", "00010000", "00000000", "00000001",
    #                  "00001110", "00000000", "00000000", "00000011",
    #                  "00000001", "00100000", "00000000", "00000010",
    #                  "00000001", "00110000", "00000000", "00000011",
    #                  "00000110", "00010000", "00000000", "00000001",
    #                  "00000111", "00100000", "00000000", "00000001",
    #                  "00001000", "00110000", "00000000", "00000001",
    #                  "00000000", "00000000", "00000000", "00000000", ]
    memory.load_program(id_generator.create_id(), instructions1)
    os.create_process("bbb", 0)
    memory.load_program(id_generator.create_id(), instructions2)
    os.create_process("ccc", 0)
    # memory.load_program(id_generator.create_id(), instructions3)
    # os.create_process("aaa", 0)
    print("here" + str(id_generator.get_create_id()))

    cpu.start()
    timer.start()
    time.sleep(20)
    print(os.process_pid)
    print(os.process_start_timer)
    print(os.process_running_timer)
    os.process_exit()
    time.sleep(3)
    print(str(threading.enumerate()))