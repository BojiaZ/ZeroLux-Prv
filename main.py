from PySide6.QtWidgets import (
    QMenu, QWidget, QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QStackedWidget
)
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtGui import QIcon, QPixmap, QShortcut
from PySide6.QtCore import Qt, QSize

from ui.topbar import TopBar
from ui.leftbar.leftbar import LeftBar
from ui.main_content.main_content import MainContent

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
        self.left_bar.setFixedWidth(240)
        area_layout.addWidget(self.left_bar)

        # 右内容区（直接用MainContent）
        self.main_content = MainContent()
        area_layout.addWidget(self.main_content)
        main_layout.addWidget(main_area)

        # 左栏点击 → 切换页面
        self.left_bar.page_selected.connect(self.main_content.goto)
        # 页面切换完成 → 左栏高亮
        self.main_content.page_changed.connect(self.left_bar.set_highlight)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
