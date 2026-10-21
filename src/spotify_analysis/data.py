"""Loading and cleaning of the Spotify Songs 2023 dataset."""

import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW_PATH = ROOT / "data" / "raw" / "spotify-2023.csv"
PROCESSED_PATH = ROOT / "data" / "processed" / "spotify-2023-cleaned.csv"

TEXT_COLUMNS = ["track_name", "artist(s)_name"]
COMMA_NUMBER_COLUMNS = ["in_deezer_playlists", "in_shazam_charts"]


def load_raw(path: Path = RAW_PATH) -> pd.DataFrame:
    """Read the raw Kaggle CSV. Undecodable bytes become U+FFFD."""
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Download spotify-2023.csv from Kaggle first (see data/README.md)."
        )
    return pd.read_csv(path, encoding="utf-8", encoding_errors="replace")


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Return a cleaned copy of the raw dataframe.

    - collapse runs of U+FFFD (characters already lost in the Kaggle export)
    - ``streams`` -> numeric; the one corrupted row becomes NaN
    - thousands separators removed from Deezer playlists / Shazam charts
    - missing ``key`` -> "Unknown" (instead of guessing a key)
    - duplicate track/artist pairs: keep the row with the most streams
    """
    df = df.copy()

    for col in TEXT_COLUMNS:
        df[col] = df[col].str.replace("�+", "�", regex=True).str.strip()

    df["streams"] = pd.to_numeric(df["streams"], errors="coerce").astype("Int64")
    for col in COMMA_NUMBER_COLUMNS:
        df[col] = pd.to_numeric(
            df[col].astype("string").str.replace(",", "", regex=False),
            errors="coerce",
        ).astype("Int64")

    df["key"] = df["key"].fillna("Unknown")

    df = (
        df.sort_values("streams", ascending=False, na_position="last")
        .drop_duplicates(subset=TEXT_COLUMNS, keep="first")
        .sort_index()
        .reset_index(drop=True)
    )
    return df


def load_clean(path: Path = PROCESSED_PATH) -> pd.DataFrame:
    """Read the cleaned CSV written by ``scripts/clean_data.py``."""
    if not path.exists():
        raise FileNotFoundError(f"{path} not found. Run `python scripts/clean_data.py` first.")
    return pd.read_csv(path, encoding="utf-8")
