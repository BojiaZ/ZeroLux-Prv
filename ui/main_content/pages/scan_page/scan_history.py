from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QHeaderView, QPushButton,
    QDialog, QMessageBox
)
from PySide6.QtCore import Qt, Slot
from managers.history_manager import HistoryManager
from structs.actionresults import ActionResult


class ScanHistory(QWidget):
    """扫描历史记录页（只读）"""

    def __init__(self, history_mgr: HistoryManager, parent=None):
        super().__init__(parent)
        self.history_mgr = history_mgr
        self._build_ui()

    # ---------- public ----------
    def refresh(self):
        self.table.setRowCount(0)
        for e in self.history_mgr.entries:
            row = self.table.rowCount(); self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(e.id)))
            self.table.setItem(row, 1, QTableWidgetItem(e.start_time))
            self.table.setItem(row, 2, QTableWidgetItem(str(len(e.action_results))))

            btn = QPushButton("查看")
            if not e.action_results:
                btn.setDisabled(True)
            btn.clicked.connect(lambda _, entry=e: self._show_detail(entry))
            self.table.setCellWidget(row, 3, btn)

    # ---------- UI ----------
    def _build_ui(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(18)

        headers = ["ID", "时间", "检测发生", "详情"]
        self.table = QTableWidget(0, len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.NoSelection)
        self.table.setStyleSheet(
            "QTableWidget{background:#f4f5f7;color:#202529;font-size:14px;}"
            "QTableWidget::item{padding:8px;}"
            "QHeaderView::section{background:#f4f5f7;color:#202529;font-weight:bold;}"
        )
        lay.addWidget(self.table, 1)

    # ---------- detail dialog ----------
    def _show_detail(self, entry):
        if not entry.action_results:
            QMessageBox.information(self, "详情", "本次扫描未发现威胁")
            return

        dlg = QDialog(self); dlg.setWindowTitle("扫描详情")
        v = QVBoxLayout(dlg)

        hdr = ["文件路径", "原因", "动作", "状态", "错误"]
        tbl = QTableWidget(0, len(hdr))
        tbl.setHorizontalHeaderLabels(hdr)
        tbl.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        tbl.verticalHeader().setVisible(False)
        tbl.setEditTriggers(QTableWidget.NoEditTriggers)
        tbl.setStyleSheet(
            "QTableWidget{background:#f4f5f7;color:#202529;font-size:14px;}"
            "QTableWidget::item{padding:8px;}"
            "QHeaderView::section{background:#f4f5f7;color:#202529;font-weight:bold;}"
        )

        for a in entry.action_results:
            row = tbl.rowCount(); tbl.insertRow(row)
            tbl.setItem(row, 0, QTableWidgetItem(a.file_path))
            tbl.setItem(row, 1, QTableWidgetItem(a.reason))
            tbl.setItem(row, 2, QTableWidgetItem(a.recommend))
            tbl.setItem(row, 3, QTableWidgetItem("成功" if a.handled else "失败"))
            tbl.setItem(row, 4, QTableWidgetItem(a.error or ""))

        v.addWidget(tbl)
        dlg.resize(820, 420)
        dlg.exec()
