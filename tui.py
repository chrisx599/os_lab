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



# from PyQt6.QtCore import QTimer
# from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel

# # 创建应用程序和主窗口
# app = QApplication([])
# window = QMainWindow()

# # 创建 QLabel 用于显示动态内容
# label = QLabel("Initial Text")
# window.setCentralWidget(label)

# # 创建 QTimer
# timer = QTimer()
# timer.setInterval(1000)  # 每隔 1 秒触发一次定时器

# # 定义定时器触发时执行的槽函数
# def update_label():
#     label.setText("Updated Text")

# # 将槽函数与定时器的 timeout 信号关联
# timer.timeout.connect(update_label)

# # 启动定时器
# timer.start()

# # 显示主窗口
# window.show()
# app.exec()


# from treelib import Tree

# tree = Tree()
# tree.create_node("A", "a")  # 创建根节点
# tree.create_node("B", "b", parent="a")  # 创建子节点
# tree.create_node("C", "c", parent="a")  # 创建另一个子节点
# lists = tree.all_nodes()
# for item in lists:
#     print(tree.children(item.identifier))
#     a = []
#     if a:
#         print("1")


import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QTreeView, QVBoxLayout, QWidget
from PyQt6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon, QFileSystemModel, QStandardItemModel, 
    QImage, QKeySequence, QLinearGradient, QPainter, QStandardItem,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # 创建一个QTreeView对象
        self.tree_view = QTreeView(self)
        self.tree_view.setHeaderHidden(True)
        self.tree_view.setSortingEnabled(True)
        self.tree_view.setGeometry(0,0,200,200)

        # 创建一个QStandardItemModel对象，用于存储数据
        self.model = QStandardItemModel()
        self.tree_view.setModel(self.model)

        # 创建根节点并添加到模型中
        root_item = self.model.invisibleRootItem()
        root_item.appendRow([QStandardItem("Parent Item"), QStandardItem("Child Item 1"), QStandardItem("Child Item 2")])

        # 创建子节点并添加到模型中
        child_item = root_item.child(0)
        child_item.appendRow([QStandardItem("Grandchild Item 1"), QStandardItem("Grandchild Item 2")])

        # 创建根节点并添加到模型中
        root_item2 = self.model.invisibleRootItem()
        root_item2.appendRow([QStandardItem("dddParent Item"), QStandardItem("Child Item 1"), QStandardItem("Child Item 2")])

        # 创建子节点并添加到模型中
        child_item2 = root_item2.child(1)
        child_item2.appendRow([QStandardItem("Grandchild Item 1"), QStandardItem("Grandchild Item 2")])

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

