import os
import shutil

class ExecuteEngine:
    """
    处置动作引擎

    职责：
        - 提供文件删除、隔离、还原等批量操作的接口
        - 返回每个文件的操作结果，供路由或UI处理

    方法：
        - delete_files(files: list[str]) -> dict
            批量删除文件，返回各文件的处理结果
        - quarantine_files(files: list[str], quarantine_dir: str) -> dict
            批量隔离文件，返回各文件的处理结果
        - restore_files(files: list[str], origin_paths: list[str]) -> dict
            批量还原文件，返回各文件的处理结果

    说明：
        - 单个文件操作请直接将文件路径打包成长度为1的list
        - 所有返回值均为 dict[str, bool]，key为文件路径，value为是否成功
    """

    def delete_files(self, files: list[str]) -> dict:
        """
        批量删除文件。

        Args:
            files (list[str]): 待删除文件路径列表

        Returns:
            dict[str, bool]: 每个文件的操作结果，True为成功，False为失败
        """
        results = {}
        for file_path in files:
            try:
                os.remove(file_path)
                results[file_path] = True
            except Exception as e:
                print(f"[ERROR] Delete failed: {file_path} - {e}")
                results[file_path] = False
        return results

    def quarantine_files(self, files: list[str], quarantine_dir: str) -> dict:
        """
        批量隔离文件。

        Args:
            files (list[str]): 待隔离文件路径列表
            quarantine_dir (str): 隔离区目标目录

        Returns:
            dict[str, bool]: 每个文件的操作结果
        """
        results = {}
        if not os.path.exists(quarantine_dir):
            os.makedirs(quarantine_dir)
        for file_path in files:
            try:
                shutil.move(file_path, quarantine_dir)
                results[file_path] = True
            except Exception as e:
                print(f"[ERROR] Quarantine failed: {file_path} - {e}")
                results[file_path] = False
        return results

    def restore_files(self, files: list[str], origin_paths: list[str]) -> dict:
        """
        批量还原文件。

        Args:
            files (list[str]): 待还原文件在隔离区的路径
            origin_paths (list[str]): 每个文件原始路径（与files一一对应）

        Returns:
            dict[str, bool]: 每个文件的操作结果
        """
        results = {}
        for file_path, origin_path in zip(files, origin_paths):
            try:
                shutil.move(file_path, origin_path)
                results[file_path] = True
            except Exception as e:
                print(f"[ERROR] Restore failed: {file_path} - {e}")
                results[file_path] = False
        return results
