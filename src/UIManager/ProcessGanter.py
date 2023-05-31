"""
Writen by Liang Zhengyang
"""
import sys
from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QFont
from PyQt6.QtCore import Qt, QTimer
from ProcessManager.Semaphore import Semaphore
import threading
from time import sleep

class GanttChartView(QGraphicsView):
    """
    甘特图界面类
    """
    def __init__(self, os):
        super().__init__()
        self.h = 40 # 每个条高多少
        self.start_x = 120
        self.init_ui()
        
        self.os = os


        # 定时更新MemoryUI中的内容
        self.timer = QTimer(self)
        self.timer.setInterval(500)  # 每隔 0.5 秒触发一次定时器
        # 将槽函数与定时器的 timeout 信号关联
        self.timer.timeout.connect(self.show_ganter)
        # 启动定时器
        self.timer.start()

    def show_ganter(self):
        # 获取process数据
        pid_list = self.os.process_pid
        start_list = self.os.process_start_timer
        stop_list = self.os.process_running_timer
        # print(pid_list)
        # print(start_list)
        # print(stop_list)
        # 运行实例程序
        # pid_list, start_list, stop_list = instance_pro()

        # for i in pid_list:
        #     self.add_rect(str(pid_list[i]), start_list[i], stop_list[i], i)
        num = len(pid_list)
        is_first = [True] * num
        for i in range(num):
            self.add_rect(str(pid_list[i]), start_list[i], stop_list[i], i, is_first)

    def init_ui(self):
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        # 设置视图属性
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # 设置视图大小和原点位置
        self.setSceneRect(0, 0, 800, 600)
        self.setFixedSize(800, 600)

        # 添加进程名称标签
        # process_labels = ["Process 1", "Process 2", "Process 3"]
        # for i, label in enumerate(process_labels):
        #     text_item = self.scene.addText(label)
        #     text_item.setFont(QFont("Arial", 10))
        #     text_item.setDefaultTextColor(Qt.GlobalColor.black)
        #     text_item.setPos(0, 50 + i * 55)  # 根据需要调整位置

        # # 绘制甘特图条形
        # rect1 = self.scene.addRect(100, 50, 200, 50)
        # rect1.setBrush(QBrush(QColor("blue")))

        # rect2 = self.scene.addRect(150, 150, 150, 50)
        # rect2.setBrush(QBrush(QColor("red")))

        # rect3 = self.scene.addRect(300, 100, 100, 50)
        # rect3.setBrush(QBrush(QColor("green")))

        # self.add_rect("6667", 18, 60, 3)

        self.setWindowTitle("Gantt Chart")

    def add_rect(self, process_id:str, start_time:int, run_time:int, i:int, is_first:list[bool]):
        """
        向图中添加内容
        """
        if is_first[int(process_id)]:
            text_item = self.scene.addText(process_id)
            text_item.setFont(QFont("Arial", 10))
            text_item.setDefaultTextColor(Qt.GlobalColor.black)
            text_item.setPos(0, 50 + i * 55)  # 根据需要调整位置
            # period = start_time - run_time
            rect1 = self.scene.addRect(start_time * 10 + 15, 25 + int(process_id) * 30, run_time * 10, self.h)
            # rect1 = self.scene.addRect(start_time + 20, 50 + i * 50, run_time * 10, self.h)
            rect1.setBrush(QBrush(QColor("green")))
            is_first[int(process_id)] = False
        else:
            rect1 = self.scene.addRect(start_time * 10 + 15, 25 + int(process_id) * 30, run_time * 10, self.h)
            # rect1 = self.scene.addRect(start_time, 50 + i * 50, run_time * 10, self.h)
            rect1.setBrush(QBrush(QColor("green")))

    # def instance_pro(self):
    #     self.semaphore = Semaphore(3)

    #     # 创建多个线程进行测试
    #     threads = []
    #     for i in range(5):
    #         t = threading.Thread(target=self.worker, args=(i,))
    #         threads.append(t)
    #         t.start()

    #     # 等待所有线程执行完成
    #     for t in threads:
    #         t.join()

    # def worker(self, id):
    #         print(f'Worker {id} 正在执行')
    #         self.semaphore.wait()
    #         for i in range(5):
    #             print(f'Worker {id} 正在执行{i}部分')
    #             sleep(5)
    #         # 这里可以添加需要执行的代码
    #         self.semaphore.signal()
    #         print(f'Worker {id} 释放信号量')

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = GanttChartView()
    view.show()
    sys.exit(app.exec())