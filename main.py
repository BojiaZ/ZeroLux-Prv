from PySide6.QtWidgets import  QMenu, QWidget, QApplication, QMainWindow, QVBoxLayout, QHBoxLayout
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QSize
# 下面这几个区域你可以先用占位类，后面写完 topbar.py 等再导入真实的
from ui.topbar import TopBar
from ui.leftbar import LeftBar
# from ui.homecard import HomeCard
# from ui.logcard import LogCard

# 暂时用占位类（便于跑通框架）
class HomeCard(QWidget):
    pass

class LogCard(QWidget):
    pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 设置窗口图标
        self.setWindowIcon(QIcon("resources/icons/Zerolux_logo.svg"))

        # 设置窗口属性
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("Zerolux Prv1.0")
        self.resize(900, 600)
        self.setFixedSize(900, 600)
        # 整个窗口主背景
        central = QWidget()
        central.setStyleSheet("background: #f4f5f7;")  # main.py里，整个窗口底色

        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        # 顶部栏
        self.top_bar = TopBar()
        self.top_bar.setFixedHeight(56)  # 高度先定死，便于留空间
        main_layout.addWidget(self.top_bar)
        # 下方主区
        bottom = QWidget()
        bottom_layout = QHBoxLayout(bottom)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(0)
        # 左侧导航栏
        self.left_bar = LeftBar()
        self.left_bar.setFixedWidth(260)  # 宽度先定死
        bottom_layout.addWidget(self.left_bar)
        # 右侧主内容区
        right_area = QWidget()
        right_layout = QVBoxLayout(right_area)
        right_layout.setContentsMargins(48, 32, 48, 32)  # 四周大留白
        right_layout.setSpacing(24)
        self.home_card = HomeCard()
        self.home_card.setFixedHeight(220)  # 先定高
        self.log_card = LogCard()
        right_layout.addWidget(self.home_card)
        right_layout.addWidget(self.log_card)
        bottom_layout.addWidget(right_area)
        main_layout.addWidget(bottom)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
