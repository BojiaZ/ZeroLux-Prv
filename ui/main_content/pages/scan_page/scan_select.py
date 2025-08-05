from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QStackedWidget, QGridLayout, QFrame, QFileDialog
)
from PySide6.QtCore import Signal, Qt

from scans.scans_router import ScanRoute
from .scan_history import ScanHistory
from managers.history_manager import HistoryManager

class ScanSelectPage(QWidget):
    # 扫描模式、路径（custom模式才有路径，否则为""）
    sig_start_scan = Signal(str, str)  # (mode, custom_path)

    def __init__(self, history_mgr: HistoryManager,parent=None):
        super().__init__(parent)

        self.history_mgr = history_mgr     # 保存实例

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 1. 顶部标题描述
        header = QVBoxLayout()
        header.setContentsMargins(0, 8, 0, 20)
        header.setSpacing(12)
        title = QLabel("病毒扫描")
        title.setStyleSheet("font-size:26px; font-weight:bold; color:#202529;")
        desc = QLabel("针对系统安全的多种扫描，按您需选择扫描范围，帮助您排查并清除难以察觉的恶意软件，让隐患无所遁形。")
        desc.setStyleSheet("color:#3a434d; font-size:15px;")
        desc.setContentsMargins(0, 0, 20, 0)
        desc.setWordWrap(True)
        header.addWidget(title)
        header.addWidget(desc)
        layout.addLayout(header)
        layout.addSpacing(12)

        # ------- 顶部Tab -------
        self.tabs = ["即时扫描", "扫描历史"]
        self.tab_idx = 0
        self.tab_bar = QHBoxLayout()
        self.tab_bar.setContentsMargins(0, 0, 0, 0)
        self.tab_bar.setSpacing(32)
        self.tab_labels = []
        for i, text in enumerate(self.tabs):
            lab = QLabel(text)
            lab.setCursor(Qt.PointingHandCursor)
            self.tab_labels.append(lab)
            self.tab_bar.addWidget(lab)
            lab.mousePressEvent = lambda evt, idx=i: self.switch_tab(idx)
        self.tab_bar.addStretch()
        layout.addLayout(self.tab_bar)
        self._update_tab_styles()

        # ------- 内容区 -------
        self.stacked = QStackedWidget()
        self.stacked.addWidget(self._scan_content())
        self.history_page   = ScanHistory(history_mgr)   # ★ 新增
        self.stacked.addWidget(self._history_content())
        self.stacked.addWidget(self.history_page)
        layout.addWidget(self.stacked)

    # ---------- Tab 切换 ----------
    def switch_tab(self, idx):
        self.tab_idx = idx
        self.stacked.setCurrentIndex(idx)
        if idx == 1:                          # 当切到 “扫描历史” 时刷新
            self.history_page.refresh()
        self._update_tab_styles()

    def _update_tab_styles(self):
        for i, lab in enumerate(self.tab_labels):
            if i == self.tab_idx:
                lab.setStyleSheet("""
                    QLabel {
                        color: #15bcc6;
                        font-size:18px;
                        font-weight: bold;
                        border: none;
                        padding-bottom: 5px;
                        border-bottom: 2.5px solid #15bcc6;
                    }
                """)
            else:
                lab.setStyleSheet("""
                    QLabel {
                        color: #a2adb6;
                        font-size:18px;
                        font-weight: normal;
                        border: none;
                        padding-bottom: 5px;
                        border-bottom: 2.5px solid transparent;
                    }
                    QLabel:hover {
                        color: #15bcc6;
                        border-bottom: 2.5px solid #bdeff4;
                    }
                """)

    def _scan_content(self):
        """
        构建主扫描选择区，三种模式三行，custom扫描弹出文件/文件夹选择对话框
        """
        content = QWidget()
        content.setFixedWidth(620)
        content.setFixedHeight(240)
        grid = QGridLayout(content)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(16)

        grid.setColumnStretch(0, 0)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(2, 0)

        items = [
            # title, desc, 按钮文本, mode
            ("智能扫描", "快速检查系统关键区域，高效识别常见威胁与风险。", "运行智能扫描", "smart"),
            ("全盘扫描", "全面扫描整台电脑，检测所有可能的威胁。", "运行全盘扫描", "full"),
            ("针对性扫描", "扫描指定文件夹或外置驱动器。", "运行针对性扫描", "custom")
        ]

        for i, (title, desc, btn_text, mode) in enumerate(items):
            t = QLabel(title)
            t.setStyleSheet("""
                font-size:17px;
                font-weight:bold;
                color:#222;
                margin:0;
                padding:0;
            """)
            t.setFixedWidth(92)
            t.setFixedHeight(28)
            grid.addWidget(t, i, 0, alignment=Qt.AlignRight | Qt.AlignVCenter)

            d = QLabel(desc)
            d.setStyleSheet("color:#324252; font-size:14px; margin:0; padding:0;")
            d.setWordWrap(True)
            d.setFixedWidth(410)
            grid.addWidget(d, i, 1, alignment=Qt.AlignLeft | Qt.AlignVCenter)

            btn = QPushButton(btn_text)
            btn.setFixedWidth(116)
            btn.setStyleSheet("""
            QPushButton {
                background: #eafafd;
                color: #15bcc6;
                border-radius: 7px;
                border: 2px solid #15bcc6;
                font-weight: bold;
                font-size: 14px;
                min-width: 120px;
                padding: 2px 10px;
            }
            QPushButton:hover {
                background: #b8f1fc;
            }
            """)
            # 按钮点击逻辑：custom 模式弹窗，否则直接发射信号
            if mode == "custom":
                btn.clicked.connect(self._on_custom_scan)
            else:
                btn.clicked.connect(lambda _, m=mode: self.sig_start_scan.emit(m, ""))

            grid.addWidget(btn, i, 2, alignment=Qt.AlignLeft | Qt.AlignVCenter)

        return content


    # ---------- 针对性扫描 --------
    def _on_custom_scan(self):
        """
        弹出对话框选择自定义扫描路径，并将结果通过信号发射到主逻辑
        """
        # 你可以根据需求弹文件夹（推荐）或文件
        # 选择文件夹:
        path = QFileDialog.getExistingDirectory(self, "选择扫描文件夹")
        # 选择单文件：
        # path, _ = QFileDialog.getOpenFileName(self, "选择文件")
        if path:
            self.sig_start_scan.emit("custom", path)

    def _history_content(self):
        # 不再用占位，直接返回真实页面（兼容旧调用）
        return self.history_page
