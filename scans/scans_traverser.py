import os
import time
from PySide6.QtCore import QThread, Signal
from structs.traverseprogress import TraverseProgress
from structs.scanresult import ScanResult
from engine.static_engine import StaticEngine

class Traverser(QThread):
    """
    遍历扫描线程（QThread 版）

    职责：
        - 递归遍历指定目录下所有文件
        - 对每个文件调用静态查杀引擎（StaticEngine）检测
        - 实时发送进度与扫描结果信号
        - 支持暂停、恢复和停止

    发送的信号：
        - signal_progress(TraverseProgress)
            当前扫描文件路径和进度百分比，UI/控制器可用于实时展示进度。
        - signal_scan_result(ScanResult)
            单文件扫描结果，UI/控制器可用于结果列表展示。
        - signal_scan_finished()
            扫描结束信号，UI/控制器可用于解锁界面或提示完成。
        - signal_scan_all_results(list[ScanResult])
            （新增）全部扫描结果（适合UI/日志一次性展示/操作）

    接收的信号/调用的接口：
        - set_params(root_path: str)
            设置本次扫描的目标路径（需在 start() 前调用）。
        - pause()
            暂停扫描（被控制器或UI调用）。
        - resume()
            恢复扫描（被控制器或UI调用）。
        - stop()
            停止扫描（被控制器或UI调用）。

    主要方法：
        - start()
            启动线程（父类QThread自带）。
        - run()
            线程主循环（自动调用，不需外部手动调用）。

    用法示例：
        traverser = Traverser()
        traverser.set_params(r"D:\test")
        traverser.signal_progress.connect(...)
        traverser.signal_scan_result.connect(...)
        traverser.signal_scan_finished.connect(...)
        traverser.start()
        traverser.pause()
        traverser.resume()
        traverser.stop()
    """

    signal_progress = Signal(object)      # TraverseProgress实例
    signal_scan_result = Signal(object)   # ScanResult实例
    signal_scan_finished = Signal()
    signal_scan_all_results = Signal(list)   # 新增批量结果信号

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.root_path = None
        self._paused = False
        self._stopped = False
        self._all_results = []  # 新增收集所有结果

    def set_params(self, paths: list[str]):
        """
        设置要扫描的根目录路径（启动前调用）
        """
        self.paths = [os.path.abspath(p) for p in paths]   # 全部转绝对路径
        print(f"[Traverser] got top paths: {self.paths}")

    def pause(self):
        """暂停扫描"""
        self._paused = True

    def resume(self):
        """恢复扫描"""
        self._paused = False

    def stop(self):
        """停止扫描"""
        self._stopped = True

    def run(self):
        """
        线程入口，执行遍历和检测流程。
        外部调用 self.start() 启动线程
        """
        print("[Traverser] start scanning...")
        self.static_engine = StaticEngine()
        if not self.paths:
            print("[Traverser] paths empty, finish immediately")
            self.signal_scan_finished.emit()
            self.signal_scan_all_results.emit([])
            return

        files = self._traverse_files(self.paths)
        total_files = len(files)
        print(f"[Traverser] total files = {total_files}")
        self._all_results = []

        if total_files == 0:
            self.signal_scan_finished.emit()
            self.signal_scan_all_results.emit([])
            return
        
        # run() 里 —— 开始扫描就先发 0%，避免界面空白
        self.signal_progress.emit(
            TraverseProgress(current_file="", percent_complete=0,
                            done=0, total=total_files)
        )

        for idx, file_path in enumerate(files):
            if self._stopped:
                break

            # 暂停机制：若self._paused为True，则持续sleep，直到恢复
            while self._paused and not self._stopped:
                time.sleep(0.1)

            # 计算进度并发送信号
            percent = (idx + 1) / total_files * 100
            progress = TraverseProgress(
                current_file=file_path,
                percent_complete=percent,
                done=idx + 1,
                total=total_files
            )
            self.signal_progress.emit(progress)

            # 调用静态查杀引擎检测文件
            result = self.static_engine.check_file_by_hash(file_path)
            self.signal_scan_result.emit(result)
            self._all_results.append(result)  # 收集

        # 发送扫描完成信号
        self.signal_scan_finished.emit()
        self.signal_scan_all_results.emit(self._all_results)   # 批量发给UI

        self.static_engine.close()

    def _traverse_files(self, paths: list[str]) -> list[str]:
        """
        递归遍历指定目录或单文件，返回所有文件完整路径列表。

        Args:
            root_path (str): 目录或文件路径

        Returns:
            list[str]: 全部待扫描文件的绝对路径
        """
        all_files: list[str] = []
        for p in paths:
            if os.path.isfile(p):
                all_files.append(os.path.abspath(p))
            else:
                for dirpath, _, filenames in os.walk(p):
                    for name in filenames:
                        all_files.append(os.path.join(dirpath, name))
        return all_files
