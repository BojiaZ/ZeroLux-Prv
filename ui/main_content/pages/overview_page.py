from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QSizePolicy
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtCore import Qt

class OverviewPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 32, 20, 32)  # 四周留白
        layout.setSpacing(28)

        # 状态卡片
        status_card = QFrame()
        status_card.setFixedHeight(120)
        status_card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        status_card.setStyleSheet("background: transparent; border: none;")
        layout.addWidget(status_card)

        # 关键：用 QHBoxLayout 把 SVG 塞进去
        status_layout = QHBoxLayout(status_card)
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_layout.setSpacing(0)
        # 加载 SVG（路径按你的资源实际放置路径来）
        svg = QSvgWidget("resources/pages/status_safe.svg")
        svg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        status_layout.addWidget(svg)

        # 功能按钮区
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(32)
        btn_layout.setAlignment(Qt.AlignCenter)

        btn_layout.addWidget(FunctionCard(
            "resources/overview/scan_blue.svg", "快速扫描", "查杀系统关键位置"))
        btn_layout.addWidget(FunctionCard(
            "resources/overview/update.svg", "更新组件", "同步病毒库和组件"))
        btn_layout.addWidget(FunctionCard(
            "resources/overview/report.svg", "安全报告", "查看最近安全活动"))

        layout.addLayout(btn_layout)
        layout.addStretch()

# 功能卡片
class FunctionCard(QFrame):
    def __init__(self, icon_path, title, desc, parent=None):
        super().__init__(parent)
        self.setFixedSize(180, 180)
        self.setStyleSheet("""
            QFrame {
                background: #f5f7fb;
                border-radius: 18px;
                border: 1.5px solid #e7e9f0;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(10)

        self.icon = QSvgWidget(icon_path)
        self.icon.setFixedSize(48, 48)
        layout.addWidget(self.icon)

        # 设置标题
        self.title = QLabel(title)
        layout.addWidget(self.title)
        self.title.setStyleSheet("font-size: 17px; font-weight: 700; color: #222; border: none; background: transparent;")

        # 设置描述
        self.desc = QLabel(desc)
        self.desc.setVisible(False)
        layout.addWidget(self.desc)
        self.desc.setStyleSheet("font-size: 15px; font-weight: 700; color: #888; border: none; background: transparent;")

    def enterEvent(self, event):
        self.icon.setFixedSize(40, 40)
        self.desc.setVisible(True)
        self.setStyleSheet("""
            QFrame {
                background: transparent;
                border-radius: 18px;
                border: 1.5px solid #b0d8f5;
            }
        """)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.icon.setFixedSize(48, 48)
        self.desc.setVisible(False)
        self.setStyleSheet("""
            QFrame {
                background: transparent;
                border-radius: 18px;
                border: 1.5px solid #e7e9f0;
            }
        """)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        print(f"点击了 {self.title.text()} 卡片")
        super().mousePressEvent(event)