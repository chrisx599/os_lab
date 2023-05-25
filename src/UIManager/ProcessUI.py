"""
Writen by Liang Zhengyang
"""
from PyQt6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect, QThread,
    QSize, QTime, QUrl, Qt)
from PyQt6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon, QFileSystemModel,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PyQt6.QtWidgets import (QApplication, QHeaderView, QLabel, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget, QHBoxLayout)

from qfluentwidgets import (LineEdit, PushButton, TableView, TreeView)
from ProcessGanter import GanttChartView
from OS import OS
import threading

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

        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.BaseEdit = LineEdit(self.widget)
        self.BaseEdit.setObjectName(u"BaseEdit")

        self.verticalLayout.addWidget(self.BaseEdit)

        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.LimitEdit = LineEdit(self.widget)
        self.LimitEdit.setObjectName(u"LimitEdit")

        self.verticalLayout.addWidget(self.LimitEdit)

        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)

        self.SizeEdit = LineEdit(self.widget)
        self.SizeEdit.setObjectName(u"SizeEdit")

        self.verticalLayout.addWidget(self.SizeEdit)

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


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u57fa\u5740:", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u4e0a\u9650:", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u4ee3\u7801\u5927\u5c0f:", None))
        self.CreateProButton.setText(QCoreApplication.translate("Form", u"\u521b\u5efa\u8fdb\u7a0b", None))
        self.StopProButton.setText(QCoreApplication.translate("Form", u"\u7ec8\u6b62\u8fdb\u7a0b", None))
        self.ViewButton.setText(QCoreApplication.translate("Form", u"\u67e5\u770b\u8fdb\u7a0b\u5e76\u53d1", None))
    # retranslateUi



class ProcessUI():
    def __init__(self) -> None:
        self.window = QWidget()
        self.ui = Ui_Form()
        self.ui.setupUi(self.window)

        self.signal()

    def signal(self):
        self.ui.ViewButton.clicked.connect(self.show_ganter)
        self.ui.CreateProButton.clicked.connect(self.create_process)
        self.ui.StopProButton.clicked.connect(self.stop_process)

    def show_ganter_thread(self):
        # 创建新线程对象
        # thread = MyThread()
        # # 启动线程
        # thread.start()
        # # 等待线程结束
        # thread.wait()

        # 创建新线程对象
        thread = QThread()

        # 设置自定义线程类为线程对象的父类
        my_thread = MyThread()
        my_thread.moveToThread(thread)

        # 连接启动信号和槽函数
        thread.started.connect(my_thread.run)
        # 启动线程
        thread.start()

        # 等待线程结束
        thread.wait()

    def show_pro_tree(self):
        """
        在self.ui.view中展示进程树
        """
        # 获取到进程的数据


    def show_ganter(self):
        self.view = GanttChartView()
        self.view.show()

    def create_process(self):
        """
        创建进程槽函数
        """
        # 获取基址、上限、代码大小
        base = self.ui.BaseEdit.text()
        limit = self.ui.LimitEdit.text()
        size = self.ui.SizeEdit.text()
        pass

    def stop_process(self):
        """
        终止进程槽函数
        """
        pass


# 自定义线程类
class MyThread(QThread):
    def run(self):
        self.view = GanttChartView()
        self.view.show()


if __name__ == "__main__":
    app = QApplication([])
    window = ProcessUI()
    window.window.show()
    
    app.exec()