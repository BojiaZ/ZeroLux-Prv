from dataclasses import dataclass

@dataclass
class TraverseProgress:
    current_file: str       # 当前遍历到的文件路径
    percent_complete: float # 完成百分比，0~100