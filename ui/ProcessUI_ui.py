# Form implementation generated from reading ui file 'c:\Users\13287\Documents\GitHub\os_lab\ui\ProcessUI.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 600)
        self.TableView = TableView(parent=Form)
        self.TableView.setGeometry(QtCore.QRect(0, 0, 600, 600))
        self.TableView.setObjectName("TableView")
        self.widget = QtWidgets.QWidget(parent=Form)
        self.widget.setGeometry(QtCore.QRect(650, 90, 130, 401))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(parent=self.widget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.BaseEdit = LineEdit(parent=self.widget)
        self.BaseEdit.setObjectName("BaseEdit")
        self.verticalLayout.addWidget(self.BaseEdit)
        self.label_2 = QtWidgets.QLabel(parent=self.widget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.LimitEdit = LineEdit(parent=self.widget)
        self.LimitEdit.setObjectName("LimitEdit")
        self.verticalLayout.addWidget(self.LimitEdit)
        self.label_3 = QtWidgets.QLabel(parent=self.widget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.SizeEdit = LineEdit(parent=self.widget)
        self.SizeEdit.setObjectName("SizeEdit")
        self.verticalLayout.addWidget(self.SizeEdit)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.CreateProButton = PushButton(parent=self.widget)
        self.CreateProButton.setObjectName("CreateProButton")
        self.verticalLayout.addWidget(self.CreateProButton)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.StopProButton = PushButton(parent=self.widget)
        self.StopProButton.setObjectName("StopProButton")
        self.verticalLayout.addWidget(self.StopProButton)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.ViewButton = PushButton(parent=self.widget)
        self.ViewButton.setObjectName("ViewButton")
        self.verticalLayout.addWidget(self.ViewButton)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "基址:"))
        self.label_2.setText(_translate("Form", "上限:"))
        self.label_3.setText(_translate("Form", "代码大小:"))
        self.CreateProButton.setText(_translate("Form", "创建进程"))
        self.StopProButton.setText(_translate("Form", "终止进程"))
        self.ViewButton.setText(_translate("Form", "查看进程并发"))
from qfluentwidgets import LineEdit, PushButton, TableView
