# Spotify Songs 2023 – Data Analysis

![Status](https://img.shields.io/badge/Status-Work%20in%20Progress-orange?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-data%20wrangling-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-notebooks-F37626?style=for-the-badge&logo=jupyter&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-visualization-11557C?style=for-the-badge)
![Seaborn](https://img.shields.io/badge/Seaborn-visualization-4C72B0?style=for-the-badge)
![Plotly](https://img.shields.io/badge/Plotly-interactive%20dashboard-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

Analysis of the **Most Streamed Spotify Songs 2023** dataset from Kaggle.

The goal of this project is to explore and visualize characteristics of Spotify's most streamed songs in 2023, with a focus on musical and audio-related features such as **Key, Mode, BPM, Danceability, Energy** and other song attributes.

## Dataset

The dataset used in this project is:

**Most Streamed Spotify Songs 2023**
Created by **Nidula Elgiriyewithana**

[View the dataset on Kaggle](https://www.kaggle.com/datasets/nelgiriyewithana/top-spotify-songs-2023)

The dataset contains **953 songs and 24 variables**, including information about:

- Track and artist
- Release date
- Spotify streams
- Spotify playlists and charts
- Apple Music playlists and charts
- Deezer playlists and charts
- Song characteristics and audio features
- Key and mode
- BPM / tempo
- Danceability
- Energy
- Valence
- Acousticness
- Instrumentalness
- Liveness
- Speechiness

## Project Structure

```text
spotify-analysis/
│
├── data/
│   ├── raw/
│   │   └── spotify-2023.csv
│   │
│   └── processed/
│       └── spotify-2023-cleaned.csv
│
├── notebooks/
│   ├── 01_exploration.ipynb
│   ├── 02_cleaning.ipynb
│   ├── 03_exploratory_analysis.ipynb
│   └── 04_visualization.ipynb
│
├── dashboard/
│   └── spotify_dashboard.ipynb
│
└── README.md
```

## Status

This project is under active development. Data cleaning and exploratory analysis are done; the interactive dashboard currently covers top streamed songs, top keys, and the major/minor distribution, with more views planned.