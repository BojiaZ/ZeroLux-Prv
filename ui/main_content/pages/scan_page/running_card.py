# ui/pages/scan_page/scan_card.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QToolButton, QProgressBar, QPushButton, QGraphicsDropShadowEffect
)
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtGui  import QIcon, QColor
from PySide6.QtCore import Qt, QDateTime, Signal, QSize

# ===== 视觉常量 =====
CARD_BG     = "#ECEFF3"
CARD_BORDER = "#dfe3e8"
CARD_RADIUS = 12
CARD_SHADOW = "0 2px 6px rgba(0,0,0,0.08)"
PRIMARY     = "#009CA6"
TEXT_MAIN   = "#222"
TEXT_SECOND = "#555"

ICON_DIR = "resources/icons/scan_page/{}"   # scan.svg 等

BTN_QSS = f"""
QToolButton {{
    background: {PRIMARY};
    border: none;
    border-radius: 4px;
    padding: 6px;
}}
QToolButton:hover {{
    background: #008b9b;
}}
"""


class RunningCard(QWidget):
    pause_clicked  = Signal(int)
    resume_clicked = Signal(int)
    cancel_clicked = Signal(int)
    show_log       = Signal(int)

    def __init__(self, record_id: int, scan_mode: str):
        super().__init__()
        self.id = record_id
        self.state = "running"   # 支持暂停/恢复切换

        self.mode = scan_mode

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

        self.stack = QVBoxLayout(self)
        self._build_running_page(scan_mode)

    def _build_running_page(self, mode:str):
        root = QVBoxLayout()
        root.setContentsMargins(24, 18, 24, 18)
        root.setSpacing(12)

        # 顶行 : 图标 + 标题 + 时间 + 操作按钮
        top = QHBoxLayout()
        icon = QSvgWidget(ICON_DIR.format("scan.svg"))
        icon.setStyleSheet(f"background:transparent; border:none")
        icon.setFixedSize(20, 20)
        top.addWidget(icon)

        title = QLabel(self._mode_zh(mode))
        title.setStyleSheet("font-size:16px; border:none; font-weight:600;color:"+TEXT_MAIN)
        top.addWidget(title)
        top.addStretch()

        ts = QLabel(QDateTime.currentDateTime().toString("yyyy/M/d  HH:mm:ss"))
        ts.setStyleSheet("font-size:12px; border:none; color:"+TEXT_SECOND)
        top.addWidget(ts)

        # ▶/⏸ toggle
        self.btn_toggle = QToolButton()
        self._set_toggle_icon("pause")
        self.btn_toggle.setCursor(Qt.PointingHandCursor)
        self.btn_toggle.setStyleSheet(BTN_QSS)
        self.btn_toggle.clicked.connect(self._toggle_pause_resume)
        top.addWidget(self.btn_toggle)

        # × cancel
        btn_cancel = QToolButton()
        btn_cancel.setIcon(QIcon(ICON_DIR.format("cancel.svg")))
        btn_cancel.setIconSize(QSize(16, 16))
        btn_cancel.setCursor(Qt.PointingHandCursor)
        btn_cancel.setStyleSheet(BTN_QSS)
        btn_cancel.clicked.connect(lambda: self.cancel_clicked.emit(self.id))
        top.addWidget(btn_cancel)

        root.addLayout(top)

        # 状态行（显示进度和路径）
        self.lbl_status = QLabel("扫描进行中… 0%")
        self.lbl_status.setStyleSheet("font-size:14px; border:none; color:"+TEXT_MAIN)
        self.lbl_path = QLabel("")
        self.lbl_path.setStyleSheet("font-size:12px; border:none; color:"+TEXT_SECOND)
        root.addWidget(self.lbl_status)
        root.addWidget(self.lbl_path)

        # 进度条
        self.bar = QProgressBar()
        self.bar.setRange(0, 100)
        self.bar.setValue(0)
        self.bar.setTextVisible(False)
        self.bar.setFixedHeight(6)
        self.bar.setStyleSheet(f"""
            QProgressBar{{background:transparent;border:none;border-radius:3px}}
            QProgressBar::chunk{{background:{PRIMARY};border-radius:3px}}
        """)
        root.addWidget(self.bar)

        # 底行：详情 + “显示日志”
        bottom = QHBoxLayout()
        self.lbl_detail = QLabel("检测发生: 0")
        self.lbl_detail.setStyleSheet("font-size:12px; border:none; color:"+TEXT_SECOND)
        bottom.addWidget(self.lbl_detail)
        bottom.addStretch()

        btn_log = QPushButton("显示日志")
        btn_log.setCursor(Qt.PointingHandCursor)
        btn_log.setStyleSheet(f"""
            QPushButton{{color:{PRIMARY};border:none;background:transparent;font-size:13px}}
            QPushButton:hover{{text-decoration:underline}}
        """)
        btn_log.clicked.connect(lambda: self.show_log.emit(self.id))
        bottom.addWidget(btn_log)

        root.addLayout(bottom)
        self.stack.addLayout(root)

    # —— 公共接口 ————————————————————
    def update_progress(self, percent: int, path: str):
        if percent > 100:
            percent = 100
        self.bar.setValue(percent)
        self.lbl_status.setText(f"扫描进行中… {percent}%")
        self.lbl_path.setText(path if path else "")

    def set_paused(self, paused: bool):
        if paused:
            self.state = "paused"
            self._set_toggle_icon("resume")
            self.lbl_status.setText("已暂停")
        else:
            self.state = "running"
            percent = self.bar.value()
            self._set_toggle_icon("pause")
            self.lbl_status.setText(f"扫描进行中… {percent}%")

    # —— 工具 ————————————————————————
    def _mode_zh(self, mode):
        return {"smart":"智能扫描","full":"计算机扫描",
                "custom":"自定义扫描","removable":"移动磁盘扫描"}.get(mode, mode)

    def _set_toggle_icon(self, name: str):
        self.btn_toggle.setIcon(QIcon(ICON_DIR.format(f"{name}.svg")))
        self.btn_toggle.setIconSize(QSize(16, 16))

    def _toggle_pause_resume(self):
        if self.state == "running":
            self.state = "paused"
            self._set_toggle_icon("resume")
            self.lbl_status.setText("已暂停")
            self.pause_clicked.emit(self.id)
        elif self.state == "paused":
            self.state = "running"
            self._set_toggle_icon("pause")
            percent = self.bar.value()
            self.lbl_status.setText(f"扫描进行中… {percent}%")
            self.resume_clicked.emit(self.id)
    
    