import json, itertools, datetime, pathlib
from structs.history_entry import ScanHistoryEntry
from structs.actionresults import ActionResult    # ← 改成 ActionResult

class HistoryManager:
    _ID = itertools.count(1)

    def __init__(self, path="db/history.json"):
        self.path = pathlib.Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._load()

    # ---------- IO ----------
    def _load(self):
        if self.path.exists():
            with open(self.path, encoding="utf-8") as f:
                raw = json.load(f)
            self.entries = [self._deserialize(e) for e in raw]
            # 更新 _ID 起点
            if self.entries:
                HistoryManager._ID = itertools.count(self.entries[0].id + 1)
        else:
            self.entries = []

    def _save(self):
        data = [self._serialize(e) for e in self.entries]
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # ---------- public ----------
    def add_entry(self, start_ts, action_results):
        entry = ScanHistoryEntry(
            id = next(self._ID),
            start_time = datetime.datetime.fromtimestamp(start_ts)
                         .strftime("%Y-%m-%d %H:%M:%S"),
            action_results = action_results     # [] 或 list[ActionResult]
        )
        self.entries.insert(0, entry)
        self._save()

    # ---------- helpers ----------
    def _serialize(self, e: ScanHistoryEntry):
        d = e.__dict__.copy()
        d["action_results"] = [r.__dict__ for r in e.action_results]
        return d

    def _deserialize(self, d: dict):
        d["action_results"] = [ActionResult(**r) for r in d.get("action_results", [])]
        return ScanHistoryEntry(**d)
