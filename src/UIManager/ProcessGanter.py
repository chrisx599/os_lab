"""
Writen by Liang Zhengyang
"""
import sys
from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QFont
from PyQt6.QtCore import Qt

class GanttChartView(QGraphicsView):
    """
    甘特图界面类
    """
    def __init__(self):
        super().__init__()
        self.h = 50 # 每个条高多少
        self.start_x = 120
        self.init_ui()



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
        process_labels = ["Process 1", "Process 2", "Process 3"]
        for i, label in enumerate(process_labels):
            text_item = self.scene.addText(label)
            text_item.setFont(QFont("Arial", 10))
            text_item.setDefaultTextColor(Qt.GlobalColor.black)
            text_item.setPos(0, 50 + i * 55)  # 根据需要调整位置

        # 绘制甘特图条形
        rect1 = self.scene.addRect(100, 50, 200, 50)
        rect1.setBrush(QBrush(QColor("blue")))

        rect2 = self.scene.addRect(150, 150, 150, 50)
        rect2.setBrush(QBrush(QColor("red")))

        rect3 = self.scene.addRect(300, 100, 100, 50)
        rect3.setBrush(QBrush(QColor("green")))

        self.add_rect("6667", 18, 60, 3)

        self.setWindowTitle("Gantt Chart")

    def add_rect(self, process_id:str, start_time:int, end_time:int, i:int):
        """
        向图中添加内容
        """
        text_item = self.scene.addText(process_id)
        text_item.setFont(QFont("Arial", 10))
        text_item.setDefaultTextColor(Qt.GlobalColor.black)
        text_item.setPos(0, 50 + i * 55)  # 根据需要调整位置
        period = start_time - end_time
        rect1 = self.scene.addRect(start_time, 50 + i * 50, period, self.h)
        rect1.setBrush(QBrush(QColor("black")))

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = GanttChartView()
    view.show()
    sys.exit(app.exec())