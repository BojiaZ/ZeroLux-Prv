from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PySide6.QtCore import Signal

class SelectorBar(QWidget):
    """顶部 3-4 个按钮：快速 / 全盘 / 自定义 / 历史"""
    start_scan = Signal(str)     # quick / full / custom
    show_history = Signal()      # 查看历史（可选）

    def __init__(self):
        super().__init__()
        bar = QHBoxLayout(self)
        bar.setSpacing(12)

        for key, text in [("quick", "快速扫描"),
                          ("full", "全盘扫描"),
                          ("custom", "自定义扫描")]:
            btn = QPushButton(text)
            btn.clicked.connect(lambda _=False, k=key: self.start_scan.emit(k))
            bar.addWidget(btn)