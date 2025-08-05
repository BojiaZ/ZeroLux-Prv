# structs/actionresult.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class ActionResult:
    file_path: str
    file_name: str
    recommend: str
    engine: str
    handled: bool
    handle_time: str
    reason: str
    comment: Optional[str] = None
    origin_path: Optional[str] = None
    error: Optional[str] = None
