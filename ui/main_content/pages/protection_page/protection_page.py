# ui/pages/protection_page/protection_page.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui      import QPixmap, QPainter, QPen, QColor
from PySide6.QtCore     import Qt, QSize

# ---- 视觉常量 ----
PRIMARY      = "#009CA6"
CARD_BG      = "#FFFFFF"
CARD_BORDER  = "#e1e1e1"
CARD_RADIUS  = 16

def _generate_lock_icon(size: int = 48) -> QPixmap:
    """动态绘制简易锁图标，返回 QPixmap（透明背景）"""
    pix = QPixmap(QSize(size, size))
    pix.fill(Qt.transparent)

    painter = QPainter(pix)
    painter.setRenderHint(QPainter.Antialiasing)
    pen = QPen(QColor(PRIMARY))
    pen.setWidth(3)
    painter.setPen(pen)

    # 锁体矩形
    body = pix.rect().adjusted(size*0.2, size*0.45, -size*0.2, -size*0.1)
    painter.drawRoundedRect(body, 6, 6)

    # 锁梁圆弧
    arc = pix.rect().adjusted(size*0.25, size*0.05, -size*0.25, size*0.45)
    painter.drawArc(arc, 30*16, 120*16)   # 起止角 *16（Qt 单位）

    painter.end()
    return pix

class ProtectionPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # ---- 整体居中 ----
        root = QVBoxLayout(self)
        root.setAlignment(Qt.AlignCenter)

        # ---- 占位卡片 ----
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

        # 图标
        icon_lbl = QLabel()
        icon_lbl.setPixmap(_generate_lock_icon())
        icon_lbl.setAlignment(Qt.AlignCenter)
        c_layout.addWidget(icon_lbl)

        # 标题
        title_lbl = QLabel("实时防护")
        title_lbl.setAlignment(Qt.AlignCenter)
        title_lbl.setStyleSheet("font-size:18px; font-weight:600; color:#333;")
        c_layout.addWidget(title_lbl)

        # 副标题
        sub_lbl = QLabel("该功能正在开发中")
        sub_lbl.setAlignment(Qt.AlignCenter)
        sub_lbl.setWordWrap(True)
        sub_lbl.setStyleSheet("font-size:12px; color:#777;")
        c_layout.addWidget(sub_lbl)

        # 把卡片放到页面中心
        root.addWidget(card)
