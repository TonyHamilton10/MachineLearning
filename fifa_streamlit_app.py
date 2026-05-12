import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from streamlit.components.v1 import html

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="FIFA Elite Analytics",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# ADVANCED SAAS CSS + ANIMATIONS
# =========================================================

st.markdown("""
<style>

/* =========================
MAIN APP
========================= */

.stApp {
    background: linear-gradient(
        135deg,
        #020617 0%,
        #0f172a 40%,
        #111827 100%
    );
    color: white;
}

/* =========================
SIDEBAR
========================= */

section[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.95);
    border-right: 1px solid rgba(255,255,255,0.05);
}

/* =========================
SCROLLBAR
========================= */

::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: #0f172a;
}

::-webkit-scrollbar-thumb {
    background: #2563eb;
    border-radius: 10px;
}

/* =========================
ANIMATIONS
========================= */

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }

    to {
        opacity: 1;
        transform: translateY(0px);
    }
}

@keyframes pulseGlow {
    0% {
        box-shadow: 0 0 10px rgba(37,99,235,0.2);
    }

    50% {
        box-shadow: 0 0 35px rgba(37,99,235,0.5);
    }

    100% {
        box-shadow: 0 0 10px rgba(37,99,235,0.2);
    }
}

@keyframes floatCard {
    0% {
        transform: translateY(0px);
    }

    50% {
        transform: translateY(-8px);
    }

    100% {
        transform: translateY(0px);
    }
}

/* =========================
HERO SECTION
========================= */

.hero-container {
    position: relative;
    overflow: hidden;
    background: linear-gradient(
        135deg,
        rgba(37,99,235,0.95),
        rgba(29,78,216,0.92)
    );

    border-radius: 30px;
    padding: 60px;
    margin-bottom: 30px;

    animation:
        fadeInUp 1s ease,
        pulseGlow 4s infinite;

    backdrop-filter: blur(20px);

    border: 1px solid rgba(255,255,255,0.08);
}

.hero-container::before {
    content: "";
    position: absolute;

    width: 400px;
    height: 400px;

    background: rgba(255,255,255,0.08);

    border-radius: 50%;

    top: -150px;
    right: -120px;
}

.hero-title {
    font-size: 4rem;
    font-weight: 900;
    color: white;
    margin-bottom: 10px;
}

.hero-subtitle {
    font-size: 1.3rem;
    opacity: 0.9;
}

.player-name {
    font-size: 3rem;
    font-weight: 800;
    margin-top: 25px;
}

.rating-badge {
    background: rgba(255,255,255,0.15);
    display: inline-block;
    padding: 15px 25px;
    border-radius: 20px;
    margin-top: 20px;
    font-size: 2rem;
    font-weight: 900;
}

/* =========================
METRIC CARDS
========================= */

.metric-card {
    background: rgba(17,24,39,0.7);

    border-radius: 24px;

    padding: 25px;

    backdrop-filter: blur(18px);

    border: 1px solid rgba(255,255,255,0.06);

    transition: 0.4s;

    animation: fadeInUp 1s ease;
}

.metric-card:hover {
    transform: translateY(-10px) scale(1.02);

    border: 1px solid rgba(59,130,246,0.5);

    box-shadow:
        0 20px 35px rgba(37,99,235,0.25);
}

.metric-title {
    color: #94a3b8;
    font-size: 1rem;
    margin-bottom: 10px;
}

.metric-value {
    font-size: 2.2rem;
    font-weight: 900;
    color: white;
}

/* =========================
TABLES
========================= */

[data-testid="stDataFrame"] {
    background: rgba(17,24,39,0.75);
    border-radius: 20px;
    padding: 10px;
    border: 1px solid rgba(255,255,255,0.05);
}

/* =========================
PLOTLY
========================= */

.js-plotly-plot {
    border-radius: 20px;
    overflow: hidden;
}

/* =========================
HEADINGS
========================= */

h1, h2, h3 {
    color: white !important;
}

/* =========================
BUTTONS
========================= */

.stButton > button {
    background: linear-gradient(
        135deg,
        #2563eb,
        #1d4ed8
    );

    color: white;
    border-radius: 14px;
    border: none;
    padding: 12px 24px;

    font-weight: 700;

    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 12px 25px rgba(37,99,235,0.35);
}

/* =========================
TABS
========================= */

.stTabs [data-baseweb="tab"] {
    background: rgba(17,24,39,0.75);
    border-radius: 14px;
    margin-right: 10px;
    padding: 10px 20px;
}

.stTabs [aria-selected="true"] {
    background: #2563eb !important;
}

/* =========================
FLOATING GLASS EFFECT
========================= */

.glass {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(18px);
    border: 1px solid rgba(255,255,255,0.08);
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    csv_path = "fifa_data_cleaned.csv"

    if not os.path.exists(csv_path):
        st.error("Dataset not found.")
        return None

    df = pd.read_csv(csv_path)

    numeric_cols = [
        "Overall",
        "Potential",
        "Wage",
        "Value"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    return df


df = load_data()

if df is None:
    st.stop()

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("""
# ⚽ FIFA ELITE

### SaaS Analytics Platform
""")

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Top Players",
        "Club Analytics",
        "Market Value"
    ]
)

# =========================================================
# TOP PLAYERS
# =========================================================

top_players = df.nlargest(20, "Overall")

best_player = df.loc[df["Overall"].idxmax()]

# =========================================================
# HERO SECTION
# =========================================================

st.markdown(f"""
<div class="hero-container">

<div class="hero-title">
⚽ FIFA Elite Analytics
</div>

<div class="hero-subtitle">
Next Generation Football Intelligence Platform
</div>

<div class="player-name">
🌟 {best_player['Name']}
</div>

<div style="font-size:1.2rem;margin-top:10px;">
{best_player['Club']} • {best_player['Position']}
</div>

<div class="rating-badge">
⭐ {int(best_player['Overall'])} Overall
</div>

</div>
""", unsafe_allow_html=True)

# =========================================================
# FLOATING PARTICLES HTML
# =========================================================

particles_html = """
<!DOCTYPE html>
<html>
<head>
<style>

body {
    margin: 0;
    overflow: hidden;
}

.circle {
    position: fixed;
    border-radius: 50%;
    background: rgba(59,130,246,0.15);
    animation: float 15s infinite linear;
}

.circle:nth-child(1){
    width:120px;
    height:120px;
    left:10%;
    animation-duration:20s;
}

.circle:nth-child(2){
    width:180px;
    height:180px;
    left:70%;
    animation-duration:25s;
}

.circle:nth-child(3){
    width:90px;
    height:90px;
    left:40%;
    animation-duration:18s;
}

@keyframes float {

    from{
        transform:translateY(100vh);
    }

    to{
        transform:translateY(-120vh);
    }
}

</style>
</head>

<body>

<div class="circle"></div>
<div class="circle"></div>
<div class="circle"></div>

</body>
</html>
"""

html(particles_html, height=0)

# =========================================================
# KPI SECTION
# =========================================================

col1, col2, col3, col4 = st.columns(4)

metrics = [
    (
        "Average Rating",
        f"{top_players['Overall'].mean():.1f}"
    ),

    (
        "Highest Potential",
        f"{top_players['Potential'].max():.0f}"
    ),

    (
        "Highest Wage",
        f"${top_players['Wage'].max()/1000:.0f}K"
    ),

    (
        "Elite Players",
        f"{len(top_players)}"
    )
]

for col, metric in zip([col1,col2,col3,col4], metrics):

    with col:

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">
                {metric[0]}
            </div>

            <div class="metric-value">
                {metric[1]}
            </div>
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# OVERVIEW PAGE
# =========================================================

if page == "Overview":

    st.markdown("## 📊 Player Ratings")

    fig = px.bar(
        top_players,
        x="Name",
        y="Overall",
        color="Overall",
        template="plotly_dark",
        text="Overall"
    )

    fig.update_layout(
        height=550,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_tickangle=-45
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# TOP PLAYERS PAGE
# =========================================================

elif page == "Top Players":

    st.markdown("## 🌟 Elite Players")

    st.dataframe(
        top_players[
            [
                "Name",
                "Club",
                "Position",
                "Overall",
                "Potential",
                "Age",
                "Nationality"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

# =========================================================
# CLUB ANALYTICS
# =========================================================

elif page == "Club Analytics":

    club_df = (
        df.groupby("Club")
        .agg({
            "Overall":"mean",
            "Wage":"sum",
            "Name":"count"
        })
        .reset_index()
    )

    club_df.columns = [
        "Club",
        "Avg Rating",
        "Total Wage",
        "Players"
    ]

    top_clubs = club_df.sort_values(
        "Avg Rating",
        ascending=False
    ).head(15)

    fig = px.scatter(
        top_clubs,
        x="Players",
        y="Avg Rating",
        size="Total Wage",
        hover_name="Club",
        template="plotly_dark"
    )

    fig.update_layout(
        height=600,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# MARKET VALUE
# =========================================================

elif page == "Market Value":

    if "Value" in df.columns:

        fig = px.treemap(
            top_players,
            path=["Club","Name"],
            values="Value",
            color="Overall",
            template="plotly_dark"
        )

        fig.update_layout(
            height=700,
            paper_bgcolor='rgba(0,0,0,0)'
        )

        st.plotly_chart(fig, use_container_width=True)

# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<br><br>

<div style="
    text-align:center;
    padding:30px;
    border-radius:20px;

    background:
    linear-gradient(
        135deg,
        rgba(37,99,235,0.2),
        rgba(29,78,216,0.1)
    );

    border:1px solid rgba(255,255,255,0.06);

    backdrop-filter:blur(20px);

">

<h2>
⚽ FIFA Elite Analytics
</h2>

<p style="opacity:0.8;">
Professional SaaS Football Intelligence Dashboard
</p>

</div>
""", unsafe_allow_html=True)