# # coding:utf-8
# import sys
# from PyQt6.QtCore import Qt
# from PyQt6.QtGui import QFileSystemModel
# from PyQt6.QtWidgets import QApplication, QWidget, QTreeWidgetItem, QHBoxLayout

# from qfluentwidgets import TreeWidget, setTheme, Theme, TreeView


# class Demo(QWidget):
#     """ 树形控件演示 """

#     def __init__(self):
#         super().__init__()
#         self.hBoxLayout = QHBoxLayout(self)
#         self.setStyleSheet("Demo{background:rgb(255,255,255)}")
#         # setTheme(Theme.DARK)

#         self.view = TreeView(self)
#         model = QFileSystemModel()
#         model.setRootPath('.')
#         self.view.setModel(model)

#         self.hBoxLayout.addWidget(self.view)
#         self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
#         self.resize(700, 600)


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     w = Demo()
#     w.show()
#     sys.exit(app.exec())




# coding:utf-8
# import sys

# from PyQt6.QtCore import Qt
# from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
# from qfluentwidgets import IndeterminateProgressBar, ProgressBar


# class Demo(QWidget):

#     def __init__(self):
#         super().__init__()
#         self.vBoxLayout = QVBoxLayout(self)
#         self.progressBar = ProgressBar(self)
#         # self.inProgressBar = IndeterminateProgressBar(self)

#         self.progressBar.setValue(50)
#         self.vBoxLayout.addWidget(self.progressBar)
#         # self.vBoxLayout.addWidget(self.inProgressBar)
#         self.vBoxLayout.setContentsMargins(30, 30, 30, 30)
#         self.resize(400, 400)


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     w = Demo()
#     w.show()
#     app.exec()



from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel

# 创建应用程序和主窗口
app = QApplication([])
window = QMainWindow()

# 创建 QLabel 用于显示动态内容
label = QLabel("Initial Text")
window.setCentralWidget(label)

# 创建 QTimer
timer = QTimer()
timer.setInterval(1000)  # 每隔 1 秒触发一次定时器

# 定义定时器触发时执行的槽函数
def update_label():
    label.setText("Updated Text")

# 将槽函数与定时器的 timeout 信号关联
timer.timeout.connect(update_label)

# 启动定时器
timer.start()

# 显示主窗口
window.show()
app.exec()
