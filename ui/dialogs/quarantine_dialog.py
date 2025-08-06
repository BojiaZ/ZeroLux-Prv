# ui/dialogs/quarantine_dialog.py
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QHeaderView, QTableWidgetItem,
    QWidget, QHBoxLayout, QPushButton, QMessageBox, QAbstractItemView
)
from PySide6.QtCore import Qt
from PySide6.QtGui  import QPalette

from quarantine.quarantine_route import QuarantineRoute
from structs.actionresults import ActionResult


class QuarantineDialog(QDialog):
    """隔离区弹窗：原路径 / 状态 / 行内操作"""

    def __init__(self, q_route: QuarantineRoute, parent=None):
        super().__init__(parent)
        self.setWindowTitle("隔离区")
        self.resize(900, 520)

        self.q_route = q_route
        self._build_ui()

        # —— 信号 ——（实时刷新）
        q_route.signal_quarantine_list.connect(self._load)
        q_route.signal_quarantine_action_result.connect(self._on_action_result)
        q_route.signal_quarantine_action_finished.connect(
            lambda: self._load(self.q_route.items)
        )

   # ---------------- UI ----------------
    def _build_ui(self):
        v = QVBoxLayout(self)
        v.setContentsMargins(32, 24, 32, 24)
        v.setSpacing(18)


        # 新表头 4 列
        headers = ["原路径", "原因", "状态 / 错误", "操作"]
        self.tbl = QTableWidget(0, len(headers))
        self.tbl.setHorizontalHeaderLabels(headers)

        # 列宽：0、1 自适应；2 固定 120；3 ResizeToContents
        self.tbl.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tbl.setColumnWidth(1, 120)
        self.tbl.setColumnWidth(2, 80)
        self.tbl.setColumnWidth(3, 100)

        self.tbl.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tbl.setSelectionMode(QAbstractItemView.NoSelection)
        self.tbl.verticalHeader().setVisible(False)
        self.tbl.verticalHeader().setDefaultSectionSize(35)
        self.tbl.setStyleSheet(
            "QTableWidget{background:#f4f5f7;color:#202529;font-size:14px;}"
            "QTableWidget::item{padding:6px;}"
            "QHeaderView::section{background:#f4f5f7;color:#202529;font-weight:bold;}"
        )
        v.addWidget(self.tbl, 1)

    # ------------- 数据加载 -------------
    def open_and_refresh(self):
        self.q_route.get_quarantine_list()
        self.exec()

    # ------------- 数据加载 -------------
    def _load(self, items: list[ActionResult]):
        self.tbl.setRowCount(0)
        for ar in items:
            r = self.tbl.rowCount()
            self.tbl.insertRow(r)

            self.tbl.setItem(r, 0, QTableWidgetItem(ar.origin_path or "—"))
            self.tbl.setItem(r, 1, QTableWidgetItem(ar.reason or "—"))

            status = "成功" if ar.handled else f"失败: {ar.error}"
            self.tbl.setItem(r, 2, QTableWidgetItem(status))

            # 行内按钮
            cell = QWidget(); h = QHBoxLayout(cell)
            h.setContentsMargins(0, 0, 0, 0); h.setSpacing(4)
            btn_rest = self._mk_btn("还原", lambda _, x=ar: self._restore(x))
            btn_del  = self._mk_btn("删除", lambda _, x=ar: self._delete(x))
            h.addWidget(btn_rest); h.addWidget(btn_del); h.addStretch()
            self.tbl.setCellWidget(r, 3, cell)

    # ------------- 操作 -------------
    def _restore(self, ar: ActionResult):
        self.q_route.restore_items([ar])

    def _delete(self, ar: ActionResult):
        if self._confirm("确定永久删除选中文件？此操作不可恢复！"):
            self.q_route.delete_items([ar])

    # ------------- 回调 -------------
    def _on_action_result(self, ar: ActionResult, ok: bool, msg: str):
        # 直接刷新整表
        self._load(self.q_route.items)

    # ------------- 辅助 -------------
    def _mk_btn(self, text, slot):
        btn = QPushButton(text)
        btn.setFixedSize(40, 18)
        btn.clicked.connect(slot)
        btn.setStyleSheet("QPushButton{background:#eafafd;color:#15bcc6;"
                          "border:1px solid #15bcc6;border-radius:4px;"
                          "font-size:13px;}"
                          "QPushButton:hover{background:#b8f1fc;}")
        return btn

    # ------------- 辅助 -------------
    def _confirm(self, msg) -> bool:
        box = QMessageBox(self)
        box.setWindowTitle("确认")
        box.setText(msg)
        box.setIcon(QMessageBox.Question)
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        pal = box.palette()
        pal.setColor(QPalette.Text,        Qt.black)
        pal.setColor(QPalette.WindowText,  Qt.black)
        pal.setColor(QPalette.ButtonText,  Qt.black)   # ★ Yes/No 按钮文字
        box.setPalette(pal)

        # 保险起见再用 stylesheet 强制
        box.setStyleSheet("QLabel{color:black;} QPushButton{color:black;}")

        return box.exec() == QMessageBox.Yes