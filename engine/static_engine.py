import os
import sqlite3
from structs.scanresult import ScanResult
from .calc_hash import calc_md5

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
        # 1. 定位到项目根目录下的 db/mal_hashes.db
        base_dir = os.path.dirname(__file__)
        root_dir = os.path.abspath(os.path.join(base_dir, '..'))
        self.DB_PATH = os.path.join(root_dir, 'db', 'mal_hashes.db')

        # 2. 打开 SQLite 连接
        self.conn = sqlite3.connect(self.DB_PATH)
        self.cur = self.conn.cursor()

    def check_file_by_hash(self, filepath) -> ScanResult:
        """
        检查给定文件是否命中哈希库。

        参数：
        - filepath (str): 待检测文件路径

        返回：
        - ScanResult 对象，包含文件路径、检测状态、威胁类型、建议操作、注释等信息。
        """
        # 只用 MD5
        md5 = calc_md5(filepath).lower()

        # 直接 SQL 查询
        self.cur.execute("SELECT md5 FROM hashes WHERE md5 = ?", (md5,))
        if self.cur.fetchone():
            return ScanResult(
                file_path=filepath,
                detected=True,
                threat_type="Known Malware",
                reason="MD5 Hash Match",
                recommend="quarantine",
                comment="VirusShare MD5 (DB)",
                engine="static",
                hash_value=md5
            )
        
        return ScanResult(
            file_path=filepath,
            detected=False,
            engine="static",
            hash_value=md5
        )
    
    def close(self):
        """关闭数据库连接，程序退出前调用。"""
        self.conn.close()