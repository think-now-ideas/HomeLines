"""Internet-Überwachung per Ping mit Ausfallprotokoll."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging
import re

from homeassistant.util import dt as dt_util

from .const import HISTORY_DAYS, RECENT_OUTAGES

_LOGGER = logging.getLogger(__name__)

try:
    from icmplib import async_ping
    from icmplib.exceptions import ICMPLibError, SocketPermissionError

    HAS_ICMPLIB = True
except ImportError:  # pragma: no cover
    HAS_ICMPLIB = False

_RE_RECV = re.compile(r"(\d+) packets transmitted, (\d+) (?:packets )?received")
_RE_RTT = re.compile(r"=\s*[\d.]+/([\d.]+)/")

CAUSE_INTERNET = "internet"
CAUSE_LOCAL = "local"
CAUSE_UNKNOWN = "unknown"


@dataclass
class PingResult:
    host: str
    reachable: bool
    latency: float | None
    loss: float


class Pinger:
    """Wählt automatisch eine funktionierende Ping-Methode."""

    def __init__(self) -> None:
        self._privileged: bool | None = True if HAS_ICMPLIB else None

    async def ping(self, host: str, count: int, timeout: float = 2) -> PingResult:
        if self._privileged is not None:
            try:
                r = await async_ping(host, count=count, interval=0.3, timeout=timeout,
                                     privileged=self._privileged)
                return PingResult(host, r.is_alive, round(r.avg_rtt, 1) if r.is_alive else None,
                                  round(r.packet_loss * 100, 1))
            except SocketPermissionError:
                if self._privileged:
                    self._privileged = False
                    return await self.ping(host, count, timeout)
                self._privileged = None
            except ICMPLibError as err:
                _LOGGER.debug("icmplib: %s", err)
                return PingResult(host, False, None, 100.0)
        return await self._subprocess(host, count, timeout)

    async def _subprocess(self, host: str, count: int, timeout: float) -> PingResult:
        try:
            proc = await asyncio.create_subprocess_exec(
                "ping", "-n", "-q", "-c", str(count), "-W", str(int(timeout)), host,
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.DEVNULL)
            out, _ = await asyncio.wait_for(proc.communicate(), count * timeout + 5)
        except (OSError, TimeoutError):
            return PingResult(host, False, None, 100.0)
        text = out.decode(errors="ignore")
        m = _RE_RECV.search(text)
        sent, recv = (int(m.group(1)), int(m.group(2))) if m else (count, 0)
        rtt = _RE_RTT.search(text)
        loss = 100.0 if sent == 0 else round((sent - recv) / sent * 100, 1)
        return PingResult(host, recv > 0, float(rtt.group(1)) if rtt and recv else None, loss)


def fmt_duration(seconds: float) -> str:
    seconds = int(seconds)
    h, rest = divmod(seconds, 3600)
    m, s = divmod(rest, 60)
    if h:
        return f"{h} h {m} min"
    if m:
        return f"{m} min {s} s"
    return f"{s} s"


class OutageLog:
    """Ausfälle: Beginn, Ende, Ursache. Persistenz übernimmt der Aufrufer."""

    def __init__(self, data: dict | None = None) -> None:
        data = data or {}
        self.outages: list[dict] = data.get("outages", [])
        self.current: dict | None = data.get("current")

    def as_dict(self) -> dict:
        return {"outages": self.outages, "current": self.current}

    def start(self, when: datetime, cause: str) -> None:
        if self.current is None:
            self.current = {"start": when.isoformat(), "cause": cause, "last_offline": when.isoformat()}

    def touch(self, when: datetime, cause: str) -> None:
        if self.current:
            self.current["last_offline"] = when.isoformat()
            if cause == CAUSE_LOCAL:
                self.current["cause"] = CAUSE_LOCAL

    def end(self, when: datetime, interrupted: bool = False) -> dict | None:
        if self.current is None:
            return None
        start = dt_util.parse_datetime(self.current["start"])
        end = when if not interrupted else dt_util.parse_datetime(self.current["last_offline"])
        entry = {
            "start": self.current["start"],
            "end": end.isoformat(),
            "duration": max(0, int((end - start).total_seconds())),
            "cause": self.current.get("cause", CAUSE_UNKNOWN),
            "interrupted_by_restart": interrupted,
        }
        self.outages.append(entry)
        self.current = None
        self.prune(when)
        return entry

    def prune(self, now: datetime) -> None:
        cutoff = now - timedelta(days=HISTORY_DAYS)
        self.outages = [o for o in self.outages if dt_util.parse_datetime(o["end"]) >= cutoff]

    def _window(self, now: datetime, days: float) -> list[tuple[datetime, datetime]]:
        start = now - timedelta(days=days)
        spans = []
        for o in self.outages:
            s, e = dt_util.parse_datetime(o["start"]), dt_util.parse_datetime(o["end"])
            if e >= start:
                spans.append((max(s, start), e))
        if self.current:
            spans.append((max(dt_util.parse_datetime(self.current["start"]), start), now))
        return spans

    def count(self, now: datetime, days: float) -> int:
        return len(self._window(now, days))

    def downtime(self, now: datetime, days: float) -> int:
        return int(sum((e - s).total_seconds() for s, e in self._window(now, days)))

    def availability(self, now: datetime, days: float) -> float:
        return round(100 - self.downtime(now, days) / (days * 86400) * 100, 3)

    def recent(self) -> list[dict]:
        out = []
        for o in reversed(self.outages[-RECENT_OUTAGES:]):
            start = dt_util.as_local(dt_util.parse_datetime(o["start"]))
            out.append({"start": start.strftime("%d.%m.%Y %H:%M:%S"),
                        "duration": fmt_duration(o["duration"]), "seconds": o["duration"],
                        "cause": o["cause"]})
        return out
