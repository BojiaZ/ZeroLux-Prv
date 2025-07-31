# engine.py
from PySide6.QtCore import QObject, Signal, QThread
import os
import time
import ctypes, string
import psutil

class ScanWorker(QThread):
    progress = Signal(int, str)    # (百分比, 当前路径)
    finished = Signal()
    paused = Signal()
    resumed = Signal()
    
    def __init__(self, paths):
        super().__init__()
        self.paths = paths
        self._pause = False
        self._stop = False

    def run(self):
        # —— 先统计总文件数
        all_files = []
        for folder in self.paths:
            for root, dirs, files in os.walk(folder):
                for f in files:
                    all_files.append(os.path.join(root, f))
        total = len(all_files)
        if total == 0:
            self.progress.emit(100, "(无文件)")
            self.finished.emit()
            return

        # —— 正式遍历，实时进度
        for i, file_path in enumerate(all_files):
            if self._stop:
                return
            while self._pause:
                self.paused.emit()
                time.sleep(0.1)
            percent = int((i + 1) / total * 100)
            self.progress.emit(percent, file_path)
            time.sleep(0.01)  # 模拟扫描速度
        self.finished.emit()

    def pause(self):
        self._pause = True

    def resume(self):
        if self._pause:
            self._pause = False
            self.resumed.emit()

    def stop(self):
        self._stop = True
        self._pause = False  # 避免线程停在pause
        self.wait()          # 等线程安全退出

class ScanEngine(QObject):
    progress = Signal(int, str)    # (百分比, 路径)
    finished = Signal()
    paused = Signal()
    resumed = Signal()

    def __init__(self):
        super().__init__()
        self.worker = None

    def start_scan(self, mode: str, *, custom_paths=None):
        paths = self._select_paths(mode, custom_paths)
        self.worker = ScanWorker(paths)
        self.worker.progress.connect(self.progress.emit)
        self.worker.finished.connect(self.finished.emit)
        self.worker.paused.connect(self.paused.emit)
        self.worker.resumed.connect(self.resumed.emit)
        self.worker.start()

    def pause(self):
        if self.worker:
            self.worker.pause()

    def resume(self):
        if self.worker:
            self.worker.resume()

    def stop(self):
        if self.worker:
            self.worker.stop()
            self.worker = None

    # ---------- 路径选择 ----------
    def _select_paths(self, mode: str, custom_paths):
        """
        根据扫描模式返回要遍历的根路径列表
        smart       → 系统关键目录
        full        → 所有固定磁盘根目录
        custom      → 调用方传进来的自定义列表
        removable   → 可移动磁盘根目录
        """
        dispatch = {
            "smart":     self._smart_paths,
            "full":      self._fixed_drive_roots,
            "removable": self.removable_drives,
            "custom":    lambda: custom_paths #or self._smart_paths()
        }

       # 若 mode 不在字典，用 smart 兜底
        return dispatch.get(mode, self._smart_paths)()

    # ---------- 各模式下的具体实现 ----------
    def _smart_paths(self):
        try:
            username = os.getlogin()
        except Exception:
            username = os.environ.get('USERNAME', 'Public')
        return [
            fr"C:\Windows\System32",
            fr"C:\Program Files",
            fr"C:\Users\{username}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup",
            fr"C:\Users\{username}\Desktop",
        ]

    def _fixed_drive_roots(self):
        bitmask = ctypes.windll.kernel32.GetLogicalDrives()
        roots = []
        for i, letter in enumerate(string.ascii_uppercase):
            if bitmask & (1 << i):
                drive = f"{letter}:\\"
                # DRIVE_FIXED = 3
                if ctypes.windll.kernel32.GetDriveTypeW(drive) == 3:
                    roots.append(drive)
        return roots

    @staticmethod
    def removable_drives():
        import os, ctypes, string, psutil
        drives = []
        if os.name == "nt":
            bitmask = ctypes.windll.kernel32.GetLogicalDrives()
            for i, letter in enumerate(string.ascii_uppercase):
                if bitmask & (1 << i) and \
                   ctypes.windll.kernel32.GetDriveTypeW(f"{letter}:\\") == 2:
                    drives.append(f"{letter}:\\")
        else:
            for p in psutil.disk_partitions():
                if "removable" in p.opts.lower():
                    drives.append(p.mountpoint)
        return drives
