# ui/pages/settings_page/settings_page.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui      import QPixmap, QPainter, QPen, QColor
from PySide6.QtCore     import Qt, QSize

# ---- 视觉常量 ----
PRIMARY      = "#009CA6"
CARD_BG      = "#FFFFFF"
CARD_BORDER  = "#e1e1e1"
CARD_RADIUS  = 16

def _draw_lock_icon(size: int = 48) -> QPixmap:
    """绘制简易锁图标，与 Protection/Update 占位一致"""
    pix = QPixmap(QSize(size, size))
    pix.fill(Qt.transparent)

    painter = QPainter(pix)
    painter.setRenderHint(QPainter.Antialiasing)
    pen = QPen(QColor(PRIMARY))
    pen.setWidth(3)
    painter.setPen(pen)

    # 锁体
    body = pix.rect().adjusted(size*0.2, size*0.45, -size*0.2, -size*0.1)
    painter.drawRoundedRect(body, 6, 6)

    # 锁梁
    arc = pix.rect().adjusted(size*0.25, size*0.05, -size*0.25, size*0.45)
    painter.drawArc(arc, 30*16, 120*16)

    painter.end()
    return pix

class SettingsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        root = QVBoxLayout(self)
        root.setAlignment(Qt.AlignCenter)

        card = QWidget()
        card.setFixedSize(320, 180)
        card.setAttribute(Qt.WA_StyledBackground, True)
        card.setStyleSheet(f"""
            background:{CARD_BG};
            border:1px solid {CARD_BORDER};
            border-radius:{CARD_RADIUS}px;
        """)

        c_layout = QVBoxLayout(card)
        c_layout.setContentsMargins(24, 24, 24, 24)
        c_layout.setSpacing(12)
        c_layout.setAlignment(Qt.AlignCenter)

        # 锁图标
        icon_lbl = QLabel()
        icon_lbl.setPixmap(_draw_lock_icon())
        icon_lbl.setAlignment(Qt.AlignCenter)
        c_layout.addWidget(icon_lbl)

        # 主标题
        title_lbl = QLabel("设置")
        title_lbl.setAlignment(Qt.AlignCenter)
        title_lbl.setStyleSheet("font-size:18px; font-weight:600; color:#333;")
        c_layout.addWidget(title_lbl)

        # 副标题
        sub_lbl = QLabel("更多个性化选项敬请期待")
        sub_lbl.setAlignment(Qt.AlignCenter)
        sub_lbl.setWordWrap(True)
        sub_lbl.setStyleSheet("font-size:12px; color:#777;")
        c_layout.addWidget(sub_lbl)

        root.addWidget(card)
