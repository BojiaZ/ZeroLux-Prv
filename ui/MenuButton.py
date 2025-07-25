# MenuButton.py
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtGui import QPainter, QColor, QBrush
from PySide6.QtCore import Qt, QSize, QByteArray, Signal

class MenuButton(QWidget):
    clicked = Signal()  # 如果需要点击事件，可以定义一个信号

    def __init__(self, icon_path, text, parent=None):
        super().__init__(parent)

        # 设置初始状态
        self.setMouseTracking(True)
        self.hovered = False
        self.selected = False
        
        # 布局
        layout = QHBoxLayout(self)
        layout.setContentsMargins(32, 10, 8, 10)  # 上下10，左右同前
        layout.setSpacing(13)  # 图标和文字更宽松

        # 拼接图标路径并创建初始图标
        self.icon_base = icon_path  # 保存图标基础名
        self.icon_widget = QSvgWidget(f"resources/icons/menu_icon/{self.icon_base}_gray.svg")
        self.icon_widget.setFixedSize(QSize(26, 26))

        # 文字标签
        self.text_label = QLabel(text)
        self.text_label.setStyleSheet("font-size: 17px; color: #444; font-weight: 500;")

        # 添加到布局
        layout.addWidget(self.icon_widget)
        layout.addWidget(self.text_label, 1)

        self.setFixedHeight(52)  # 每行更高
        self.setStyleSheet("background: transparent; border-radius: 8px;")

    def enterEvent(self, event):
        self.hovered = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.hovered = False
        self.update()  # 触发paintEvent
        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect().adjusted(12, 4, -12, -4)

        if self.hovered:
            painter.setBrush(QBrush(QColor(0, 0, 0, 8)))  # hover
        else:
            painter.setBrush(Qt.NoBrush)

        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 8, 8)
        super().paintEvent(event)
    
    def mousePressEvent(self, event):
        self.clicked.emit()  # 发信号，LeftBar负责管理选中逻辑
        super().mousePressEvent(event)

    def setSelected(self, value: bool):
        self.selected = value
        # 1. 变更图标
        if self.selected:
            # 例如 self.icon_base = "overview" 时
            icon_file = f"resources/icons/menu_icon/{self.icon_base}_blue.svg"
        else:
            icon_file = f"resources/icons/menu_icon/{self.icon_base}_gray.svg"
        self.icon_widget.load(icon_file)

        # 2. 文字色（可选）
        self.updateColors()
        self.update()

        # 修改文字的字体加粗
        if self.selected:
            # 设置选中时字体加粗
            self.text_label.setStyleSheet("font-size: 17px; color: #009CA6; font-weight: 600;")
        else:
            # 恢复常规样式
            self.text_label.setStyleSheet("font-size: 17px; color: #444; font-weight: normal;")

    def updateColors(self):
        select_color = "#009CA6"
        normal_color = "#444"
        if self.selected:
            self.text_label.setStyleSheet(f"font-size: 17px; color: {select_color}; font-weight: 500;")
        else:
            self.text_label.setStyleSheet(f"font-size: 17px; color: {normal_color}; font-weight: 500;")
