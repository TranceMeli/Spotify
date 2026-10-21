"""Create data/processed/spotify-2023-cleaned.csv from the raw data."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from spotify_analysis.data import PROCESSED_PATH, clean, load_raw  # noqa: E402

if __name__ == "__main__":
    raw = load_raw()
    cleaned = clean(raw)
    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(PROCESSED_PATH, index=False, encoding="utf-8", lineterminator="\n")
    print(f"{len(raw)} raw rows -> {len(cleaned)} cleaned rows: {PROCESSED_PATH}")
