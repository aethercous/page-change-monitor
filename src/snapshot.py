from __future__ import annotations
import hashlib, json
from pathlib import Path
import httpx
from bs4 import BeautifulSoup

def capture(url: str) -> dict:
    with httpx.Client(follow_redirects=True, timeout=30.0, headers={"User-Agent": "page-change-monitor/1.0"}) as c:
        r = c.get(url)
        r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")
    for t in soup(["script", "style", "nav", "footer"]):
        t.decompose()
    text = " ".join(soup.get_text(" ", strip=True).split())
    return {
        "url": url,
        "hash": hashlib.sha256(text.encode()).hexdigest(),
        "text": text[:20000],
    }

def load_store(path: Path) -> dict | None:
    if not path.exists():
        return None
    return json.loads(path.read_text())

def save_store(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))
