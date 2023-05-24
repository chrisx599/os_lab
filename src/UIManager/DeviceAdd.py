"""
添加设备窗口界面
"""

from PyQt6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PyQt6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PyQt6.QtWidgets import (QApplication, QLabel, QSizePolicy, QWidget)

from qfluentwidgets import (LineEdit, PushButton)

class Ui_DeviceAdd(object):
    def setupUi(self, DeviceAdd):
        if not DeviceAdd.objectName():
            DeviceAdd.setObjectName(u"DeviceAdd")
        DeviceAdd.resize(400, 300)
        self.TrueAddButton = PushButton(DeviceAdd)
        self.TrueAddButton.setObjectName(u"TrueAddButton")
        self.TrueAddButton.setGeometry(QRect(80, 220, 102, 32))
        self.DevTypeEdit = LineEdit(DeviceAdd)
        self.DevTypeEdit.setObjectName(u"LineEdit")
        self.DevTypeEdit.setGeometry(QRect(140, 70, 128, 33))
        self.DevIDEdit = LineEdit(DeviceAdd)
        self.DevIDEdit.setObjectName(u"LineEdit_2")
        self.DevIDEdit.setGeometry(QRect(140, 140, 128, 33))
        self.DevTypelabel = QLabel(DeviceAdd)
        self.DevTypelabel.setObjectName(u"DevTypelabel")
        self.DevTypelabel.setGeometry(QRect(70, 80, 71, 20))
        self.DevIDlabel = QLabel(DeviceAdd)
        self.DevIDlabel.setObjectName(u"DevIDlabel")
        self.DevIDlabel.setGeometry(QRect(80, 150, 41, 16))
        self.NotAddButton = PushButton(DeviceAdd)
        self.NotAddButton.setObjectName(u"NotAddButton")
        self.NotAddButton.setGeometry(QRect(220, 220, 102, 32))

        self.retranslateUi(DeviceAdd)

        QMetaObject.connectSlotsByName(DeviceAdd)


    def retranslateUi(self, DeviceAdd):
        DeviceAdd.setWindowTitle(QCoreApplication.translate("DeviceAdd", u"Form", None))
        self.TrueAddButton.setText(QCoreApplication.translate("DeviceAdd", u"\u786e\u8ba4\u6dfb\u52a0", None))
        self.DevTypelabel.setText(QCoreApplication.translate("DeviceAdd", u"\u8bbe\u5907\u7c7b\u578b", None))
        self.DevIDlabel.setText(QCoreApplication.translate("DeviceAdd", u"\u8bbe\u5907ID", None))
        self.NotAddButton.setText(QCoreApplication.translate("DeviceAdd", u"\u53d6\u6d88\u6dfb\u52a0", None))
    # retranslateUi

class DeviceAdd():
    def __init__(self) -> None:
        super().__init__()
        self.window = QWidget()
        self.ui = Ui_DeviceAdd()
        self.ui.setupUi(self.window)

        self.signal()

    def signal(self):
        self.ui.TrueAddButton.clicked.connect(self.true_add)
        self.ui.NotAddButton.clicked.connect(self.not_add)

    def true_add(self):
        dev_type = self.ui.DevTypeEdit.text()
        dev_id = self.ui.DevIDEdit.text()
        print(dev_type, dev_id)

    def not_add(self):
        self.window.close()
    

if __name__ == "__main__":
    app = QApplication([])
    window = DeviceAdd()
    window.window.show()
    
    app.exec()
