from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QLabel
from PyQt6.QtWidgets import QLineEdit, QPlainTextEdit
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt, QDir
import os

from DeviceUI import DeviceManager

# 导入自定义包
import sys
import os
current_path = os.getcwd()
sys.path.append(current_path + "\src")
sys.path.append(current_path + "\src\DeviceManager")
from System import System

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
    
    def runCommand(self):
        cmd = self.cmdInput.text()
        self.currentDir = QDir.currentPath()
        self.cmd_implement(cmd)
        self.cmdOutput.appendPlainText(self.currentDir + '> ' + cmd)
        self.cmdInput.clear()


    def cmd_implement(self, cmd):
        cmd = str(cmd)
        tokens = cmd.split(" ")
        if tokens[0] == "cd":
            # 检查路径是否存在
            if os.path.exists(tokens[1]):
                os.chdir(tokens[1])
                self.currentDir = QDir.currentPath()
            else:
                self.cmdOutput.appendPlainText(self.currentDir + '> ' + 
                                               "Error:Please check your path")
        elif tokens[0] == "ls":
            pass
        elif tokens[0] == "mkdir":
            pass
        elif tokens[0] == "touch":
            pass
        elif tokens[0] == "rm":
            pass
        elif tokens[0] == "mv":
            pass
        elif tokens[0] == "cp":
            pass
        elif tokens[0] == "cat":
            pass
        elif tokens[0] == "echo":
            pass
        elif tokens[0] == "clear":
            pass
        elif tokens[0] == "jobs":
            pass
        elif tokens[0] == "mem":
            pass
        elif tokens[0] == "dev":
            self.dev_ui = DeviceManager(self.system.device_st)
            self.dev_ui.window.show()
        elif tokens[0] == "help":
            pass
        else:
            self.cmdOutput.appendPlainText(self.currentDir + '> '
                                            + "Error:Please check your command, \""
                                            + cmd + "\" not a available command, use help to check")

    def eventFilter(self, obj, event):
        if event.type() == QKeyEvent.Type.KeyPress and event.key() == Qt.Key.Key_Tab:
            return True
        return super().eventFilter(obj, event)

if __name__ == '__main__':
    app = QApplication([])
    window = CommandLineWindow()
    window.show()
    app.exec()

