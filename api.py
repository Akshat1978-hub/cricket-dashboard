"""
api.py — CricAPI integration for IPL Dashboard
Handles all external API calls with caching and error handling.
"""

import os
import requests
import streamlit as st
from datetime import datetime

# ─── API Config ───────────────────────────────────────────────────────────────

def get_api_key() -> str:
    """Retrieve API key from st.secrets or .env"""
    try:
        return st.secrets["CRICKET_API_KEY"]
    except Exception:
        from dotenv import load_dotenv
        load_dotenv()
        key = os.getenv("CRICKET_API_KEY", "")
        if not key:
            raise ValueError(
                "❌ API key not found. Set CRICKET_API_KEY in .env or st.secrets."
            )
        return key

BASE_URL = "https://api.cricapi.com/v1"

def _get(endpoint: str, params: dict = None) -> dict:
    """Generic GET with error handling."""
    try:
        key = get_api_key()
        params = params or {}
        params["apikey"] = key
        resp = requests.get(f"{BASE_URL}/{endpoint}", params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") != "success":
            raise ValueError(data.get("reason", "API returned non-success status"))
        return data
    except requests.exceptions.ConnectionError:
        raise ConnectionError("🌐 Network error — check your internet connection.")
    except requests.exceptions.Timeout:
        raise TimeoutError("⏱ Request timed out. API may be slow.")
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"HTTP {e.response.status_code}: {e}")

# ─── Cached API Calls ─────────────────────────────────────────────────────────

@st.cache_data(ttl=30, show_spinner=False)
def fetch_current_matches() -> list:
    """Fetch all current/live matches."""
    data = _get("currentMatches", {"offset": 0})
    return data.get("data", [])

@st.cache_data(ttl=30, show_spinner=False)
def fetch_ipl_matches() -> list:
    """Filter current matches for IPL only."""
    matches = fetch_current_matches()
    ipl = [
        m for m in matches
        if "ipl" in m.get("series_id", "").lower()
        or "indian premier" in (m.get("series", "") or "").lower()
        or "ipl" in (m.get("name", "") or "").lower()
        or "ipl" in str(m).lower()
    ]
    return ipl if ipl else matches  # fallback: show all if no IPL tag

@st.cache_data(ttl=60, show_spinner=False)
def fetch_match_info(match_id: str) -> dict:
    """Fetch detailed info for a single match."""
    data = _get("match_info", {"id": match_id})
    return data.get("data", {})

@st.cache_data(ttl=120, show_spinner=False)
def fetch_series_list() -> list:
    """Fetch current series list."""
    data = _get("series", {"offset": 0})
    return data.get("data", [])

@st.cache_data(ttl=300, show_spinner=False)
def fetch_players_by_team(team_id: str) -> list:
    """Fetch squad for a given team."""
    data = _get("players", {"search": team_id})
    return data.get("data", [])

@st.cache_data(ttl=600, show_spinner=False)
def fetch_player_info(player_id: str) -> dict:
    """Fetch detailed player profile."""
    data = _get("players_info", {"id": player_id})
    return data.get("data", {})

# ─── Demo / Fallback Data ─────────────────────────────────────────────────────

def get_demo_matches() -> list:
    """Richly detailed demo data when API key is absent."""
    return [
        {
            "id": "demo-1",
            "name": "Mumbai Indians vs Chennai Super Kings",
            "matchType": "T20",
            "status": "Mumbai Indians won by 5 wickets",
            "venue": "Wankhede Stadium, Mumbai",
            "date": "2025-04-10",
            "teams": ["Mumbai Indians", "Chennai Super Kings"],
            "score": [
                {"r": 189, "w": 4, "o": 20.0, "inning": "Mumbai Indians Inning 1"},
                {"r": 184, "w": 6, "o": 20.0, "inning": "Chennai Super Kings Inning 1"},
            ],
            "series_id": "ipl-2025",
            "toss": {"winner": "Mumbai Indians", "decision": "bat"},
        },
        {
            "id": "demo-2",
            "name": "Royal Challengers Bengaluru vs Kolkata Knight Riders",
            "matchType": "T20",
            "status": "Match in progress",
            "venue": "M. Chinnaswamy Stadium, Bengaluru",
            "date": "2025-04-10",
            "teams": ["Royal Challengers Bengaluru", "Kolkata Knight Riders"],
            "score": [
                {"r": 142, "w": 3, "o": 15.2, "inning": "Royal Challengers Bengaluru Inning 1"},
            ],
            "series_id": "ipl-2025",
            "toss": {"winner": "Kolkata Knight Riders", "decision": "field"},
        },
        {
            "id": "demo-3",
            "name": "Rajasthan Royals vs Delhi Capitals",
            "matchType": "T20",
            "status": "Rajasthan Royals won by 8 runs",
            "venue": "Sawai Mansingh Stadium, Jaipur",
            "date": "2025-04-09",
            "teams": ["Rajasthan Royals", "Delhi Capitals"],
            "score": [
                {"r": 201, "w": 5, "o": 20.0, "inning": "Rajasthan Royals Inning 1"},
                {"r": 193, "w": 8, "o": 20.0, "inning": "Delhi Capitals Inning 1"},
            ],
            "series_id": "ipl-2025",
            "toss": {"winner": "Rajasthan Royals", "decision": "bat"},
        },
        {
            "id": "demo-4",
            "name": "Sunrisers Hyderabad vs Punjab Kings",
            "matchType": "T20",
            "status": "Match in progress",
            "venue": "Rajiv Gandhi International Stadium, Hyderabad",
            "date": "2025-04-10",
            "teams": ["Sunrisers Hyderabad", "Punjab Kings"],
            "score": [
                {"r": 167, "w": 7, "o": 20.0, "inning": "Sunrisers Hyderabad Inning 1"},
                {"r": 98, "w": 4, "o": 12.3, "inning": "Punjab Kings Inning 1"},
            ],
            "series_id": "ipl-2025",
            "toss": {"winner": "Punjab Kings", "decision": "field"},
        },
        {
            "id": "demo-5",
            "name": "Gujarat Titans vs Lucknow Super Giants",
            "matchType": "T20",
            "status": "Gujarat Titans won by 3 wickets",
            "venue": "Narendra Modi Stadium, Ahmedabad",
            "date": "2025-04-08",
            "teams": ["Gujarat Titans", "Lucknow Super Giants"],
            "score": [
                {"r": 176, "w": 7, "o": 20.0, "inning": "Gujarat Titans Inning 1"},
                {"r": 174, "w": 9, "o": 20.0, "inning": "Lucknow Super Giants Inning 1"},
            ],
            "series_id": "ipl-2025",
            "toss": {"winner": "Lucknow Super Giants", "decision": "bat"},
        },
    ]

def get_demo_players() -> list:
    return [
        {"id": "p1",  "name": "Rohit Sharma",      "team": "Mumbai Indians",              "role": "Batsman",      "runs": 487, "wickets": 0,  "avg": 38.2},
        {"id": "p2",  "name": "MS Dhoni",           "team": "Chennai Super Kings",         "role": "WK-Batsman",   "runs": 312, "wickets": 0,  "avg": 44.5},
        {"id": "p3",  "name": "Virat Kohli",        "team": "Royal Challengers Bengaluru", "role": "Batsman",      "runs": 521, "wickets": 0,  "avg": 46.8},
        {"id": "p4",  "name": "Jasprit Bumrah",     "team": "Mumbai Indians",              "role": "Bowler",       "runs": 12,  "wickets": 18, "avg": 0.0},
        {"id": "p5",  "name": "Ravindra Jadeja",    "team": "Chennai Super Kings",         "role": "All-Rounder",  "runs": 198, "wickets": 14, "avg": 22.1},
        {"id": "p6",  "name": "KL Rahul",           "team": "Lucknow Super Giants",        "role": "WK-Batsman",   "runs": 445, "wickets": 0,  "avg": 40.5},
        {"id": "p7",  "name": "Shubman Gill",       "team": "Gujarat Titans",              "role": "Batsman",      "runs": 468, "wickets": 0,  "avg": 42.5},
        {"id": "p8",  "name": "Hardik Pandya",      "team": "Mumbai Indians",              "role": "All-Rounder",  "runs": 267, "wickets": 11, "avg": 26.7},
        {"id": "p9",  "name": "Yuzvendra Chahal",   "team": "Rajasthan Royals",            "role": "Bowler",       "runs": 5,   "wickets": 21, "avg": 0.0},
        {"id": "p10", "name": "Sanju Samson",       "team": "Rajasthan Royals",            "role": "WK-Batsman",   "runs": 389, "wickets": 0,  "avg": 35.4},
        {"id": "p11", "name": "Andre Russell",      "team": "Kolkata Knight Riders",       "role": "All-Rounder",  "runs": 301, "wickets": 9,  "avg": 30.1},
        {"id": "p12", "name": "Pat Cummins",        "team": "Kolkata Knight Riders",       "role": "Bowler",       "runs": 45,  "wickets": 15, "avg": 0.0},
    ]
