from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class ProtectionPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        label = QLabel("这是『保护』页面")
        label.setStyleSheet("font-size: 24px; color: #3a7;")
        layout.addWidget(label)
