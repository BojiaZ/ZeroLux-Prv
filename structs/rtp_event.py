from dataclasses import dataclass, field
from typing import Optional

@dataclass
class RTPEvent:
    event_id: str
    event_type: str          # 上述几种枚举
    timestamp: str           # 精确到秒
    component: str           # "RTP" / "SCAN" / "PROTECT" ...
    file_path: str           # 文件相关事件路径
    description: str         # 展示用完整描述
    summary: str             # 列表摘要（日志、通知用）
    recommend_action: str    # "QUARANTINE" / "DELETE" / "ALLOW" / "REBOOT" ...
    process_name: Optional[str] = ""  # 进程相关可填（有默认值的放后面）
    buttons: list = field(default_factory=list) # ["查看详情", "立即隔离", ...]
    extra: dict = field(default_factory=dict)   # 扩展信息，兼容未来字段
