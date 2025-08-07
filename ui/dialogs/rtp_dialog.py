# ui/dialog/rtp_dialog.py
from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt

class RTPDialog(QDialog):
    """安全弹窗：展示威胁信息 + 操作按钮"""

    def __init__(self, event: dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle("安全威胁告警")
        self.setMinimumWidth(400)
        self.event = event
        self._build_ui()

    def _build_ui(self):
        v = QVBoxLayout(self)
        v.setSpacing(18)

        title = QLabel(f"检测到威胁事件：{self.event.get('event_type', '未知')}")
        title.setStyleSheet("font-size:20px;font-weight:bold;color:#a00")
        v.addWidget(title)

        desc = QLabel(self.event.get("description", ""))
        desc.setWordWrap(True)
        desc.setStyleSheet("font-size:15px;")
        v.addWidget(desc)

        file_path = self.event.get("file_path", "")
        if file_path:
            fp = QLabel(f"<b>文件路径：</b>{file_path}")
            fp.setTextInteractionFlags(Qt.TextSelectableByMouse)
            v.addWidget(fp)

        btns = QHBoxLayout()
        for btn_txt in self.event.get("buttons", ["关闭"]):
            btn = QPushButton(btn_txt)
            btn.clicked.connect(lambda _, b=btn_txt: self._handle_btn(b))
            btns.addWidget(btn)
        v.addLayout(btns)

    def _handle_btn(self, btn_text):
        print(f"[RTPDialog] 用户点击按钮: {btn_text}")
        # 后续可以加信号/回调实现与主控通信
        self.accept()
