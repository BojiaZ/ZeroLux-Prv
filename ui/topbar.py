from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QPushButton, QVBoxLayout
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
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
        self.setStyleSheet("background: #f4f5f7;")

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
        min_button = QPushButton()
        min_icon_normal = QIcon("resources/icons/topbar_icon/min_gray.svg")  # 正常状态图标
        min_button.setIcon(min_icon_normal)
        min_button.setIconSize(QSize(32, 32))  # 设置图标大小
        min_button.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
                color: #888;  /* 设置按钮文字颜色 */
            }
            QPushButton:hover {
            background: rgba(0, 0, 0, 0.05);  /* 使用 rgba 设置透明灰色背景 */
            color: #2186eb;  /* 鼠标悬停时文字颜色 */
            border-radius: 6px;  /* 圆角 */
        }
        """)
        min_button.clicked.connect(lambda: self.window().showMinimized())

        # --- 5. 右侧关闭按钮 ---
        close_button = QPushButton()
        close_icon_normal = QIcon("resources/icons/topbar_icon/close_gray.svg")  # 关闭按钮图标
        close_icon_hover = QIcon("resources/icons/topbar_icon/close_white.svg")  # 悬停时的白色图标
        close_button.setIcon(close_icon_normal)
        close_button.setIconSize(QSize(32, 32))  # 设置图标大小
        close_button.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
                color: #888;  /* 设置按钮文字颜色 */
            }
            QPushButton:hover {
                background: #c93b32;  /* 鼠标悬停时的背景颜色 */
                color: #c00;  /* 鼠标悬停时文字颜色 */
                border-radius: 6px;  /* 圆角 */
            }
        """)
        close_button.clicked.connect(lambda: self.window().close())

        # **hover时更换图标**
        close_button.enterEvent = lambda event: close_button.setIcon(close_icon_hover)
        close_button.leaveEvent = lambda event: close_button.setIcon(close_icon_normal)

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