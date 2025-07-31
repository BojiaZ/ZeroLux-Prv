# engine/engine_interface.py
from PySide6.QtCore import QObject, Signal
import os, ctypes, string, psutil
from .scan_worker import ScanWorker

class EngineInterface(QObject):
    """UI 侧唯一依赖的引擎入口：选路径 + 调度 ScanWorker"""
    progress = Signal(int, str)
    finished = Signal()
    paused   = Signal()
    resumed  = Signal()

    def __init__(self):
        super().__init__()
        self.worker = None

    # --------- 外部 API ---------
    def start_scan(self, mode: str, *, custom_paths=None):
        paths = self._select_paths(mode, custom_paths)
        self.worker = ScanWorker(paths)
        # 桥接信号
        self.worker.progress.connect(self.progress.emit)
        self.worker.finished.connect(self.finished.emit)
        self.worker.paused.connect(self.paused.emit)
        self.worker.resumed.connect(self.resumed.emit)
        self.worker.start()

    def pause(self):   self.worker and self.worker.pause()
    def resume(self):  self.worker and self.worker.resume()
    def stop(self):
        if self.worker:
            self.worker.stop()
            self.worker = None

    # --------- 路径选择 ---------
    def _select_paths(self, mode: str, custom_paths):
        dispatch = {
            "smart":     self._smart_paths,
            "full":      self._fixed_drive_roots,
            "removable": self.removable_drives,
            "custom":    (lambda: custom_paths or []),
        }
        return dispatch.get(mode, self._smart_paths)()

    # --------- 各模式实现 ---------
    def _smart_paths(self):
        user = os.getenv("USERNAME", "Public")
        return [
            r"C:\Windows\System32",
            r"C:\Program Files",
            fr"C:\Users\{user}\Desktop",
        ]

    def _fixed_drive_roots(self):
        bitmask = ctypes.windll.kernel32.GetLogicalDrives()
        roots = [
            f"{ltr}:\\"
            for i, ltr in enumerate(string.ascii_uppercase)
            if bitmask & (1 << i)
            and ctypes.windll.kernel32.GetDriveTypeW(f"{ltr}:\\") == 3     # DRIVE_FIXED
        ]
        return roots

    @staticmethod
    def removable_drives():
        if os.name == "nt":
            bitmask = ctypes.windll.kernel32.GetLogicalDrives()
            return [
                f"{ltr}:\\"
                for i, ltr in enumerate(string.ascii_uppercase)
                if bitmask & (1 << i)
                and ctypes.windll.kernel32.GetDriveTypeW(f"{ltr}:\\") == 2  # DRIVE_REMOVABLE
            ]
        else:
            return [
                p.mountpoint for p in psutil.disk_partitions()
                if "removable" in p.opts.lower()
            ]
