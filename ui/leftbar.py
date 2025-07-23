# ui/LeftBar.py
from PySide6.QtWidgets import QWidget, QVBoxLayout
from .MenuButton import MenuButton

class LeftBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 固定侧栏宽度
        self.setFixedWidth(260)

        # 垂直布局，设置上边距和按钮间距
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 24, 0, 0)  # 上24px，其它0
        layout.setSpacing(12)                   # 按钮间距12px

        # 直接添加几个按钮，路径对照你的项目结构
        layout.addWidget(MenuButton("resources/icons/menu_icon/overview.svg",          "Overview"))
        layout.addWidget(MenuButton("resources/icons/menu_icon/protect.svg",           "RealTime-Protection"))
        layout.addWidget(MenuButton("resources/icons/menu_icon/scan.svg",              "Scan"))
        layout.addWidget(MenuButton("resources/icons/menu_icon/update.svg",            "Update"))
        layout.addWidget(MenuButton("resources/icons/menu_icon/setting.svg",           "Setting"))

        # 底部留空
        layout.addStretch()

        # 应用背景色
        self.setStyleSheet("background: #f6f7f9;")
