import subprocess
import sys
import os

def run_bg(script):
    if sys.platform == "win32":
        # Windows下用新控制台打开，开发看日志方便
        subprocess.Popen([sys.executable, script], creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        subprocess.Popen([sys.executable, script])

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    run_bg(os.path.join(base_dir, "rtp_guard.py"))
    run_bg(os.path.join(base_dir, "managers", "dialog_manager.py"))
    run_bg(os.path.join(base_dir, "managers", "log_manager.py"))
    # 最后再拉起主UI窗口
    subprocess.Popen([sys.executable, os.path.join(base_dir, "main.py")])
