from PySide6.QtCore import QObject, Signal, Slot
from scans.scans_traverser import Traverser
import os

def expand_user_paths(patterns):
    # 自动将 %USERNAME% 替换成实际用户名
    username = os.getlogin()
    return [p.replace("%USERNAME%", username) for p in patterns]

class ScanRoute(QObject):
    """
    扫描路由器（调度器）

    职责：
        - 根据UI请求（模式/路径）启动遍历扫描线程（Traverser）
        - 控制扫描线程的启动、暂停、恢复、停止
        - 监听Traverser发射的信号并转发给UI/scanpage
        - 管理线程生命周期，支持多次启动

    发送的信号：
        - signal_progress(object): 单个TraverseProgress实例，实时进度
        - signal_scan_result(object): 单个ScanResult实例，实时结果
        - signal_scan_finished(): 扫描完成信号
        - signal_scan_all_results(list): 全部扫描结果，list[ScanResult]

    接收的信号：
        - Traverser.signal_progress(object): 转发为本类的signal_progress
        - Traverser.signal_scan_result(object): 转发为本类的signal_scan_result
        - Traverser.signal_scan_finished(): 转发为本类的signal_scan_finished
        - Traverser.signal_scan_all_results(list): 转发为本类的signal_scan_all_results

    方法：
        - start_scan(mode: str, custom_path: str = None)
        - pause_scan()
        - resume_scan()
        - stop_scan()
    """

    signal_progress = Signal(object)
    signal_scan_result = Signal(object)
    signal_scan_finished = Signal()
    signal_scan_all_results = Signal(list)  # 新增批量结果信号

    def __init__(self):
        super().__init__()
        self.traverser = None  # 当前扫描线程对象
    
    

    @Slot(str, str)
    def start_scan(self, mode: str, custom_path: str = None):
        """
        根据模式启动扫描任务。

        Args:
            mode (str): 扫描模式（'full', 'smart', 'custom'）
            custom_path (str): 自定义扫描路径（仅当mode='custom'时用）
        """
        # 路径选择逻辑
        if mode == "full":
            paths = [f"{chr(d)}:\\" for d in range(67, 91) if os.path.exists(f"{chr(d)}:\\")]
        elif mode == "smart":
            smart_patterns = [
                r"C:\Windows",
                r"C:\Windows\System32",
                r"C:\Program Files",
                r"C:\Program Files (x86)",
                r"C:\Users",
                r"C:\Users\Public",
                r"C:\Users\%USERNAME%\AppData",
                r"C:\Users\%USERNAME%\Desktop",
                r"C:\Users\%USERNAME%\Downloads",
                r"C:\Users\%USERNAME%\Documents"
            ]
            paths = expand_user_paths(smart_patterns)
        elif mode == "custom" and custom_path:
            paths = [custom_path]
        else:
            paths = ["C:\\"]
        
        # 若有旧扫描线程，先停掉并回收
        if self.traverser is not None:
            self.traverser.stop()
            self.traverser.wait()

        # 新建扫描线程
        self.traverser = Traverser()
        self.traverser.set_params(paths)
        # 信号转发给外部
        self.traverser.signal_progress.connect(self.signal_progress)
        self.traverser.signal_scan_result.connect(self.signal_scan_result)
        self.traverser.signal_scan_finished.connect(self.signal_scan_finished)
        self.traverser.signal_scan_all_results.connect(self.signal_scan_all_results)  # 新增
        self.traverser.start()  # 启动线程扫描

    @Slot()
    def pause_scan(self):
        """暂停扫描"""
        if self.traverser is not None:
            self.traverser.pause()

    @Slot()
    def resume_scan(self):
        """恢复扫描"""
        if self.traverser is not None:
            self.traverser.resume()

    @Slot()
    def stop_scan(self):
        """停止扫描"""
        if self.traverser is not None:
            self.traverser.stop()
