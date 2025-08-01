import os
from structs.scanresult import ScanResult
from .calc_hash import calc_md5, calc_sha1, calc_sha256

class StaticEngine:
    """
    静态查杀引擎（基于哈希库）

    功能：
    - 加载固定路径的哈希库文件
    - 计算文件的 MD5、SHA1、SHA256
    - 判断文件是否命中哈希库
    - 返回标准 ScanResult 对象

    属性：
    - hash_db (dict): 哈希库映射，key 为小写哈希值，value 为注释说明
    - HASH_DB_PATH (str): 哈希库文件路径（固定）

    方法：
    - check_file_by_hash(filepath: str) -> ScanResult
        接受文件路径，返回检测结果对象 ScanResult
    """
    def __init__(self):
        self.hash_db = None
        self.HASH_DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'loki_hashes.txt')
        self._load_hash_db()

    def _load_hash_db(self):
        """
        加载哈希库文件到内存。

        无参数，直接读取固定路径文件。

        异常处理：
        - 文件不存在时打印警告，不抛异常。
        """
        hash_db = {}
        try:
            with open(self.HASH_DB_PATH, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    parts = line.split(';', 1)
                    if len(parts) != 2:
                        continue
                    hash_val, comment = parts
                    hash_db[hash_val.lower()] = comment
        except FileNotFoundError:
            print(f"[WARN] Hash DB file not found: {self.HASH_DB_PATH}")
        self.hash_db = hash_db

    def check_file_by_hash(self, filepath) -> ScanResult:
        """
        检查给定文件是否命中哈希库。

        参数：
        - filepath (str): 待检测文件路径

        返回：
        - ScanResult 对象，包含文件路径、检测状态、威胁类型、建议操作、注释等信息。
        """
        md5 = calc_md5(filepath)
        sha1 = calc_sha1(filepath)
        sha256 = calc_sha256(filepath)

        for h in (md5, sha1, sha256):
            if h in self.hash_db:
                return ScanResult(
                    file_path=filepath,
                    detected=True,
                    threat_type="Known Malware (Hash Match)",
                    recommend="delete",
                    comment=self.hash_db[h],
                    engine="static",
                    hash_value=h
                )
        return ScanResult(
            file_path=filepath,
            detected=False,
            engine="static",
            hash_value=md5
        )