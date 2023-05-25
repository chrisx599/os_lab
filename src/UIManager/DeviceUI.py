"""
Writen by Liang Zhengyang
Device界面
包括Device界面中的信号与槽的全部定义设置
"""

from PyQt6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect, 
    QSize, QTime, QUrl, Qt)
from PyQt6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QStandardItemModel,
    QFont, QFontDatabase, QGradient, QIcon, QStandardItem,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PyQt6.QtWidgets import (QApplication, QSizePolicy, QWidget, QTableView, QHeaderView,
                             QVBoxLayout)


from qfluentwidgets import (ListView, PushButton, TableView)

from DeviceAdd import DeviceAdd


class Ui_DeviceManager(object):
    def setupUi(self, DeviceManager):
        if not DeviceManager.objectName():
            DeviceManager.setObjectName(u"DeviceManager")
        DeviceManager.resize(500, 600)
        self.AddDeviceButton = PushButton(DeviceManager)
        self.AddDeviceButton.setObjectName(u"AddDeviceButton")
        self.AddDeviceButton.setGeometry(QRect(90, 560, 102, 32))
        self.DelDeviceButton = PushButton(DeviceManager)
        self.DelDeviceButton.setObjectName(u"DelDeviceButton")
        self.DelDeviceButton.setGeometry(QRect(290, 560, 102, 32))
        self.TableView = TableView(DeviceManager)
        self.TableView.setObjectName(u"TableView")
        self.TableView.setGeometry(QRect(0, 0, 500, 550))

        self.retranslateUi(DeviceManager)

        QMetaObject.connectSlotsByName(DeviceManager)
    # setupUi

    def retranslateUi(self, DeviceManager):
        DeviceManager.setWindowTitle(QCoreApplication.translate("DeviceManager", u"Form", None))
        self.AddDeviceButton.setText(QCoreApplication.translate("DeviceManager", u"\u6dfb\u52a0\u8bbe\u5907", None))
        self.DelDeviceButton.setText(QCoreApplication.translate("DeviceManager", u"\u5220\u9664\u8bbe\u5907", None))
    # retranslateUi


class DeviceManager():
    def __init__(self, device_st) -> None:
        self.window = QWidget()
        self.ui = Ui_DeviceManager()
        self.ui.setupUi(self.window)
        self.device_st = device_st

        self.signal()

        self.show_device()

    def signal(self):
        self.ui.AddDeviceButton.clicked.connect(self.add_device)
        self.ui.DelDeviceButton.clicked.connect(self.del_device)

    def add_device(self):
        self.dev_add = DeviceAdd(self)
        self.dev_add.window.show()

    def del_device(self):
        selected_row = self.ui.TableView.selectionModel().selectedRows()
        self.device_st.del_dev(int(selected_row[0].data()))
        self.show_device()


    def show_device(self):
        # 创建 QStandardItemModel 模型
        model = QStandardItemModel()

        # 设置表头
        header_labels = ["编号", "类型", "状态"]
        model.setHorizontalHeaderLabels(header_labels)

        # 添加数据行
        for key in self.device_st.table.keys():
            items = [QStandardItem(item) for item in [str(key), self.device_st.table[key].dev_type
                                     , self.device_st.table[key].status]]
            model.appendRow(items)
            
        self.ui.TableView.setModel(model)

if __name__ == "__main__":
    app = QApplication([])
    window = DeviceManager()
    window.window.show()
    
    app.exec()