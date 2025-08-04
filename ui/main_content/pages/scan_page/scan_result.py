from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor


class ScanResultPage(QWidget):
    """结果页

    • 根据扫描是否被 *用户终止* / *自然完成*、以及是否发现威胁，动态展示：
        1. 居中大字提示
        2. （可选）威胁文件表格
        3. 『完成』按钮返回扫描选择页
    """

    back_requested = Signal()   # 点击『完成』后发射，由 ScanPage 切回选择页

    def __init__(self, parent=None):
        super().__init__(parent)

        self.vbox = QVBoxLayout(self)
        self.vbox.setContentsMargins(32, 32, 32, 24)
        self.vbox.setSpacing(24)

        # --- 提示大字 ---
        self.lab_msg = QLabel()
        self.lab_msg.setAlignment(Qt.AlignCenter)
        self.lab_msg.setStyleSheet("font-size:24px;font-weight:bold;color:#202529")
        self.vbox.addWidget(self.lab_msg)

        # --- 威胁表格 ---
        self.table = QTableWidget(0, 2, self)
        self.table.setHorizontalHeaderLabels(["文件路径", "威胁类型"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.NoSelection)
        self.table.setStyleSheet(
            "QTableWidget{background:#f4f5f7;color:#202529;font-size:14px;}"
            "QTableWidget::item{padding:8px;}"
            "QHeaderView::section{background:#f4f5f7;color:#202529;font-weight:bold;}"
        )
        self.vbox.addWidget(self.table, 5)

        # --- 完成按钮 ---
        btn_done = QPushButton("完成")
        btn_done.setFixedSize(100, 34)
        btn_done.setStyleSheet(
            "QPushButton{background:#15bcc6;color:white;font-weight:bold;border:none;border-radius:6px;}"
            "QPushButton:hover{background:#1198a1;}"
        )
        btn_done.clicked.connect(self.back_requested)
        h = QHBoxLayout(); h.addStretch(); h.addWidget(btn_done); h.addStretch()
        self.vbox.addLayout(h)

    # ------------------------------------------------------------------
    def load_data(self, results, stopped: bool):
        """由 ScanPage 调用。

        Parameters
        ----------
        results : list[ScanResult]
            扫描过程中收集的结果列表
        stopped : bool
            True  → 用户主动点击『停止』\n
            False → 线程自然跑完
        """
        threats = [r for r in results if getattr(r, "detected", False)]

        # 1️⃣ 顶部提示信息
        if stopped:
            self.lab_msg.setText("扫描被用户终止")
        elif threats:
            self.lab_msg.setText("扫描完成，发现威胁")
        else:
            self.lab_msg.setText("扫描完成，未发现威胁")

        # 2️⃣ 表格填充（仅当有威胁时显示）
        self.table.setRowCount(0)
        if threats:
            red = QColor("#c85151")
            for r in threats:
                row = self.table.rowCount(); self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(r.file_path))
                item = QTableWidgetItem(r.threat_type)
                item.setForeground(red)
                self.table.setItem(row, 1, item)
            self.table.show()
        else:
            self.table.hide()
