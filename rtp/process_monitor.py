import socket
import json
from uuid import uuid4
from datetime import datetime

def send_event(event_json: str, host='127.0.0.1', port=22334):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall((event_json + '\n').encode('utf-8'))

if __name__ == "__main__":
    # 伪造一个 RTPEvent 事件
    event = {
        "event_id": str(uuid4()),
        "event_type": "virus_detected",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "component": "ProcessMonitor",
        "file_path": "C:/Program Files/test/evil.exe",
        "process_name": "evil.exe",
        "description": "检测到可疑进程 evil.exe，疑似木马",
        "summary": "发现可疑进程",
        "recommend_action": "QUARANTINE",
        "buttons": ["隔离", "忽略"],
        "extra": {"pid": 1234, "md5": "1234567890abcdef"}
    }
    send_event(json.dumps(event))
    print("已向RTPGuard发送威胁事件。")
