from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame, QHBoxLayout, QPushButton
from PyQt6.QtGui import QColor, QPalette, QPixmap
from PyQt6.QtCore import Qt, QTimer

class CompletePage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # ========== State ==========
        self.remaining_time = 5

        self.setup_background()
        self.init_ui()
        self.setup_timer()

    def setup_background(self):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#60C7FF"))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

    def init_ui(self):
        # === Top Banner ===
        logo = QLabel()
        logo.setPixmap(QPixmap("assets/ncal_logo_white_transparent.png").scaledToWidth(80))
        logo.setAlignment(Qt.AlignmentFlag.AlignRight)

        top_layout = QVBoxLayout()
        top_layout.addWidget(logo, alignment=Qt.AlignmentFlag.AlignRight)

        # === check ===
        check_label = QLabel()
        logo_pixmap = QPixmap("assets/check.png").scaledToWidth(
            380, Qt.TransformationMode.SmoothTransformation
        )
        check_label.setPixmap(logo_pixmap)
        check_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # === payment complete
        payment_complete_label = QLabel("Payment Completed")
        payment_complete_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        payment_complete_label.setStyleSheet("color: black; font-size: 35px; font-weight: bold;")

        # === continue shopping btn ===
        continue_shopping_btn = QPushButton("Continue Shopping")
        continue_shopping_btn.setStyleSheet("background-color: #27AE61; font-size: 24px; border-radius: 16px;")
        continue_shopping_btn.setFixedWidth(320)
        continue_shopping_btn.setFixedHeight(64)

        continue_shopping_btn.clicked.connect(self.continue_shopping_handle)

        # === timer ===
        self.timer_label = QLabel("<return to menu in 5>")
        self.timer_label.setStyleSheet("""
            border-radius: 16px;
            font-size: 20px;
            padding: 4px 20px;
            color: black;
        """)
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # === White Container ===
        white_container = QFrame()
        white_container.setFixedSize(500, 710)
        white_container.setStyleSheet("background-color: white; border-radius: 16px; ")
        white_container_layout = QVBoxLayout()
        white_container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        


        # Add to container
        white_container.setLayout(white_container_layout)
        white_container_layout.addSpacing(80)
        white_container_layout.addWidget(check_label)
        white_container_layout.addStretch()
        white_container_layout.addWidget(payment_complete_label)
        white_container_layout.addStretch()
        white_container_layout.addWidget(continue_shopping_btn, alignment=Qt.AlignmentFlag.AlignHCenter)
        white_container_layout.addWidget(self.timer_label)


        # === Main Layout ===
        center_layout = QVBoxLayout()
        center_layout.addStretch()
        center_layout.addWidget(white_container, alignment=Qt.AlignmentFlag.AlignHCenter)
        center_layout.addStretch()


        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(center_layout)
        self.setLayout(main_layout)

    # ------------------------------
    # Timer Handling
    # ------------------------------

    def continue_shopping_handle(self):
        self.timer.stop()
        self.main_window.goto_list()

    def setup_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

    def update_timer(self):
        self.remaining_time -= 1
        if self.remaining_time <= 0:
            self.timer.stop()
            self.main_window.goto_default()
            return

        seconds = self.remaining_time % 60
        self.timer_label.setText(f"<return to menu in {seconds}>")
