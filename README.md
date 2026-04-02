# 🏏 IPL Live Dashboard

A **production-grade, real-time Indian Premier League analytics dashboard** built with Streamlit. Features live match scores, team analytics, player stats, win probability, and a premium dark-theme UI — suitable for a professional portfolio.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🔴 **Live Matches** | Real-time scores, wickets, overs, venue, match status |
| 🔄 **Auto-Refresh** | Automatic data refresh every 30 seconds |
| 📊 **Team Analytics** | Runs comparison, performance trends, points table |
| 🧑‍💻 **Player Stats** | Grid cards, leaderboards, batting/bowling charts |
| 🎯 **Win Probability** | Live in-match probability with animated progress bars |
| 🎨 **Dark Theme UI** | Syne + DM Sans fonts, gold accent, premium card layout |
| ⚡ **Demo Mode** | Works without an API key using rich sample IPL data |
| 🔐 **Secure API** | Reads key from `.env` locally or `st.secrets` on cloud |

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ipl-dashboard.git
cd ipl-dashboard
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API key

```bash
cp .env.example .env
# Open .env and paste your CricAPI key
```

### 5. Run the app

```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

---

## 🔑 API Setup

1. Visit [https://cricapi.com](https://cricapi.com)
2. Create a free account (free tier: 100 req/day)
3. Copy your API key from the dashboard
4. Paste it into `.env`:
   ```
   CRICKET_API_KEY=your_key_here
   ```

> **No API key?** The dashboard works in **Demo Mode** with realistic sample IPL 2025 data. You can also enter the key directly in the sidebar.

---

## 📁 Project Structure

```
ipl_dashboard/
├── app.py                   # Main Streamlit entry point
├── api.py                   # CricAPI integration & demo data
├── utils.py                 # Helpers, team metadata, win probability
├── components/
│   ├── cards.py             # HTML card components + global CSS
│   └── charts.py            # Plotly chart builders
├── pages/
│   ├── live_matches.py      # Live Matches tab
│   ├── team_analytics.py    # Team Analytics tab
│   └── player_stats.py      # Player Stats tab
├── .streamlit/
│   └── secrets.toml         # Streamlit Cloud secrets (gitignored)
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## ☁️ Deploy to Streamlit Cloud

1. Push your code to GitHub (without `.env` — it's gitignored)
2. Go to [https://share.streamlit.io](https://share.streamlit.io)
3. Click **New App** → select your repo → set `app.py` as entry point
4. Under **Advanced settings → Secrets**, add:
   ```toml
   CRICKET_API_KEY = "your_key_here"
   ```
5. Click **Deploy** 🚀

---

## 🛠️ Tech Stack

- **[Streamlit](https://streamlit.io)** — UI framework
- **[Plotly](https://plotly.com/python/)** — interactive charts
- **[CricAPI](https://cricapi.com)** — cricket data API
- **[streamlit-autorefresh](https://github.com/kmcgrady/streamlit-autorefresh)** — 30s auto-refresh
- **[python-dotenv](https://pypi.org/project/python-dotenv/)** — env var management
- **Google Fonts** — Syne (headings) + DM Sans (body)

---

## 📸 Screenshots

> Add screenshots here after running locally.

| Live Matches | Team Analytics | Player Stats |
|---|---|---|
| *(screenshot)* | *(screenshot)* | *(screenshot)* |

---

## 🎨 Design Philosophy

The UI was designed to feel like a **premium SaaS analytics product** (Stripe/Notion-style):

- **Dark base** (`#0a0a12`) with elevated card surfaces
- **Gold accent** (`#e8c94d`) for metrics and highlights  
- **Live green** (`#00e676`) with pulse animation for live matches
- **Syne** display font for headings (bold, geometric)
- **DM Sans** for body text (legible, modern)
- Custom CSS hover states, glow borders, and animated badges

---

## 🤝 Contributing

PRs welcome! Please open an issue first to discuss changes.

---

## 📄 License

MIT License — free to use for personal and commercial projects.

---

*Built with ❤️ for IPL 2025*
