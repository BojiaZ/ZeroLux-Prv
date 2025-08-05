# scan_result.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QProgressBar,
    QStackedWidget, QFrame
)
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QColor

from structs.actionresults import ActionResult
from execute.execute_router import ExecuteRoute


class ScanResultPage(QWidget):
    """
    扫描结果页 —— 根据是否发现威胁分两种视图：

    1. no_threat_view  : 无威胁 → 仅提示文字 + 完成按钮
    2. threat_handle_view : 有威胁 → 复制 ScanningPage 风格，提供“一键处理”流程
    """

    # 外部信号
    back_requested   = Signal()            # 返回扫描选择页
    handle_requested = Signal(list)        # 批量处理请求（发送 ScanResult 列表）

    # ---------- ctor ----------
    def __init__(self, execute_route: ExecuteRoute, parent=None):
        super().__init__(parent)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        self.stack = QStackedWidget(self)
        root.addWidget(self.stack)

        # 1️⃣ 无威胁视图
        self._init_no_threat_view()

        # 2️⃣ 有威胁视图
        self._init_threat_view()

        # 内部状态
        self._threats  = []        # ScanResult 列表
        self._path2row = {}        # file_path -> row idx
        self._handled  = 0

        self.execute_route = execute_route
        self.execute_route.signal_execute_progress.connect(self._on_action_progress)
        self.execute_route.signal_execute_result.connect(self._on_action_result)
        self.execute_route.signal_execute_finished.connect(self._on_action_finished)
        self.handle_requested.connect(self.execute_route.handle_results)

    # ------------------------------------------------------------------
    #                           视图初始化
    # ------------------------------------------------------------------
    def _init_no_threat_view(self):
        page = QWidget()
        vbox = QVBoxLayout(page)
        vbox.setContentsMargins(32, 32, 32, 24)
        vbox.setSpacing(40)

        # 中央提示
        self.lab_msg = QLabel("")
        self.lab_msg.setAlignment(Qt.AlignCenter)
        self.lab_msg.setStyleSheet("font-size:24px;font-weight:bold;color:#202529")
        vbox.addStretch()
        vbox.addWidget(self.lab_msg)
        vbox.addStretch()

        # 完成按钮
        btn_done = QPushButton("完成")
        btn_done.setFixedSize(110, 36)
        btn_done.setStyleSheet(
            "QPushButton{background:#15bcc6;color:white;font-weight:bold;border:none;border-radius:6px;}"
            "QPushButton:hover{background:#1198a1;}"
        )
        btn_done.clicked.connect(self.back_requested)
        h = QHBoxLayout(); h.addStretch(); h.addWidget(btn_done); h.addStretch()
        vbox.addLayout(h)

        self.stack.addWidget(page)          # index 0

    def _init_threat_view(self):
        page = QWidget()
        vbox = QVBoxLayout(page)
        vbox.setContentsMargins(32, 32, 32, 24)
        vbox.setSpacing(18)

        # 标题 & 描述
        self.lab_title = QLabel("扫描完成")
        self.lab_title.setStyleSheet("font-size:26px;font-weight:bold;color:#202529")
        self.lab_desc  = QLabel()
        self.lab_desc.setStyleSheet("font-size:16px;color:#202529")
        vbox.addWidget(self.lab_title)
        vbox.addWidget(self.lab_desc)

        # 当前处理路径
        path_row = QHBoxLayout(); path_row.setSpacing(12)
        self.lab_path = QLabel("")
        self.lab_path.setStyleSheet("font-size:13px;color:#202529")
        path_row.addWidget(self.lab_path, 1)
        vbox.addLayout(path_row)

        # 进度条
        self.progress = QProgressBar(); self.progress.setFixedHeight(8)
        self.progress.setRange(0, 100); self.progress.setTextVisible(False)
        self.progress.setStyleSheet(
            "QProgressBar{background:#e8f3f6;border-radius:4px;}"
            "QProgressBar::chunk{background:#15bcc6;border-radius:4px;}"
        )
        vbox.addWidget(self.progress)

        # 分隔线
        line = QFrame(); line.setFrameShape(QFrame.HLine); line.setFixedHeight(1)
        line.setStyleSheet("background:#e4e8eb")
        vbox.addWidget(line)

        # 详细表格
        headers = ["文件路径", "原因", "威胁类型", "处理建议", "处理状态"]
        self.table = QTableWidget(0, len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        for i in range(1, len(headers)):
            self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.NoSelection)
        self.table.setStyleSheet(
            "QTableWidget{background:#f4f5f7;color:#202529;font-size:14px;}"
            "QTableWidget::item{padding:6px;}"
            "QHeaderView::section{background:#f4f5f7;color:#202529;font-weight:bold;}"
        )
        vbox.addWidget(self.table, 1)

        # 底部统计 & 按钮
        bottom = QHBoxLayout(); bottom.setSpacing(24)
        self.lab_total     = QLabel(); self.lab_total.setStyleSheet("font-size:14px;color:#202529")
        self.lab_processed = QLabel(); self.lab_processed.setStyleSheet("font-size:14px;color:#202529")
        bottom.addWidget(self.lab_total)
        bottom.addWidget(self.lab_processed)
        bottom.addStretch()

        self.btn_handle = QPushButton("一键处理")
        self.btn_handle.setFixedSize(100, 32)
        self.btn_handle.setStyleSheet(
            "QPushButton{background:#eafafd;color:#15bcc6;border:2px solid #15bcc6;"
            "border-radius:5px;font-weight:bold;}"
            "QPushButton:hover{background:#b8f1fc;}"
        )
        self.btn_handle.clicked.connect(self._start_handle)

        self.btn_done = QPushButton("完成")
        self.btn_done.setFixedSize(100, 32)
        self.btn_done.setDisabled(True)
        self.btn_done.setStyleSheet(
            "QPushButton{background:#15bcc6;color:white;font-weight:bold;border:none;border-radius:5px;}"
            "QPushButton:hover{background:#1198a1;}"
            "QPushButton:disabled{background:#9adfe4;}"
        )
        self.btn_done.clicked.connect(self.back_requested)

        bottom.addWidget(self.btn_handle)
        bottom.addWidget(self.btn_done)
        vbox.addLayout(bottom)

        self.stack.addWidget(page)          # index 1

    # ------------------------------------------------------------------
    #                             外部接口
    # ------------------------------------------------------------------
    def load_data(self, results, stopped: bool):
        """
        ScanPage → load_data

        • 无威胁 → 只显示提示
        • 有威胁 → 初始化处理视图
        """
        threats = [r for r in results if getattr(r, "detected", False)]
        self._threats  = threats
        self._path2row = {}
        self._handled  = 0

        if not threats:       # —— 无威胁场景 ——
            self.lab_msg.setText("扫描被用户终止" if stopped else "扫描完成，未发现威胁")
            self.stack.setCurrentIndex(0)
            return

        # —— 有威胁场景 ——
        self.stack.setCurrentIndex(1)

        status = "扫描被用户终止" if stopped else "扫描完成"
        self.lab_title.setText(status)
        self.lab_desc.setText(f"发现 {len(threats)} 个风险项，待处理")
        self.lab_total.setText(f"总计：{len(threats)}")
        self.lab_processed.setText("已处理：0")
        self.progress.setValue(0)
        self.lab_path.clear()
        self.btn_handle.setEnabled(True)
        self.btn_done.setDisabled(True)

        # 填充表格
        self.table.setRowCount(0)
        for t in threats:
            row = self.table.rowCount(); self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(t.file_path))
            self.table.setItem(row, 1, QTableWidgetItem(getattr(t, "reason", "-")))
            self.table.setItem(row, 2, QTableWidgetItem(t.threat_type))
            self.table.setItem(row, 3, QTableWidgetItem(getattr(t, "recommend", "delete")))
            status_item = QTableWidgetItem("未处理")
            status_item.setForeground(QColor("#202529"))
            self.table.setItem(row, 4, status_item)
            self._path2row[t.file_path] = row

    # 路由器绑定（一次性）
    def bind_router(self, router):
        router.signal_action_progress.connect(self._on_action_progress)
        router.signal_action_result.connect(self._on_action_result)
        router.signal_action_finished.connect(self._on_action_finished)

    # ------------------------------------------------------------------
    #                            按钮槽
    # ------------------------------------------------------------------
    def _start_handle(self):
        if not self._threats:
            return
        self.btn_handle.setDisabled(True)
        self.handle_requested.emit(self._threats)

    # ------------------------------------------------------------------
    #                              Slots
    # ------------------------------------------------------------------
    @Slot(object)
    def _on_action_progress(self, p):
        percent = getattr(p, "percent", int(p.done / max(p.total, 1) * 100))
        self.progress.setValue(percent)
        self.lab_path.setText(f"正在处理：{getattr(p, 'current_path', '')}")

    @Slot(object)
    def _on_action_result(self, r: ActionResult):
        row = self._path2row.get(r.file_path)
        if row is None:
            return
        item = self.table.item(row, 4)
        if r.handled and not r.error:
            item.setText("已处理"); item.setForeground(QColor("#15bcc6"))
        else:
            item.setText("失败"); item.setForeground(QColor("#c85151"))
        self._handled += 1
        self.lab_processed.setText(f"已处理：{self._handled}")

    @Slot(list)
    def _on_action_finished(self, results: list[ActionResult]):
        self.progress.setValue(100)
        self.lab_path.setText("全部处理完成")
        self.btn_done.setEnabled(True)
