from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QProgressBar
from PySide6.QtCore import Signal

class ScanCard(QWidget):
    """展示一次扫描的进度 / 结果"""
    pause_clicked   = Signal(int)
    cancel_clicked  = Signal(int)
    show_log        = Signal(int)
    delete_requested= Signal(int)

    def __init__(self, record_id: int, mode: str):
        super().__init__()
        self.id = record_id
        self.mode = mode

        lay = QVBoxLayout(self)
        self.title = QLabel(f"{mode} 扫描进行中…")
        self.progress = QProgressBar()
        self.progress.setValue(0)

        btn_log = QPushButton("显示日志")
        btn_del = QPushButton("删除")

        btn_log.clicked.connect(lambda: self.show_log.emit(self.id))
        btn_del.clicked.connect(lambda: self.delete_requested.emit(self.id))

        lay.addWidget(self.title)
        lay.addWidget(self.progress)
        lay.addWidget(btn_log)
        lay.addWidget(btn_del)

    # --- API 被 ScanPage 调 ---
    def update_progress(self, p: int):
        self.progress.setValue(p)
        if p >= 100:
            self.title.setText(f"{self.mode} 扫描已完成 ✓")
