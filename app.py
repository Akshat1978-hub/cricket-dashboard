"""
app.py — IPL Live Dashboard 🏏
Production-grade Streamlit app with real-time data, modern UI, and full interactivity.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from datetime import datetime

# ─── Page Config (must be first Streamlit call) ───────────────────────────────
st.set_page_config(
    page_title="IPL Live Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Auto-refresh ─────────────────────────────────────────────────────────────
try:
    from streamlit_autorefresh import st_autorefresh
    refresh_count = st_autorefresh(interval=30_000, limit=None, key="ipl_autorefresh")
except ImportError:
    refresh_count = 0  # graceful fallback

# ─── Imports ──────────────────────────────────────────────────────────────────
from components.cards import GLOBAL_CSS
from api import fetch_ipl_matches, get_demo_matches, get_demo_players
import pages.live_matches as live_matches_page
import pages.team_analytics as team_analytics_page
import pages.player_stats as player_stats_page

# ─── Inject CSS ───────────────────────────────────────────────────────────────
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ─── Data Loading ─────────────────────────────────────────────────────────────

DEMO_MODE = False

@st.cache_data(ttl=30, show_spinner=False)
def load_matches():
    global DEMO_MODE
    try:
        matches = fetch_ipl_matches()
        if not matches:
            raise ValueError("No matches returned from API")
        DEMO_MODE = False
        return matches, False
    except Exception as e:
        return get_demo_matches(), True

@st.cache_data(ttl=300, show_spinner=False)
def load_players():
    return get_demo_players()

# ─── Header ───────────────────────────────────────────────────────────────────
now = datetime.now().strftime("%d %b %Y · %I:%M %p")
st.markdown(f"""
<div class="ipl-header">
  <div class="ipl-header-logo">🏏</div>
  <div class="ipl-header-text">
    <h1>IPL Live Dashboard</h1>
    <p>Indian Premier League 2025 · Real-time Analytics Platform</p>
  </div>
  <div style="margin-left:auto; text-align:right">
    <div class="refresh-info">🔄 Auto-refresh every 30s · {now}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
<div style="padding:16px 0 8px">
  <div style="font-family:Syne,sans-serif; font-size:20px; font-weight:800; color:#f0f0fa">⚙️ Controls</div>
  <div style="font-size:12px; color:#55556a; margin-top:4px">Dashboard settings & filters</div>
</div>
""", unsafe_allow_html=True)

    st.divider()

    # Manual refresh
    if st.button("🔄 Refresh Now", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # API Key input (if not set)
    api_key_set = bool(os.getenv("CRICKET_API_KEY", ""))
    try:
        api_key_set = bool(st.secrets.get("CRICKET_API_KEY", ""))
    except Exception:
        pass

    if not api_key_set:
        with st.expander("🔑 Enter API Key", expanded=False):
            entered_key = st.text_input("CricAPI Key", type="password", key="api_key_input",
                                        help="Get free key at cricapi.com")
            if entered_key:
                os.environ["CRICKET_API_KEY"] = entered_key
                st.cache_data.clear()
                st.success("Key saved for this session!")
                st.rerun()
            st.caption("Without a key, demo data is shown.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
<div style="font-size:11px; color:#55556a; line-height:1.6">
  <div style="color:#8888aa; font-family:Syne,sans-serif; font-weight:600; margin-bottom:8px">About</div>
  Built with Streamlit · Data from CricAPI<br>
  Auto-refreshes every 30 seconds.<br><br>
  <span style="color:#e8c94d">★ IPL 2025 Season</span>
</div>
""", unsafe_allow_html=True)

    st.divider()
    # Refresh counter
    if refresh_count:
        st.caption(f"⚡ Refreshed {refresh_count} time(s) this session")

# ─── Load Data ────────────────────────────────────────────────────────────────
with st.spinner("⚡ Loading match data..."):
    matches, demo_mode = load_matches()
    players = load_players()

# Demo banner
if demo_mode:
    st.markdown("""
<div class="demo-banner">
  <strong>📋 Demo Mode</strong> — Live data unavailable (no API key or API error).
  Enter your <a href="https://cricapi.com" target="_blank" style="color:#e8c94d">CricAPI</a> key in the sidebar to see real IPL data.
  Showing sample IPL 2025 match data.
</div>
""", unsafe_allow_html=True)

# ─── Tab Navigation ───────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "🏏  Live Matches",
    "📊  Team Analytics",
    "🧑‍💻  Player Stats",
])

with tab1:
    live_matches_page.render(matches, demo_mode=demo_mode)

with tab2:
    team_analytics_page.render(matches, players)

with tab3:
    player_stats_page.render(players)

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="
  margin-top: 48px;
  padding: 20px 0;
  border-top: 1px solid rgba(255,255,255,0.06);
  text-align: center;
  font-size: 12px;
  color: #55556a;
">
  IPL Live Dashboard · Built with ❤️ using Streamlit & Plotly · Data: CricAPI ·
  <span style="color: #e8c94d">IPL 2025</span>
</div>
""", unsafe_allow_html=True)
