from PySide6.QtCore import QObject, Signal, Slot
from structs.scanresult import ScanResult
from structs.actionresults import ActionResult
from .execute_engine import ExecuteEngine
from quarantine.quarantine_route import QuarantineRoute
import os
import datetime

class ExecuteRoute(QObject):
    """
    动作路由器（调度器）

    职责：
        - 批量接收 scanresult 列表，按 recommend 字段自动分流（delete/quarantine/restore）
        - 调用 ExecuteEngine 执行具体动作，收集 ActionResult 列表
        - 实时发射进度和单项结果信号
        - 最终批量发射全部处置结果，供 UI 展示、隔离区/历史记录管理
    """

    # 信号：进度百分比，单项ActionResult，批量全部ActionResult
    signal_execute_progress = Signal(float, str)
    signal_execute_result = Signal(object)     # ActionResult
    signal_execute_finished = Signal(list)     # list[ActionResult]

    def __init__(self, quarantine_route: QuarantineRoute):
        super().__init__()
        self.engine = ExecuteEngine()          # 初始化底层处置引擎
        self.q_route = quarantine_route

    @Slot(list)
    def handle_results(self, srs: list[ScanResult]):
        total     = len(srs)
        processed = 0
        results   = []

        self.signal_execute_progress.emit(0.0, "")

        for sr in srs:
            if sr.recommend == "delete":
                ok = self.engine.delete_files([sr.file_path])[sr.file_path]
                ar = ActionResult(
                    file_path   = sr.file_path,
                    file_name   = os.path.basename(sr.file_path),
                    recommend   = "delete",
                    handled     = ok,
                    reason      = sr.reason,
                    engine      = sr.engine,
                    comment     = sr.comment,
                    handle_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    error       = "" if ok else "Delete failed"
                )
            elif sr.recommend == "quarantine":
                ar = self.q_route.isolate_single(sr)   # ★ 同步隔离
            else:
                ar = ActionResult(
                    file_path = sr.file_path,
                    file_name = os.path.basename(sr.file_path),
                    recommend = sr.recommend,
                    handled   = False,
                    reason    = sr.reason,
                    engine    = sr.engine,
                    comment   = sr.comment,
                    handle_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    error     = f"Unknown action: {sr.recommend}"
                )

            # ---- 回推 UI ----
            results.append(ar)
            processed += 1
            self.signal_execute_result.emit(ar)
            self.signal_execute_progress.emit(processed/total*100, sr.file_path)

        # 全部结束
        self.signal_execute_progress.emit(100.0, "")
        self.signal_execute_finished.emit(results)