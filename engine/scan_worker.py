# engine/scan_worker.py
from PySide6.QtCore import QThread, Signal
import os, time

class ScanWorker(QThread):
    """纯扫描线程：遍历文件夹并上报进度"""
    progress = Signal(int, str)     # (百分比, 当前路径)
    finished = Signal()
    paused   = Signal()
    resumed  = Signal()

    def __init__(self, paths: list[str]):
        super().__init__()
        self.paths  = paths
        self._pause = False
        self._stop  = False

    # ---------------- 主逻辑 ----------------
    def run(self):
        all_files = [
            os.path.join(r, f)
            for folder in self.paths
            for r, _, files in os.walk(folder)
            for f in files
        ]
        total = len(all_files)
        if total == 0:
            self.progress.emit(100, "(无文件)")
            self.finished.emit()
            return

        for i, file_path in enumerate(all_files, start=1):
            if self._stop:
                return
            while self._pause:
                self.paused.emit()
                time.sleep(0.1)

            pct = int(i / total * 100)
            self.progress.emit(pct, file_path)
            time.sleep(0.01)            # 模拟扫描速度

        self.finished.emit()

    # ---------------- 控制接口 ----------------   
    def pause(self):   self._pause = True
    def resume(self):
        if self._pause:
            self._pause = False
            self.resumed.emit()
    def stop(self):
        self._stop, self._pause = True, False
        self.wait()
