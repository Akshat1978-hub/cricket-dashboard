"""
utils.py — Helper utilities for IPL Dashboard
"""

from __future__ import annotations
import re
from datetime import datetime

# ─── Team Meta ────────────────────────────────────────────────────────────────

TEAM_META = {
    "Mumbai Indians": {
        "short": "MI",
        "primary": "#004BA0",
        "accent": "#D1AB3E",
        "emoji": "🔵",
    },
    "Chennai Super Kings": {
        "short": "CSK",
        "primary": "#F9CD05",
        "accent": "#00548E",
        "emoji": "🟡",
    },
    "Royal Challengers Bengaluru": {
        "short": "RCB",
        "primary": "#EC1C24",
        "accent": "#1B1B1B",
        "emoji": "🔴",
    },
    "Kolkata Knight Riders": {
        "short": "KKR",
        "primary": "#3A225D",
        "accent": "#F2CB05",
        "emoji": "🟣",
    },
    "Delhi Capitals": {
        "short": "DC",
        "primary": "#0078BC",
        "accent": "#EF1C25",
        "emoji": "🔵",
    },
    "Rajasthan Royals": {
        "short": "RR",
        "primary": "#EA1A85",
        "accent": "#254AA5",
        "emoji": "🩷",
    },
    "Sunrisers Hyderabad": {
        "short": "SRH",
        "primary": "#F7A721",
        "accent": "#E8461A",
        "emoji": "🟠",
    },
    "Punjab Kings": {
        "short": "PBKS",
        "primary": "#ED1B24",
        "accent": "#A7A9AC",
        "emoji": "🔴",
    },
    "Gujarat Titans": {
        "short": "GT",
        "primary": "#1C1C1C",
        "accent": "#2F8BC8",
        "emoji": "⚫",
    },
    "Lucknow Super Giants": {
        "short": "LSG",
        "primary": "#A72056",
        "accent": "#FBDD2B",
        "emoji": "🩵",
    },
}

ALL_TEAMS = list(TEAM_META.keys())

# ─── Match Parsing ─────────────────────────────────────────────────────────────

def is_live(match: dict) -> bool:
    status = (match.get("status") or "").lower()
    return any(kw in status for kw in ["progress", "live", "innings", "batting", "bowling"])

def is_completed(match: dict) -> bool:
    status = (match.get("status") or "").lower()
    return any(kw in status for kw in ["won", "draw", "tie", "abandoned", "no result"])

def parse_score(score_list: list) -> list[dict]:
    """Normalise score objects into dicts."""
    if not score_list:
        return []
    result = []
    for s in score_list:
        result.append({
            "inning": s.get("inning", ""),
            "runs": s.get("r", 0),
            "wickets": s.get("w", 0),
            "overs": float(s.get("o", 0)),
        })
    return result

def get_team_short(name: str) -> str:
    meta = TEAM_META.get(name)
    if meta:
        return meta["short"]
    words = name.split()
    return "".join(w[0].upper() for w in words[:3])

def get_team_color(name: str, key: str = "primary") -> str:
    return TEAM_META.get(name, {}).get(key, "#888888")

# ─── Win Probability ──────────────────────────────────────────────────────────

def calculate_win_probability(
    batting_team: str,
    runs_scored: int,
    wickets_lost: int,
    overs_done: float,
    target: int | None = None,
    total_overs: float = 20.0,
) -> tuple[float, float]:
    """
    Returns (batting_team_prob, bowling_team_prob) as percentages (0-100).
    Uses a simplified DL-style heuristic.
    """
    overs_remaining = max(total_overs - overs_done, 0)
    wickets_remaining = 10 - wickets_lost

    if target is None:
        # First innings — estimate based on resources used
        resource_pct = overs_done / total_overs
        resource_boost = (wickets_remaining / 10) * 0.4
        batting_prob = min(50 + (resource_pct * 25) + (resource_boost * 25), 80)
        return round(batting_prob, 1), round(100 - batting_prob, 1)

    # Second innings chase
    runs_needed = target - runs_scored
    if runs_needed <= 0:
        return 95.0, 5.0
    if overs_remaining <= 0 or wickets_remaining <= 0:
        return 5.0, 95.0

    req_rate = runs_needed / overs_remaining if overs_remaining else 999
    curr_rate = runs_scored / overs_done if overs_done else 0

    # Wickets in hand factor
    wicket_factor = wickets_remaining / 10

    # Rate comparison
    rate_ratio = curr_rate / req_rate if req_rate else 2.0

    base_prob = 50.0
    base_prob += (rate_ratio - 1) * 30   # rate advantage
    base_prob += (wicket_factor - 0.5) * 20  # wickets in hand

    prob = max(5.0, min(95.0, base_prob))
    return round(prob, 1), round(100 - prob, 1)

# ─── Formatting ───────────────────────────────────────────────────────────────

def format_score(score: dict) -> str:
    return f"{score['runs']}/{score['wickets']} ({score['overs']} ov)"

def format_datetime(dt_str: str) -> str:
    try:
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        return dt.strftime("%d %b %Y, %I:%M %p")
    except Exception:
        return dt_str

def truncate(text: str, max_len: int = 30) -> str:
    return text if len(text) <= max_len else text[:max_len - 1] + "…"

def avatar_url(name: str, bg: str = "1a1a2e", color: str = "e8c94d") -> str:
    initials = "+".join(p[0].upper() for p in name.split()[:2])
    return f"https://ui-avatars.com/api/?name={initials}&background={bg}&color={color}&size=128&bold=true&rounded=true"
