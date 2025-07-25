from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QSizePolicy, QHBoxLayout
from PySide6.QtSvgWidgets import QSvgWidget

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

        # 主内容区
        main_frame = QFrame()
        main_frame.setStyleSheet(
            "background: white; border: 2px solid black; border-radius: 16px;"
        )
        main_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(main_frame)
