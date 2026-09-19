import json
from datetime import datetime, timezone
from pathlib import Path
AUDIT_FILE = Path("audit.log")
def write_audit(event: dict):
    event = {"ts": datetime.now(timezone.utc).isoformat(), **event}
    with AUDIT_FILE.open("a", encoding="utf-8") as f: f.write(json.dumps(event, ensure_ascii=False) + "\n")
