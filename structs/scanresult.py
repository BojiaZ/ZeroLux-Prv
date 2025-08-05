# structs/scanresult.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class ScanResult:
    """
    单文件扫描结果对象（ScanResult）

    字段/Attributes:
        file_path (str): 扫描到的当前文件路径（可为绝对或相对路径，若为隔离区项，指隔离区文件实际路径）
        detected (bool): 是否命中威胁
        threat_type (Optional[str]): 威胁类型/分类（如病毒、木马、后门等）
        threat_level (Optional[str]): 威胁等级（如 High, Medium, Low，高/中/低）
        recommend (Optional[str]): 检测引擎建议的处置动作
        comment (Optional[str]): 威胁描述/备注/报告链接等
        engine (Optional[str]): 检测引擎（如 static, yara, ai）
        hash_value (Optional[str]): 文件的哈希值（md5/sha1/sha256均可）
        rule_id (Optional[str]): 检测规则编号/标签（如yara规则名、hash库行号）
        origin_path (Optional[str]): 原始路径（隔离区特有字段，指被隔离前的真实路径）
        quarantine_time (Optional[str]): 隔离时间（如"2024-08-01 14:32:22"，隔离区用）
    """

    file_path: str
    detected: bool
    threat_type: Optional[str] = None
    threat_level: Optional[str] = None
    recommend: Optional[str] = None
    comment: Optional[str] = None
    engine: Optional[str] = None
    hash_value: Optional[str] = None
    rule_id: Optional[str] = None
    reason : Optional[str] = None
    # ===== 隔离区专用扩展字段 =====
    origin_path: Optional[str] = None
    quarantine_time: Optional[str] = None
