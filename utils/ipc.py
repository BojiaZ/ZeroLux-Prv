import socket
import threading
import json

def send_event(event_json: str, host='127.0.0.1', port=22334):
    """ 发送事件字符串到指定主机和端口 """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        # 为了简单，发送数据后加一个换行符，方便分割多条消息
        s.sendall((event_json + '\n').encode('utf-8'))

def listen_events(on_event: callable, host='127.0.0.1', port=22334):
    """ 启动监听，收到消息就回调 on_event(event_dict) """
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
                            event = json.loads(line)
                            on_event(event)
                        except Exception as e:
                            print(f"收到无法解析的消息: {line}，错误: {e}")

    def server():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port))
            s.listen()
            print(f"[ipc] 正在监听 {host}:{port}")
            while True:
                conn, addr = s.accept()
                threading.Thread(target=handler, args=(conn, addr), daemon=True).start()

    threading.Thread(target=server, daemon=True).start()
