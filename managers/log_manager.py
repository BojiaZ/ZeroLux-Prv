import socket
import threading
import json
import itertools
import datetime
import pathlib
from PySide6.QtCore import QObject, Signal
from structs.log_entry import LogEntry

class LogManager(QObject):
    signal_new_log = Signal()  # 新日志信号（无参数，也可以带LogEntry对象）
    _ID = itertools.count(1)

    def __init__(self, path="db/logs.json"):
        super().__init__()  # 一定要super
        self.path = pathlib.Path(path)
        self.path.parent.mkdir(exist_ok=True)
        self._load()
        # 启动 socket server，默认不开，可以手动调用
        self._server_thread = None

    # ---------- public ----------
    def log(self, component: str, event_type: str,
            summary: str, path: str = "") -> LogEntry:
        entry = LogEntry(
            id        = next(self._ID),
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            path      = path,
            component = component,
            event_type= event_type,
            summary   = summary
        )
        self.entries.insert(0, entry)
        self._save()
        self.signal_new_log.emit()   # <<< 新增这句
        return entry

    def add_logentry(self, entry: LogEntry):
        """直接用LogEntry插入（供socket server用）"""
        # 避免ID冲突
        if entry.id >= next(self._ID):
            LogManager._ID = itertools.count(entry.id + 1)
        self.entries.insert(0, entry)
        self._save()
        self.signal_new_log.emit()   # <<< 新增这句
        return entry

    # ---------- io ----------
    def _load(self):
        if self.path.exists():
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            self.entries = [LogEntry(**d) for d in raw]
            if self.entries:
                LogManager._ID = itertools.count(self.entries[0].id + 1)
        else:
            self.entries = []

    def _save(self):
        self.path.write_text(
            json.dumps([e.__dict__ for e in self.entries],
                       ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    # ---------- 新增socket server部分 ----------
    def start_socket_server(self, host="127.0.0.1", port=22337):
        """启动日志socket服务端（后台线程）"""
        if self._server_thread and self._server_thread.is_alive():
            print("[LogManager] 日志socket服务已启动。")
            return

        def handler(conn, addr):
            buffer = ""
            with conn:
                while True:
                    data = conn.recv(4096)
                    if not data:
                        break
                    buffer += data.decode('utf-8')
                    while '\n' in buffer:
                        line, buffer = buffer.split('\n', 1)
                        if line.strip():
                            try:
                                d = json.loads(line)
                                entry = LogEntry(**d)
                                self.add_logentry(entry)
                                print(f"[LogManager] 收到并记录新日志: {entry}")
                            except Exception as e:
                                print(f"[LogManager] 解析或写入日志失败: {line}，错误: {e}")

        def server():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((host, port))
                s.listen()
                print(f"[LogManager] 日志socket监听: {host}:{port}")
                while True:
                    conn, addr = s.accept()
                    threading.Thread(target=handler, args=(conn, addr), daemon=True).start()

        self._server_thread = threading.Thread(target=server, daemon=True)
        self._server_thread.start()

# 用法举例（启动服务端监听）：
if __name__ == "__main__":
    log_mgr = LogManager()
    log_mgr.start_socket_server()   # 启动 socket 服务（不会影响你和UI的API/交互）
    # ... 你原来的和UI的连接、方法照常用
    # 为了防止主线程退出，可以加一个死循环或用其他方式阻塞
    import time
    while True:
        time.sleep(60)
