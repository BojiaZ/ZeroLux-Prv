from dataclasses import dataclass

@dataclass
class LogEntry:
    id: int
    timestamp: str      # "2025-08-05 18:21:33"
    path: str           # 触发对象路径，可为空字符串
    component: str      # RTP / SCAN / UPDATE / PROTECT ...
    event_type: str     # INIT / BLOCK / CLEAN / STOP ...
    summary: str        # 摘要一句话（列表展示）
