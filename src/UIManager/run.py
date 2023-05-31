"""
Writen by Liang Zhengyang
"""
import pickle
from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QLabel
from PyQt6.QtWidgets import QLineEdit, QPlainTextEdit
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt, QDir, QTimer
import os
from collections import deque
import queue


# 导入自定义包
import sys
import os
current_path = os.getcwd()
sys.path.append(current_path + "\src")
sys.path.append(current_path + "\src\DeviceManager")
sys.path.append(current_path + "\src\FileManager")
sys.path.append(current_path + "\src\ProcessManager")
sys.path.append(current_path + "\src\MemoryManager")
from DeviceUI import DeviceManager
from System import System
from MemoryUI import MemoryUI
from ProcessUI import ProcessUI
import threading
from time import sleep

class CommandLineWindow():
    def __init__(self):
        # 初始化系统的各个模块
        self.system = System()
        # 创建QT应用
        self.app = QApplication([])
        print('Power OS start Version:v1.0')

        # 关机信号
        self.shut = False
        while not self.shut:
            cmd = input("Command > ")
            self.runCommand(cmd)
        self.app.exit()


    def runCommand(self, cmd):
        print('Result > ' + cmd)
        self.cmd_implement(cmd)


    def cmd_implement(self, cmd:str):
        """
        处理命令输入框输入进的指令
        """
        # cmd = str(cmd)
        tokens = cmd.split(" ")
        if tokens[0] == "ls":
            print('')
            self.system.file_manager.filecore.tree.show()
        elif tokens[0] == "new":
            state = self.system.file_manager.create_File(tokens[1], tokens[2])
            if state:
                print('Result > Successfully create!')
            else:
                print('Result > Failed create!')
        elif tokens[0] == "rm":
            state = self.system.file_manager.del_File(tokens[1])
            if state:
                print('Result > Successfully delete!')
            else:
                print('Result > Failed delete!')
        elif tokens[0] == "rename":
            state = self.system.file_manager.rename_File(tokens[1], tokens[2])
            if state:
                print('Result > Successfully rename!')
            else:
                print('Result > Failed rename!')
        elif tokens[0] == "disk":
            if len(tokens) == 1:
                print('Result > Error command!')
            else:
                if tokens[1] == "--rate":
                    self.system.file_manager.check_Disk()
                elif tokens[1] == "--content":
                    self.system.file_manager.print_disk()
                else:
                    print('Result > Error command!')
        elif tokens[0] == "cat":
            print('')
            self.system.file_manager.read_File(tokens[1])
        elif tokens[0] == "write":
            self.system.file_manager.write_File(tokens[1], tokens[2])
        elif tokens[0] == "clear":
            self.cmdOutput.clear()
        elif tokens[0] == "jobs":
            self.jobs_ui = ProcessUI(self.system)
            self.jobs_ui.window.show()
        elif tokens[0] == "mem":
            self.mem_ui = MemoryUI(self.system.container.resolve("memory"))
            self.mem_ui.window.show()
        elif tokens[0] == "dev":
            self.dev_ui = DeviceManager(self.system.device_st)
            self.dev_ui.window.show()
        elif tokens[0] == "wins":
            self.system.file_manager.write_instruction()
        elif tokens[0] == "rins":
            if len(tokens) == 1:
                self.system.file_manager.read_instruction()
            else:
                self.system.file_manager.read_instruction(tokens[1])
        elif tokens[0] == "quit":
            self.shut = True
            self.shutdown()
            print('Result > successfully shut down')
        elif tokens[0] == "log":
            if tokens[1]:
                self.show_log(tokens[1])
            else:
                print('Result > please input line number')
        elif tokens[0] == "help":
            print('Result > new <parentfile> <childrenfile>:show file tree')
            print('       > cat <filename>:view file content')
            print('       > rename <filename> <newname>:rename file name')
            print('       > rm <filename>:delete file')
            print('       > ls:show file tree')
            print('       > write <filename> <content>:write file')
            print('       > disk [--rate]:write file')
            print('       > disk [--content]:write file')
            print('       > dev:open device viewer')
            print('       > mem:open memory viewer')
            print('       > quit:shut down Power OS')
            print('       > wins:write instruction in file')
            print('       > rins:read application instruction')
            print('       > jobs:open process viewer')
            print('       > log <numbers>:list last numbers system log')
        else:
            print('Result > '
                                            + "Error:Please check your command, \""
                                            + cmd + "\" not a available command, use help to check")

    def show_log(self, line_limit):
        """
        打印日志函数\n
        line_limit输入接口是一个str字符串
        """
        lines = deque(maxlen=int(line_limit))  # 创建一个指定长度的 deque
        with open('system.log', 'r') as file:
            for line in file:
                lines.append(line.rstrip())  # 保存当前行到 deque 中

        for line in lines:
            print(line)  # 处理读取的行数据


    
    def shutdown(self):
        """
        关闭命令行主体窗口时进行的操作
        """
        # 在窗口关闭时执行的操作
        #############################################
        # 保存文件树结构
        self.system.file_manager.save()
        # 保存磁盘文件
        self.system.file_manager.saveDisk()
        # 保存设备信息
        self.system.device_st.save()
        # 终止所有线程
        self.system.os.process_exit()

        sleep(2)
        for thread in threading.enumerate():
            print(f"Thread name: {thread.name}")
        #############################################




if __name__ == '__main__':
    window = CommandLineWindow()

