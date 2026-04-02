"""
components/cards.py
-------------------
Global CSS + reusable HTML card builders for the IPL Dashboard.
Import GLOBAL_CSS and inject it with st.markdown(GLOBAL_CSS, unsafe_allow_html=True).
"""

# ── Lazy imports so this module can be syntax-checked without streamlit ────────
try:
    from utils import (
        is_live, is_completed, get_team_color, get_team_short,
        parse_score, avatar_url, truncate,
    )
except ImportError:  # graceful fallback if utils isn't on path yet
    def is_live(m): return "progress" in str(m.get("status","")).lower()
    def is_completed(m): return "won" in str(m.get("status","")).lower()
    def get_team_color(name, key="primary"): return "#e8c94d"
    def get_team_short(name): return "".join(w[0].upper() for w in name.split()[:3])
    def parse_score(s): return s or []
    def truncate(t, n=30): return t[:n-1]+"…" if len(t)>n else t
    def avatar_url(name, **kw):
        i = "+".join(p[0].upper() for p in name.split()[:2])
        return f"https://ui-avatars.com/api/?name={i}&background=1a1a2e&color=e8c94d&size=128&bold=true&rounded=true"


# ═══════════════════════════════════════════════════════════════════════════════
#  GLOBAL_CSS  — inject once at the top of app.py
# ═══════════════════════════════════════════════════════════════════════════════

GLOBAL_CSS = """
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500&display=swap');

/* ── Design Tokens ── */
:root {
  --bg-base:        #0a0a12;
  --bg-card:        #111120;
  --bg-card-hover:  #161628;
  --bg-elevated:    #1a1a2e;
  --border:         rgba(255,255,255,0.07);
  --border-glow:    rgba(232,201,77,0.35);
  --text-primary:   #f0f0fa;
  --text-secondary: #8888aa;
  --text-muted:     #55556a;
  --gold:           #e8c94d;
  --gold-dim:       #a88d30;
  --live-green:     #00e676;
  --radius-lg:      16px;
  --radius-md:      10px;
  --radius-sm:      6px;
  --shadow-card:    0 4px 24px rgba(0,0,0,.45), 0 1px 4px rgba(0,0,0,.3);
  --shadow-hover:   0 8px 40px rgba(0,0,0,.6),  0 2px 8px rgba(0,0,0,.4);
  --transition:     all .22s cubic-bezier(.4,0,.2,1);
}

/* ── Global Reset ── */
html, body, [class*="css"] {
  font-family: 'DM Sans', sans-serif !important;
  background-color: var(--bg-base) !important;
  color: var(--text-primary) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar        { width:5px; height:5px; }
::-webkit-scrollbar-track  { background: var(--bg-base); }
::-webkit-scrollbar-thumb  { background: var(--border); border-radius:99px; }

/* ── Streamlit surface overrides ── */
.stApp                          { background: var(--bg-base) !important; }
section[data-testid="stSidebar"]{ background: #0d0d1a !important; border-right:1px solid var(--border); }

/* Tabs */
.stTabs [data-baseweb="tab-list"]{
  background: var(--bg-elevated) !important;
  border-radius: var(--radius-md) !important;
  padding: 4px !important; gap: 4px !important;
}
.stTabs [data-baseweb="tab"]{
  background: transparent !important;
  color: var(--text-secondary) !important;
  border-radius: var(--radius-sm) !important;
  font-family: 'Syne', sans-serif !important;
  font-weight: 600 !important; font-size: 13px !important;
  letter-spacing: .03em; transition: var(--transition) !important;
}
.stTabs [aria-selected="true"]{
  background: var(--bg-card) !important;
  color: var(--gold) !important;
  box-shadow: 0 1px 6px rgba(0,0,0,.4) !important;
}

/* Inputs / selects */
.stSelectbox > div > div,
.stMultiSelect > div > div {
  background: var(--bg-elevated) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--text-primary) !important;
}

/* Button */
.stButton > button {
  background: linear-gradient(135deg,#e8c94d,#a88d30) !important;
  color: #0a0a12 !important; border:none !important;
  border-radius: var(--radius-sm) !important;
  font-family: 'Syne', sans-serif !important;
  font-weight: 700 !important; letter-spacing:.05em;
  transition: var(--transition) !important;
}
.stButton > button:hover{
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(232,201,77,.35) !important;
}

/* Metric cards */
div[data-testid="metric-container"]{
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-md) !important;
  padding: 16px !important;
}

/* Progress bar */
.stProgress > div > div > div {
  background: linear-gradient(90deg, var(--gold), var(--live-green)) !important;
  border-radius: 99px !important;
}

/* Expander */
.stExpander {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-md) !important;
}

/* ── App Header ── */
.ipl-header{
  display:flex; align-items:center; gap:14px;
  padding:8px 0 24px; border-bottom:1px solid var(--border); margin-bottom:24px;
}
.ipl-header-logo{
  width:52px; height:52px;
  background:linear-gradient(135deg,#e8c94d,#a88d30);
  border-radius:14px; display:flex; align-items:center;
  justify-content:center; font-size:26px; flex-shrink:0;
  box-shadow:0 4px 16px rgba(232,201,77,.3);
}
.ipl-header-text h1{
  font-family:'Syne',sans-serif !important;
  font-weight:800; font-size:28px;
  color:var(--text-primary); margin:0; line-height:1.1;
}
.ipl-header-text p{ font-size:13px; color:var(--text-secondary); margin:2px 0 0; }

/* ── Live Badge ── */
.live-badge{
  display:inline-flex; align-items:center; gap:6px;
  background:rgba(0,230,118,.12); border:1px solid rgba(0,230,118,.3);
  color:var(--live-green); font-family:'Syne',sans-serif;
  font-size:10px; font-weight:700; letter-spacing:.12em;
  padding:3px 10px; border-radius:99px; text-transform:uppercase;
}
.live-badge::before{
  content:''; width:6px; height:6px;
  background:var(--live-green); border-radius:50%;
  animation:pulse 1.4s ease-in-out infinite;
}
@keyframes pulse{
  0%,100%{ opacity:1; transform:scale(1); }
  50%     { opacity:.4; transform:scale(.7); }
}

/* ── Match Card ── */
.match-card{
  background:var(--bg-card); border:1px solid var(--border);
  border-radius:var(--radius-lg); padding:20px; margin-bottom:16px;
  transition:var(--transition); position:relative; overflow:hidden;
}
.match-card::before{
  content:''; position:absolute; top:0; left:0; right:0; height:2px;
  background:linear-gradient(90deg,transparent,var(--gold-dim),transparent);
  opacity:0; transition:var(--transition);
}
.match-card:hover{ border-color:var(--border-glow); box-shadow:var(--shadow-hover); background:var(--bg-card-hover); }
.match-card:hover::before{ opacity:1; }
.match-card.live{
  border-color:rgba(0,230,118,.25);
  box-shadow:0 0 0 1px rgba(0,230,118,.1), var(--shadow-card);
}
.match-card.live::before{
  opacity:1;
  background:linear-gradient(90deg,transparent,var(--live-green),transparent);
}
.match-card-header{
  display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:16px;
}
.match-title{
  font-family:'Syne',sans-serif; font-size:15px; font-weight:700;
  color:var(--text-primary); line-height:1.3;
}
.match-meta { font-size:11px; color:var(--text-muted); margin-top:3px; }
.match-venue{ font-size:12px; color:var(--text-secondary); margin-top:12px; }

/* ── Score Row ── */
.score-row{
  display:flex; align-items:center; justify-content:space-between;
  background:var(--bg-elevated); border-radius:var(--radius-sm);
  padding:10px 14px; margin:4px 0;
}
.score-team { font-family:'Syne',sans-serif; font-size:13px; font-weight:700; color:var(--text-primary); }
.score-value{ font-family:'Syne',sans-serif; font-size:16px; font-weight:800; color:var(--gold); }
.score-overs{ font-size:11px; color:var(--text-muted); }
.match-status     { font-size:12px; margin-top:12px; padding:6px 10px; background:rgba(255,255,255,.04); border-radius:var(--radius-sm); color:var(--text-secondary); }
.match-status.won { color:var(--live-green); background:rgba(0,230,118,.07); }

/* ── Player Card ── */
.player-card{
  background:var(--bg-card); border:1px solid var(--border);
  border-radius:var(--radius-lg); padding:18px 16px;
  text-align:center; transition:var(--transition); height:100%;
}
.player-card:hover{ border-color:var(--border-glow); box-shadow:var(--shadow-hover); }
.player-avatar{
  width:70px; height:70px; border-radius:50%; margin:0 auto 10px;
  display:block; border:2px solid var(--border-glow); object-fit:cover;
}
.player-name { font-family:'Syne',sans-serif; font-size:14px; font-weight:700; color:var(--text-primary); margin-bottom:2px; }
.player-team { font-size:11px; color:var(--text-muted); margin-bottom:10px; }
.player-role-badge{
  display:inline-block; font-size:10px; font-weight:600;
  padding:2px 8px; border-radius:99px;
  background:rgba(232,201,77,.1); border:1px solid rgba(232,201,77,.25);
  color:var(--gold); margin-bottom:12px; font-family:'Syne',sans-serif;
}
.player-stats{ display:flex; justify-content:space-around; border-top:1px solid var(--border); padding-top:10px; margin-top:6px; }
.player-stat-item{ text-align:center; }
.player-stat-value{ font-family:'Syne',sans-serif; font-size:18px; font-weight:800; color:var(--text-primary); }
.player-stat-label{ font-size:9px; text-transform:uppercase; letter-spacing:.08em; color:var(--text-muted); margin-top:1px; }

/* ── Section Heading ── */
.section-heading{
  font-family:'Syne',sans-serif; font-size:20px; font-weight:800;
  color:var(--text-primary); letter-spacing:-.01em; margin:8px 0 18px;
  display:flex; align-items:center; gap:10px;
}
.section-heading::after{ content:''; flex:1; height:1px; background:var(--border); }

/* ── KPI Card ── */
.kpi-card{
  background:var(--bg-card); border:1px solid var(--border);
  border-radius:var(--radius-md); padding:16px 20px; transition:var(--transition);
}
.kpi-card:hover{ border-color:var(--border-glow); }
.kpi-label { font-size:11px; text-transform:uppercase; letter-spacing:.1em; color:var(--text-muted); font-weight:600; }
.kpi-value { font-family:'Syne',sans-serif; font-size:32px; font-weight:800; color:var(--gold); line-height:1.1; margin:4px 0 2px; }
.kpi-sub   { font-size:12px; color:var(--text-secondary); }

/* ── Win Probability Bar ── */
.prob-bar-wrapper{
  background:var(--bg-elevated); border-radius:var(--radius-lg);
  padding:20px; border:1px solid var(--border); margin:16px 0;
}
.prob-bar-label{
  display:flex; justify-content:space-between;
  font-family:'Syne',sans-serif; font-size:13px; font-weight:700; margin-bottom:10px;
}
.prob-bar-track{ height:10px; border-radius:99px; background:var(--border); overflow:hidden; }
.prob-bar-fill { height:100%; border-radius:99px; transition:width .8s cubic-bezier(.4,0,.2,1); }

/* ── Misc ── */
.refresh-info{
  display:flex; align-items:center; gap:8px; font-size:11px; color:var(--text-muted);
  padding:6px 12px; background:rgba(255,255,255,.03);
  border-radius:var(--radius-sm); border:1px solid var(--border);
}
.demo-banner{
  background:linear-gradient(90deg,rgba(232,201,77,.08),rgba(232,201,77,.03));
  border:1px solid rgba(232,201,77,.2); border-radius:var(--radius-md);
  padding:12px 16px; font-size:13px; color:var(--gold); margin-bottom:20px;
}
.demo-banner strong{ font-family:'Syne',sans-serif; }
</style>
"""


# ═══════════════════════════════════════════════════════════════════════════════
#  HTML CARD BUILDERS
# ═══════════════════════════════════════════════════════════════════════════════

def match_card_html(match: dict) -> str:
    """Return HTML string for a single match card."""
    live      = is_live(match)
    completed = is_completed(match)
    name      = match.get("name", "Match")
    teams     = match.get("teams", [])
    venue     = match.get("venue", "Venue TBD")
    status    = match.get("status", "")
    date      = match.get("date", "")
    scores    = parse_score(match.get("score", []))

    card_cls = "match-card live" if live else "match-card"
    badge    = '<span class="live-badge">Live</span>' if live else ""

    score_html = ""
    for s in scores:
        inning_label = s["inning"].replace(" Inning 1","").replace(" Inning 2","")
        color = get_team_color(
            next((t for t in teams if t[:8] in inning_label[:20]), teams[0] if teams else ""),
        )
        score_html += f"""
        <div class="score-row">
          <div><div class="score-team" style="color:{color}">{truncate(inning_label, 28)}</div></div>
          <div style="text-align:right">
            <div class="score-value">{s['runs']}/{s['wickets']}</div>
            <div class="score-overs">{s['overs']} ov</div>
          </div>
        </div>"""

    if not score_html:
        score_html = '<div class="score-row"><div class="score-team" style="color:var(--text-muted)">Match yet to begin</div></div>'

    status_cls  = "match-status won" if completed else "match-status"
    status_icon = "🏆" if completed else ("⚡" if live else "📅")

    return f"""
<div class="{card_cls}">
  <div class="match-card-header">
    <div>
      <div class="match-title">{truncate(name, 45)}</div>
      <div class="match-meta">📅 {date}</div>
    </div>
    {badge}
  </div>
  {score_html}
  <div class="match-venue">📍 {truncate(venue, 50)}</div>
  <div class="{status_cls}">{status_icon} {status}</div>
</div>"""


def player_card_html(player: dict) -> str:
    """Return HTML string for a single player card."""
    name  = player.get("name", "Unknown")
    team  = player.get("team", "")
    role  = player.get("role", "Player")
    runs  = player.get("runs", 0)
    wkts  = player.get("wickets", 0)
    avg   = player.get("avg", 0.0)
    img   = player.get("image", "") or avatar_url(name)
    color = get_team_color(team)

    return f"""
<div class="player-card">
  <img class="player-avatar" src="{img}" alt="{name}"
       onerror="this.src='{avatar_url(name)}'" />
  <div class="player-name">{name}</div>
  <div class="player-team" style="color:{color}">{team}</div>
  <div class="player-role-badge">{role}</div>
  <div class="player-stats">
    <div class="player-stat-item">
      <div class="player-stat-value">{runs}</div>
      <div class="player-stat-label">Runs</div>
    </div>
    <div class="player-stat-item">
      <div class="player-stat-value">{wkts}</div>
      <div class="player-stat-label">Wickets</div>
    </div>
    <div class="player-stat-item">
      <div class="player-stat-value">{avg}</div>
      <div class="player-stat-label">Avg</div>
    </div>
  </div>
</div>"""


def win_prob_html(team1: str, team2: str, prob1: float, prob2: float) -> str:
    """Dual-team win probability bar."""
    c1 = get_team_color(team1)
    c2 = get_team_color(team2)
    s1 = get_team_short(team1)
    s2 = get_team_short(team2)
    return f"""
<div class="prob-bar-wrapper">
  <div class="prob-bar-label">
    <span style="color:{c1}">{s1} {prob1}%</span>
    <span style="color:{c2}">{prob2}% {s2}</span>
  </div>
  <div class="prob-bar-track">
    <div class="prob-bar-fill"
         style="width:{prob1}%; background:linear-gradient(90deg,{c1},{c2});"></div>
  </div>
</div>"""


def kpi_html(label: str, value, sub: str = "") -> str:
    """Single KPI tile."""
    return f"""
<div class="kpi-card">
  <div class="kpi-label">{label}</div>
  <div class="kpi-value">{value}</div>
  <div class="kpi-sub">{sub}</div>
</div>"""
