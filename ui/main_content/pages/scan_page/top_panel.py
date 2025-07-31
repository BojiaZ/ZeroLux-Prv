# ui/pages/scan_page/top_panel.py
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QToolButton, QMenu, QSizePolicy, QFileDialog
)
from PySide6.QtGui import QPixmap, QAction
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtCore import Qt, Signal

# --------- 配色常量（和全局保持一致即可调） ----------
PRIMARY      = "#009CA6"                   # 主题蓝绿
TEXT         = "#444"                      # 正文字体
CARD_BG      = "#ffffff"
CARD_BORDER  = "#e1e1e1"
CARD_SHADOW  = "0 1px 6px rgba(0,0,0,0.08)"
HOVER_SHADOW = "0 3px 12px rgba(0,0,0,0.12)"
ICON64       = "resources/icons/menu_icon/scan_gray.svg"

# --------- 通用卡片 QSS ----------
CARD_QSS = f"""
QPushButton, QToolButton {{
  background: {CARD_BG};
  border: 1px solid {CARD_BORDER};
  border-radius: 14px;
  padding: 20px;
}}
QPushButton:hover, QToolButton:hover {{
  border-color: {CARD_BORDER};

}}
QPushButton:pressed, QToolButton:pressed {{

}}
QToolButton::menu-indicator {{ image:none; }}
"""

class TopPanel(QWidget):
    start_scan = Signal(str, list)        # smart / full / custom / removable

    def __init__(self):
        super().__init__()

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(18)

        # ---------------- 页面大标题 ----------------
        title = QLabel("计算机扫描")
        title.setStyleSheet("font-size:24px; font-weight:600; color:#1b1b1b;")
        root.addWidget(title)

        # ---------------- 卡片行 ----------------
        row = QHBoxLayout()
        row.setSpacing(18)

        # ① 智能扫描卡片（左）
        btn_smart = QPushButton()
        btn_smart.setCursor(Qt.PointingHandCursor)
        btn_smart.setStyleSheet(CARD_QSS)
        btn_smart.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        btn_smart.clicked.connect(lambda: self.start_scan.emit("smart", []))

        q_layout = QHBoxLayout(btn_smart)
        q_layout.setContentsMargins(20, 12, 20, 12)   # ← 左右 20 px
        q_layout.setSpacing(14)                       # 图标 ↔ 文字
        q_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        icon = QSvgWidget(ICON64)          # ICON64 = svg 路径
        icon.setFixedSize(40, 40)    
        icon.setStyleSheet(f"background: transparent; margin-top:-10px;")      # 确保 40×40
        q_layout.addWidget(icon)

        vtxt = QVBoxLayout()
        vtxt.setSpacing(4)
        vtxt.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        lbl1 = QLabel("智能扫描")
        lbl1.setStyleSheet(f"font-size:16px; color:{PRIMARY}; font-weight:500; background:transparent;")
        lbl2 = QLabel("扫描系统关键位置并清除威胁")
        lbl2.setStyleSheet(f"font-size:12px; color:{TEXT}; background:transparent;")

        vtxt.addWidget(lbl1)
        vtxt.addWidget(lbl2)
        q_layout.addLayout(vtxt)


        # ② 高级扫描卡片（右）
        btn_adv = QToolButton()
        btn_adv.setCursor(Qt.PointingHandCursor)
        btn_adv.setPopupMode(QToolButton.InstantPopup)
        btn_adv.setStyleSheet(CARD_QSS)
        btn_adv.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        a_layout = QVBoxLayout(btn_adv)
        a_layout.setContentsMargins(20, 12, 20, 12)   # ← 同步左右缩进
        a_layout.setSpacing(4)
        a_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        lbl3 = QLabel("高级扫描  ▼")
        lbl3.setStyleSheet(f"font-size:16px; color:{PRIMARY}; font-weight:500; background:transparent;")
        lbl4 = QLabel("自定义和可移动磁盘扫描")
        lbl4.setStyleSheet(f"font-size:12px; color:{TEXT};  background:transparent;")

        a_layout.addWidget(lbl3)
        a_layout.addWidget(lbl4)
        a_layout.setSpacing(5)
        a_layout.setSpacing(5)
        # 下拉菜单
        menu = QMenu(btn_adv)
        menu.setStyleSheet(f"""
            QMenu {{
              background:{CARD_BG};
              border:1px solid {CARD_BORDER};
              padding:6px 0;
            }}
            QMenu::item {{
              padding:6px 26px;
              color:{TEXT};
            }}
            QMenu::item:selected {{
              background: {PRIMARY}22;
              color:{PRIMARY};
            }}
        """)
        for txt, mode in [("全盘扫描",  "full"),
                          ("自定义扫描","custom"),
                          ("可移动磁盘","removable")]:
            act = QAction(txt, menu)

            if mode == "custom":
                def _pick_dir(_checked=False, *, self=self):
                    path = QFileDialog.getExistingDirectory(
                        self, "选择扫描文件夹", r"C:\\", QFileDialog.ShowDirsOnly
                    )
                    if path:
                        self.start_scan.emit("custom", [path])
                act.triggered.connect(_pick_dir)
            else:
                act.triggered.connect(lambda _, mode=mode: self.start_scan.emit(mode, []))

            menu.addAction(act)
        btn_adv.setMenu(menu)

        # 将两卡片放入行，并等权重撑满
        row.addWidget(btn_smart, 1)
        row.addWidget(btn_adv,   1)
        root.addLayout(row)

        # 底部灰色分隔线
        sep = QWidget()
        sep.setFixedHeight(1)
        sep.setStyleSheet(f"background:{CARD_BORDER};")
        root.addWidget(sep)
