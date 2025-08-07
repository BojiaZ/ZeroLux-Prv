from PySide6.QtWidgets import (
    QMenu, QWidget, QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QSystemTrayIcon
)
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtGui import QIcon, QPixmap, QShortcut, QAction
from PySide6.QtCore import Qt, QSize, QEvent
from ui.dialogs.log_dialog import LogDialog
from ui.topbar import TopBar
from ui.leftbar.leftbar import LeftBar
from ui.main_content.main_content import MainContent

# ==== 业务路由层 ====
from execute.execute_router import ExecuteRoute
from quarantine.quarantine_route import QuarantineRoute
from scans.scans_router import ScanRoute
from managers.log_manager import LogManager

class HomeCard(QWidget): pass
class LogCard(QWidget): pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("resources/icons/Zerolux_logo.svg"))
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("Zerolux Antivirus")
        self.resize(900, 600)
        self.setFixedSize(900, 600)

        central = QWidget()
        central.setStyleSheet("background: #f4f5f7;")
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 业务对象初始化 —— 正确顺序
        self.quarantine_route = QuarantineRoute()          # 无需参数
        self.execute_route    = ExecuteRoute(self.quarantine_route)
        self.scan_route       = ScanRoute()
        self.log_mgr          = LogManager()

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
        self.main_content = MainContent(scan_route=self.scan_route, execute_route=self.execute_route, log_mgr=self.log_mgr, quarantine_route=self.quarantine_route)
        area_layout.addWidget(self.main_content)
        main_layout.addWidget(main_area)

        # 左栏点击 → 切换页面
        self.left_bar.page_selected.connect(self.main_content.goto)
        # 页面切换完成 → 左栏高亮
        self.main_content.page_changed.connect(self.left_bar.set_highlight)

        #初始化托盘
        self.init_tray_icon()


    def init_tray_icon(self):
        # SVG 直接转 QIcon
        icon = QIcon("resources/icons/Zerolux_logo.svg")
        self.tray_icon = QSystemTrayIcon(icon, self)
        self.tray_icon.setToolTip("Zerolux Antivirus")

        # 托盘菜单
        tray_menu = QMenu()
        action_show = QAction("打开主界面", self)
        action_quit = QAction("退出", self)
        tray_menu.addAction(action_show)
        tray_menu.addAction(action_quit)
        self.tray_icon.setContextMenu(tray_menu)

        # 信号绑定
        action_show.triggered.connect(self.show_window)
        action_quit.triggered.connect(QApplication.instance().quit)
        self.tray_icon.activated.connect(self.on_tray_activated)

        self.tray_icon.show()


    def show_window(self):
        self.showNormal()
        self.raise_()
        self.activateWindow()

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            # 单击托盘图标时
            self.show_window()
    
    def closeEvent(self, event):
        # 拦截关闭事件 → 隐藏窗口到托盘而不真正退出
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "Zerolux Antivirus",
            "程序已最小化到托盘，可右键托盘图标操作。",
            QSystemTrayIcon.Information,
            2000
        )

    def changeEvent(self, event):
        # 拦截最小化
        if event.type() == QEvent.WindowStateChange:
            if self.isMinimized():
                self.hide()
        super().changeEvent(event)

    
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
    