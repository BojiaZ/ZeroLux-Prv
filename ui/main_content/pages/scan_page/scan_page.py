# scan/scan_page.py
from PySide6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout
from PySide6.QtCore import Slot

from .scan_select import ScanSelectPage
from scans.scans_router import ScanRoute
from .scanning import ScanningPage
from .scan_result import ScanResultPage
from execute.execute_router import ExecuteRoute
from managers.history_manager import HistoryManager
import time

class ScanPage(QWidget):
    def __init__(self, scan_route: ScanRoute, execute_route: ExecuteRoute, parent=None):
        super().__init__(parent)

        #标记
        self._has_written_history = False

        #因为扫描历史和日志打算分系统所以扫描历史只在这里实例化
        self.history_mgr = HistoryManager()

        self.scan_route = scan_route
        self.execute_route = execute_route
        self.stacked = QStackedWidget(self)

        # 实例化各子页面
        self.select_page = ScanSelectPage(self.history_mgr)
        self.scanning_page = ScanningPage(scan_route)
        self.result_page = ScanResultPage(execute_route)


        # 挂到堆栈
        self.stacked.addWidget(self.select_page)      # index 0
        self.stacked.addWidget(self.scanning_page)  # index 1
        self.stacked.addWidget(self.result_page)    # index 2

        layout = QVBoxLayout(self)
        layout.addWidget(self.stacked)

        # 默认展示模式选择页
        self.goto_select()

        # ① 选择页 → 扫描页
        self.select_page.sig_start_scan.connect(self._on_start_scan)

        # ② 结果页 “完成” → 返回选择页
        self.result_page.back_requested.connect(self.goto_select)

        # ③ Router 扫描结束（批量结果） → 跳结果页
        self.scan_route.signal_scan_all_results.connect(self._on_all_results)

        # 监听处置结束（无论是否有威胁，只要“一键处理”按钮被点过）
        self.execute_route.signal_execute_finished.connect(self._on_execute_finished)
        scan_route.signal_scan_finished.connect(self._on_scan_finished)


    

    # 当 SelectPage 发射 start_scan 时：
    def _on_start_scan(self, mode, path):

        # 1️⃣ 记录开始信息 -------------
        self._scan_start_ts = time.time()
        self._has_written_history = False
        self._scan_mode     = mode

        # 1) 先把页面切到 scanning_page
        self.scanning_page.reset()          # ← 新增
        self.scanning_page.set_mode(mode)       # ← 告诉它当前模式
        self.stacked.setCurrentWidget(self.scanning_page)

        # 2) 再让 Router 真正去启动扫描
        self.scan_route.start_scan(mode, path)

        


    # ---------- 页面切换 ----------
    def goto_select(self):
        self.stacked.setCurrentWidget(self.select_page)
    
    def _on_all_results(self, results: list):
        stopped = getattr(self.scanning_page, "_aborted", False)
        self._goto_result(stopped=stopped, results=results)

    
    def _goto_result(self, stopped: bool, results: list):
        self.result_page.load_data(results, stopped)
        self.stacked.setCurrentWidget(self.result_page)

    @Slot(list)
    def _on_execute_finished(self, action_results: list):
        print("[DEBUG] add history:", len(action_results))
        duration = time.time() - self._scan_start_ts

        self.history_mgr.add_entry(
            self._scan_start_ts,       # start_ts
            action_results             # action_results
        )
        self._has_written_history = True
        if self.select_page.tab_idx == 1:          # 如果正在历史页
            self.select_page.history_page.refresh()

    @Slot()
    def _on_scan_finished(self):
        # 只有当 _on_execute_finished 没写过才兜底
        if not self._has_written_history:
            self.history_mgr.add_entry(
                start_ts       = self._scan_start_ts,
                action_results = []           # 空列表代表无处置
            )
            if self.select_page.tab_idx == 1:
                self.select_page.history_page.refresh()
            self._has_written_history = True