from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PySide6.QtSvgWidgets import QSvgWidget

class FunctionCard(QFrame):
    """可复用功能卡片。hover 缩放图标，显示描述。点击发射 clicked(key) 信号。"""
    clicked = Signal(str)   # 例如 "scan" / "update" / "report"

    def __init__(self, icon_path: str, title: str, desc: str,
                 key: str | None = None, parent=None):
        super().__init__(parent)
        self._key = key or title

        self.setFixedSize(180, 180)
        self._set_normal_style()

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(10)

        self.icon = QSvgWidget(icon_path)
        self.icon.setFixedSize(48, 48)
        layout.addWidget(self.icon)

        self.title = QLabel(title)
        self.title.setStyleSheet(
            "font-size: 17px; font-weight: 700; color: #222; "
            "border: none; background: transparent;")
        layout.addWidget(self.title)

        self.desc = QLabel(desc)
        self.desc.setVisible(False)
        self.desc.setWordWrap(True)
        self.desc.setAlignment(Qt.AlignHCenter)
        self.desc.setStyleSheet(
            "font-size: 15px; font-weight: 700; color: #888; "
            "border: none; background: transparent;")
        layout.addWidget(self.desc)

    # --- hover 效果 ---
    def enterEvent(self, event):
        self.icon.setFixedSize(40, 40)
        self.desc.setVisible(True)
        self._set_hover_style()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.icon.setFixedSize(48, 48)
        self.desc.setVisible(False)
        self._set_normal_style()
        super().leaveEvent(event)

    # --- 点击 ---
    def mousePressEvent(self, event):
        # 需要按下就触发就保留 press；若想防抖改为 mouseReleaseEvent。
        self.clicked.emit(self._key)
        super().mousePressEvent(event)

    # --- 样式 ---
    def _set_normal_style(self):
        self.setStyleSheet("""
            QFrame {
                background: #f5f7fb;
                border-radius: 18px;
                border: 1.5px solid #e7e9f0;
            }
        """)

    def _set_hover_style(self):
        self.setStyleSheet("""
            QFrame {
                background: transparent;
                border-radius: 18px;
                border: 1.5px solid #b0d8f5;
            }
        """)
