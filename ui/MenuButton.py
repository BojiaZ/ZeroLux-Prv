# MenuButton.py
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, QSize, QByteArray

class MenuButton(QWidget):
    def __init__(self, icon_path, text, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(32, 10, 8, 10)  # 上下10，左右同前
        layout.setSpacing(16)  # 图标和文字更宽松

        self.icon_widget = QSvgWidget(icon_path)
        self.icon_widget.setFixedSize(QSize(26, 26))

        self.text_label = QLabel(text)
        self.text_label.setStyleSheet("font-size: 17px; color: #444; font-weight: 500;")

        layout.addWidget(self.icon_widget)
        layout.addWidget(self.text_label, 1)

        self.setFixedHeight(52)  # 每行更高
        self.setStyleSheet("background: transparent; border-radius: 8px;")
