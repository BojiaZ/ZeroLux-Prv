# ui/pages/update_page/update_page.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui      import QPixmap, QPainter, QPen, QColor
from PySide6.QtCore     import Qt, QSize

# ---- 视觉常量 ----
PRIMARY      = "#009CA6"
CARD_BG      = "#FFFFFF"
CARD_BORDER  = "#e1e1e1"
CARD_RADIUS  = 16

def _draw_update_icon(size: int = 48) -> QPixmap:
    """
    动态绘制一个简易“更新”双箭头循环图标
    （同样可用于占位，无需外部资源）
    """
    pix = QPixmap(QSize(size, size))
    pix.fill(Qt.transparent)

    p = QPainter(pix)
    p.setRenderHint(QPainter.Antialiasing)
    pen = QPen(QColor(PRIMARY))
    pen.setWidth(3)
    p.setPen(pen)

    # 半圆箭头 1
    rect1 = pix.rect().adjusted(size*0.15, size*0.15,
                                -size*0.35, -size*0.35)
    p.drawArc(rect1, 30*16, 200*16)
    # 箭头尖
    p.drawLine(rect1.center().x()+size*0.25, rect1.top()+size*0.1,
               rect1.center().x()+size*0.1, rect1.top())

    # 半圆箭头 2（反向）
    rect2 = pix.rect().adjusted(size*0.35, size*0.35,
                                -size*0.15, -size*0.15)
    p.drawArc(rect2, 210*16, 200*16)
    p.drawLine(rect2.center().x()-size*0.25, rect2.bottom()-size*0.1,
               rect2.center().x()-size*0.1, rect2.bottom())

    p.end()
    return pix

class UpdatePage(QWidget):
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

        # 图标
        icon_lbl = QLabel()
        icon_lbl.setPixmap(_draw_update_icon())
        icon_lbl.setAlignment(Qt.AlignCenter)
        c_layout.addWidget(icon_lbl)

        # 主标题
        title_lbl = QLabel("更新中心")
        title_lbl.setAlignment(Qt.AlignCenter)
        title_lbl.setStyleSheet("font-size:18px; font-weight:600; color:#333;")
        c_layout.addWidget(title_lbl)

        # 副标题
        sub_lbl = QLabel("自动更新模块建设中")
        sub_lbl.setAlignment(Qt.AlignCenter)
        sub_lbl.setWordWrap(True)
        sub_lbl.setStyleSheet("font-size:12px; color:#777;")
        c_layout.addWidget(sub_lbl)

        root.addWidget(card)
