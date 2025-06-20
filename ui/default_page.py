from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class DefaultPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout()
        label = QLabel("Welcome to POS System")
        button = QPushButton("ไปยังหน้ารายการสินค้า")
        button.clicked.connect(self.main_window.goto_list)

        layout.addWidget(label)
        layout.addWidget(button)
        self.setLayout(layout)
