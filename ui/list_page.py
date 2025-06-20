from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QFrame, QScrollArea
)
from PyQt6.QtGui import QColor, QPalette, QPixmap
from PyQt6.QtCore import Qt, QTimer


class ListPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # ========== State ==========
        self.remaining_time = 3 * 60
        self.products = [
            {"name": "น้ำเปล่าขวดเล็ก", "qty": 1, "price": 5.00},
            {"name": "โค้กกระป๋อง", "qty": 2, "price": 14.00},

        ]

        # ========== UI Setup ==========
        self.setup_background()
        self.setup_timer()
        self.init_ui()

        # ========== Load Products ==========
        self.update_product_list()

    # ------------------------------
    # UI Initialization
    # ------------------------------

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

        self_checkout = QLabel("Self - Checkout")
        self_checkout.setStyleSheet("font-size: 48px; font-weight: bold; color: white; margin-bottom: 26px;")

        top_layout = QVBoxLayout()
        top_layout.addWidget(logo, alignment=Qt.AlignmentFlag.AlignRight)
        top_layout.addWidget(self_checkout)

        # === White Container ===
        white_container = QFrame()
        white_container.setFixedSize(550, 710)
        white_container.setStyleSheet("background-color: white; border-radius: 16px;")
        white_container_layout = QVBoxLayout()
        white_container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Header (Cart + Timer)
        cart_label = QLabel("Cart")
        cart_label.setStyleSheet("font-size: 36px; font-weight: bold; color: black;")

        self.timer_label = QLabel("3:00")
        self.timer_label.setStyleSheet("""
            background-color: #FF862F;
            border-radius: 16px;
            font-size: 20px;
            padding: 4px 20px;
            color: white;
        """)

        header_layout = QHBoxLayout()
        header_layout.addSpacing(8)
        header_layout.addWidget(cart_label)
        header_layout.addStretch()
        header_layout.addWidget(self.timer_label)

        # Column Headers
        col_header_layout = QHBoxLayout()
        product_col = QLabel("Product")
        quantity_col = QLabel("Quantity")
        price_col = QLabel("Price")

        for label in [product_col, quantity_col, price_col]:
            label.setStyleSheet("font-size: 24px; font-weight: bold; color: black;")

        col_header_layout.addSpacing(8)
        col_header_layout.addWidget(product_col)
        col_header_layout.addStretch()
        col_header_layout.addWidget(quantity_col)
        col_header_layout.addSpacing(35)
        col_header_layout.addWidget(price_col)
        col_header_layout.addSpacing(8)

        # Product Area
        self.no_product_label = QLabel("Add product by using barcode scanner")
        self.no_product_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.no_product_label.setStyleSheet("font-size: 20px; color: black; margin-top: 12px;")

        self.product_list_layout = QVBoxLayout()

        # Total Label
        self.total_label = QLabel("Total: 0.00")
        self.total_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.total_label.setStyleSheet("font-size: 28px; font-weight: bold; color: black; margin-top: 12px;")

        # Add to container
        white_container_layout.addLayout(header_layout)
        white_container_layout.addLayout(col_header_layout)
        white_container_layout.addWidget(self.no_product_label)
        white_container_layout.addLayout(self.product_list_layout)
        white_container_layout.addStretch()
        white_container_layout.addWidget(self.total_label)
        white_container.setLayout(white_container_layout)

        # === Bottom Buttons ===
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            font-size: 24px;
            padding: 12px;
            width: 100px;
            color: #5E5E5E;
            background-color: white;
            border-radius: 24px;
        """)
        cancel_btn.clicked.connect(self.main_window.goto_default)

        pay_btn = QPushButton("Pay")
        pay_btn.setStyleSheet("""
            font-size: 24px;
            padding: 12px;
            width: 100px;
            background-color: #27AE61;
            border-radius: 24px;
            color: white;
        """)
        pay_btn.clicked.connect(self.handle_pay)

        btn_layout = QHBoxLayout()
        btn_layout.addSpacing(8)
        btn_layout.addWidget(cancel_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(pay_btn)
        btn_layout.addSpacing(8)

        # === Main Layout ===
        center_layout = QVBoxLayout()
        center_layout.addWidget(white_container, alignment=Qt.AlignmentFlag.AlignHCenter)
        center_layout.addStretch()

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(center_layout)
        main_layout.addLayout(btn_layout)
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

    # ------------------------------
    # Product Logic
    # ------------------------------

    def update_product_list(self):
        self.clear_layout(self.product_list_layout)
        total = 0.0

        if not self.products:
            self.no_product_label.show()
        else:
            self.no_product_label.hide()
            for product in self.products:
                row = self.create_product_row(product["name"], product["qty"], product["price"])
                self.product_list_layout.addLayout(row)

                divider = QFrame()
                divider.setFrameShape(QFrame.Shape.HLine)
                divider.setFrameShadow(QFrame.Shadow.Plain)
                divider.setStyleSheet("color: #DADADA; background-color: #DADADA;")
                divider.setFixedHeight(1)
                self.product_list_layout.addWidget(divider)

                total += product["qty"] * product["price"]

        self.total_label.setText(f"Total: {total:.2f}")
    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())
    def create_product_row(self, name, qty, price):
        layout = QHBoxLayout()

        name_label = QLabel(name)
        name_label.setStyleSheet("font-size: 16px; color: black;")

        # Quantity controls
        qty_layout = QHBoxLayout()

        minus_btn = QPushButton("-")
        minus_btn.setFixedSize(30, 30)
        minus_btn.setStyleSheet(
            "font-size: 16px; text-align: center; background-color: #EF5350; color: white; border-radius: 15px;")

        plus_btn = QPushButton("+")
        plus_btn.setFixedSize(30, 30)
        plus_btn.setStyleSheet(
            "font-size: 16px; text-align: center; background-color: #4CAF50; color: white; border-radius: 15px;")

        qty_label = QLabel(str(qty))
        qty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        qty_label.setFixedWidth(20)
        qty_label.setStyleSheet("font-size: 16px; color: black;")

        minus_btn.clicked.connect(lambda _, n=name: self.change_quantity_by_name(n, -1))
        plus_btn.clicked.connect(lambda _, n=name: self.change_quantity_by_name(n, +1))

        qty_layout.addWidget(minus_btn)
        qty_layout.addWidget(qty_label)
        qty_layout.addWidget(plus_btn)

        price_label = QLabel(f"{price:.2f}")
        price_label.setFixedWidth(50)
        price_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        price_label.setStyleSheet("font-size: 16px; color: black;")

        layout.addSpacing(8)
        layout.addWidget(name_label)
        layout.addStretch()
        layout.addLayout(qty_layout)
        layout.addSpacing(45)
        layout.addWidget(price_label)
        layout.addSpacing(8)

        return layout
    def change_quantity_by_name(self, name: str, delta: int):

        for i, product in enumerate(self.products):
            if product["name"] == name:
                new_qty = product["qty"] + delta
                if new_qty >= 1:
                    self.products[i]["qty"] = new_qty
                else:
                    del self.products[i]
                break
        self.update_product_list()

    
    def change_quantity(self, index: int, delta: int):
        product = self.products[index]
        new_qty = product["qty"] + delta

        if new_qty >= 1:
            self.products[index]["qty"] = new_qty
        elif new_qty <= 0:
            del self.products[index] 

        self.update_product_list()

    def handle_pay(self):
        total = sum(p["qty"] * p["price"] for p in self.products)
        self.main_window.goto_qrcode(total)