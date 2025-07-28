# ui/pages/scan_page/scan_card.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QProgressBar, QSizePolicy, QSpacerItem
)
from PySide6.QtCore import Qt, Signal, QDateTime

# ───────── 视觉常量 ─────────
PRIMARY       = "#009CA6"
CARD_BG       = "rgba(245,247,250,0.85)"    # 淡灰 + 15% 透明
CARD_BORDER   = "#d8dce2"
CARD_SHADOW   = "0 1px 4px rgba(0,0,0,0.06)"
CARD_RADIUS   = 10
TEXT_MAIN     = "#222"
TEXT_SECOND   = "#666"

class ScanCard(QWidget):
    """一次扫描记录卡片（ESET 风）"""
    show_log         = Signal(int)
    delete_requested = Signal(int)

    def __init__(self, record_id: int, mode: str):
        super().__init__()
        self.id   = record_id
        self.mode = mode

        # ︙ UI 自身样式
        self.setStyleSheet(f"""
            background: {CARD_BG};
            border: 1px solid {CARD_BORDER};
            border-radius: {CARD_RADIUS}px;
            box-shadow: {CARD_SHADOW};
        """)
        self.setAutoFillBackground(True)

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 14, 20, 14)
        root.setSpacing(10)

        # ─── 第一行：√ 图标 + 标题 + 时间 ───
        h_top = QHBoxLayout()
        tick  = QLabel("✔")
        tick.setStyleSheet("color:#3aa31b; font-size:22px;")
        h_top.addWidget(tick)

        self.title = QLabel(f"{self._mode_zh(mode)}")
        self.title.setStyleSheet(f"font-size:16px; color:{TEXT_MAIN}; font-weight:600;")
        h_top.addWidget(self.title)

        h_top.addStretch()

        ts = QDateTime.currentDateTime().toString("yyyy/M/d  HH:mm:ss")
        self.time_label = QLabel(ts)
        self.time_label.setStyleSheet(f"font-size:12px; color:{TEXT_SECOND};")
        h_top.addWidget(self.time_label)

        root.addLayout(h_top)

        # ─── 第二行：状态行 ───
        self.status = QLabel("扫描完成")
        self.status.setStyleSheet(f"font-size:14px; color:{TEXT_MAIN};")
        root.addWidget(self.status)

        # ─── 第三行：进度条 ───
        self.progress = QProgressBar()
        self.progress.setFixedHeight(8)
        self.progress.setRange(0, 100)
        self.progress.setValue(100)        # 默认完成
        self.progress.setTextVisible(False)
        self.progress.setStyleSheet(f"""
            QProgressBar {{
                background: transparent;
                border-radius:4px;
            }}
            QProgressBar::chunk {{
                background:{PRIMARY};
                border-radius:4px;
            }}
        """)
        root.addWidget(self.progress)

        # ─── 第四行：细节 + 右侧操作按钮 ───
        h_bot = QHBoxLayout()

        self.detail = QLabel("检测发生: 0\n使用的检测引擎: 31597 (20250728)")
        self.detail.setStyleSheet(f"font-size:13px; color:{TEXT_SECOND}; line-height:18px;")
        h_bot.addWidget(self.detail)

        h_bot.addStretch()

        self.btn_delete = QPushButton("解除")
        self.btn_delete.setCursor(Qt.PointingHandCursor)
        self.btn_delete.setStyleSheet(f"""
            QPushButton {{
                background:#e8eef7;
                padding:5px 18px;
                border-radius:6px;
                color:{PRIMARY};
                border:none;
            }}
            QPushButton:hover {{ background:#e0e8f2; }}
        """)
        self.btn_delete.clicked.connect(lambda: self.delete_requested.emit(self.id))
        h_bot.addWidget(self.btn_delete)

        root.addLayout(h_bot)

        # ─── 展示日志链接 ───
        link = QPushButton("显示日志")
        link.setCursor(Qt.PointingHandCursor)
        link.setStyleSheet(f"""
            QPushButton {{
                color:{PRIMARY};
                border:none;
                background:transparent;
                font-size:14px;
            }}
            QPushButton:hover {{ text-decoration: underline; }}
        """)
        link.clicked.connect(lambda: self.show_log.emit(self.id))
        root.addWidget(link, alignment=Qt.AlignLeft)

    # ──────────────────────────────────────────
    # Public API
    def update_progress(self, percent: int):
        self.progress.setValue(percent)
        if percent >= 100:
            self.status.setText("扫描完成")
        else:
            self.status.setText(f"扫描进行中… {percent}%")

    def _mode_zh(self, mode: str) -> str:
        mapping = {"quick":"快速扫描", "full":"计算机扫描",
                   "custom":"自定义扫描", "removable":"移动磁盘扫描"}
        return mapping.get(mode, mode)
