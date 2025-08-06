# quarantine/quarantine_engine.py
import shutil, pathlib, subprocess, os

# 隔离区目录
QUAR_DIR = pathlib.Path("data/quarantine")


# ────────── ACL 工具 ──────────
def _lock_acl(path: pathlib.Path):
    """
    仅 Administrators 与 SYSTEM 可读写，其他全部拒绝
    icacls <file> /inheritance:r /grant:r Administrators:F SYSTEM:F
    """
    subprocess.call(
        ['icacls', str(path), '/inheritance:r',
         '/grant:r', 'Administrators:F', 'SYSTEM:F'],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )


def _unlock_acl(path: pathlib.Path):
    """恢复继承，等同默认权限：icacls <file> /inheritance:e"""
    subprocess.call(
        ['icacls', str(path), '/inheritance:e'],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )


# ────────── QuarantineEngine ──────────
class QuarantineEngine:
    """
    负责隔离 / 还原 / 删除（仅 Windows）
    调用者：QuarantineRoute 或 ExecuteRoute
    """

    # ===== 隔离 =====
    def isolate(self, src_path: str) -> tuple[bool, str, str]:
        """
        把 src_path 移动到隔离区并锁权限
        Returns: ok, new_path, err_msg
        """
        try:
            src = pathlib.Path(src_path)
            if not src.exists():
                raise FileNotFoundError(src_path)

            QUAR_DIR.mkdir(parents=True, exist_ok=True)
            dst = QUAR_DIR / f"{src.name}.qtn"              # 改后缀
            shutil.move(src, dst, copy_function=shutil.copy2)
            _lock_acl(dst)
            return True, str(dst), ""
        except Exception as e:
            return False, src_path, str(e)
        
        self.store

    # ===== 还原 =====
    def restore(self, iso_path: str, origin_path: str) -> tuple[bool, str]:
        """
        将隔离文件移回 origin_path 并解锁 ACL
        Returns: ok, err_msg
        """
        try:
            iso = pathlib.Path(iso_path)
            if not iso.exists():
                raise FileNotFoundError(iso_path)

            dst = pathlib.Path(origin_path)
            dst.parent.mkdir(parents=True, exist_ok=True)

            _unlock_acl(iso)

            # 去掉 .qtn 扩展（若有）
            true_name = iso.stem if iso.suffix == ".qtn" else iso.name
            dst = dst.with_name(true_name)

            shutil.move(iso, dst, copy_function=shutil.copy2)
            return True, ""
        except Exception as e:
            return False, str(e)

    # ===== 删除 =====
    def delete(self, iso_path: str) -> tuple[bool, str]:
        """
        彻底删除隔离文件
        Returns: ok, err_msg
        """
        try:
            pathlib.Path(iso_path).unlink(missing_ok=True)
            return True, ""
        except Exception as e:
            return False, str(e)
