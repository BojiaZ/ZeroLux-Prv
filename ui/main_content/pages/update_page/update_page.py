from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class UpdatePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        label = QLabel("这是『更新』页面")
        label.setStyleSheet("font-size: 24px; color: #a73;")
        layout.addWidget(label)
