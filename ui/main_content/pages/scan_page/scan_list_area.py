from PySide6.QtWidgets import QScrollArea, QWidget, QVBoxLayout

class ScanListArea(QScrollArea):
    """垂直放置多个 ScanCard，可滚动"""
    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)

        container = QWidget()
        self.vbox = QVBoxLayout(container)
        self.vbox.addStretch()              # 占位弹性
        self.setWidget(container)

    def add_card(self, card):
        self.vbox.insertWidget(self.vbox.count() - 1, card)

    def remove_card(self, card):
        card.setParent(None)
        card.deleteLater()
