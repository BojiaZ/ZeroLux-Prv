from PySide6.QtCore import QObject, Signal, Slot
from structs.scanresult import ScanResult
from structs.actionresults import ActionResult
from .execute_engine import ExecuteEngine
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
    signal_execute_progress = Signal(float)
    signal_execute_result = Signal(object)     # ActionResult
    signal_execute_finished = Signal(list)     # list[ActionResult]

    def __init__(self):
        super().__init__()
        self.engine = ExecuteEngine()          # 初始化底层处置引擎

    @Slot(list)
    def handle_results(self, scan_results: list):
        """
        统一批量处理 scanresult（支持多种动作），根据 recommend 字段分流，
        每项处理后发实时结果，全部结束后发全部 ActionResult 列表。
        """
        results = []  # 存所有ActionResult
        total = len(scan_results)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 记录操作时间
        for idx, s in enumerate(scan_results):
            # 取文件名，方便UI展示
            file_name = os.path.basename(s.file_path)

            # 根据 recommend 字段，决定执行什么操作
            if s.recommend == "delete":
                # 删除操作
                ok = self.engine.delete_files([s.file_path])[s.file_path]
                error_msg = "" if ok else "Delete failed"
            elif s.recommend == "quarantine":
                # 隔离操作（隔离区目录可配置）
                ok = self.engine.quarantine_files([s.file_path], "db/quarantine")[s.file_path]
                error_msg = "" if ok else "Quarantine failed"
            else:
                # 其他未知/暂不支持操作
                ok = False
                error_msg = f"Unknown action: {s.recommend}"

            # 组装 ActionResult 对象，便于UI和隔离区统一管理
            action = ActionResult(
                file_path=s.file_path,             # 文件实际路径
                file_name=file_name,               # 文件名
                recommend=s.recommend,             # 推荐操作
                engine=s.engine or "",             # 检测引擎
                handled=ok,                        # 是否处理成功
                handle_time=now,                   # 操作时间
                comment=s.comment,                 # 备注/描述
                origin_path=getattr(s, "origin_path", None), # 隔离前原始路径（可选）
                error=error_msg,                   # 错误信息
                reason=s.reason
            )

            self.signal_execute_result.emit(action)  # 实时发送单项处理结果，供UI刷新
            results.append(action)                   # 收集到总列表里

            percent = (idx + 1) / total * 100 if total else 100  # 进度百分比
            self.signal_execute_progress.emit(percent)           # 实时发送进度

        self.signal_execute_finished.emit(results)   # 全部处理完后批量发回全部结果列表
