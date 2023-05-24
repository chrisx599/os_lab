# import sys
# from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPlainTextEdit
# from PyQt6.QtCore import QTextStream, Qt

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.init_ui()

#     def init_ui(self):
#         self.setWindowTitle("Terminal Output")

#         # 创建一个QPlainTextEdit小部件
#         self.plainTextEdit = QPlainTextEdit()
#         self.plainTextEdit.setReadOnly(True)  # 设置为只读模式

#         # 设置布局
#         layout = QVBoxLayout()
#         layout.addWidget(self.plainTextEdit)

#         # 创建一个包含QPlainTextEdit的QWidget小部件作为主窗口的中心部件
#         central_widget = QWidget()
#         central_widget.setLayout(layout)
#         self.setCentralWidget(central_widget)

#         # 重定向标准输出流至QPlainTextEdit
#         sys.stdout = Stream(stdout=self.plainTextEdit)

#         # 输出一些示例内容
#         print("Hello, World!")
#         for i in range(5):
#             print(f"Line {i}")

# class Stream:
#     def __init__(self, stdout=None):
#         self.stdout = stdout

#     def write(self, text):
#         self.stdout.insertPlainText(text)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())


# import sys
# from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
# from PyQt6.QtGui import QPainter, QBrush, QPen, QColor
# from PyQt6.QtCore import Qt

# class GanttChartView(QGraphicsView):
#     def __init__(self):
#         super().__init__()
#         self.init_ui()

#     def init_ui(self):
#         scene = QGraphicsScene(self)
#         self.setScene(scene)

#         # 绘制甘特图条形
#         rect1 = scene.addRect(50, 50, 200, 50)
#         rect1.setBrush(QBrush(QColor("blue")))

#         rect2 = scene.addRect(100, 150, 150, 50)
#         rect2.setBrush(QBrush(QColor("red")))

#         rect3 = scene.addRect(250, 100, 100, 50)
#         rect3.setBrush(QBrush(QColor("green")))

#         self.setWindowTitle("Gantt Chart")

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     view = GanttChartView()
#     view.show()
#     sys.exit(app.exec())

# import sys
# from PyQt6.QtWidgets import QApplication, QMainWindow, QPlainTextEdit
# from PyQt6.QtCore import QProcess, QIODevice

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.output_widget = QPlainTextEdit(self)
#         self.setCentralWidget(self.output_widget)

#         self.process = QProcess(self)
#         self.process.readyReadStandardOutput.connect(self.handle_output)

#         self.run_command("ls -l")  # 示例命令

#     def run_command(self, command):
#         self.output_widget.clear()
#         self.process.start(command)

#     def handle_output(self):
#         output = self.process.readAllStandardOutput().data().decode()
#         self.output_widget.appendPlainText(output)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())


from treelib import Tree, Node
import pickle

# 创建树对象并添加节点
tree = Tree()
tree.create_node("A", "a")
tree.create_node("B", "b", parent="a")
tree.create_node("C", "c", parent="a")


# # 保存树到文件
# tree.save2file("tree.json")


# 保存树到文件
# tree_json = tree.to_dict()
with open('tree.pkl', 'wb') as file:
    pickle.dump(tree, file)


# 遍历加载的树
with open('tree.pkl', 'rb') as file:
    load_tree = pickle.load(file)

load_tree.show()

print(load_tree)



