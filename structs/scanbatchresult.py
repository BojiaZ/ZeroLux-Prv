# structs/scanbatchresult.py
from dataclasses import dataclass
from typing import List
from structs.scanresult import ScanResult

@dataclass
class ScanBatchResult:
    results: List[ScanResult]   # 批量扫描结果
