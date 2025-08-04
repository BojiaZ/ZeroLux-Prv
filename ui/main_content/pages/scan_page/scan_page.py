# scan/scan_page.py
from PySide6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout

from .scan_select import ScanSelectPage
from scans.scans_router import ScanRoute
from .scanning import ScanningPage

class ScanPage(QWidget):
    def __init__(self, scan_route: ScanRoute, parent=None):
        super().__init__(parent)

        self.scan_route = scan_route
        self.stacked = QStackedWidget(self)

        # 实例化各子页面
        self.select_page = ScanSelectPage()
        self.scanning_page = ScanningPage(scan_route)
        # self.result_page = ScanResultPage()
        # self.history_page = ScanHistoryPage()

        # 挂到堆栈
        self.stacked.addWidget(self.select_page)      # index 0
        self.stacked.addWidget(self.scanning_page)  # index 1
        # self.stacked.addWidget(self.result_page)    # index 2
        # self.stacked.addWidget(self.history_page)   # index 3

        layout = QVBoxLayout(self)
        layout.addWidget(self.stacked)

        # 默认展示模式选择页
        self.goto_select()

        # 信号连接：比如 select_page 完成选择后进入扫描
        self.select_page.sig_start_scan.connect(self._on_start_scan)
    

    # 当 SelectPage 发射 start_scan 时：
    def _on_start_scan(self, mode, path):
        # 1) 先把页面切到 scanning_page
        self.scanning_page.set_mode(mode)       # ← 告诉它当前模式
        self.stacked.setCurrentWidget(self.scanning_page)

        # 2) 再让 Router 真正去启动扫描
        self.scan_route.start_scan(mode, path)

    # ---------- 页面切换 ----------
    def goto_select(self):
        self.stacked.setCurrentWidget(self.select_page)

    # 后续补充
    # def goto_scanning(self, mode): ...
    # def goto_result(self, ...): ...
    # def goto_history(self): ...
