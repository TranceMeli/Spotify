"""Build the standalone dashboard HTML (dashboard/spotify_dashboard.html)."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from spotify_analysis.data import load_clean  # noqa: E402
from spotify_analysis.report import build_html  # noqa: E402

if __name__ == "__main__":
    html_path = ROOT / "dashboard" / "spotify_dashboard.html"
    html_path.write_text(build_html(load_clean()), encoding="utf-8")
    print(f"wrote {html_path}")
