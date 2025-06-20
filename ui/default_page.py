from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGraphicsOpacityEffect
from PyQt6.QtGui import QColor, QPalette, QPixmap
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve


class DefaultPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.set_background_color("#60C7FF")
        self.setup_ui()
        self.setup_fade_animation()

    # ------------------------------
    # UI Initialization
    # ------------------------------

    def setup_ui(self):
        self.logo_label = QLabel()
        logo_pixmap = QPixmap("assets/ncal_logo_white_transparent.png").scaledToWidth(
            450, Qt.TransformationMode.SmoothTransformation
        )
        self.logo_label.setPixmap(logo_pixmap)
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title_label = QLabel("Self Check-out station")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("""
            font-size: 48px;
            font-weight: 600;
        """)

        self.touch_to_start = QLabel("< touch to start >")
        self.touch_to_start.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.touch_to_start.setStyleSheet("""
            font-size: 48px;
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.logo_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.touch_to_start)

        self.setLayout(layout)

    # ------------------------------
    # Background and Style
    # ------------------------------

    def set_background_color(self, hex_color: str):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(hex_color))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

    # ------------------------------
    # Animation Handling
    # ------------------------------

    def setup_fade_animation(self):
        opacity = QGraphicsOpacityEffect()
        self.touch_to_start.setGraphicsEffect(opacity)

        animation = QPropertyAnimation(opacity, b"opacity")
        animation.setDuration(1000)
        animation.setStartValue(1.0)
        animation.setEndValue(0.2)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        animation.setLoopCount(-1)
        animation.start()

        self.fade_anim = animation  # keep reference

    # ------------------------------
    # Touch / Mouse Event
    # ------------------------------

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.main_window.goto_list()
