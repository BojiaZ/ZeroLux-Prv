from PySide6.QtWidgets import QScrollArea, QWidget, QVBoxLayout
from PySide6.QtCore    import Qt

_SCROLLER_QSS = """
/* 轨道完全透明，只剩滑块 */
QScrollBar:vertical {
    background: transparent;
    width: 6px;
    margin: 2px 0;
}
/* 滑块 */
QScrollBar::handle:vertical {
    background: #b0b0b0;
    min-height: 40px;
    border-radius: 3px;
}
/* hover 时稍深一点 */
QScrollBar::handle:vertical:hover {
    background: #909090;
}
/* 把上下箭头 & 空白段统统隐藏 */
QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical,
QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: none;
    height: 0px;
}
"""

class ScanListArea(QScrollArea):
    """垂直放置多个 ScanCard，可滚动；横向滚动条禁用，纵向极简"""
    def __init__(self, parent=None):
        super().__init__(parent)

        # --- 仅纵向滚动 ---
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy  (Qt.ScrollBarAsNeeded)

        # --- 极简滚动条样式 ---
        self.setStyleSheet(_SCROLLER_QSS)

        # --- 内部容器 ---
        container = QWidget()
        self.vbox = QVBoxLayout(container)
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.vbox.setSpacing(12)
        self.vbox.addStretch()              # 占位弹性
        self.setWidget(container)

    # ------- 公共接口 -------
    def add_card(self, card):
        """
        默认把新卡片插到顶部（索引 0），
        Stretch 占位一直留在最底，保证布局向上对齐。
        """
        self.vbox.insertWidget(0, card)   # ↩️ 关键改动

    def remove_card(self, card):
        """从布局移除并安全删除"""
        card.setParent(None)
        card.deleteLater()
