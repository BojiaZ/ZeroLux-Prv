from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QTableWidget, QHeaderView, QTableWidgetItem
)
from PySide6.QtCore import Qt
from managers.log_manager import LogManager
import json
from structs.log_entry import LogEntry


class LogDialog(QDialog):
    """安全日志弹窗：时间 / 路径 / 组件 / 事件类型 / 摘要"""

    def __init__(self, log_mgr: LogManager, parent=None):
        super().__init__(parent)
        self.setWindowTitle("安全日志")
        self.resize(860, 520)
        self.log_mgr = log_mgr
        self._build_ui()
        self.refresh()  # 初次加载
        # 若想实时刷新，可打开下面这行
        self.log_mgr.signal_new_log.connect(self.refresh)

    # ---------- UI ----------
    def _build_ui(self):
        v = QVBoxLayout(self)
        v.setContentsMargins(32, 24, 32, 24)
        v.setSpacing(18)

        title = QLabel("安全日志")
        title.setStyleSheet("font-size:22px;font-weight:bold;color:#202529")
        v.addWidget(title)

        hdrs = ["时间", "路径", "组件", "事件类型", "摘要"]
        self.tbl = QTableWidget(0, len(hdrs))
        self.tbl.setHorizontalHeaderLabels(hdrs)

        self.tbl.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tbl.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tbl.setColumnWidth(2, 80)
        self.tbl.setColumnWidth(3, 90)
        self.tbl.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)

        self.tbl.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.tbl.verticalHeader().setVisible(False)
        self.tbl.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tbl.setSelectionMode(QTableWidget.NoSelection)
        self.tbl.verticalHeader().setDefaultSectionSize(30)
        self.tbl.setStyleSheet(
            "QTableWidget{background:#f4f5f7;color:#202529;font-size:14px;}"
            "QTableWidget::item{padding:8px;}"
            "QHeaderView::section{background:#f4f5f7;color:#202529;font-weight:bold;}"
        )
        v.addWidget(self.tbl, 1)

        self.refresh()           # 初次加载

    # ---------- 数据 ----------
    def refresh(self):
        # 每次刷新都从文件读取最新日志
        path = self.log_mgr.path
        if path.exists():
            raw = json.loads(path.read_text(encoding="utf-8"))
            entries = [LogEntry(**d) for d in raw]
        else:
            entries = []
        self.tbl.setRowCount(0)
        for e in entries:
            r = self.tbl.rowCount(); self.tbl.insertRow(r)
            self.tbl.setItem(r, 0, QTableWidgetItem(e.timestamp))
            self.tbl.setItem(r, 1, QTableWidgetItem(e.path or "—"))
            self.tbl.setItem(r, 2, QTableWidgetItem(e.component))
            self.tbl.setItem(r, 3, QTableWidgetItem(e.event_type))
            self.tbl.setItem(r, 4, QTableWidgetItem(e.summary))

    