from PySide6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout
from PySide6.QtCore import Slot

from .pages import OVERVIEW, PROTECTION, SCAN, UPDATE, SETTINGS
from .pages.overview_page import OverviewPage
from .pages.protection_page import ProtectionPage
from .pages.scan_page import ScanPage
from .pages.update_page import UpdatePage
from .pages.settings_page import SettingsPage

class MainContent(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.stack = QStackedWidget(self)

        # 保留实例引用，后续可直接调用页面方法
        self.overview_page   = OverviewPage()
        self.scan_page       = ScanPage()
        self.protection_page = ProtectionPage()
        self.update_page     = UpdatePage()
        self.settings_page   = SettingsPage()

        # 键 -> index 的映射（不要重复键）
        self._page_index = {
            OVERVIEW:   self.stack.addWidget(self.overview_page),
            SCAN:       self.stack.addWidget(self.scan_page),
            PROTECTION: self.stack.addWidget(self.protection_page),
            UPDATE:     self.stack.addWidget(self.update_page),
            SETTINGS:   self.stack.addWidget(self.settings_page),
        }

        # 概览页卡片动作
        self.overview_page.actionRequested.connect(self._on_overview_action)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.stack)

        self.goto(OVERVIEW)  # 指定默认页

    def goto(self, key: str):
        idx = self._page_index.get(key)
        if idx is not None:
            self.stack.setCurrentIndex(idx)

    @Slot(str)
    def _on_overview_action(self, key: str):
        if key == "scan":
            self.goto(SCAN)
            if hasattr(self.scan_page, "start_quick_scan"):
                self.scan_page.start_quick_scan()
        elif key == "update":
            self.goto(UPDATE)
        elif key == "report":
            # 未来接日志页，这里跳转过去；暂时先忽略或跳设置
            # self.goto(LOG)
            pass
