"""Fenster aus Bausteinen (ab 0.9.0): Prüfen und Bereinigen, bevor gespeichert wird.

Ein Fenster ist eine Liste von Bausteinen. Gespeichert wird nur, was die Karte versteht;
alles andere fällt weg. So kann eine fehlerhafte oder fremde Datei nichts kaputt machen.
"""

from __future__ import annotations

import re
from typing import Any

BLOCK_TYPES = ("values", "chart", "actions", "log", "text", "phone")
CHART_KINDS = ("line", "area", "bar", "strip")
RANGES = ("24h", "7d", "30d")
LOG_SOURCES = ("outages", "switch", "reconnect")
TONES = ("info", "warn", "err")
WHEN = ("unavail", "below", "above", "is", "isnot")
COLORS = ("blue", "orange", "green", "purple", "red", "gray", "teal", "pink")

MAX_WINDOWS = 40
MAX_BLOCKS = 20
MAX_ENTITIES = 40
MAX_RULES = 8
MAX_TEXT = 500

_ENTITY = re.compile(r"^[a-z_]+\.[a-z0-9_]+$")
_KEY = re.compile(r"^[A-Za-z0-9_\-]{1,40}$")


def _txt(v: Any, n: int = 80) -> str:
    return str(v or "").strip()[:n]


def _ents(v: Any) -> list[str]:
    out: list[str] = []
    for e in v if isinstance(v, list) else []:
        e = str(e).strip()
        if _ENTITY.match(e) and e not in out:
            out.append(e)
    return out[:MAX_ENTITIES]


def _rules(v: Any) -> list[dict]:
    out = []
    for r in v if isinstance(v, list) else []:
        if not isinstance(r, dict) or r.get("when") not in WHEN:
            continue
        out.append({
            "c": "err" if r.get("c") == "err" else "warn",
            "any": "all" if r.get("any") == "all" else "any",
            "grp": _txt(r.get("grp") or "all", 30),
            "when": r["when"],
            "v": _txt(r.get("v"), 40),
        })
    return out[:MAX_RULES]


def clean_block(b: Any) -> dict | None:
    if not isinstance(b, dict) or b.get("t") not in BLOCK_TYPES:
        return None
    t = b["t"]
    out: dict[str, Any] = {"t": t}
    if t != "text":
        out["title"] = _txt(b.get("title"))
    if t in ("values", "chart", "actions"):
        out["ents"] = _ents(b.get("ents"))
    if t == "values":
        out["rules"] = _rules(b.get("rules"))
        out["style"] = "list" if b.get("style") == "list" else "tiles"
    elif t == "chart":
        lim = b.get("limit") if isinstance(b.get("limit"), dict) else {}
        out.update({
            "kind": b.get("kind") if b.get("kind") in CHART_KINDS else "line",
            "range": b.get("range") if b.get("range") in RANGES else "24h",
            "mode": "separate" if b.get("mode") == "separate" else "together",
            "colors": {e: c for e, c in (b.get("colors") if isinstance(b.get("colors"), dict) else {}).items()
                       if e in out["ents"] and c in COLORS},
            "limit": {"on": bool(lim.get("on")), "v": _txt(lim.get("v"), 20),
                      "dir": "above" if lim.get("dir") == "above" else "below",
                      "c": "err" if lim.get("c") == "err" else "warn"},
            "stats": bool(b.get("stats")),
        })
    elif t == "log":
        out["src"] = b.get("src") if b.get("src") in LOG_SOURCES else "outages"
        try:
            out["n"] = max(1, min(20, int(b.get("n") or 5)))
        except (TypeError, ValueError):
            out["n"] = 5
        out["style"] = "list" if b.get("style") == "list" else "timeline"
    elif t == "text":
        out["text"] = _txt(b.get("text"), MAX_TEXT)
        out["tone"] = b.get("tone") if b.get("tone") in TONES else "info"
    return out


def clean_windows(w: Any) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    for k, blocks in (w.items() if isinstance(w, dict) else []):
        if not _KEY.match(str(k)) or not isinstance(blocks, list):
            continue
        cleaned = [c for c in (clean_block(b) for b in blocks[:MAX_BLOCKS]) if c]
        out[str(k)] = cleaned
        if len(out) >= MAX_WINDOWS:
            break
    return out
