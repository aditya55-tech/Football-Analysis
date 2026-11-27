"""
app.py
------
Football Player Performance Analytics Dashboard
Powered by Streamlit + Plotly

⚠️  All data is SYNTHETIC and does NOT represent real-world football statistics.

Run:
    streamlit run app.py
"""

import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------------------------
# 1. Page configuration  (must be the FIRST Streamlit call)
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Football Analytics Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# 2. CSS — dark football-inspired theme
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #0a0e13;
        --surface: #121820;
        --surface-2: #18202a;
        --border: #232d3a;
        --text: #e8eef5;
        --muted: #8795a6;
        --green: #00ff87;
        --blue: #00b4d8;
        --amber: #f59e0b;
    }

    html, body, [class*="css"], .stApp { font-family: 'Inter', system-ui, sans-serif; }
    .stApp {
        background:
            radial-gradient(1200px 500px at 85% -10%, rgba(0,255,135,0.07), transparent 60%),
            radial-gradient(900px 400px at -10% 0%, rgba(0,180,216,0.06), transparent 60%),
            var(--bg);
        color: var(--text);
    }

    /* ── Hide default Streamlit chrome ── */
    #MainMenu, footer { visibility: hidden; }
    header[data-testid="stHeader"] { background: transparent; }
    .block-container { padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1400px; }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f151c 0%, #0b1016 100%);
        border-right: 1px solid var(--border);
    }
    .brand {
        display: flex; align-items: center; gap: 10px;
        font-weight: 800; font-size: 18px; letter-spacing: -0.01em;
        padding: 4px 0 2px 0;
    }
    .brand-badge {
        width: 34px; height: 34px; border-radius: 10px;
        display: inline-flex; align-items: center; justify-content: center;
        background: linear-gradient(135deg, #00ff87, #00b4d8);
        color: #04210f; font-size: 18px;
    }
    .side-label {
        font-size: 11px; text-transform: uppercase; letter-spacing: 0.12em;
        color: var(--muted); margin: 14px 0 6px 0; font-weight: 600;
    }

    /* Nav radio → pill buttons */
    [data-testid="stSidebar"] div[role="radiogroup"] { gap: 6px; }
    [data-testid="stSidebar"] div[role="radiogroup"] > label {
        background: transparent; border: 1px solid transparent;
        border-radius: 10px; padding: 9px 12px; width: 100%;
        transition: all .15s ease; cursor: pointer;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
        background: var(--surface-2); border-color: var(--border);
    }
    [data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) {
        background: linear-gradient(90deg, rgba(0,255,135,0.16), rgba(0,255,135,0.03));
        border-color: rgba(0,255,135,0.35);
    }
    [data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child { display: none; }
    [data-testid="stSidebar"] div[role="radiogroup"] p { font-weight: 600; font-size: 14px; }

    .match-pill {
        background: var(--surface-2); border: 1px solid var(--border);
        border-radius: 12px; padding: 10px 14px; margin: 4px 0 10px 0;
        font-size: 13px; color: var(--muted);
    }
    .match-pill b { color: var(--green); font-size: 18px; margin-right: 4px; }
    .chip {
        display: inline-block; padding: 2px 10px; margin: 2px 4px 2px 0;
        border-radius: 999px; font-size: 11px; font-weight: 600;
        background: rgba(0,180,216,0.12); color: #7dd8ee; border: 1px solid rgba(0,180,216,0.3);
    }

    /* ── Page hero header ── */
    .hero {
        position: relative; overflow: hidden;
        background: linear-gradient(120deg, #0f1f1a 0%, #0f1a24 55%, #121820 100%);
        border: 1px solid var(--border); border-radius: 18px;
        padding: 24px 28px; margin-bottom: 14px;
    }
    .hero::after {
        content: ""; position: absolute; right: -60px; top: -60px;
        width: 240px; height: 240px; border-radius: 50%;
        border: 2px solid rgba(0,255,135,0.15);
        box-shadow: 0 0 0 28px rgba(0,255,135,0.04), 0 0 0 56px rgba(0,255,135,0.025);
    }
    .hero h1 { margin: 0; font-size: 28px; font-weight: 800; letter-spacing: -0.02em; }
    .hero p  { margin: 6px 0 0 0; color: var(--muted); font-size: 14px; }

    /* ── KPI cards ── */
    .kpi-card {
        background: linear-gradient(160deg, var(--surface-2), var(--surface));
        border: 1px solid var(--border); border-radius: 16px;
        padding: 18px 20px; position: relative; overflow: hidden;
        transition: transform .15s ease, border-color .15s ease;
    }
    .kpi-card:hover { transform: translateY(-2px); border-color: rgba(0,255,135,0.45); }
    .kpi-card::before {
        content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: 4px;
        background: var(--accent, #00ff87);
    }
    .kpi-icon { font-size: 18px; margin-bottom: 6px; }
    .kpi-label {
        font-size: 11px; color: var(--muted); text-transform: uppercase;
        letter-spacing: 0.1em; font-weight: 600; margin-bottom: 4px;
    }
    .kpi-value { font-size: 30px; font-weight: 800; color: var(--accent, #00ff87); line-height: 1.1; }
    .kpi-sub { font-size: 12px; color: var(--muted); margin-top: 4px; }

    /* ── Headings ── */
    h2, h3 { color: var(--text); font-weight: 700; letter-spacing: -0.01em; }
    h3 { font-size: 18px !important; margin-top: 0.6rem; }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] { gap: 6px; border-bottom: 1px solid var(--border); }
    .stTabs [data-baseweb="tab"] {
        background: transparent; border-radius: 10px 10px 0 0;
        padding: 10px 16px; color: var(--muted); font-weight: 600;
    }
    .stTabs [aria-selected="true"] { color: var(--green) !important; background: rgba(0,255,135,0.07); }
    .stTabs [data-baseweb="tab-highlight"] { background-color: var(--green) !important; }

    /* ── Chart / table containers ── */
    .js-plotly-plot { border-radius: 14px; }
    [data-testid="stPlotlyChart"] {
        background: var(--surface); border: 1px solid var(--border);
        border-radius: 14px; padding: 6px;
    }
    [data-testid="stDataFrame"] {
        border: 1px solid var(--border); border-radius: 14px; overflow: hidden;
    }
    [data-testid="stExpander"] {
        background: var(--surface); border: 1px solid var(--border); border-radius: 14px;
    }

    /* ── Inputs & buttons ── */
    .stButton > button {
        width: 100%; border-radius: 10px; border: 1px solid var(--border);
        background: var(--surface-2); color: var(--text); font-weight: 600;
        transition: all .15s ease;
    }
    .stButton > button:hover { border-color: var(--green); color: var(--green); }
    .stDownloadButton > button {
        background: linear-gradient(135deg, #1fa653, #238636); color: #fff;
        border: none; border-radius: 10px; font-weight: 700; padding: 8px 18px;
    }
    .stDownloadButton > button:hover { filter: brightness(1.12); }
    [data-testid="stMetricDelta"] { color: var(--green) !important; }

    /* ── Disclaimer banner (slim) ── */
    .synthetic-banner {
        background: rgba(245,158,11,0.08);
        border: 1px solid rgba(245,158,11,0.3);
        border-radius: 10px; padding: 7px 14px;
        color: #fbbf24; font-size: 12px; margin-bottom: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# 3. Data loading & caching
# ---------------------------------------------------------------------------
CSV_PATH = "football_players.csv"


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    """Load dataset from CSV; generate it first if absent."""
    if not os.path.exists(path):
        st.toast("CSV not found — generating synthetic dataset…", icon="⚙️")
        from generate_data import generate_dataset
        generate_dataset(path)
    df = pd.read_csv(path)
    return df


df_raw = load_data(CSV_PATH)

# ---------------------------------------------------------------------------
# 4. Sidebar — navigation + filters
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        '<div class="brand"><span class="brand-badge">⚽</span>Football Analytics</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="side-label">Navigate</div>', unsafe_allow_html=True)
    page = st.radio(
        "Navigate",
        ["📊  Overview", "👤  Player Analysis", "🏟️  Team Analysis", "🎽  Position Analysis"],
        label_visibility="collapsed",
    )
    page = page.split("  ", 1)[1]  # strip the emoji prefix

    st.markdown('<div class="side-label">Filters</div>', unsafe_allow_html=True)

    # Season
    seasons = ["All"] + sorted(df_raw["season"].unique().tolist())
    sel_season = st.selectbox("Season", seasons)

    # Team — depends on season filter
    df_s = df_raw if sel_season == "All" else df_raw[df_raw["season"] == sel_season]
    teams = ["All"] + sorted(df_s["team"].unique().tolist())
    sel_team = st.selectbox("Team", teams)

    # Position
    positions = ["All"] + sorted(df_raw["position"].unique().tolist())
    sel_position = st.selectbox("Position", positions)

    # Player multi-select — narrows to season+team+position slice
    df_stacked = df_s.copy()
    if sel_team != "All":
        df_stacked = df_stacked[df_stacked["team"] == sel_team]
    if sel_position != "All":
        df_stacked = df_stacked[df_stacked["position"] == sel_position]

    player_options = sorted(df_stacked["player_name"].unique().tolist())
    sel_players = st.multiselect("Player(s)", player_options, default=[])

    # Live match count + active filter chips
    _n_match = len(df_stacked) if not sel_players else int(df_stacked["player_name"].isin(sel_players).sum())
    _chips = "".join(
        f'<span class="chip">{v}</span>'
        for v in [sel_season, sel_team, sel_position]
        if v != "All"
    ) + "".join(f'<span class="chip">{p}</span>' for p in sel_players[:3])
    st.markdown(
        f'<div class="match-pill"><b>{_n_match}</b> of {len(df_raw)} records'
        f'<div style="margin-top:6px">{_chips or "No filters applied"}</div></div>',
        unsafe_allow_html=True,
    )

    # Reset filters button
    if st.button("↺  Reset Filters"):
        st.session_state.clear()
        st.rerun()

    st.caption("⚠️ All data is **synthetic** and does not represent real football statistics.")

# ---------------------------------------------------------------------------
# 5. Apply filters
# ---------------------------------------------------------------------------
df = df_raw.copy()

if sel_season != "All":
    df = df[df["season"] == sel_season]
if sel_team != "All":
    df = df[df["team"] == sel_team]
if sel_position != "All":
    df = df[df["position"] == sel_position]
if sel_players:
    df = df[df["player_name"].isin(sel_players)]

# ---------------------------------------------------------------------------
# 6. Validation guard
# ---------------------------------------------------------------------------
def _empty_state_guard(df: pd.DataFrame) -> bool:
    """Show a warning and return False if the filtered DataFrame is empty."""
    if len(df) == 0:
        st.warning(
            "⚠️ No players match the current filters. "
            "Try broadening your selection or click **↺ Reset Filters** in the sidebar.",
            icon="🔍",
        )
        return False
    return True

# ---------------------------------------------------------------------------
# 7. Shared utilities
# ---------------------------------------------------------------------------
DARK_TEMPLATE = "plotly_dark"
GREEN = "#00ff87"
ACCENT_COLORS = [
    "#00ff87", "#00b4d8", "#f59e0b", "#f43f5e",
    "#a78bfa", "#34d399", "#fb923c", "#60a5fa",
]

POSITION_COLORS = {
    "GK": "#f59e0b",
    "DEF": "#00b4d8",
    "MID": "#a78bfa",
    "FWD": "#f43f5e",
}


def _chart_layout(fig, height: int = 420):
    """Apply consistent layout settings to every chart."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e8eef5", size=12, family="Inter, sans-serif"),
        title=dict(font=dict(size=15), x=0.02, xanchor="left"),
        margin=dict(l=40, r=20, t=55, b=40),
        height=height,
        hovermode="closest",
        hoverlabel=dict(bgcolor="#18202a", bordercolor="#232d3a", font_size=12),
        legend=dict(
            bgcolor="rgba(0,0,0,0)", borderwidth=0,
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
        ),
    )
    fig.update_xaxes(gridcolor="#1c2531", zerolinecolor="#1c2531", linecolor="#232d3a")
    fig.update_yaxes(gridcolor="#1c2531", zerolinecolor="#1c2531", linecolor="#232d3a")
    return fig


def _page_header(title: str, subtitle: str):
    """Hero banner at the top of each page."""
    st.markdown(
        f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>',
        unsafe_allow_html=True,
    )


def _kpi_card(col, label, value, sub, icon="", accent="#00ff87"):
    col.markdown(
        f'<div class="kpi-card" style="--accent:{accent}">'
        f'<div class="kpi-icon">{icon}</div>'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'<div class="kpi-sub">{sub}</div>'
        f"</div>",
        unsafe_allow_html=True,
    )


def render_data_table(df: pd.DataFrame, key_prefix: str = ""):
    """Searchable player statistics table with CSV download."""
    st.markdown("### 📋 Player Statistics")

    search = st.text_input(
        "Search player by name",
        placeholder="e.g. Luca Silva",
        key=f"{key_prefix}_search",
    )
    display_df = df.copy()
    if search.strip():
        mask = display_df["player_name"].str.contains(search.strip(), case=False, na=False)
        display_df = display_df[mask]

    st.dataframe(
        display_df.reset_index(drop=True),
        width="stretch",
        height=320,
    )

    csv_bytes = display_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️  Download filtered data as CSV",
        data=csv_bytes,
        file_name="football_players_filtered.csv",
        mime="text/csv",
        key=f"{key_prefix}_download",
    )


def _synthetic_banner():
    st.markdown(
        '<div class="synthetic-banner">'
        "⚠️ <strong>Synthetic data</strong> — all names, teams and statistics are randomly "
        "generated and do <strong>not</strong> represent real football results."
        "</div>",
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# 8. Page functions
# ---------------------------------------------------------------------------

# ── 8a. Overview ────────────────────────────────────────────────────────────

def page_overview(df: pd.DataFrame):
    _page_header("📊 Dashboard Overview", "Season-wide KPIs, top scorers and goal distribution for the current selection.")
    _synthetic_banner()

    if not _empty_state_guard(df):
        return

    # KPI calculations
    total_players  = df["player_id"].nunique()
    total_goals    = int(df["goals"].sum())
    total_assists  = int(df["assists"].sum())
    total_minutes  = int(df["minutes_played"].sum())
    avg_rating     = round(float(df["rating"].mean()), 2)

    c1, c2, c3, c4, c5 = st.columns(5)
    _kpi_card(c1, "Total Players",  f"{total_players:,}", "unique players",     "👥", "#00ff87")
    _kpi_card(c2, "Total Goals",    f"{total_goals:,}",   "across selection",   "⚽", "#00b4d8")
    _kpi_card(c3, "Total Assists",  f"{total_assists:,}", "across selection",   "🎯", "#a78bfa")
    _kpi_card(c4, "Minutes Played", f"{total_minutes:,}", "total minutes",      "⏱️", "#f59e0b")
    _kpi_card(c5, "Avg Rating",     f"{avg_rating}",      "out of 9.5",         "⭐", "#f43f5e")

    st.markdown("<br>", unsafe_allow_html=True)

    # Top-10 leaderboard
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown("### 🏆 Top 10 Players")
        top10 = (
            df[["player_name", "team", "position", "season", "goals", "assists",
                "minutes_played", "rating"]]
            .sort_values(["goals", "assists"], ascending=False)
            .head(10)
            .reset_index(drop=True)
        )
        top10.index += 1  # 1-based rank
        st.dataframe(top10, width="stretch", height=360)

    with col_right:
        # Goals distribution by position pie
        pos_goals = df.groupby("position")["goals"].sum().reset_index()
        fig_pie = px.pie(
            pos_goals,
            names="position",
            values="goals",
            title="Goals by Position",
            color="position",
            color_discrete_map=POSITION_COLORS,
            template=DARK_TEMPLATE,
            hole=0.4,
        )
        _chart_layout(fig_pie, height=360)
        st.plotly_chart(fig_pie, width="stretch")

    st.markdown("---")
    render_data_table(df, key_prefix="overview")


# ── 8b. Player Analysis ─────────────────────────────────────────────────────

def page_player(df: pd.DataFrame):
    _page_header("👤 Player Analysis", "Scoring efficiency, creativity and head-to-head player comparison.")
    _synthetic_banner()

    if not _empty_state_guard(df):
        return

    # Derived column: shot conversion rate
    df = df.copy()
    df["conversion_rate"] = (
        df["goals"] / df["shots"].replace(0, np.nan)
    ).fillna(0).round(3)

    tab_ga, tab_sg, tab_radar = st.tabs(
        ["⚡ Goals vs Assists", "🎯 Shots vs Goals", "📡 Player Comparison"]
    )

    # ── Scatter 1: Goals vs Assists ──────────────────────────────────────────
    fig_ga = px.scatter(
        df,
        x="assists",
        y="goals",
        color="position",
        color_discrete_map=POSITION_COLORS,
        hover_data=["player_name", "team", "season", "appearances"],
        size="appearances",
        size_max=18,
        title="Goals vs Assists (size = appearances)",
        labels={"assists": "Assists", "goals": "Goals"},
        template=DARK_TEMPLATE,
    )
    _chart_layout(fig_ga, height=480)
    with tab_ga:
        st.plotly_chart(fig_ga, width="stretch")

    # ── Scatter 2: Shots vs Goals ────────────────────────────────────────────
    fig_sg = px.scatter(
        df,
        x="shots",
        y="goals",
        color="position",
        color_discrete_map=POSITION_COLORS,
        hover_data=["player_name", "team", "conversion_rate"],
        size="appearances",
        size_max=18,
        title="Shots vs Goals (hover for conversion rate)",
        labels={"shots": "Total Shots", "goals": "Goals Scored"},
        template=DARK_TEMPLATE,
    )
    _chart_layout(fig_sg, height=480)
    with tab_sg:
        st.plotly_chart(fig_sg, width="stretch")

    # ── Radar: Player Comparison ─────────────────────────────────────────────
    with tab_radar:
        _radar_section(df)

    st.markdown("---")
    render_data_table(df, key_prefix="player")


def _radar_section(df: pd.DataFrame):
    st.caption("Select up to 3 players to compare across 6 key stats.")

    all_players = sorted(df["player_name"].unique().tolist())
    selected = st.multiselect(
        "Choose players to compare",
        all_players,
        default=all_players[:2] if len(all_players) >= 2 else all_players,
        key="radar_select",
    )

    if len(selected) > 3:
        st.warning("Please select at most 3 players for a clean comparison.", icon="⚠️")
        selected = selected[:3]

    if selected:
        radar_cols = ["goals", "assists", "rating", "tackles", "passes", "shots"]
        radar_labels = ["Goals", "Assists", "Rating", "Tackles", "Passes", "Shots"]

        sub = df[df["player_name"].isin(selected)].groupby("player_name")[radar_cols].mean()

        # Normalise each stat to 0–1 range across the full filtered dataset
        stat_max = df[radar_cols].max()
        stat_max = stat_max.replace(0, 1)  # avoid division by zero

        fig_radar = go.Figure()
        for i, player in enumerate(selected):
            if player not in sub.index:
                continue
            vals = (sub.loc[player] / stat_max).values.tolist()
            vals += [vals[0]]  # close the polygon
            fig_radar.add_trace(
                go.Scatterpolar(
                    r=vals,
                    theta=radar_labels + [radar_labels[0]],
                    fill="toself",
                    name=player,
                    line=dict(color=ACCENT_COLORS[i % len(ACCENT_COLORS)]),
                    fillcolor=ACCENT_COLORS[i % len(ACCENT_COLORS)],
                    opacity=0.25,
                )
            )

        fig_radar.update_layout(
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(
                    visible=True,
                    range=[0, 1],
                    gridcolor="#21262d",
                    tickfont=dict(color="#8b949e", size=9),
                ),
                angularaxis=dict(gridcolor="#21262d"),
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e8eef5", family="Inter, sans-serif"),
            legend=dict(bgcolor="rgba(0,0,0,0)"),
            title="Normalised Player Comparison (0–1 scale)",
            template=DARK_TEMPLATE,
            height=520,
        )
        st.plotly_chart(fig_radar, width="stretch")
    else:
        st.info("Select at least one player above to display the radar chart.")


# ── 8c. Team Analysis ───────────────────────────────────────────────────────

def page_team(df: pd.DataFrame):
    _page_header("🏟️ Team Analysis", "How each club stacks up on output, squad size and rating.")
    _synthetic_banner()

    if not _empty_state_guard(df):
        return

    # Aggregate by team
    team_agg = (
        df.groupby("team")
        .agg(
            total_goals=("goals", "sum"),
            total_assists=("assists", "sum"),
            total_shots=("shots", "sum"),
            avg_rating=("rating", "mean"),
            player_count=("player_id", "nunique"),
        )
        .reset_index()
    )
    team_agg["avg_rating"] = team_agg["avg_rating"].round(2)
    team_agg = team_agg.sort_values("total_goals", ascending=False)

    # ── Grouped bar: Goals & Assists per team ────────────────────────────────
    st.markdown("### ⚽ Goals & Assists per Team")
    fig_ga = px.bar(
        team_agg.melt(id_vars="team", value_vars=["total_goals", "total_assists"],
                      var_name="metric", value_name="count"),
        x="team",
        y="count",
        color="metric",
        barmode="group",
        color_discrete_map={"total_goals": GREEN, "total_assists": "#00b4d8"},
        labels={"team": "Club", "count": "Total", "metric": "Metric"},
        title="Total Goals and Assists by Team",
        template=DARK_TEMPLATE,
    )
    _chart_layout(fig_ga, height=400)
    fig_ga.update_xaxes(tickangle=-30)
    st.plotly_chart(fig_ga, width="stretch")

    col_left, col_right = st.columns(2)

    # ── Bar: Player count ────────────────────────────────────────────────────
    with col_left:
        st.markdown("### 👥 Squad Size per Team")
        fig_pc = px.bar(
            team_agg,
            x="team",
            y="player_count",
            color="player_count",
            color_continuous_scale=[[0, "#21262d"], [1, GREEN]],
            labels={"team": "Club", "player_count": "Players"},
            title="Number of Players per Team",
            template=DARK_TEMPLATE,
        )
        _chart_layout(fig_pc, height=360)
        fig_pc.update_xaxes(tickangle=-30)
        st.plotly_chart(fig_pc, width="stretch")

    # ── Bar: Average rating ──────────────────────────────────────────────────
    with col_right:
        st.markdown("### ⭐ Average Rating per Team")
        fig_ar = px.bar(
            team_agg,
            x="team",
            y="avg_rating",
            color="avg_rating",
            color_continuous_scale=[[0, "#21262d"], [1, "#f59e0b"]],
            labels={"team": "Club", "avg_rating": "Avg Rating"},
            title="Average Player Rating by Team",
            template=DARK_TEMPLATE,
        )
        fig_ar.update_layout(yaxis=dict(range=[0, 10]))
        _chart_layout(fig_ar, height=360)
        fig_ar.update_xaxes(tickangle=-30)
        st.plotly_chart(fig_ar, width="stretch")

    # ── Team summary table ───────────────────────────────────────────────────
    st.markdown("### 📋 Team Summary Table")
    display_agg = team_agg.rename(columns={
        "team": "Club",
        "total_goals": "Goals",
        "total_assists": "Assists",
        "total_shots": "Shots",
        "avg_rating": "Avg Rating",
        "player_count": "Players",
    })
    st.dataframe(display_agg.reset_index(drop=True), width="stretch")

    st.markdown("---")
    render_data_table(df, key_prefix="team")


# ── 8d. Position Analysis ────────────────────────────────────────────────────

def page_position(df: pd.DataFrame):
    _page_header("🎽 Position Analysis", "Role-specific highlights and distributions across GK, DEF, MID and FWD.")
    _synthetic_banner()

    if not _empty_state_guard(df):
        return

    # ── Position-specific callout metrics ────────────────────────────────────
    st.markdown("### 📌 Position Highlights")
    pos_data = df.groupby("position")

    c_gk, c_def, c_mid, c_fwd = st.columns(4)

    def _safe_mean(df_pos, col):
        sub = df[df["position"] == df_pos]
        return round(float(sub[col].mean()), 1) if len(sub) > 0 else "N/A"

    _kpi_card(c_gk,  "GK · Avg Saves",       _safe_mean("GK", "saves"),       "per goalkeeper", "🧤", POSITION_COLORS["GK"])
    _kpi_card(c_def, "DEF · Avg Tackles",    _safe_mean("DEF", "tackles"),    "per defender",   "🛡️", POSITION_COLORS["DEF"])
    _kpi_card(c_mid, "MID · Avg Key Passes", _safe_mean("MID", "key_passes"), "per midfielder",  "🎯", POSITION_COLORS["MID"])
    _kpi_card(c_fwd, "FWD · Avg Goals",      _safe_mean("FWD", "goals"),      "per forward",    "⚡", POSITION_COLORS["FWD"])

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Box plot: Rating by position ──────────────────────────────────────────
    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown("### 📦 Rating Distribution by Position")
        fig_box = px.box(
            df,
            x="position",
            y="rating",
            color="position",
            color_discrete_map=POSITION_COLORS,
            points="outliers",
            title="Player Rating Distribution (box plot)",
            labels={"position": "Position", "rating": "Rating"},
            template=DARK_TEMPLATE,
            category_orders={"position": ["GK", "DEF", "MID", "FWD"]},
        )
        _chart_layout(fig_box, height=400)
        st.plotly_chart(fig_box, width="stretch")

    # ── Stacked bar: Goals & Assists by position ──────────────────────────────
    with col_r:
        st.markdown("### 📊 Goals & Assists by Position")
        pos_stats = (
            df.groupby("position")[["goals", "assists"]]
            .sum()
            .reset_index()
            .melt(id_vars="position", value_vars=["goals", "assists"],
                  var_name="metric", value_name="total")
        )
        fig_stacked = px.bar(
            pos_stats,
            x="position",
            y="total",
            color="metric",
            barmode="stack",
            color_discrete_map={"goals": GREEN, "assists": "#00b4d8"},
            labels={"position": "Position", "total": "Total", "metric": "Metric"},
            title="Total Goals and Assists by Position",
            template=DARK_TEMPLATE,
            category_orders={"position": ["GK", "DEF", "MID", "FWD"]},
        )
        _chart_layout(fig_stacked, height=400)
        st.plotly_chart(fig_stacked, width="stretch")

    # ── Violin: Minutes played by position ───────────────────────────────────
    st.markdown("### ⏱️ Minutes Played Distribution by Position")
    fig_violin = px.violin(
        df,
        x="position",
        y="minutes_played",
        color="position",
        color_discrete_map=POSITION_COLORS,
        box=True,
        points="outliers",
        title="Minutes Played per Player by Position",
        labels={"position": "Position", "minutes_played": "Minutes Played"},
        template=DARK_TEMPLATE,
        category_orders={"position": ["GK", "DEF", "MID", "FWD"]},
    )
    _chart_layout(fig_violin, height=380)
    st.plotly_chart(fig_violin, width="stretch")

    st.markdown("---")
    render_data_table(df, key_prefix="position")


# ---------------------------------------------------------------------------
# 9. Page router
# ---------------------------------------------------------------------------
if page == "Overview":
    page_overview(df)
elif page == "Player Analysis":
    page_player(df)
elif page == "Team Analysis":
    page_team(df)
elif page == "Position Analysis":
    page_position(df)
