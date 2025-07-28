# pages/ScanPage.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class ScanPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(30)

        # 返回按钮
        self.back_btn = QPushButton("← 返回")
        self.back_btn.setFixedSize(100, 40)
        self.back_btn.setStyleSheet("""
            QPushButton {
                background: #f0f0f0;
                border-radius: 6px;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.back_btn, alignment=Qt.AlignLeft)

        # 页面标题
        title = QLabel("病毒扫描")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        layout.addWidget(title)

        # 三个按钮横向排列
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(30)

        self.quick_scan_btn = self.create_scan_button("快速扫描")
        self.full_scan_btn = self.create_scan_button("全盘扫描")
        self.custom_scan_btn = self.create_scan_button("自定义扫描")

        btn_layout.addWidget(self.quick_scan_btn)
        btn_layout.addWidget(self.full_scan_btn)
        btn_layout.addWidget(self.custom_scan_btn)

        layout.addLayout(btn_layout)

    def create_scan_button(self, text):
        btn = QPushButton(text)
        btn.setFixedSize(180, 120)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #E4E9F7;
                border-radius: 12px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d0ddfa;
            }
        """)
        return btn
