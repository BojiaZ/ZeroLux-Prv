from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt, Signal, QDateTime, QTimer
import weakref
from .top_panel import TopPanel
from .scan_list_area import ScanListArea
from .running_card import RunningCard
from .result_card import ResultCard
from engine.engine import ScanEngine

class ScanPage(QWidget):
    """子路由器：顶部 SelectorBar + 下方 ScanListArea"""
    def __init__(self):
        super().__init__()

        self._sig_cache = []   # <--- 新增：缓存 (signal, slot) 对
        self._next_id = 1
        self._cards = {}

        root = QVBoxLayout(self)
        root.setContentsMargins(32, 16, 32, 24)
        root.setSpacing(16)

        # 顶部操作条
        self.top = TopPanel()
        self.top.start_scan.connect(self._start_scan)
        root.addWidget(self.top)

        # 扫描记录列表
        self.area = ScanListArea()
        root.addWidget(self.area, 1)

        self.engine = None
        self._running_card = None

    def _start_scan(self, scan_mode: str):
        """启动智能扫描（只允许一个任务同时进行）"""
        # 已有任务在运行，直接忽略
        if self.engine is not None:
            print("已有扫描任务在运行，请等待完成。")
            return
        
        cid = self._next_id
        self._next_id += 1

        card = RunningCard(cid, scan_mode)
        self._cards[cid] = card
        self.area.add_card(card)
        self._running_card = card

        card.pause_clicked.connect(self._pause_scan)
        card.resume_clicked.connect(self._resume_scan)
        card.cancel_clicked.connect(self._cancel_scan)
        card.show_log.connect(self._show_log)
        
        self.engine = ScanEngine()
        
        # ---- 1. 进度 ----
        progress_slot = card.update_progress
        self.engine.progress.connect(progress_slot)
        self._sig_cache.append((self.engine.progress, progress_slot))

        # ---- 2. finished ----
        finished_slot = lambda cid_=cid, mode_=scan_mode, card_=card: \
            self._on_scan_finished(cid_, mode_, card_)
        self.engine.finished.connect(finished_slot)
        self._sig_cache.append((self.engine.finished, finished_slot))

        # ---- 3. 暂停 / 恢复 ----
        pause_slot = lambda: card.set_paused(True)
        resume_slot = lambda: card.set_paused(False)
        self.engine.paused.connect(pause_slot)
        self.engine.resumed.connect(resume_slot)
        self._sig_cache += [
            (self.engine.paused, pause_slot),
            (self.engine.resumed, resume_slot)
        ]

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
            self._disconnect_all()
            self.engine = None
            
            if self._running_card:
                # 取消时也用结果卡替换
                cid = self._running_card.id
                mode = self._running_card.mode
                found = 0
                engine_ver = "31608 (20250729)"
                dt = QDateTime.currentDateTime()
                status = "canceled"
                self.area.remove_card(self._running_card)
                result_card = ResultCard(cid, mode, found, engine_ver, dt, status)
                self.area.add_card(result_card)
                result_card.remove_clicked.connect(lambda _=None, rc=result_card: self.area.remove_card(rc))
                result_card.show_log.connect(self._show_log)
            self._running_card = None

    def _on_scan_finished(self, cid: int, scan_mode: str, card: RunningCard):
        """扫描完成后把 RunningCard → ResultCard"""
        self._disconnect_all()

        # 1. 清理 UI 中的 RunningCard
        self.area.remove_card(card)
        self._cards.pop(cid, None)

        # 2. 组装结果数据（这里写死，后面记得用真实值）
        found       = 0
        engine_ver  = "31608 (20250729)"
        finished_at = QDateTime.currentDateTime()
        status      = "done"

        # 3. 新建 ResultCard
        result_card = ResultCard(cid, scan_mode, found, engine_ver, finished_at, status)
        self.area.add_card(result_card)

        # 4. 链接 ResultCard 的信号
        result_card.remove_clicked.connect(
            lambda _=None, rc=result_card: self.area.remove_card(rc)
        )
        result_card.show_log.connect(self._show_log)

        # 5. 复位状态
        self._running_card = None
        eng = self.engine          # 把当前对象暂存
        self.engine = None         # 先逻辑置空，下一次点击能启动
        if eng:                    # 可能已在取消流程中置空
            # 等事件循环空闲时再 deleteLater -> 避免“线程仍在运行”
            QTimer.singleShot(0, eng.deleteLater)


    def _show_log(self, cid: int):
        print(f"[Demo] 打开 #{cid} 日志弹窗…")

    def _disconnect_all(self):
        """安全地把之前缓存的所有信号都断开"""
        for sig, slot in self._sig_cache:
            try:
                sig.disconnect(slot)
            except (TypeError, RuntimeError):
                pass
        self._sig_cache.clear()