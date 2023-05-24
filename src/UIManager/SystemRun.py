"""
Writen by Liang Zhengyang
"""
import pickle
from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QLabel
from PyQt6.QtWidgets import QLineEdit, QPlainTextEdit
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt, QDir
import os


# 导入自定义包
import sys
import os
current_path = os.getcwd()
sys.path.append(current_path + "\src")
sys.path.append(current_path + "\src\DeviceManager")
sys.path.append(current_path + "\src\FileManager")
sys.path.append(current_path + "\src\ProcessManager")
from DeviceUI import DeviceManager
from System import System
from MemoryUI import MemoryUI
from ProcessUI import ProcessUI

class CommandLineWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.system = System()

        self.setWindowTitle("PowerOS")
        self.resize(1000, 650)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0) # 去除边界

        self.cmdOutput = QPlainTextEdit()
        self.cmdOutput.setReadOnly(True)
        self.cmdOutput.setStyleSheet("""
        QPlainTextEdit {
            background-color: black;
            color: white;
            border: none;
            font-family: "Courier New", Courier, monospace;
        }""")
        main_layout.addWidget(self.cmdOutput)
        
        layout = QHBoxLayout()

        self.promptLabel = QLabel("Command> ")
        self.promptLabel.setStyleSheet("""
        QLabel {
            background-color: black;
            color: green;
            font-family: "Courier New", Courier, monospace;
        }""")
        layout.addWidget(self.promptLabel)

        self.cmdInput = QLineEdit()
        self.cmdInput.returnPressed.connect(self.runCommand)
        self.cmdInput.installEventFilter(self)
        self.cmdInput.setStyleSheet("""
        QLineEdit {
            background-color: black;
            color: green;
            border: none;
            selection-background-color: green;
            selection-color: black;
            font-family: "Courier New", Courier, monospace;
        }""")
        layout.addWidget(self.cmdInput)

        main_layout.addLayout(layout)
 
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
 
        self.setStyleSheet("""
        QMainWindow {
            background-color: black;
            color: white;
            font-family: "Courier New", Courier, monospace;
        }""")

        self.cmdInput.setFocus()

        # 重定向标准输出流至QPlainTextEdit
        sys.stdout = Stream(stdout=self.cmdOutput)

    
    def runCommand(self):
        cmd = self.cmdInput.text()
        # self.currentDir = QDir.currentPath()
        self.cmdOutput.appendPlainText('Result > ' + cmd)
        self.cmd_implement(cmd)
        # self.cmdOutput.appendPlainText(self.currentDir + '> ' + cmd)
        # self.cmdOutput.appendPlainText('Result > ' + cmd)
        self.cmdInput.clear()


    def cmd_implement(self, cmd):
        cmd = str(cmd)
        tokens = cmd.split(" ")
        if tokens[0] == "ls":
            self.system.file_manager.filecore.tree.show()
        elif tokens[0] == "new":
            state = self.system.file_manager.create_File(tokens[1], tokens[2])
            if state:
                self.cmdOutput.appendPlainText('Result > Successfully create!')
            else:
                self.cmdOutput.appendPlainText('Result > Failed create!')
        elif tokens[0] == "rm":
            state = self.system.file_manager.del_File(tokens[1])
            if state:
                self.cmdOutput.appendPlainText('Result > Successfully delete!')
            else:
                self.cmdOutput.appendPlainText('Result > Failed delete!')
        elif tokens[0] == "rename":
            state = self.system.file_manager.del_File(tokens[1], tokens[2])
            if state:
                self.cmdOutput.appendPlainText('Result > Successfully rename!')
            else:
                self.cmdOutput.appendPlainText('Result > Failed rename!')
        elif tokens[0] == "disk":
            if tokens[1] == "--rate":
                self.system.file_manager.check_Disk()
            elif tokens[1] == "--content":
                self.system.file_manager.print_disk()
            else:
                self.cmdOutput.appendPlainText('Result > Error command!')
        elif tokens[0] == "cat":
            self.system.file_manager.read_File(tokens[1])
        elif tokens[0] == "write":
            self.system.file_manager.write_File(tokens[1], tokens[2])
        elif tokens[0] == "clear":
            self.cmdOutput.clear()
        elif tokens[0] == "jobs":
            self.jobs_ui = ProcessUI()
            self.jobs_ui.window.show()
        elif tokens[0] == "mem":
            self.mem_ui = MemoryUI()
            self.mem_ui.window.show()
        elif tokens[0] == "dev":
            self.dev_ui = DeviceManager(self.system.device_st)
            self.dev_ui.window.show()
        elif tokens[0] == "help":
            self.cmdOutput.appendPlainText('Result > new <parentfile> <childrenfile>:show file tree')
            self.cmdOutput.appendPlainText('       > cat <filename>:view file content')
            self.cmdOutput.appendPlainText('       > rename <filename> <newname>:rename file name')
            self.cmdOutput.appendPlainText('       > rm <filename>:delete file')
            self.cmdOutput.appendPlainText('       > ls:show file tree')
            self.cmdOutput.appendPlainText('       > ls:show file tree')
        else:
            self.cmdOutput.appendPlainText('Result > '
                                            + "Error:Please check your command, \""
                                            + cmd + "\" not a available command, use help to check")

    def eventFilter(self, obj, event):
        if event.type() == QKeyEvent.Type.KeyPress and event.key() == Qt.Key.Key_Tab:
            return True
        return super().eventFilter(obj, event)
    
    def closeEvent(self, event):
        # 在窗口关闭时执行的操作
        # 保存文件树结构
        self.system.file_manager.save()
        self.system.file_manager.saveDisk()
        # 调用父类的 closeEvent() 方法以确保窗口正常关闭
        super().closeEvent(event)

class Stream:
    """
    重定向终端文件到qt窗口中
    """
    def __init__(self, stdout=None):
        self.stdout = stdout

    def write(self, text):
        self.stdout.appendPlainText(text)

    def flush(self):
        pass  # 这里可以添加适当的刷新操作

if __name__ == '__main__':
    app = QApplication([])
    window = CommandLineWindow()
    window.show()
    app.exec()

