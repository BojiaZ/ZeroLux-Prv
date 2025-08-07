import socket
import threading
import json
from itertools import count

# 导入数据结构
from structs.rtp_event import RTPEvent
from structs.log_entry import LogEntry

# 端口配置
DIALOG_MANAGER_HOST = "127.0.0.1"
DIALOG_MANAGER_PORT = 22336

LOG_MANAGER_HOST = "127.0.0.1"
LOG_MANAGER_PORT = 22337

GUARD_LISTEN_HOST = "127.0.0.1"
GUARD_LISTEN_PORT = 22334

# 日志 id 生成器
log_id_counter = count(1)

def gen_log_id():
    return next(log_id_counter)

# 发送数据给目标 manager
def send_to_manager(json_str: str, host: str, port: int, name="Manager"):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall((json_str + '\n').encode('utf-8'))
    except Exception as e:
        print(f"[RTPGuard] 发送到 {name} 失败: {e}")

def handle_event(event_dict: dict):
    # 1. DialogManager：全量 RTPEvent
    send_to_manager(json.dumps(event_dict), DIALOG_MANAGER_HOST, DIALOG_MANAGER_PORT, name="DialogManager")
    print("[RTPGuard] 已转发到 DialogManager")

    # 2. LogManager：生成 LogEntry
    try:
        log_entry = LogEntry(
            id=gen_log_id(),
            timestamp=event_dict.get("timestamp", ""),
            path=event_dict.get("file_path", ""),
            component=event_dict.get("component", ""),
            event_type=event_dict.get("event_type", ""),
            summary=event_dict.get("summary", "")
        )
        # dataclass 转 dict → json
        from dataclasses import asdict
        send_to_manager(json.dumps(asdict(log_entry)), LOG_MANAGER_HOST, LOG_MANAGER_PORT, name="LogManager")
        print("[RTPGuard] 已转发到 LogManager")
    except Exception as e:
        print(f"[RTPGuard] 转换/发送 LogEntry 失败: {e}")

def handle_conn(conn, addr):
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
                        event = json.loads(line)
                        print(f"[RTPGuard] 收到事件: {event.get('event_type')} 来自: {event.get('component')}")
                        handle_event(event)
                    except Exception as e:
                        print(f"[RTPGuard] 解析事件失败: {line}，错误: {e}")

def start_guard_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((GUARD_LISTEN_HOST, GUARD_LISTEN_PORT))
        s.listen()
        print(f"[RTPGuard] 正在监听: {GUARD_LISTEN_HOST}:{GUARD_LISTEN_PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_conn, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_guard_server()
    input("Press Enter to exit...")
