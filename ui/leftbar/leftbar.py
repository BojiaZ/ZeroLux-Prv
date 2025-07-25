# ui/leftbar/leftbar.py
from PySide6.QtWidgets import QWidget, QVBoxLayout
from .menu_button import MenuButton
from functools import partial
from PySide6.QtCore import Signal

class LeftBar(QWidget):
    page_selected = Signal(str)   # 新增：选中页面的信号
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 固定侧栏宽度
        #self.setFixedWidth(180)

        # 垂直布局，设置上边距和按钮间距
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 24, 0, 0)  # 上24px，其它0
        layout.setSpacing(12)                   # 按钮间距12px

        # 记录所有按钮
        self.buttons = []
        self.items = [
            ("overview", "概览"),
            ("protect", "保护"),
            ("scan", "扫描"),
            ("update", "更新"),
            ("setting", "设置"),
        ]
        for icon_base, text in self.items:
            btn = MenuButton(icon_base, text)
            btn.clicked.connect(partial(self.select_button, btn))
            layout.addWidget(btn)
            self.buttons.append(btn)

        layout.addStretch()

        # 默认选中第一个按钮
        if self.buttons:
            self.select_button(self.buttons[0])

        # 底部留空
        layout.addStretch()

        # 应用背景色
        self.setStyleSheet("background: #f4f5f7;")
    
    def select_button(self, btn):
        for b in self.buttons:
            b.setSelected(False)
        btn.setSelected(True)
        # 找到按钮在 items 里的序号
        idx = self.buttons.index(btn)
        page_name = self.items[idx][0]
        self.page_selected.emit(page_name)
