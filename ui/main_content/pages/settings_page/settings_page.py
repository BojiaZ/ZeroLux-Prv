from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class SettingsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        label = QLabel("这是『设置』页面")
        label.setStyleSheet("font-size: 24px; color: #888;")
        layout.addWidget(label)
