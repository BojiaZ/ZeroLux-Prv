from PySide6.QtWidgets import (
    QMenu, QWidget, QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QStackedWidget
)
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtGui import QIcon, QPixmap, QShortcut
from PySide6.QtCore import Qt, QSize

from ui.topbar import TopBar
from ui.leftbar import LeftBar
from pages.overview_page import OverviewPage

class HomeCard(QWidget): pass
class LogCard(QWidget): pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("resources/icons/Zerolux_logo.svg"))
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("Zerolux Prv1.0")
        self.resize(900, 600)
        self.setFixedSize(900, 600)

        # 中央主容器
        central = QWidget()
        central.setStyleSheet("background: #f4f5f7;")
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 顶部栏
        self.top_bar = TopBar()
        self.top_bar.setFixedHeight(56)
        main_layout.addWidget(self.top_bar)

        # 主区（横向）：左导航+右内容
        main_area = QWidget()
        area_layout = QHBoxLayout(main_area)
        area_layout.setContentsMargins(0, 0, 0, 0)
        area_layout.setSpacing(0)

        # 左侧导航栏
        self.left_bar = LeftBar()
        self.left_bar.setFixedWidth(240)  # 这里可以方便调整侧栏宽度
        area_layout.addWidget(self.left_bar)

        # 右内容区（所有页面装在QStackedWidget里）
        self.main_widget = QStackedWidget()
        self.main_widget.setContentsMargins(0, 0, 0, 0)

        self.overview_page = OverviewPage()
        self.log_card = LogCard()
        self.main_widget.addWidget(self.overview_page)  # index 0
        self.main_widget.addWidget(self.log_card)       # index 1
        self.main_widget.setCurrentIndex(0)

        area_layout.addWidget(self.main_widget)
        main_layout.addWidget(main_area)

        # 测试快捷键切换
        self.shortcut1 = QShortcut(Qt.Key_F1, self)
        self.shortcut1.activated.connect(lambda: self.main_widget.setCurrentIndex(0))
        self.shortcut2 = QShortcut(Qt.Key_F2, self)
        self.shortcut2.activated.connect(lambda: self.main_widget.setCurrentIndex(1))

        # 后续可以用 self.left_bar 的信号连接 self.main_widget.setCurrentIndex

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
