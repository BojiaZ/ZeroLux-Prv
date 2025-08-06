from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy
from PySide6.QtSvgWidgets import QSvgWidget
from .function_card import FunctionCard   # <—— 关键
from managers.log_manager import LogManager
from ui.dialogs.log_dialog import LogDialog

class OverviewPage(QWidget):
    actionRequested = Signal(str)  # "scan" / "update" / "report"

    def __init__(self, log_mgr: LogManager, parent=None):
        super().__init__(parent)

        self.log_mgr = log_mgr 

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 32, 20, 32)
        layout.setSpacing(28)

        status_card = QFrame()
        status_card.setFixedHeight(120)
        status_card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        status_card.setStyleSheet("background: transparent; border: none;")
        layout.addWidget(status_card)

        status_layout = QHBoxLayout(status_card)
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_layout.setSpacing(0)

        svg = QSvgWidget("resources/pages/status_safe.svg")
        svg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        status_layout.addWidget(svg)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(32)
        btn_layout.setAlignment(Qt.AlignCenter)

        card_scan = FunctionCard("resources/overview/scan_blue.svg", "计算机扫描", "按需扫描计算机", key="scan")
        card_update = FunctionCard("resources/overview/update.svg", "更新组件", "同步病毒库和组件", key="update")
        card_report = FunctionCard("resources/overview/report.svg", "安全报告", "查看最近安全活动", key="report")

        card_scan.clicked.connect(self.actionRequested)
        card_update.clicked.connect(self.actionRequested)
        # --- 把 report 同时连到信号 & 本地槽 ---
        card_report.clicked.connect(self.actionRequested)
        card_report.clicked.connect(self._show_log_dialog)

        btn_layout.addWidget(card_scan)
        btn_layout.addWidget(card_update)
        btn_layout.addWidget(card_report)

        layout.addLayout(btn_layout)
        layout.addStretch()

    def _show_log_dialog(self):
        dlg = LogDialog(self.log_mgr, self)
        dlg.exec()            # 弹窗内会先 refresh()