from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class QRCodePage(QWidget):
    def __init__(self, main_window, total_price: float):
        super().__init__()
        self.main_window = main_window
        self.total_price = total_price

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        total_label = QLabel(f"Total to pay: {self.total_price:.2f} THB")
        layout.addWidget(total_label)
        self.setLayout(layout)
