# quarantine/quarantine_route.py
from PySide6.QtCore import QObject, Signal, Slot
from structs.actionresults import ActionResult
from structs.scanresult    import ScanResult
from managers.quarantine_manager import QuarantineManager
from quarantine.quarantine_engine import QuarantineEngine
import os, datetime

class QuarantineRoute(QObject):
    """
    隔离区路由器
      • 向 ExecuteRoute 提供 isolate (批量隔离) 能力
      • 向 UI 提供 restore / delete (批量还原/删除) 能力
    """

    # —— UI 侧信号 ——
    signal_quarantine_list            = Signal(list)          # list[ActionResult]
    signal_quarantine_action_result   = Signal(object, bool, str)  # item, ok, msg
    signal_quarantine_action_finished = Signal()

    # —— ExecuteRoute 回调 ——（*ExecuteRoute 监听此信号*）
    signal_quarantine_done            = Signal(list)          # list[ActionResult]

    # ------------------------------------------------------------------
    def __init__(self):
        super().__init__()
        # ① 先建持久化管理器并加载历史隔离项
        self.store = QuarantineManager()
        self.items = self.store.load()          # list[ActionResult]

        self.engine = QuarantineEngine()

        # ③ （可选）启动就把当前隔离列表发给 UI
        if self.items:
            self.signal_quarantine_list.emit(self.items)


    # ========= ExecuteRoute 发起：批量隔离 =========
     # —— 新增同步接口 —— #
    def isolate_single(self, sr: ScanResult) -> ActionResult:
        ok, dst, err = self.engine.isolate(sr.file_path)
        ar = ActionResult(
            file_path   = dst if ok else sr.file_path,
            origin_path = sr.file_path,
            file_name   = os.path.basename(sr.file_path),
            recommend   = "quarantine",
            handled     = ok,
            reason      = sr.reason,
            engine      = sr.engine,
            comment     = sr.comment,
            handle_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            error       = err
        )
        if ok:
            self.items.append(ar)
            QuarantineManager().save(self.items)
            self.signal_quarantine_list.emit(self.items)     # 实时推送给隔离区 UI
        return ar

    # ========= UI 主动拉取列表 =========
    @Slot()
    def get_quarantine_list(self):
        self.signal_quarantine_list.emit(self.items)

    # ========= UI 还原 =========
    @Slot(list)
    def restore_items(self, ars: list[ActionResult]):
        for ar in ars:
            ok, err = self.engine.restore(ar.file_path, ar.origin_path)
            self.signal_quarantine_action_result.emit(ar, ok, err)
            if ok:
                # 用 file_path 来找条目，而不是靠对象身份
                self.items = [x for x in self.items if x.file_path != ar.file_path]

        self.store.save(self.items)        # ← 持久化
        self.signal_quarantine_action_finished.emit()
        self.signal_quarantine_list.emit(self.items)
        

    # ========= UI 删除 =========
    @Slot(list)
    def delete_items(self, ars: list[ActionResult]):
        for ar in ars:
            ok, err = self.engine.delete(ar.file_path)
            self.signal_quarantine_action_result.emit(ar, ok, err)
            if ok:
                # 用 file_path 来找条目，而不是靠对象身份
                self.items = [x for x in self.items if x.file_path != ar.file_path]

        self.store.save(self.items)        # ← 持久化
        self.signal_quarantine_action_finished.emit()
        self.signal_quarantine_list.emit(self.items)
