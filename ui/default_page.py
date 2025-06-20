from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGraphicsOpacityEffect
from PyQt6.QtGui import QColor, QPalette, QPixmap
from PyQt6.QtCore import Qt, QPropertyAnimation ,QEasingCurve

class DefaultPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#60C7FF"))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)

        image_label = QLabel()
        pixmap = QPixmap("assets/ncal_logo_white_transparent.png")  
        pixmap = pixmap.scaledToWidth(450, Qt.TransformationMode.SmoothTransformation)  
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Self Check-out station")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            '''
            font-size: 48px;
            font-weight: 600;
            '''
        )

        self.touch_to_start = QLabel("< touch to start >")
        self.touch_to_start.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.touch_to_start.setStyleSheet(
            '''
            font-size: 48px;
            '''
        )

        # fade animation
        self.setup_fade_animation()

        vbox.addWidget(image_label)
        vbox.addWidget(title)
        vbox.addWidget(self.touch_to_start)

        self.setLayout(vbox)

    def setup_fade_animation(self):
        opacity_effect = QGraphicsOpacityEffect()
        self.touch_to_start.setGraphicsEffect(opacity_effect)

        # animation opacity 1.0 → 0.2 → 1.0
        self.fade_anim = QPropertyAnimation(opacity_effect, b"opacity")
        self.fade_anim.setDuration(1000)  # 1 sec/round
        self.fade_anim.setStartValue(1.0)
        self.fade_anim.setEndValue(0.2)
        self.fade_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.fade_anim.setLoopCount(-1)  # infinity

        self.fade_anim.start()

    
    # not sure this will work with touchscreen
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.main_window.goto_list()

