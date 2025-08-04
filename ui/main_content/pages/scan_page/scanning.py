from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QProgressBar, QTableWidget, QTableWidgetItem, QHeaderView, QFrame
)
from PySide6.QtCore import Qt, QElapsedTimer, Slot, Signal


class ScanningPage(QWidget):
    """实时扫描页（火绒布局 / Zerolux 主题）
    --------------------------------------------------
    * `set_mode(mode)` 在进入页面前调用，更新标题 & 描述文本
    * 监听 ScanRoute 四个信号：
        - signal_progress(obj)：必须含 `total`, `done`, `current_path`, `percent`
        - signal_scan_result(ScanResult)
        - signal_scan_finished()
    * UI 组件
        1. 标题 (mode → 中文)
        2. 描述 "正在进行xxx扫描…"
        3. 当前遍历路径（灰色小字） & 计时(右对齐)
        4. 细长进度条
        5. 结果表格 (路径 | 威胁类型)
        6. 底部统计 & 暂停 / 停止
    """
    scan_aborted = Signal()          # ← 新增

    MODE2TEXT = {
        "smart": "智能扫描",
        "full": "全盘扫描",
        "custom": "自定义扫描",
    }

    # ---------- ctor ----------
    def __init__(self, scan_route, parent=None):
        super().__init__(parent)
        self.route = scan_route
        self._timer = QElapsedTimer()
        self._paused = False
        self._current_mode = "custom"

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 32, 24)
        root.setSpacing(20)

        # 1. 标题 & 描述
        self.lab_title = QLabel(); 
        self.lab_title.setStyleSheet("font-size:26px;font-weight:bold;color:#202529")
        self.lab_desc = QLabel();  
        self.lab_desc.setStyleSheet("font-size:16px;color:#202529")
        root.addWidget(self.lab_title)
        root.addWidget(self.lab_desc)

        # 2. 当前路径 + 时间
        path_row = QHBoxLayout(); path_row.setSpacing(12)
        self.lab_path = QLabel("准备扫描…"); self.lab_path.setStyleSheet("font-size:13px;color:#202529")
        self.lab_time = QLabel("00:00");   self.lab_time.setStyleSheet("font-size:13px;color:#202529")
        path_row.addWidget(self.lab_path, 1)
        path_row.addWidget(self.lab_time, 0, Qt.AlignRight)
        root.addLayout(path_row)

        # 3. 进度条
        self.progress = QProgressBar(); self.progress.setFixedHeight(8)
        self.progress.setRange(0, 100); self.progress.setTextVisible(False)
        self.progress.setStyleSheet(
            "QProgressBar{background:#e8f3f6;border-radius:4px;}"
            "QProgressBar::chunk{background:#15bcc6;border-radius:4px;}"
        )
        root.addWidget(self.progress)

        # 分隔线
        line = QFrame(); line.setFrameShape(QFrame.HLine); line.setFixedHeight(1)
        line.setStyleSheet("background:#e4e8eb")
        root.addWidget(line)

        # 4. 结果表格
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["文件路径", "威胁类型"])
        self.table.setStyleSheet(
            "QTableWidget{background:#f4f5f7;color:#202529;font-size:14px;}"
            "QTableWidget::item{padding:8px;}"
            "QHeaderView::section{background:#f4f5f7;color:#202529;font-weight:bold;}"
        )
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.NoSelection)
        root.addWidget(self.table, 1)

        # 5. 底部信息 & 按钮
        bottom = QHBoxLayout(); bottom.setSpacing(24)
        self.lab_files = QLabel("已扫描文件：0");   self.lab_files.setStyleSheet("font-size:14px;color:#202529")
        self.lab_threat = QLabel("发现威胁：0");  self.lab_threat.setStyleSheet("font-size:14px;color:#c85151;font-weight:bold")
        bottom.addWidget(self.lab_files)
        bottom.addWidget(self.lab_threat)
        bottom.addStretch()

        self.btn_pause = QPushButton("暂停")
        self.btn_stop  = QPushButton("停止")
        for b in (self.btn_pause, self.btn_stop):
            b.setFixedSize(80, 28)
            b.setStyleSheet(
                "QPushButton{background:#eafafd;color:#15bcc6;border:2px solid #15bcc6;border-radius:5px;font-weight:bold;}"
                "QPushButton:hover{background:#b8f1fc;}"
            )
        bottom.addWidget(self.btn_pause)
        bottom.addWidget(self.btn_stop)
        root.addLayout(bottom)

        # 按钮槽
        self.btn_pause.clicked.connect(self._toggle_pause)
        self.btn_stop.clicked.connect(self._stop_scan)

        # 连接 route 信号
        self.route.signal_progress.connect(self._on_progress)
        self.route.signal_scan_result.connect(self._on_result)
        self.route.signal_scan_finished.connect(self._on_finish)

    # ---------- 外部接口 ----------
    def set_mode(self, mode: str):
        self._current_mode = mode
        txt = self.MODE2TEXT.get(mode, "自定义扫描")
        print(f"[ScanningPage] set mode to {txt}")
        self.lab_title.setText(txt)
        self.lab_desc.setText(f"正在进行{txt}…")

    # ---------- 路由器槽 ----------
    @Slot(object)
    def _on_progress(self, p):
        if not self._timer.isValid():
            self._timer.start()
        percent = getattr(p, "percent", int(p.done / max(p.total, 1) * 100))
        self.progress.setValue(percent)

        self.lab_files.setText(f"已扫描文件：{p.done}")
        elapsed = int(self._timer.elapsed()/1000)
        self.lab_time.setText(f"{elapsed//60:02d}:{elapsed%60:02d}")
        self.lab_path.setText(getattr(p, "current_path",
                         getattr(p, "current_file", "")))

    @Slot(object)
    def _on_result(self, r):
        if not getattr(r, "detected", False):
            return
        row = self.table.rowCount(); self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(r.file_path))
        self.table.setItem(row, 1, QTableWidgetItem(r.threat_type))
        self.lab_threat.setText(f"发现威胁：{row+1}")

    @Slot()
    def _on_finish(self):
        self.progress.setValue(100)
        self.btn_pause.setDisabled(True)
        self.btn_stop.setDisabled(True)
        self.lab_desc.setText(f"{self.MODE2TEXT.get(self._current_mode, '扫描')}完成！")
        self.lab_path.clear()

    # ---------- 控制按钮 ----------
    def _toggle_pause(self):
        if self._paused:
            self.route.resume_scan(); self.btn_pause.setText("暂停")
        else:
            self.route.pause_scan();  self.btn_pause.setText("继续")
        self._paused = not self._paused

    def _stop_scan(self):
        self.route.stop_scan()
        self._aborted = True                 # 打标记
        self.btn_pause.setDisabled(True)
        self.btn_stop.setDisabled(True)
        self.lab_desc.setText("扫描已停止")

    def reset(self):
        self.table.setRowCount(0)
        self.progress.setValue(0)
        self.lab_path.clear()
        self.lab_files.setText("已扫描文件：0")
        self.lab_threat.setText("发现威胁：0")
        self._timer.invalidate()
        # ⬇️ 这三样一定要恢复
        self._paused = False
        self.btn_pause.setEnabled(True);  self.btn_pause.setText("暂停")
        self.btn_stop.setEnabled(True)
        self._aborted = False          # ← 新增
        # 计时 —— 新增
        self._timer.invalidate()          # 让计时器失效
        self.lab_time.setText("00:00")    # 时间显示归零
