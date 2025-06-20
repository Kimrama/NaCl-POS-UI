import sys

from PyQt6.QtCore import QCoreApplication, QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QPushButton, QHBoxLayout, QVBoxLayout

from ui.default_page import DefaultPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NaCl POS")
        self.setWindowIcon(QIcon("assets/ncal_logo32x32.png"))

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # when using in rasPi4
        # window.showFullScreen()   

        self.setFixedSize(QSize(600, 1024))


        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # page
        self.default_page = DefaultPage(self)

        # add page to stack
        self.stack.addWidget(self.default_page)

        self.goto_default()

    def goto_default(self):
        self.stack.setCurrentWidget(self.default_page)

    def goto_list(self):
        from ui.list_page import ListPage
        self.list_page = ListPage(self)
        self.stack.addWidget(self.list_page)
        self.stack.setCurrentWidget(self.list_page)

    def goto_qrcode(self, total_price: float):
        from ui.qrcode_page import QRCodePage
        self.qrcode_page = QRCodePage(self, total_price)
        self.stack.addWidget(self.qrcode_page)
        self.stack.setCurrentWidget(self.qrcode_page)

    def goto_complete(self):
        from ui.complete_page import CompletePage
        self.complete_page = CompletePage(self)
        self.stack.addWidget(self.complete_page)
        self.stack.setCurrentWidget(self.complete_page)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
