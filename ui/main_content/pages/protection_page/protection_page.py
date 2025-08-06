# ui/pages/protection_page/protection_page.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
)
from PySide6.QtCore import Qt

from ui.dialogs.quarantine_dialog import QuarantineDialog
from quarantine.quarantine_route  import QuarantineRoute


class ProtectionPage(QWidget):
    def __init__(self, quarantine_route: QuarantineRoute, parent=None):
        super().__init__(parent)
        self.quarantine_route = quarantine_route                # 保存路由器引用

        # ====== 根布局（如果你已有 root，就用现成的） ======
        root = QVBoxLayout(self)
        root.setContentsMargins(32, 32, 32, 24)
        root.setSpacing(18)

        # 👉 这里放你原本的“实时防护状态”组件 / 开关 / 描述 ... ...

        root.addStretch()                     # 把“隔离区”按钮顶到最下方

        # ====== 按钮栏 ======
        btn_row = QHBoxLayout()
        btn_row.addStretch()                  # 靠右
        btn_quar = QPushButton("隔离区")
        btn_quar.setFixedSize(100, 32)
        btn_quar.setStyleSheet(
            "QPushButton{background:#eafafd;color:#15bcc6;border:2px solid #15bcc6;"
            "border-radius:6px;font-weight:bold;}"
            "QPushButton:hover{background:#b8f1fc;}"
        )
        btn_quar.clicked.connect(self._open_quarantine)

        btn_row.addWidget(btn_quar)
        root.addLayout(btn_row)

    # ---------- 槽：弹出隔离区对话框 ----------
    def _open_quarantine(self):
        dlg = QuarantineDialog(self.quarantine_route, self)
        dlg.open_and_refresh()      # 先刷新再 exec()
