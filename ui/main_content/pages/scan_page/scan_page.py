from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import QTimer

from .top_panel     import TopPanel
from .scan_list_area import ScanListArea
from .scan_card      import ScanCard

class ScanPage(QWidget):
    """子路由器：顶部 SelectorBar + 下方 ScanListArea"""
    def __init__(self):
        super().__init__()
        self._next_id, self._cards = 1, {}

        root = QVBoxLayout(self)
        root.setContentsMargins(32, 16, 32, 24)
        root.setSpacing(16)

        # 顶部操作条
        self.top = TopPanel()
        self.top.start_scan.connect(self._create_fake_scan)
        root.addWidget(self.top)

        # 扫描记录列表
        self.area = ScanListArea()
        root.addWidget(self.area, 1)

    # ----------- DEMO：创建假扫描并模拟进度 ----------------
    def _create_fake_scan(self, mode: str):
        cid = self._next_id
        self._next_id += 1

        card = ScanCard(cid, mode)
        card.show_log.connect(self._show_log)
        card.delete_requested.connect(self._del_card)

        self._cards[cid] = card
        self.area.add_card(card)

        # 用 QTimer 假装跑进度
        p = {"value": 0}
        def step():
            p["value"] += 10
            card.update_progress(p["value"])
            if p["value"] >= 100:
                timer.stop()
        timer = QTimer(self)
        timer.timeout.connect(step)
        timer.start(300)

    # ----------------- 占位槽 -----------------
    def _show_log(self, cid: int):
        print(f"[Demo] 打开扫描 #{cid} 的日志弹窗…")

    def _del_card(self, cid: int):
        card = self._cards.pop(cid, None)
        if card:
            self.area.remove_card(card)
