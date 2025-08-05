# structs/history_entry.py
from dataclasses import dataclass
from typing import List
from structs.actionresults import ActionResult

@dataclass
class ScanHistoryEntry:
    id: int
    start_time: str
    action_results: List[ActionResult]      # 可能为空列表