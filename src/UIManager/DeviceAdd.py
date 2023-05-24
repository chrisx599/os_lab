# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DeviceAddoMPSKw.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

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
        self.LineEdit = LineEdit(DeviceAdd)
        self.LineEdit.setObjectName(u"LineEdit")
        self.LineEdit.setGeometry(QRect(140, 70, 128, 33))
        self.LineEdit_2 = LineEdit(DeviceAdd)
        self.LineEdit_2.setObjectName(u"LineEdit_2")
        self.LineEdit_2.setGeometry(QRect(140, 140, 128, 33))
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

        self.TrueAddButton.clicked.connect()
        self.NotAddButton.clicked.connect()

    def retranslateUi(self, DeviceAdd):
        DeviceAdd.setWindowTitle(QCoreApplication.translate("DeviceAdd", u"Form", None))
        self.TrueAddButton.setText(QCoreApplication.translate("DeviceAdd", u"\u786e\u8ba4\u6dfb\u52a0", None))
        self.DevTypelabel.setText(QCoreApplication.translate("DeviceAdd", u"\u8bbe\u5907\u7c7b\u578b", None))
        self.DevIDlabel.setText(QCoreApplication.translate("DeviceAdd", u"\u8bbe\u5907ID", None))
        self.NotAddButton.setText(QCoreApplication.translate("DeviceAdd", u"\u53d6\u6d88\u6dfb\u52a0", None))
    # retranslateUi

if __name__ == "__main__":
    app = QApplication([])
    window = QWidget()
    ui = Ui_DeviceAdd()
    ui.setupUi(window)
    window.show()
    
    app.exec()
