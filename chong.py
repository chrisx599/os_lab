import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit
from PyQt6.QtCore import Qt, QTimer
import threading
import queue
import time

class WorkerThread(threading.Thread):
    def __init__(self, output_queue):
        super().__init__()
        self.output_queue = output_queue

    def run(self):
        # 模拟线程中的输出
        for i in range(10):
            output = f"Thread {threading.get_ident()}: Message {i}"
            self.output_queue.put(output)
            time.sleep(1)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)

        self.output_queue = queue.Queue()
        self.worker_threads = []

        self.start_threads()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_output)
        self.timer.start(1000)

    def start_threads(self):
        for _ in range(3):
            thread = WorkerThread(self.output_queue)
            thread.start()
            self.worker_threads.append(thread)

    def update_output(self):
        while not self.output_queue.empty():
            output = self.output_queue.get()
            self.textEdit.append(output.strip())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())


import sys
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit
from io import StringIO
import contextlib

class PrintOutput(QObject):
    outputReceived = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.outputBuffer = StringIO()

    def write(self, s):
        self.outputBuffer.write(s)
        self.outputBuffer.seek(0)
        self.outputReceived.emit(self.outputBuffer.getvalue())
        self.outputBuffer.seek(0, 2)

    def flush(self):
        pass

@contextlib.contextmanager
def redirect_stdout(new_target):
    old_target, sys.stdout = sys.stdout, new_target
    try:
        yield new_target
    finally:
        sys.stdout = old_target

class WorkerThread(QThread):
    outputReceived = pyqtSignal(str)

    def run(self):
        with redirect_stdout(PrintOutput()) as output:
            # 模拟线程中的输出
            for i in range(10):
                print(f"Thread {self.currentThreadId()}: Message {i}")
                self.msleep(1000)
                self.outputReceived.emit(output.outputBuffer.getvalue())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)

        self.workerThreads = []

        self.startThreads()

    def startThreads(self):
        for i in range(3):
            thread = WorkerThread()
            thread.started.connect(lambda id=i: self.appendOutput(f"Thread {id} started"))
            thread.finished.connect(lambda id=i: self.appendOutput(f"Thread {id} finished"))
            thread.outputReceived.connect(self.appendOutput)
            self.workerThreads.append(thread)
            thread.start()

    def appendOutput(self, output):
        self.textEdit.append(output.strip())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())


