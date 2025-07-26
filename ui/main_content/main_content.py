# ui/main_content/main_content.py

from PySide6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout
from .pages.overview_page import OverviewPage
from .pages.protection_page import ProtectionPage
from .pages.scan_page import ScanPage
from .pages.update_page import UpdatePage
from .pages.settings_page import SettingsPage

class MainContent(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.stack = QStackedWidget()
        self._name_to_idx = {}

        # 注册页面
        self._register_page("overview", OverviewPage())
        self._register_page("scan", ScanPage())
        self._register_page("protect", ProtectionPage())
        self._register_page("scan", ScanPage())
        self._register_page("update", UpdatePage())
        self._register_page("setting", SettingsPage())

        # 可以继续加更多

        layout.addWidget(self.stack)

    def _register_page(self, name, widget):
        idx = self.stack.addWidget(widget)
        self._name_to_idx[name] = idx

    def setCurrentIndex(self, index):
        self.stack.setCurrentIndex(index)
    
    def show_page(self, name):
        idx = self._name_to_idx.get(name)
        if idx is not None:
            self.stack.setCurrentIndex(idx)

    def currentIndex(self):
        return self.stack.currentIndex()
