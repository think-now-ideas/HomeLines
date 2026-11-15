"""Wie hassfest: Platzhalter in Übersetzungen müssen gültige Namen sein ({name}, keine JSON-Beispiele)."""
import json
import re
from pathlib import Path

D = Path(__file__).parent.parent / "custom_components" / "homelines"


def _walk(node, path=""):
    if isinstance(node, dict):
        for k, v in node.items():
            yield from _walk(v, f"{path}.{k}")
    elif isinstance(node, str):
        yield path, node


def test_placeholders_are_identifiers():
    for f in [D / "strings.json", *(D / "translations").glob("*.json")]:
        for path, text in _walk(json.loads(f.read_text(encoding="utf-8"))):
            for ph in re.findall(r"\{([^}]*)\}", text):
                assert re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_]*", ph), f"{f.name}{path}: {{{ph}}}"
