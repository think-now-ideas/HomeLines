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
            **({"notify": True} if r.get("notify") is True else {}),
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


# ---------------------------------------------------------------------- Aufbau der Karte (ab 0.9.1)
BUILTIN_ROWS = ("backup", "speed", "outages")
COMBINE = ("single", "sum", "avg", "min", "max", "list", "ok_of", "count_on")
MAX_ROWS = 24


def clean_layout(v: Any) -> dict:
    """Reihenfolge, Sichtbarkeit und eigene Kacheln der Übersicht; Titel und ausgeblendete Leitungen."""
    v = v if isinstance(v, dict) else {}
    rows: list[dict] = []
    seen: set[str] = set()
    for r in v.get("rows") if isinstance(v.get("rows"), list) else []:
        if not isinstance(r, dict) or not _KEY.match(str(r.get("id", ""))) or r["id"] in seen:
            continue
        rid, on = str(r["id"]), r.get("on") is not False
        if r.get("kind") == "tile":
            rows.append({"id": rid, "kind": "tile", "on": on, "name": _txt(r.get("name"), 40) or "Kachel",
                         "icon": _txt(r.get("icon"), 60) if str(r.get("icon", "")).startswith("mdi:") else "mdi:information-outline",
                         "entities": _ents(r.get("entities")),
                         "combine": r.get("combine") if r.get("combine") in COMBINE else "single",
                         "rules": _rules(r.get("rules")), "second": "bad" if r.get("second") == "bad" else "none"})
        elif rid in BUILTIN_ROWS or re.match(r"^WAN\d$", rid):
            rows.append({"id": rid, "kind": "builtin", "on": on})
        else:
            continue
        seen.add(rid)
        if len(rows) >= MAX_ROWS:
            break
    hide = [str(x) for x in (v.get("hide_lines") or []) if re.match(r"^WAN\d$", str(x))] if isinstance(v.get("hide_lines"), list) else []
    return {"title": _txt(v.get("title"), 40), "rows": rows, "hide_lines": hide}


# ---------------------------------------------------------------------- Warnfarben auswerten (ab 0.9.2)
_NA = ("unavailable", "unknown")
WHEN_N = {"unavail": "nicht erreichbar", "below": "unter", "above": "über", "is": "gleich", "isnot": "nicht gleich"}


def _grp(state) -> str:
    if re.search(r"rufnummer|phone_number|_number_\d+_status", state.entity_id):
        return "phone"
    return state.attributes.get("device_class") or "other"


def _num(x: Any) -> float | None:
    try:
        return float(str(x).replace(",", "."))
    except (TypeError, ValueError):
        return None


def rule_hit(get, r: dict, eid: str) -> bool | None:
    """Wie hlRuleHit in der Karte: None = Regel gilt für diesen Wert nicht."""
    st = get(eid)
    if st is None or (r.get("grp", "all") != "all" and _grp(st) != r["grp"]):
        return None
    na = st.state in _NA
    if r["when"] == "unavail":
        return na
    if na:
        return False
    n, v = _num(st.state), _num(r.get("v"))
    if r["when"] == "below":
        return n is not None and v is not None and n < v
    if r["when"] == "above":
        return n is not None and v is not None and n > v
    if r["when"] == "is":
        return str(st.state) == str(r.get("v"))
    return str(st.state) != str(r.get("v"))


def tile_level(get, rules: list[dict], ents: list[str]) -> tuple[str, list[str]]:
    """Höchste Warnfarbe („err“ vor „warn“) und die Gründe als kurze Sätze."""
    lvl, why = "", []
    for r in rules:
        res = [(e, rule_hit(get, r, e)) for e in ents]
        res = [(e, x) for e, x in res if x is not None]
        hit = bool(res) and (all(x for _, x in res) if r.get("any") == "all" else any(x for _, x in res))
        if not hit:
            continue
        names = [(get(e).name if get(e) else e) for e, x in res if x]
        why.append(f"{', '.join(names)}: {WHEN_N.get(r['when'], r['when'])}{'' if r['when'] == 'unavail' else ' ' + str(r.get('v'))}")
        if r.get("c") == "err":
            lvl = "err"
        elif not lvl:
            lvl = "warn"
    return lvl, why
