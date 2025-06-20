from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame, QHBoxLayout, QPushButton
from PyQt6.QtGui import QColor, QPalette, QPixmap
from PyQt6.QtCore import Qt, QTimer

class QRCodePage(QWidget):
    def __init__(self, main_window, total_price: float):
        super().__init__()
        self.main_window = main_window
        self.total_price = total_price

        # ========== State ==========
        self.remaining_time = 2 * 60

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

        # === PromptPay ===
        self.promptpay_label = QLabel()
        promptpay_pixmap = QPixmap("assets/promptpay-logo.jpg").scaledToWidth(
            420, Qt.TransformationMode.SmoothTransformation
        )
        self.promptpay_label.setPixmap(promptpay_pixmap)
        self.promptpay_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # === timer ===
        self.timer_label = QLabel("2:00")
        self.timer_label.setStyleSheet("""
            background-color: #FF862F;
            border-radius: 16px;
            font-size: 20px;
            padding: 4px 20px;
            color: white;
        """)
        

        timer_line_layout = QHBoxLayout()
        timer_line_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        timer_line_layout.addWidget(self.timer_label)
        timer_line_layout.addSpacing(8)

        # === qrcode ===
        qrcode_label = QLabel()
        qrcode_label.setPixmap(QPixmap("assets/mock_qrcode.png").scaledToWidth(385))
        qrcode_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # === detail ===
        price_label = QLabel(f"{self.total_price:.2f} THB")
        price_label.setStyleSheet("font-size: 36px; color: #1677FF; font-weight: bold;")
        price_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        nacl_shop_label = QLabel("เน็ตเวิร์ค ช็อป")
        nacl_shop_label.setStyleSheet("font-size: 20px; color: #000000; font-weight: bold;")
        nacl_shop_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        account_name = QLabel("ชื่อบัญชี: Mr. Kimrama Dev")
        account_name.setStyleSheet("font-size: 16px; color: #000000;")
        account_name.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        shop_id = QLabel("รหัสร้านค้า: 1411043011075790606")
        shop_id.setStyleSheet("font-size: 16px; color: #000000;")
        shop_id.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        detail_layout = QVBoxLayout()
        detail_layout.addWidget(price_label)
        detail_layout.addWidget(nacl_shop_label)
        detail_layout.addWidget(account_name)
        detail_layout.addWidget(shop_id)

        # === Bottom Buttons ===
        confirm_payment_btn = QPushButton("Confirm Payment")
        confirm_payment_btn.setFixedWidth(500)
        confirm_payment_btn.setFixedHeight(70)
        confirm_payment_btn.setStyleSheet("font-size: 24px; background-color: #27AE61; border-radius: 16px;")

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedWidth(500)
        cancel_btn.setFixedHeight(55)
        cancel_btn.setStyleSheet("font-size: 24px; color: #5E5E5E; background-color: white; border-radius: 16px;")

        cancel_btn.clicked.connect(self.main_window.goto_default)

        # === White Container ===
        white_container = QFrame()
        white_container.setFixedSize(500, 710)
        white_container.setStyleSheet("background-color: white; border-radius: 16px; ")
        white_container_layout = QVBoxLayout()
        white_container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)


        # Add to container
        white_container.setLayout(white_container_layout)
        white_container_layout.addSpacing(8)
        white_container_layout.addWidget(self.promptpay_label)
        white_container_layout.addLayout(timer_line_layout)
        white_container_layout.addSpacing(8)
        white_container_layout.addWidget(qrcode_label)
        white_container_layout.addSpacing(8)
        white_container_layout.addLayout(detail_layout)

        # === Main Layout ===
        center_layout = QVBoxLayout()
        center_layout.addStretch()
        center_layout.addWidget(white_container, alignment=Qt.AlignmentFlag.AlignHCenter)
        center_layout.addStretch()
        center_layout.addWidget(confirm_payment_btn, alignment=Qt.AlignmentFlag.AlignHCenter)
        center_layout.addSpacing(10)
        center_layout.addWidget(cancel_btn, alignment=Qt.AlignmentFlag.AlignHCenter)
        center_layout.addSpacing(10)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(center_layout)
        self.setLayout(main_layout)

    # ------------------------------
    # Timer Handling
    # ------------------------------

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

        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        self.timer_label.setText(f"{minutes}:{seconds:02d}")
