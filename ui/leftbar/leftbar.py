# ui/leftbar/leftbar.py
from PySide6.QtWidgets import QWidget, QVBoxLayout
from .menu_button import MenuButton
from functools import partial
from PySide6.QtCore import Signal

class LeftBar(QWidget):
    page_selected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        # 0️⃣ 定义导航列表
        self.items = [
            ("overview", "概览"),
            ("protection", "保护"),
            ("scan", "扫描"),
            ("update", "更新"),
            ("settings", "设置"),
        ]

        # 1️⃣ 布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 24, 0, 0)
        layout.setSpacing(12)

        # 2️⃣ key→button 映射
        self._key_btn = {}

        for key, text in self.items:
            btn = MenuButton(key, text)
            btn.clicked.connect(partial(self._on_btn_clicked, key))
            layout.addWidget(btn)
            self._key_btn[key] = btn

        layout.addStretch()

        # 3️⃣ 构造完只高亮，不 emit
        self.set_highlight("overview")

        # 4️⃣ 外观
        self.setStyleSheet("background: #f4f5f7;")

    # 点击槽
    def _on_btn_clicked(self, key):
        self.set_highlight(key)
        self.page_selected.emit(key)

    # 对外：高亮
    def set_highlight(self, key: str):
        for k, btn in self._key_btn.items():
            btn.setSelected(k == key)
