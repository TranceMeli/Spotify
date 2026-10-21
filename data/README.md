# Data

The data is **not** part of this repository. The Kaggle page lists its license as
"Other (specified in description)" without further terms, so redistribution is not clearly allowed.

## Get the raw data

1. Download `spotify-2023.csv` from
   [Most Streamed Spotify Songs 2023](https://www.kaggle.com/datasets/nelgiriyewithana/top-spotify-songs-2023)
   (Kaggle, by Nidula Elgiriyewithana).
2. Save it as `data/raw/spotify-2023.csv`.
3. Create the cleaned file: `python scripts/clean_data.py` (writes `data/processed/spotify-2023-cleaned.csv`).
