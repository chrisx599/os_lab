"""
Writen by Liang Zhengyang
"""
from PyQt6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PyQt6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PyQt6.QtWidgets import (QApplication, QHeaderView, QSizePolicy, QTableWidget,
    QTableWidgetItem, QWidget, QLabel)

from qfluentwidgets import ProgressBar

class Ui_MemoryViewer(object):
    def setupUi(self, MemoryViewer):
        if not MemoryViewer.objectName():
            MemoryViewer.setObjectName(u"MemoryViewer")
        MemoryViewer.resize(500, 550)
        self.MemoryList = QTableWidget(MemoryViewer)
        if (self.MemoryList.columnCount() < 16):
            self.MemoryList.setColumnCount(16)
        if (self.MemoryList.rowCount() < 16):
            self.MemoryList.setRowCount(16)
        self.MemoryList.setObjectName(u"MemoryList")
        self.MemoryList.setGeometry(QRect(0, 0, 500, 500))
        self.MemoryList.setRowCount(16)
        self.MemoryList.setColumnCount(16)

        ##############################################################
        # 设置进度条来展示内存占用率
        self.progressBar = ProgressBar(MemoryViewer)
        self.progressBar.setValue(50)
        self.progressBar.setGeometry(0, 500, 500, 50)
        # 设置两个标签来显示已占用内存和总内存
        self.already_used = QLabel(MemoryViewer)
        self.already_used.setGeometry(50, 520, 150, 30)
        self.already_used.setText("test")
        self.all_mem = QLabel(MemoryViewer)
        self.all_mem.setGeometry(250, 520, 150, 30)
        self.all_mem.setText("dawdaw")
        # 设置一个标签来显示已占用百分比
        # self.rate = QLabel(MemoryViewer)
        # self.rate.setGeometry(400, 530, 100, 20)
        # self.rate.setText("dddd")
        ##############################################################

        # 设置格子的大小
        cell_size = 28  # 设置每个格子的大小
        
        # 设置行高和列宽
        for i in range(self.MemoryList.rowCount()):
            self.MemoryList.setRowHeight(i, cell_size)
        
        for j in range(self.MemoryList.columnCount()):
            self.MemoryList.setColumnWidth(j, cell_size)

        self.retranslateUi(MemoryViewer)

        QMetaObject.connectSlotsByName(MemoryViewer)
    # setupUi

    def retranslateUi(self, MemoryViewer):
        MemoryViewer.setWindowTitle(QCoreApplication.translate("MemoryViewer", u"Form", None))
    # retranslateUi



class MemoryUI():
    def __init__(self) -> None:
        self.window = QWidget()
        self.ui = Ui_MemoryViewer()
        self.ui.setupUi(self.window)


    def set_color(self, memory_matrix):
        for i in range(16):
            for k in range(16):
                if memory_matrix[i][k]:
                    color = QColor(0, 255, 0)  # 设置为绿色
                    item = QTableWidgetItem("")
                    # item = QTableWidgetItem("Cell Text")
                    item.setBackground(color)
                    self.ui.MemoryList.setItem(i, k, item)

    def set_label(self, already_used, all_mem):
        rate = already_used / all_mem
        self.ui.progressBar.setValue(int(rate))
        self.ui.already_used.setText("已占用内存:" + str(already_used))
        self.ui.all_mem.setText("总内存:" + str(all_mem))

if __name__ == "__main__":
    app = QApplication([])
    window = MemoryUI()
    mm = [[1,1,1,0,1,0,1,0,1,1,0,1,1,1,0,1], [1,1,1,0,1,0,1,0,1,1,0,1,1,1,0,1]
          ,[1,1,1,0,1,0,1,0,1,1,0,1,1,1,0,1], [1,1,1,0,1,0,1,0,1,1,0,1,1,1,0,1]
          ,[1,1,1,0,1,0,1,0,1,1,0,1,1,1,0,1], [1,1,1,0,1,0,1,0,1,1,0,1,1,1,0,1]
          ,[1,1,1,0,1,0,1,0,1,1,0,1,1,1,0,1], [1,1,1,0,1,0,1,0,1,1,0,1,1,1,0,1]
          ,[1,1,1,0,1,0,1,0,1,1,0,1,1,1,0,1], [1,1,1,0,1,0,1,0,1,1,0,1,1,1,0,1]
          ,[1,1,1,0,1,0,1,0,1,1,0,1,1,1,0,1], [1,1,1,0,1,0,1,0,1,1,0,1,1,1,0,1]
          ,[1,1,1,0,1,0,1,0,1,1,0,1,1,1,0,1], [1,1,1,0,1,0,1,0,1,1,0,1,1,1,0,1]
          ,[1,1,1,0,1,0,1,0,1,1,0,1,1,1,0,1], [1,1,1,0,1,0,1,0,1,1,0,1,1,1,0,1]]
    window.set_color(mm)
    window.window.show()
    
    app.exec()