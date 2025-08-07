# dialog_manager.py
import socket
import threading
import json

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
                        print(f"[DialogManager] 收到弹窗事件: {event}")
                        # 这里后续可以直接弹窗
                    except Exception as e:
                        print(f"[DialogManager] 解析事件失败: {line}，错误: {e}")

def start_server(host="127.0.0.1", port=22336):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        print(f"[DialogManager] 监听 {host}:{port} 等待RTPGuard推送弹窗事件...")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_conn, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
