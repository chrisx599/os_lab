"""
Writen by Liang Zhengyang
"""
from PyQt6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect, QThread, QTimer,
    QSize, QTime, QUrl, Qt)
from PyQt6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon, QFileSystemModel, QStandardItemModel, 
    QImage, QKeySequence, QLinearGradient, QPainter, QStandardItem,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PyQt6.QtWidgets import (QApplication, QHeaderView, QLabel, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget, QHBoxLayout, QPlainTextEdit)

from qfluentwidgets import (LineEdit, PushButton, TableView, TreeView)
from ProcessGanter import GanttChartView
from OS import OS
import threading
from treelib import Tree
from time import sleep
from ProcessManager.Semaphore import Semaphore
import queue
from ProcessManager.Banker import BankerAlgorithm

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(800, 600)
        # self.TableView = TableView(Form)
        # self.TableView.setObjectName(u"TableView")
        # self.TableView.setGeometry(QRect(0, 0, 600, 600))

        # 树形结构
        # self.hBoxLayout = QHBoxLayout(self)
        self.view = TreeView(Form)
        # model = QFileSystemModel()
        # model.setRootPath('.')
        # self.view.setModel(model)
        self.view.setGeometry(QRect(0, 0, 600, 600))

#####################################################################################################
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(650, 90, 130, 401))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum
                                            , QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_3)

        # self.label = QLabel(self.widget)
        # self.label.setObjectName(u"label")

        # self.verticalLayout.addWidget(self.label)

        # self.BaseEdit = LineEdit(self.widget)
        # self.BaseEdit.setObjectName(u"BaseEdit")

        # self.verticalLayout.addWidget(self.BaseEdit)

        # self.label_2 = QLabel(self.widget)
        # self.label_2.setObjectName(u"label_2")

        # self.verticalLayout.addWidget(self.label_2)

        # self.LimitEdit = LineEdit(self.widget)
        # self.LimitEdit.setObjectName(u"LimitEdit")

        # self.verticalLayout.addWidget(self.LimitEdit)

        # self.label_3 = QLabel(self.widget)
        # self.label_3.setObjectName(u"label_3")

        # self.verticalLayout.addWidget(self.label_3)

        # self.SizeEdit = LineEdit(self.widget)
        # self.SizeEdit.setObjectName(u"SizeEdit")

        # self.verticalLayout.addWidget(self.SizeEdit)

        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout.addWidget(self.label_4)

        self.NameEdit = LineEdit(self.widget)
        self.NameEdit.setObjectName(u"NameEdit")

        self.verticalLayout.addWidget(self.NameEdit)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum
                                            , QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.CreateProButton = PushButton(self.widget)
        self.CreateProButton.setObjectName(u"CreateProButton")

        self.verticalLayout.addWidget(self.CreateProButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum
                                          , QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.StopProButton = PushButton(self.widget)
        self.StopProButton.setObjectName(u"StopProButton")

        self.verticalLayout.addWidget(self.StopProButton)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum
                                            , QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_4)

        self.ViewButton = PushButton(self.widget)
        self.ViewButton.setObjectName(u"ViewButton")

        self.verticalLayout.addWidget(self.ViewButton)

        ###########################################################
        # 信号量部分
        self.Mullabel = QLabel(self.widget)
        self.Mullabel.setObjectName(u"Mullabel")
        self.verticalLayout.addWidget(self.Mullabel)
        self.MulEdit = LineEdit(self.widget)
        self.MulEdit.setObjectName(u"MulEdit")
        self.verticalLayout.addWidget(self.MulEdit)
        self.MulButton = PushButton(self.widget)
        self.MulButton.setObjectName(u"MulButton")
        self.verticalLayout.addWidget(self.MulButton)
        ###########################################################


        ###########################################################
        # 银行家算法部分
        self.banklabel = QLabel(self.widget)
        self.banklabel.setObjectName(u"banklabel")
        self.verticalLayout.addWidget(self.banklabel)
        self.bankEdit = LineEdit(self.widget)
        self.bankEdit.setObjectName(u"MulEdit")
        self.verticalLayout.addWidget(self.bankEdit)
        self.bankButton = PushButton(self.widget)
        self.bankButton.setObjectName(u"bankButton")
        self.verticalLayout.addWidget(self.bankButton)
        ###########################################################

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        # self.label.setText(QCoreApplication.translate("Form", u"\u57fa\u5740:", None))
        # self.label_2.setText(QCoreApplication.translate("Form", u"\u4e0a\u9650:", None))
        # self.label_3.setText(QCoreApplication.translate("Form", u"\u4ee3\u7801\u5927\u5c0f:", None))
        self.label_4.setText("程序名称:")
        self.Mullabel.setText("信号量:")
        self.MulButton.setText("进程间通信")

        self.banklabel.setText("安全序列")
        self.bankButton.setText("执行检查")

        self.CreateProButton.setText(QCoreApplication.translate("Form", u"\u521b\u5efa\u8fdb\u7a0b", None))
        self.StopProButton.setText(QCoreApplication.translate("Form", u"\u7ec8\u6b62\u8fdb\u7a0b", None))
        self.ViewButton.setText(QCoreApplication.translate("Form", u"\u67e5\u770b\u8fdb\u7a0b\u5e76\u53d1", None))
    # retranslateUi



class ProcessUI():
    def __init__(self, system) -> None:
        self.window = QWidget()
        self.ui = Ui_Form()
        self.ui.setupUi(self.window)

        # self.output = output
        self.system = system
        self.signal()

        self.show_pro_tree()

        # # 定时更新MemoryUI中的内容
        # self.timer = QTimer(self.window)
        # self.timer.setInterval(500)  # 每隔 0.5 秒触发一次定时器
        # # 将槽函数与定时器的 timeout 信号关联
        # self.timer.timeout.connect(self.show_pro_tree)
        # # 启动定时器
        # self.timer.start()

        # self.outqueue = queue.Queue()
        # # 定时更新MemoryUI中的内容
        # self.timer = QTimer(self.window)
        # self.timer.setInterval(1000)  # 每隔 0.5 秒触发一次定时器
        # # 将槽函数与定时器的 timeout 信号关联
        # self.timer.timeout.connect(self.update_cmd)
        # # # 启动定时器
        # self.timer.start()


    # def update_cmd(self):
    #     if not self.outqueue.empty():
    #         text = self.outqueue.get()
    #         self.ui.Mulout.insertPlainText(text)


    def signal(self):
        self.ui.ViewButton.clicked.connect(self.show_ganter)
        self.ui.CreateProButton.clicked.connect(self.create_process)
        self.ui.StopProButton.clicked.connect(self.stop_process)
        self.ui.MulButton.clicked.connect(self.start_mul_pro)
        self.ui.bankButton.clicked.connect(self.banker)

    def banker(self):
        # 银行家算法测试程序
        available = [3, 3, 2]  # 可用资源数目
        print(f"开始时可用资源数目{available}")
        max_claim = [
            [7, 5, 3],
            [3, 2, 2],
            [9, 0, 2],
            [2, 2, 2],
            [4, 3, 3]
        ]  # 进程对各资源的最大需求
        print(f"进程对各资源的最大需求{max_claim}")
        allocation = [
            [0, 1, 0],
            [2, 0, 0],
            [3, 0, 2],
            [2, 1, 1],
            [0, 0, 2]
        ]  # 进程已分配的资源
        print(f"进程开始时已分配的资源{allocation}")
        need = [
            [7, 4, 3],
            [1, 2, 2],
            [6, 0, 0],
            [0, 1, 1],
            [4, 3, 1]
        ]  # 进程还需要的资源
        print(f"进程开始时还需要的资源{need}")

        banker = BankerAlgorithm(available, max_claim, allocation, need)
        safe, sequence = banker.is_safe_state()
        if safe:
            self.ui.bankEdit.setText(str(sequence))
            print("系统处于安全状态，安全序列为:", sequence)
        else:
            self.ui.bankEdit.setText("无安全序列")
            print("系统处于不安全状态")

    def start_mul_pro(self):
        # 信号量测试程序
        init = self.ui.MulEdit.text()
        self.semaphore = Semaphore(int(init))

        # 创建多个线程进行测试
        threads = []
        for i in range(5):
            t = threading.Thread(target=self.worker, args=(i,))
            threads.append(t)
            t.start()

        # 等待所有线程执行完成
        for t in threads:
            t.join()
        
        print("执行完毕")


    def worker(self, id):
            self.semaphore.wait()
            print(f'Worker {id} 开始执行')
            for i in range(5):
                print(f'Worker {id} 正在执行{i}部分')
                sleep(1)
            # 这里可以添加需要执行的代码
            self.semaphore.signal()
            print(f'Worker {id} 释放信号量')
        

    # def show_ganter_thread(self):
    #     # 创建新线程对象
    #     # thread = MyThread()
    #     # # 启动线程
    #     # thread.start()
    #     # # 等待线程结束
    #     # thread.wait()

    #     # 创建新线程对象
    #     thread = QThread()

    #     # 设置自定义线程类为线程对象的父类
    #     my_thread = MyThread()
    #     my_thread.moveToThread(thread)

    #     # 连接启动信号和槽函数
    #     thread.started.connect(my_thread.run)
    #     # 启动线程
    #     thread.start()

    #     # 等待线程结束
    #     thread.wait()

    def show_pro_tree(self):
        """
        在self.ui.view中展示进程树
        """
        model = QStandardItemModel()
        # 设置表头
        header_labels = ["PID", "进程名称", "状态", "内存占用率", "运行时间"]
        model.setHorizontalHeaderLabels(header_labels)
        # 获取到进程的数据
        # pro_tree = Tree()
        pro_tree = self.system.os.get_process_tree()
        node_list = pro_tree.all_nodes()
        cnt = 0
        for item in node_list:
            # 判断是不是父节点
            if pro_tree.children(item.identifier):
                # 创建父节点并添加到模型中
                mem_rate = item.data.code_size
                root_item = model.invisibleRootItem()
                root_item.appendRow([QStandardItem(str(item.data.PID)), QStandardItem(item.data.name)
                                     , QStandardItem(item.data.state), QStandardItem(str(mem_rate)),
                                     QStandardItem(str(item.data.total_time))])
                # 将子节点全部放入父节点下
                children_list = pro_tree.children(item.identifier)
                for child in children_list:
                    child_mem_rate = child.data.code_size
                    child_item = root_item.child(cnt)
                    child_item.appendRow([QStandardItem(str(child.data.PID)), QStandardItem(child.data.name)
                                     , QStandardItem(child.data.state), QStandardItem(str(child_mem_rate)),
                                     QStandardItem(str(child.data.total_time))])
                # 父节点数量    
                cnt += 1
        
        self.ui.view.setModel(model)
                

    def show_ganter(self):
        self.view = GanttChartView(self.system.os)
        self.view.show()

    def create_process(self):
        """
        创建进程槽函数
        """
        # 获取基址、上限、代码大小
        # base = self.ui.BaseEdit.text()
        # limit = self.ui.LimitEdit.text()
        # size = self.ui.SizeEdit.text()
        name = self.ui.NameEdit.text()
        # self.os.create_process()
        instructions = ["00000001", "01010000", "10000000","00000000","00000001","00010000","00000000","00000011",
                    "00000001", "01010001", "00000000","00000000","00000001","00010000","00000000","00001100",
                    "00000010", "00010101", "00000000","00000000","00000000","00000000","00000000","00000000"]
        id_generator = self.system.container.resolve("id_generator")
        self.system.container.resolve("memory").load_program(id_generator.create_id(), instructions)
        # print("aaa666")
        self.system.os.create_process(name, 0)
        self.show_pro_tree()


    def stop_process(self):
        """
        终止进程槽函数
        """
        selected_row = self.ui.view.selectionModel().selectedRows()
        # aa = selected_row[0].data()
        # print("666")
        self.system.os.del_process(int(selected_row[0].data()))
        self.show_pro_tree()


# # 自定义线程类
# class MyThread(QThread):
#     def run(self):
#         self.view = GanttChartView()
#         self.view.show()


if __name__ == "__main__":
    app = QApplication([])
    window = ProcessUI()
    window.window.show()
    
    app.exec()