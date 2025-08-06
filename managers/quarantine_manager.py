# managers/quarantine_manager.py
import json, pathlib
from structs.actionresults import ActionResult

Q_FILE = pathlib.Path("db/quarantine.json")

class QuarantineManager:
    def load(self) -> list[ActionResult]:
        if not Q_FILE.exists() or Q_FILE.stat().st_size == 0:
            return []                             # 文件不存在或为空

        try:
            raw = json.loads(Q_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            # 文件损坏：备份原文件并重新置空
            Q_FILE.rename(Q_FILE.with_suffix(".broken.json"))
            return []

        return [ActionResult(**d) for d in raw]

    def save(self, items: list[ActionResult]):
        Q_FILE.parent.mkdir(parents=True, exist_ok=True)
        json.dump([ar.__dict__ for ar in items], Q_FILE.open("w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
