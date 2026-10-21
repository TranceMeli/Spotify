"""Standalone HTML dashboard: header, KPI strip, chart cards with insights, footer."""

from html import escape

from . import charts

KAGGLE_URL = "https://www.kaggle.com/datasets/nelgiriyewithana/top-spotify-songs-2023"
REPO_URL = "https://github.com/TranceMeli/Spotify"

CARDS = [
    ("songs", "Top 5 most streamed songs", charts.top_songs_fig, False),
    ("keys", "Top 5 keys", charts.top_keys_fig, False),
    ("mode", "Major vs. minor in the top 5 keys", charts.key_mode_fig, False),
    ("audio", "Average audio features", charts.audio_profile_fig, False),
    ("bpm", "Tempo distribution", charts.bpm_fig, True),
]

SUBTITLES = {
    "songs": "Cumulative Spotify streams per track",
    "keys": "Most common musical keys (songs with a known key)",
    "mode": "How each key splits into major and minor",
    "audio": "Mean score across all songs (0–100%)",
    "bpm": "Number of songs per 10 BPM range, darker bar = median",
}

CSS = """
:root { --green:#1DB954; --black:#191414; --muted:#6A6A6A; --bg:#F4F6F5; }
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--black);
  font-family:Inter, Circular, "Segoe UI", Arial, sans-serif; }
header { background:var(--green); color:var(--black); padding:40px 24px 34px; text-align:center; }
header h1 { margin:0; font-size:clamp(26px,4vw,40px); letter-spacing:.04em; }
header p { margin:10px auto 0; max-width:720px; font-size:16px; color:rgba(25,20,20,.8); }
.kpis { display:flex; flex-wrap:wrap; gap:14px; justify-content:center; margin-top:26px; }
.kpi { background:rgba(255,255,255,.92); border-radius:12px; padding:12px 22px; min-width:150px; }
.kpi b { display:block; font-size:26px; }
.kpi span { font-size:13px; color:var(--muted); }
main { max-width:1180px; margin:0 auto; padding:28px 16px 12px;
  display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:20px; }
.card { background:#fff; border-radius:14px; padding:20px 22px 18px;
  box-shadow:0 1px 3px rgba(0,0,0,.08); border-top:4px solid var(--green); }
.card.wide { grid-column:1 / -1; }
.card h2 { margin:0; font-size:15px; text-transform:uppercase; letter-spacing:.05em; }
.card .sub { margin:6px 0 22px; font-size:13px; color:var(--muted); }
.insight { margin:10px 0 0; padding:10px 14px; background:#F2FBF5; border-left:3px solid var(--green);
  border-radius:0 8px 8px 0; font-size:14px; line-height:1.5; }
footer { background:var(--black); color:#B3B3B3; text-align:center; padding:26px 16px;
  margin-top:20px; font-size:13px; line-height:1.7; }
footer a { color:var(--green); text-decoration:none; }
footer a:hover { text-decoration:underline; }
footer .brand { color:#fff; font-weight:700; letter-spacing:.06em; }
@media (max-width:820px) { main { grid-template-columns:1fr; } }
"""


def build_html(df) -> str:
    texts = charts.insights(df)
    cards = []
    for i, (key, title, make_fig, wide) in enumerate(CARDS):
        fig_html = make_fig(df).to_html(
            full_html=False,
            include_plotlyjs="cdn" if i == 0 else False,
            config={"displayModeBar": False, "responsive": True},
        )
        cards.append(
            f'<section class="card{" wide" if wide else ""}"><h2>{escape(title)}</h2>'
            f'<p class="sub">{escape(SUBTITLES[key])}</p>{fig_html}<p class="insight">{texts[key]}</p></section>'
        )
    kpis = "".join(f'<div class="kpi"><b>{v}</b><span>{l}</span></div>' for v, l in charts.kpis(df))
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Spotify Songs 2023 Dashboard</title>
<style>{CSS}</style>
</head>
<body>
<header>
  <h1>SPOTIFY SONGS 2023</h1>
  <p>What do the most streamed songs of 2023 have in common? Keys, modes, tempo and audio features at a glance.</p>
  <div class="kpis">{kpis}</div>
</header>
<main>
{"".join(cards)}
</main>
<footer>
  <div class="brand">SPOTIFY SONGS 2023</div>
  <div>Data: <a href="{KAGGLE_URL}">Most Streamed Spotify Songs 2023</a> by Nidula Elgiriyewithana (Kaggle)</div>
  <div>Streams are cumulative, not limited to 2023. Key charts only include songs with a known key.</div>
  <div>Built with pandas &amp; Plotly · <a href="{REPO_URL}">Source on GitHub</a></div>
</footer>
</body>
</html>
"""
