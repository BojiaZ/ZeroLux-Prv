from PySide6.QtCore import QObject, Signal, Slot
from structs.actionresults import ActionResult

class QuarantineRoute(QObject):
    """
    隔离区管理路由器

    职责：
        - 自动记录每次隔离成功的文件（监听 ExecuteRouter 的批量操作信号）
        - 管理并输出当前所有隔离区文件（list[ActionResult]）
        - 支持批量还原、批量删除，状态实时同步 UI
        - 所有操作结果和进度全信号反馈，UI和其他模块可直接对接
    """

    signal_quarantine_list = Signal(list)             # 隔离区全量文件列表（list[ActionResult]）
    signal_quarantine_action_result = Signal(object, bool, str)  # 单个隔离项操作反馈
    signal_quarantine_action_finished = Signal()                # 批量操作结束

    def __init__(self, excute_router):
        super().__init__()
        self.excute_router = excute_router
        self.quarantine_list = []  # 所有隔离区项（list[ActionResult]）

        # 监听 excute_router 的批量处置信号，隔离成功项自动入库
        self.excute_router.signal_execute_finished.connect(self._on_execute_finished)

    @Slot(list)
    def _on_execute_finished(self, action_results: list):
        """
        接收批量动作结果，将新隔离的文件自动加入隔离区
        """
        updated = False
        for item in action_results:
            if getattr(item, "recommend", None) == "quarantine" and getattr(item, "handled", False):
                if item.file_path not in [x.file_path for x in self.quarantine_list]:
                    self.quarantine_list.append(item)
                    updated = True
        if updated:
            self.signal_quarantine_list.emit(self.quarantine_list)

    @Slot()
    def get_quarantine_list(self):
        """
        主动请求当前隔离区全部文件列表
        """
        self.signal_quarantine_list.emit(self.quarantine_list)

    @Slot(list)
    def restore_items(self, items: list):
        """
        批量还原隔离区文件（UI/外部直接调用）
        """
        files = [x.file_path for x in items]
        origin_paths = [x.origin_path for x in items]
        # 绑定还原信号，仅本次有效
        self.excute_router.signal_execute_result.connect(self._on_restore_result)
        self.excute_router.signal_execute_finished.connect(self._on_restore_finished)
        self._pending_restore = set(files)
        self.excute_router.execute_restore(files, origin_paths)

    def _on_restore_result(self, file_path, ok, msg):
        """
        实时反馈还原单个文件结果
        """
        # 查找隔离区对象（ActionResult）用于回调
        item = next((x for x in self.quarantine_list if x.file_path == file_path), None)
        self.signal_quarantine_action_result.emit(item, ok, msg)
        if ok and item:
            # 操作成功，移除
            self.quarantine_list = [x for x in self.quarantine_list if x.file_path != file_path]

    def _on_restore_finished(self, *args, **kwargs):
        """
        还原批量完成，更新隔离区，断开信号
        """
        self.signal_quarantine_action_finished.emit()
        self.signal_quarantine_list.emit(self.quarantine_list)
        try:
            self.excute_router.signal_execute_result.disconnect(self._on_restore_result)
            self.excute_router.signal_execute_finished.disconnect(self._on_restore_finished)
        except Exception:
            pass

    @Slot(list)
    def delete_items(self, items: list):
        """
        批量彻底删除隔离区文件（UI/外部直接调用）
        """
        files = [x.file_path for x in items]
        self.excute_router.signal_execute_result.connect(self._on_delete_result)
        self.excute_router.signal_execute_finished.connect(self._on_delete_finished)
        self._pending_delete = set(files)
        self.excute_router.execute_delete(files)

    def _on_delete_result(self, file_path, ok, msg):
        """
        实时反馈删除单个文件结果
        """
        item = next((x for x in self.quarantine_list if x.file_path == file_path), None)
        self.signal_quarantine_action_result.emit(item, ok, msg)
        if ok and item:
            self.quarantine_list = [x for x in self.quarantine_list if x.file_path != file_path]

    def _on_delete_finished(self, *args, **kwargs):
        """
        批量删除完成，更新隔离区，断开信号
        """
        self.signal_quarantine_action_finished.emit()
        self.signal_quarantine_list.emit(self.quarantine_list)
        try:
            self.excute_router.signal_execute_result.disconnect(self._on_delete_result)
            self.excute_router.signal_execute_finished.disconnect(self._on_delete_finished)
        except Exception:
            pass
