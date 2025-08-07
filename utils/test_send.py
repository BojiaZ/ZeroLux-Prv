import ipc
import json

event = {
    "event_type": "RTP_ALERT",
    "file_path": "C:/virus/test.exe",
    "description": "检测到木马文件"
}

ipc.send_event(json.dumps(event))
print("事件已发送！")
