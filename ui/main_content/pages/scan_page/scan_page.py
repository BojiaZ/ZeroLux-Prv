from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt

from .top_panel import TopPanel
from .scan_list_area import ScanListArea
from .scan_card import ScanCard
from engine.engine import ScanEngine

class ScanPage(QWidget):
    """子路由器：顶部 SelectorBar + 下方 ScanListArea"""
    def __init__(self):
        super().__init__()
        self._next_id = 1
        self._cards = {}

        root = QVBoxLayout(self)
        root.setContentsMargins(32, 16, 32, 24)
        root.setSpacing(16)

        # 顶部操作条
        self.top = TopPanel()
        self.top.start_scan.connect(self._start_smart_scan)
        root.addWidget(self.top)

        # 扫描记录列表
        self.area = ScanListArea()
        root.addWidget(self.area, 1)

        self.engine = None
        self._running_card = None

    def _start_smart_scan(self, mode: str):
        """启动智能扫描（只允许一个任务同时进行）"""
        # 已有任务在运行，直接忽略
        if self.engine is not None:
            print("已有扫描任务在运行，请等待完成。")
            return

        cid = self._next_id
        self._next_id += 1

        card = ScanCard(cid, mode)
        self._cards[cid] = card
        self.area.add_card(card)
        self._running_card = card

        card.pause_clicked.connect(self._pause_scan)
        card.resume_clicked.connect(self._resume_scan)
        card.cancel_clicked.connect(self._cancel_scan)
        card.show_log.connect(self._show_log)

        self.engine = ScanEngine()
        self.engine.progress.connect(card.update_progress)  # (percent, path)
        self.engine.finished.connect(lambda: self._on_scan_finished(cid, card))
        self.engine.paused.connect(lambda: card.set_paused(True))
        self.engine.resumed.connect(lambda: card.set_paused(False))

        self.engine.start_scan()

    def _pause_scan(self, cid=None):
        if self.engine:
            self.engine.pause()

    def _resume_scan(self, cid=None):
        if self.engine:
            self.engine.resume()

    def _cancel_scan(self, cid=None):
        if self.engine:
            self.engine.stop()
            self.engine = None
            # 可考虑把卡片变灰或直接移除
            if self._running_card:
                self.area.remove_card(self._running_card)
            self._running_card = None

    def _on_scan_finished(self, cid, card):
        self.area.remove_card(card)
        self._cards.pop(cid, None)
        self._running_card = None
        self.engine = None
        print(f"Scan #{cid} finished.")

    def _show_log(self, cid: int):
        print(f"[Demo] 打开 #{cid} 日志弹窗…")
