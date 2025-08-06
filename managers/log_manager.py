import json, itertools, datetime, pathlib
from structs.log_entry import LogEntry

class LogManager:
    _ID = itertools.count(1)

    def __init__(self, path="data/logs.json"):
        self.path = pathlib.Path(path)
        self.path.parent.mkdir(exist_ok=True)
        self._load()

    # ---------- public ----------
    def log(self, component: str, event_type: str,
            summary: str, path: str = "") -> LogEntry:
        entry = LogEntry(
            id        = next(self._ID),
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            path      = path,
            component = component,
            event_type= event_type,
            summary   = summary
        )
        self.entries.insert(0, entry)
        self._save()
        return entry

    # ---------- io ----------
    def _load(self):
        if self.path.exists():
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            self.entries = [LogEntry(**d) for d in raw]
            if self.entries:
                LogManager._ID = itertools.count(self.entries[0].id + 1)
        else:
            self.entries = []

    def _save(self):
        self.path.write_text(
            json.dumps([e.__dict__ for e in self.entries],
                       ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
