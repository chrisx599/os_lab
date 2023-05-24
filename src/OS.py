# -*- coding:utf-8 -*-
# @FileName : OS.py
# @Time     : 2023/5/18 21:11
# @Author   : qingyao
import threading

from utils.Container import *
from processManager.PCB import *
import treelib

class OS:
    cpu = None
    process = None
    interrupt = None
    running_pcb = None
    system_time = 0

    process_tree = None


    @inject("cpu", "process", "interrupt", "timeout_event",
            "atom_lock", "running_event", "process_over_event", "new_process_event")
    def __init__(self, cpu, process, interrupt, system_time, timeout_event,
                 atom_lock, running_event, process_over_event, new_process_event):
        self.cpu = cpu
        self.interrupt = interrupt
        self.process = process
        self.system_time = system_time
        self.process_tree = treelib.Tree()
        self.timeout_event = timeout_event
        self.atom_lock = atom_lock
        self.running_event = running_event
        self.process_over_event = process_over_event
        self.new_process_event = new_process_event


    def dispatch_func(self):
        # 保存上下文环境
        ax, bx, cx, dx, axm, bxm, cxm, dxm = self.cpu.get_gen_reg()
        self.running_pcb.set_gen_reg(ax, bx, cx, dx, axm, bxm, cxm, dxm)
        pc = self.cpu.get_PC()
        self.running_pcb.set_PC(pc)
        ir = self.cpu.get_IR()
        self.running_pcb.set_IR(ir)
        # 修改进程状态
        if self.running_pcb.get_state == PCB.PROCESS_RUNNING:
            self.running_pcb.set_state(PCB.PROCESS_READY)
        # 进程调度
        next_running_pcb = self.process.dispatch_process(self.running_pcb)
        self.running_pcb = next_running_pcb
        if next_running_pcb == None:
            self.new_process_event.wait()
            self.new_process_event.clear()
        # 恢复上下文环境
        ax, bx, cx, dx, axm, bxm, cxm, dxm = self.running_pcb.get_gen_reg_all()
        self.cpu.set_gen_reg_all(ax, bx, cx, dx, axm, bxm, cxm, dxm)
        pc = self.running_pcb.get_pc()
        self.cpu.set_PC(pc)
        ir = self.running_pcb.get_IR()
        self.cpu.get_IR(ir)

    def dispatch_process(self):
        while True:
            if not self.timeout_event.is_set():
                self.timeout_event.wait()
            self.running_event.clear()
            if self.process_over_event.is_set():
                self.running_pcb.set_state(PCB.PROCESS_EXIT)
            with self.atom_lock:
                self.dispatch_func()
            self.timeout_event.clear()
            self.process_over_event.clear()
            self.running_event.set()

    def create_process(self, name, parent_pid):
        pcb = self.process.create_process(name)
        if self.process_tree.size() == 0:
            self.process_tree.create_node(name, pcb.get_PID(), data=pcb)
        else:
            self.process_tree.create_node(name, pcb.get_PID(), parent=parent_pid, data=pcb)






if __name__ == "__main__":
    run_code = 0
