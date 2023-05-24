from PyQt6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PyQt6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PyQt6.QtWidgets import (QApplication, QHeaderView, QSizePolicy, QTableWidget,
    QTableWidgetItem, QWidget)

class Ui_MemoryViewer(object):
    def setupUi(self, MemoryViewer):
        if not MemoryViewer.objectName():
            MemoryViewer.setObjectName(u"MemoryViewer")
        MemoryViewer.resize(500, 500)
        self.MemoryList = QTableWidget(MemoryViewer)
        if (self.MemoryList.columnCount() < 16):
            self.MemoryList.setColumnCount(16)
        if (self.MemoryList.rowCount() < 16):
            self.MemoryList.setRowCount(16)
        self.MemoryList.setObjectName(u"MemoryList")
        self.MemoryList.setGeometry(QRect(0, 0, 500, 500))
        self.MemoryList.setRowCount(16)
        self.MemoryList.setColumnCount(16)
        # 设置格子的大小
        cell_size = 28  # 设置每个格子的大小
        
        # 设置行高和列宽
        for i in range(self.MemoryList.rowCount()):
            self.MemoryList.setRowHeight(i, cell_size)
        
        for j in range(self.MemoryList.columnCount()):
            self.MemoryList.setColumnWidth(j, cell_size)

        self.retranslateUi(MemoryViewer)

        QMetaObject.connectSlotsByName(MemoryViewer)
    # setupUi

    def retranslateUi(self, MemoryViewer):
        MemoryViewer.setWindowTitle(QCoreApplication.translate("MemoryViewer", u"Form", None))
    # retranslateUi



class MemoryUI():
    def __init__(self) -> None:
        self.window = QWidget()
        self.ui = Ui_MemoryViewer()
        self.ui.setupUi(self.window)

if __name__ == "__main__":
    app = QApplication([])
    window = MemoryUI()
    window.window.show()
    
    app.exec()