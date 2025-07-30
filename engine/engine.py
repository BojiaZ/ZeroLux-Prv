# engine.py
from PySide6.QtCore import QObject, Signal, QThread
import os
import time

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

    def start_scan(self):
        paths = self._get_smart_scan_paths()
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

    def _get_smart_scan_paths(self):
        # 示例：你可以根据需要调整关键目录
        try:
            username = os.getlogin()
        except Exception:
            username = os.environ.get('USERNAME', 'Public')
        return [
            fr"C:\Windows\System32",
            fr"C:\Program Files",
            fr"C:\Users\{username}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup",
            # fr"C:\Users\{username}\Desktop",
        ]
