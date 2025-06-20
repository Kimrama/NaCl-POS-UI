from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSpacerItem,
    QSizePolicy, QGraphicsOpacityEffect, QFrame, QPushButton
)
from PyQt6.QtGui import QColor, QPalette, QPixmap
from PyQt6.QtCore import Qt, QTimer  

class ListPage(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        self.remaining_time = 30

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#60C7FF"))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        image_label = QLabel()
        pixmap = QPixmap("assets/ncal_logo_white_transparent.png")
        pixmap = pixmap.scaledToWidth(80, Qt.TransformationMode.SmoothTransformation)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)

        logo_line_layout = QHBoxLayout()
        logo_line_layout.addWidget(image_label)

        self_checkout = QLabel("Self - Checkout")
        self_checkout.setStyleSheet("font-size: 48px; font-weight: bold; color: white; margin-left: 8px; margin-bottom: 26px;")
        
        top_layout = QVBoxLayout()
        top_layout.addLayout(logo_line_layout)
        top_layout.addWidget(self_checkout)

        white_container = QFrame()
        white_container.setFixedSize(550, 710)
        white_container.setStyleSheet("background-color: white; border-radius: 16px;")

        white_container_layout = QVBoxLayout()
        white_container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        container_header_layout = QHBoxLayout()
        cart = QLabel("Cart")
        cart.setStyleSheet('''
                            font-size: 36px;
                            font-weight: bold;
                            color: black;
                            margin-left: 8px;
                            ''')
        
        self.timer_label = QLabel("5.00")
        self.timer_label.setStyleSheet('''
                            background-color: #FF862F; 
                            border-radius: 16px;
                            font-size: 20px;
                            padding: 4px 20px;
                            ''')

        container_header_layout.addWidget(cart)
        container_header_layout.addStretch()
        container_header_layout.addWidget(self.timer_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)
        
        white_container_layout.addLayout(container_header_layout)
        white_container.setLayout(white_container_layout)

        center_layout = QVBoxLayout()
        center_layout.addWidget(white_container, alignment=Qt.AlignmentFlag.AlignHCenter)
        center_layout.addStretch()

        button_layout = QHBoxLayout()

        cancel = QPushButton("Cancel")
        cancel.setStyleSheet('''
                            font-size: 24px;
                            padding: 12px;
                            width: 100px;
                            color: #5E5E5E;
                            background-color: white;
                            border-radius: 24px;
                            text-align: center;
                            margin-left: 8px;
                             ''')
        cancel.clicked.connect(self.main_window.goto_default)

        pay = QPushButton("Pay")
        pay.setStyleSheet('''
                            font-size: 24px;
                            padding: 12px;
                            width: 100px;
                            background-color: #27AE61;
                            border-radius: 24px;
                            text-align: center;
                            margin-right: 8px;
                             ''')

        button_layout.addWidget(cancel)
        button_layout.addStretch()
        button_layout.addWidget(pay)
        

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(center_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def update_timer(self):
        self.remaining_time -= 1

        if self.remaining_time <= 0:
            self.timer.stop()
            self.main_window.goto_default()
            return

        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        self.timer_label.setText(f"{minutes}:{seconds:02d}")
