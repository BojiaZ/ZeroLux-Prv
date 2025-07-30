from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QGraphicsDropShadowEffect
)
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, QDateTime, Signal

CARD_BG     = "#ECEFF3"
CARD_BORDER = "#dfe3e8"
CARD_RADIUS = 12
CARD_SHADOW = "0 2px 6px rgba(0,0,0,0.08)"
PRIMARY     = "#009CA6"
TEXT_MAIN   = "#222"
TEXT_SECOND = "#555"
ICON_DIR = "resources/icons/scan_page/{}"

class ResultCard(QWidget):
    remove_clicked = Signal(int)
    show_log = Signal(int)

    def __init__(self, record_id: int, mode: str,
                 found: int, engine_ver: str,
                 dt: QDateTime, status: str):
        super().__init__()
        self.id = record_id

        # — 卡片外观 —
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(f"""
            background:{CARD_BG};
            border:1px solid {CARD_BORDER};
            border-radius:{CARD_RADIUS}px;
        """)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(12)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)
        self.setFixedWidth(576)
        self.setFixedHeight(189)
        
        # — 主体布局 —
        self.stack = QVBoxLayout(self)
        self._build_result_page(mode, found, engine_ver, dt, status)

    def _build_result_page(self, mode, found, engine_ver, dt, status):
        root = QVBoxLayout()
        root.setContentsMargins(24, 18, 24, 18)
        root.setSpacing(12)

        # 顶行：图标+标题+时间
        top = QHBoxLayout()
        icon_name = "alert.svg" if found > 0 else "check.svg"
        icon = QSvgWidget(ICON_DIR.format(icon_name))
        icon.setStyleSheet("background:transparent; border:none")
        icon.setFixedSize(20, 20)
        top.addWidget(icon)

        title = QLabel(self._mode_zh(mode))
        title.setStyleSheet("font-size:16px; border:none; font-weight:600;color:"+TEXT_MAIN)
        top.addWidget(title)
        top.addStretch()

        ts = QLabel(dt.toString("yyyy/M/d  HH:mm:ss"))
        ts.setStyleSheet("font-size:12px; border:none; color:"+TEXT_SECOND)
        top.addWidget(ts)
        root.addLayout(top)

        # 状态描述
        desc_text = "扫描被用户中断" if status == "canceled" else "扫描完成"
        self.lbl_status = QLabel(desc_text)
        self.lbl_status.setStyleSheet("font-size:14px; border:none; color:"+TEXT_MAIN)
        root.addWidget(self.lbl_status)

        # 检测结果/引擎
        self.lbl_detail = QLabel(f"检测发生: {found}\n使用的检测引擎: {engine_ver}")
        self.lbl_detail.setStyleSheet("font-size:12px; border:none; color:"+TEXT_SECOND)
        root.addWidget(self.lbl_detail)

        # 底行：日志+解除
        bottom = QHBoxLayout()
        btn_log = QPushButton("显示日志")
        btn_log.setCursor(Qt.PointingHandCursor)
        btn_log.setStyleSheet(f"""
            QPushButton{{color:{PRIMARY};border:none;background:transparent;font-size:13px}}
            QPushButton:hover{{text-decoration:underline}}
        """)
        btn_log.clicked.connect(lambda: self.show_log.emit(self.id))
        bottom.addWidget(btn_log)
        bottom.addStretch()

        btn_remove = QPushButton("解除")
        btn_remove.setCursor(Qt.PointingHandCursor)
        btn_remove.setStyleSheet(f"""
            QPushButton{{
                background:#f3f7fa;
                color:{PRIMARY};
                border-radius:6px;
                border:none;
                font-size:14px;
                padding:8px 18px;
            }}
            QPushButton:hover{{background:#e0eef2;}}
        """)
        btn_remove.clicked.connect(lambda: self.remove_clicked.emit(self.id))
        bottom.addWidget(btn_remove)
        root.addLayout(bottom)

        self.stack.addLayout(root)

    def _mode_zh(self, m):
        return {"smart":"智能扫描","full":"计算机扫描",
                "custom":"自定义扫描","removable":"移动磁盘扫描"}.get(m, m)
