from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QPushButton, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtSvgWidgets import QSvgWidget


class TopBar(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # --- 1. 鼠标拖拽变量 ---
        self._drag_active = False
        self._drag_pos = None

        self.setFixedHeight(56)
        self.setStyleSheet("background: #f3f4f7;")

        # --- 2. 左侧LOGO ---
        logo_path = "resources/icons/Zerolux_logo.svg"
        logo = QSvgWidget(logo_path)
        logo.setFixedSize(28, 32)
        logo.setStyleSheet("background: transparent;")
        # --- 3. 标题 ---
        title = QLabel("Zerolux Prv1.0")
        title.setStyleSheet("""
            font-family: 'Segoe UI', Arial, Helvetica, sans-serif;
            font-size: 22px;
            font-weight: 600;
            color: #818c99;
            background: transparent;
        """)
        title.setAlignment(Qt.AlignVCenter)
        

        # --- 4. 右侧最小化按钮 ---
        min_button = QPushButton("–")
        min_button.setFixedSize(32, 32)
        min_button.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
                font-size: 18px;
                color: #888;
            }
            QPushButton:hover {
                background: #e4e9f7;
                color: #2186eb;
                border-radius: 6px;
            }
        """)
        min_button.clicked.connect(lambda: self.window().showMinimized())

        # --- 5. 右侧关闭按钮 ---
        close_button = QPushButton("X")
        close_button.setFixedSize(32, 32)
        close_button.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
                font-size: 18px;
                color: #888;
            }
            QPushButton:hover {
                background: #f9dddd;
                color: #c00;
                border-radius: 6px;
            }
        """)
        close_button.clicked.connect(lambda: self.window().close())

        # --- 6. 创建水平布局，并按顺序加入控件 ---
        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 0, 24, 0)  # 左右留点空
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignVCenter)
        layout.addWidget(logo)
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(min_button)
        layout.addWidget(close_button)

    # 鼠标按下事件处理
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_active = True
            self._drag_pos = event.globalPos() - self.window().frameGeometry().topLeft()
            event.accept()

    # 鼠标移动事件处理
    def mouseMoveEvent(self, event):
        if self._drag_active and event.buttons() & Qt.LeftButton:
            new_pos = event.globalPosition().toPoint() - self._drag_pos
            self.window().move(new_pos)
            event.accept()

    # 鼠标释放事件处理
    def mouseReleaseEvent(self, event):
        self.drag_active = False
        event.accept()