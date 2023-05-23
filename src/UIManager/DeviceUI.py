from PyQt6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PyQt6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PyQt6.QtWidgets import (QApplication, QSizePolicy, QWidget)

from qfluentwidgets import (ListView, PushButton)

class Ui_DeviceManager(object):
    def setupUi(self, DeviceManager):
        if not DeviceManager.objectName():
            DeviceManager.setObjectName(u"DeviceManager")
        DeviceManager.resize(500, 600)
        self.DeviceList = ListView(DeviceManager)
        self.DeviceList.setObjectName(u"DeviceList")
        self.DeviceList.setGeometry(QRect(0, 0, 500, 550))
        self.AddDeviceButton = PushButton(DeviceManager)
        self.AddDeviceButton.setObjectName(u"AddDeviceButton")
        self.AddDeviceButton.setGeometry(QRect(90, 560, 102, 32))
        self.DelDeviceButton = PushButton(DeviceManager)
        self.DelDeviceButton.setObjectName(u"DelDeviceButton")
        self.DelDeviceButton.setGeometry(QRect(290, 560, 102, 32))

        self.retranslateUi(DeviceManager)

        QMetaObject.connectSlotsByName(DeviceManager)
    # setupUi

    def retranslateUi(self, DeviceManager):
        DeviceManager.setWindowTitle(QCoreApplication.translate("DeviceManager", u"Form", None))
        self.AddDeviceButton.setText(QCoreApplication.translate("DeviceManager", u"\u6dfb\u52a0\u8bbe\u5907", None))
        self.DelDeviceButton.setText(QCoreApplication.translate("DeviceManager", u"\u5220\u9664\u8bbe\u5907", None))
    # retranslateUi

    def add_device(self):
        pass

    def del_device(self):
        pass

    def show_device(self):
        pass

if __name__ == "__main__":
    app = QApplication([])
    window = QWidget()
    ui = Ui_DeviceManager()
    ui.setupUi(window)
    window.show()
    
    app.exec()