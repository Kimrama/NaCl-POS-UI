import sys

from PyQt6.QtCore import QCoreApplication, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QStackedWidget, QPushButton, QHBoxLayout, QVBoxLayout

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NaCl POS")
        self.setWindowIcon(QIcon("assets/ncal_logo32x32.png"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
