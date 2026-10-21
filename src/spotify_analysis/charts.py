"""Plotly figures and data-driven insights for the Spotify Songs 2023 dashboard."""

import numpy as np
import plotly.graph_objects as go

GREEN = "#1DB954"
DARK_GREEN = "#0B5D2A"
BLACK = "#191414"
MUTED = "#6A6A6A"
GRID = "rgba(0, 0, 0, 0.07)"

AUDIO_FEATURES = {
    "danceability_%": "Danceability",
    "energy_%": "Energy",
    "valence_%": "Valence",
    "acousticness_%": "Acousticness",
    "speechiness_%": "Speechiness",
    "liveness_%": "Liveness",
    "instrumentalness_%": "Instrumentalness",
}


def format_streams(value: float) -> str:
    if value >= 1e9:
        return f"{value / 1e9:.2f}B"
    return f"{value / 1e6:.0f}M"


def _known_keys(df):
    return df[df["key"] != "Unknown"]


def _base_layout(fig: go.Figure, height: int = 340) -> go.Figure:
    fig.update_layout(
        template="plotly_white",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, Circular, Arial, sans-serif", color=BLACK, size=12),
        margin=dict(l=10, r=30, t=10, b=40),
        hoverlabel=dict(bgcolor="#FFFFFF", bordercolor=GREEN),
        showlegend=False,
    )
    fig.update_xaxes(showgrid=False, zeroline=False, tickfont=dict(color=MUTED, size=11))
    fig.update_yaxes(
        showgrid=True, gridcolor=GRID, zeroline=False, tickfont=dict(color=MUTED, size=11)
    )
    return fig


def _hbar_layout(fig: go.Figure, xmax: float, **xaxis) -> go.Figure:
    fig.update_xaxes(range=[0, xmax * 1.25], showgrid=True, gridcolor=GRID, **xaxis)
    fig.update_yaxes(
        showgrid=False,
        automargin=True,
        ticks="outside",
        ticklen=12,
        tickcolor="rgba(0,0,0,0)",
        tickfont=dict(color=BLACK, size=12),
    )
    fig.update_layout(bargap=0.38)
    return fig


def _short_title(title: str, limit: int = 24) -> str:
    short = title.split(" - ")[0].split(" (")[0]
    return short if len(short) <= limit else short[: limit - 1] + "…"


def top_songs_fig(df, n=5) -> go.Figure:
    top = df.dropna(subset=["streams"]).nlargest(n, "streams").iloc[::-1]
    streams = top["streams"].astype(float)
    names = top["track_name"].map(_short_title)
    fig = go.Figure(
        go.Bar(
            x=streams,
            y=names,
            orientation="h",
            text=streams.map(format_streams),
            textposition="outside",
            cliponaxis=False,
            marker=dict(color=GREEN, line=dict(color=DARK_GREEN, width=1.2)),
            customdata=np.stack([top["track_name"], top["artist(s)_name"]], axis=-1),
            hovertemplate="<b>%{customdata[0]}</b><br>%{customdata[1]}"
            "<br>Streams: %{x:,.0f}<extra></extra>",
        )
    )
    _base_layout(fig)
    _hbar_layout(
        fig,
        streams.max(),
        tickvals=[0, 1e9, 2e9, 3e9],
        ticktext=["0", "1B", "2B", "3B"],
        title_text="Total streams",
    )
    return fig


def top_keys_fig(df, n=5) -> go.Figure:
    share = (_known_keys(df)["key"].value_counts(normalize=True).head(n) * 100).iloc[::-1]
    fig = go.Figure(
        go.Bar(
            x=share.values,
            y=share.index,
            orientation="h",
            text=[f"{v:.1f}%" for v in share.values],
            textposition="outside",
            cliponaxis=False,
            marker=dict(color=GREEN, line=dict(color=DARK_GREEN, width=1.2)),
            hovertemplate="<b>Key %{y}</b><br>Share: %{x:.1f}%<extra></extra>",
        )
    )
    _base_layout(fig)
    _hbar_layout(fig, share.max(), ticksuffix="%", title_text="Share of songs")
    return fig


def _key_mode_pct(df, n=5):
    known = _known_keys(df)
    top = known["key"].value_counts().head(n).index
    counts = (
        known[known["key"].isin(top)]
        .groupby(["key", "mode"])
        .size()
        .unstack(fill_value=0)
        .loc[top]
    )
    return counts.div(counts.sum(axis=1), axis=0) * 100


def key_mode_fig(df, n=5) -> go.Figure:
    pct = _key_mode_pct(df, n)
    colors = {"Major": GREEN, "Minor": DARK_GREEN}
    fig = go.Figure(
        [
            go.Bar(
                x=pct.index,
                y=pct[mode],
                name=mode,
                text=[f"{v:.0f}%" for v in pct[mode]],
                textposition="outside",
                cliponaxis=False,
                marker=dict(color=colors[mode]),
                hovertemplate=f"<b>Key %{{x}}</b><br>{mode}: %{{y:.1f}}%<extra></extra>",
            )
            for mode in ("Major", "Minor")
        ]
    )
    _base_layout(fig)
    fig.update_layout(
        barmode="group",
        showlegend=True,
        legend=dict(orientation="h", x=1, xanchor="right", y=1.08, title_text=""),
        margin=dict(l=10, r=30, t=30, b=40),
    )
    fig.update_yaxes(range=[0, 100], ticksuffix="%", title_text="Share within key")
    fig.update_xaxes(title_text="Key")
    return fig


def audio_profile_fig(df) -> go.Figure:
    means = df[list(AUDIO_FEATURES)].mean().rename(AUDIO_FEATURES).sort_values()
    fig = go.Figure(
        go.Bar(
            x=means.values,
            y=means.index,
            orientation="h",
            text=[f"{v:.0f}%" for v in means.values],
            textposition="outside",
            cliponaxis=False,
            marker=dict(color=GREEN, line=dict(color=DARK_GREEN, width=1.2)),
            hovertemplate="<b>%{y}</b><br>Average: %{x:.1f}%<extra></extra>",
        )
    )
    _base_layout(fig)
    _hbar_layout(fig, 100, ticksuffix="%", title_text="Average score")
    fig.update_xaxes(range=[0, 100])
    return fig


def _bpm_bins(df):
    start = int(df["bpm"].min() // 10 * 10)
    end = int(df["bpm"].max() // 10 * 10 + 10)
    return start, end


def bpm_fig(df) -> go.Figure:
    start, end = _bpm_bins(df)
    median = df["bpm"].median()
    edges = np.arange(start, end + 10, 10)
    counts, _ = np.histogram(df["bpm"], bins=edges)
    median_bin = min(int(np.digitize(median, edges)) - 1, len(counts) - 1)
    centers = edges[:-1] + 5
    colors = [GREEN] * len(counts)
    colors[median_bin] = DARK_GREEN

    fig = go.Figure(
        go.Bar(
            x=centers,
            y=counts,
            width=9,
            marker=dict(color=colors),
            customdata=np.stack([edges[:-1], edges[1:] - 1], axis=-1),
            hovertemplate="%{customdata[0]}–%{customdata[1]} BPM<br>%{y} songs<extra></extra>",
        )
    )
    fig.add_annotation(
        x=centers[median_bin],
        y=counts[median_bin],
        text=f"<b>Median: {median:.0f} BPM</b><br>({edges[median_bin]}–{edges[median_bin + 1] - 1} BPM bar)",
        showarrow=True,
        arrowhead=2,
        arrowcolor=DARK_GREEN,
        ax=90,
        ay=-55,
        font=dict(color=BLACK, size=12),
        bgcolor="#FFFFFF",
        bordercolor=DARK_GREEN,
        borderwidth=1.5,
        borderpad=6,
    )
    _base_layout(fig)
    fig.update_layout(margin=dict(l=10, r=30, t=30, b=40))
    fig.update_xaxes(title_text="Tempo (BPM)", tickvals=edges[::2], range=[start, end])
    fig.update_yaxes(
        title_text="Number of songs", range=[0, counts.max() * 1.3], rangemode="tozero"
    )
    return fig


# ---------------------------------------------------------------- insights


def kpis(df) -> list[tuple[str, str]]:
    major = (df["mode"] == "Major").mean() * 100
    return [
        (f"{len(df):,}", "songs analysed"),
        (format_streams(df["streams"].sum()), "total streams"),
        (f"{df['bpm'].median():.0f}", "median BPM"),
        (f"{major:.0f}%", "songs in a major key"),
    ]


def insights(df) -> dict[str, str]:
    """Plain-text takeaways computed from the data, one per chart."""
    out = {}

    top = df.dropna(subset=["streams"]).nlargest(5, "streams")
    first, second = top.iloc[0], top.iloc[1]
    top5_share = top["streams"].sum() / df["streams"].sum() * 100
    out["songs"] = (
        f"<b>{first['track_name']}</b> leads with {format_streams(first['streams'])} streams, "
        f"{(first['streams'] / second['streams'] - 1) * 100:.0f}% ahead of {second['track_name']}. "
        f"The top 5 alone account for {top5_share:.1f}% of all streams. Streams are cumulative, "
        f"so older songs have a head start."
    )

    known = _known_keys(df)
    shares = known["key"].value_counts(normalize=True) * 100
    out["keys"] = (
        f"<b>{shares.index[0]}</b> is the most common key ({shares.iloc[0]:.1f}%), followed by "
        f"{shares.index[1]} and {shares.index[2]}. The top 5 keys cover {shares.head(5).sum():.0f}% "
        f"of songs; {len(df) - len(known)} songs without a key are excluded."
    )

    pct = _key_mode_pct(df)
    major_overall = (df["mode"] == "Major").mean() * 100
    most_major = pct["Major"].idxmax()
    most_minor = pct["Minor"].idxmax()
    out["mode"] = (
        f"Major dominates overall ({major_overall:.0f}% of songs). Among the top 5 keys, "
        f"<b>{most_major}</b> is the most major-leaning ({pct.loc[most_major, 'Major']:.0f}%), "
        f"while <b>{most_minor}</b> leans minor ({pct.loc[most_minor, 'Minor']:.0f}%)."
    )

    means = df[list(AUDIO_FEATURES)].mean().rename(AUDIO_FEATURES).sort_values(ascending=False)
    out["audio"] = (
        f"Hits are built to be danced to: <b>{means.index[0]}</b> ({means.iloc[0]:.0f}%) and "
        f"<b>{means.index[1]}</b> ({means.iloc[1]:.0f}%) score highest. "
        f"{means.index[-1]} averages just {means.iloc[-1]:.0f}%, so vocals-driven tracks rule."
    )

    start, end = _bpm_bins(df)
    counts, edges = np.histogram(df["bpm"], bins=np.arange(start, end + 10, 10))
    peak = counts.argmax()
    mid = ((df["bpm"] >= 90) & (df["bpm"] < 150)).mean() * 100
    out["bpm"] = (
        f"The median tempo is <b>{df['bpm'].median():.0f} BPM</b>. The busiest range is "
        f"{edges[peak]:.0f}–{edges[peak + 1]:.0f} BPM ({counts[peak]} songs), and {mid:.0f}% of "
        f"songs sit between 90 and 150 BPM."
    )
    return out
