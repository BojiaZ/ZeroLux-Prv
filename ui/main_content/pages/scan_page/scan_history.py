from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QHeaderView, QPushButton,
    QDialog, QMessageBox
)
from PySide6.QtCore import Qt, Slot
from managers.history_manager import HistoryManager
from structs.actionresults import ActionResult


class ScanHistory(QWidget):
    """扫描历史记录页（只读）"""

    def __init__(self, history_mgr: HistoryManager, parent=None):
        super().__init__(parent)
        self.history_mgr = history_mgr
        self._build_ui()

    # ---------- public ----------
    def refresh(self):
        self.table.setRowCount(0)
        for e in self.history_mgr.entries:
            row = self.table.rowCount(); self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(e.id)))
            self.table.setItem(row, 1, QTableWidgetItem(e.start_time))
            self.table.setItem(row, 2, QTableWidgetItem(str(len(e.action_results))))

            # --- 详情列：伪超链接 ---
            if e.action_results:                       # 有结果 → 可点击蓝色链接
                lab = QLabel('<a href="#">查看</a>')
                lab.setTextFormat(Qt.RichText)
                lab.setAlignment(Qt.AlignCenter)
                lab.setStyleSheet("""
                    QLabel { color:#15bcc6; font-size:13px; }
                    QLabel:hover { text-decoration: underline; }
                """)
                # openExternalLinks 必须关掉，否则默认跳 url
                lab.setOpenExternalLinks(False)
                lab.linkActivated.connect(lambda _, entry=e: self._show_detail(entry))
            else:                                      # 没结果 → 灰色禁用样式
                lab = QLabel("查看")
                lab.setAlignment(Qt.AlignCenter)
                lab.setStyleSheet("color:#c0c4c8; font-size:13px;")

            self.table.setCellWidget(row, 3, lab)

    # ---------- UI ----------
    def _build_ui(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(18)

        headers = ["ID", "时间", "检测发生", "详情"]
        self.table = QTableWidget(0, len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        # ------- 列宽策略 -------
        # 0 列：ID —— 固定宽
        self.table.setColumnWidth(0, 60)

        # 1 列：时间 —— Stretch，占剩余空间
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

        # 2 列：检测发生 —— 根据内容自适应
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)

        # 3 列：详情 —— 固定宽
        self.table.setColumnWidth(3, 50)

        # ------- 其他常规设置 -------
        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(32)      # 行高，可按需调
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.NoSelection)
        self.table.setStyleSheet("""
        /* === 表格本身保持不变 === */
        QTableWidget{background:#f4f5f7;color:#202529;font-size:14px;}
        QTableWidget::item{padding:8px;}
        QHeaderView::section{background:#f4f5f7;color:#202529;font-weight:bold;}

        /* === 纵向滚动条：极简灰色圆角 === */
        QScrollBar:vertical{
            background:transparent;         /* 透明轨道 */
            width:6px;                      /* 总宽度 */
            margin:2px 0 2px 0;             /* 上下留空，让圆角不被裁切 */
            border:none;
        }
        QScrollBar::handle:vertical{
            background:#c4c9cc;             /* 默认浅灰 */
            min-height:30px;                /* 最短长度，防止太小 */
            border-radius:3px;              /* 圆角 = 半宽 */
        }
        QScrollBar::handle:vertical:hover{
            background:#9fa5a8;             /* 悬停变深一点 */
        }
        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical{
            height:0px;                     /* 取消上下按钮 */
        }
        QScrollBar::add-page:vertical,
        QScrollBar::sub-page:vertical{
            background:transparent;         /* 剩余空白透明 */
        }

        /* === 如需横向滚动条同理，可按需追加 === */
        """)
        
        lay.addWidget(self.table, 1)

    # ---------- detail dialog ----------
    def _show_detail(self, entry):
        if not entry.action_results:
            QMessageBox.information(self, "详情", "本次扫描未发现威胁")
            return

        dlg = QDialog(self); dlg.setWindowTitle("扫描详情")
        v = QVBoxLayout(dlg)

        hdr = ["文件路径", "原因", "动作", "状态", "错误"]
        tbl = QTableWidget(0, len(hdr))
        tbl.setHorizontalHeaderLabels(hdr)
        tbl.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        tbl.verticalHeader().setVisible(False)
        tbl.setEditTriggers(QTableWidget.NoEditTriggers)
        tbl.setStyleSheet(
            "QTableWidget{background:#f4f5f7;color:#202529;font-size:14px;}"
            "QTableWidget::item{padding:8px;}"
            "QHeaderView::section{background:#f4f5f7;color:#202529;font-weight:bold;}"
        )

        for a in entry.action_results:
            row = tbl.rowCount(); tbl.insertRow(row)
            tbl.setItem(row, 0, QTableWidgetItem(a.file_path))
            tbl.setItem(row, 1, QTableWidgetItem(a.reason))
            tbl.setItem(row, 2, QTableWidgetItem(a.recommend))
            tbl.setItem(row, 3, QTableWidgetItem("成功" if a.handled else "失败"))
            tbl.setItem(row, 4, QTableWidgetItem(a.error or ""))

        v.addWidget(tbl)
        dlg.resize(820, 420)
        dlg.exec()
