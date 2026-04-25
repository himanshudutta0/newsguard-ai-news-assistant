import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

def fetch(endpoint):
    try:
        res = requests.get(BASE_URL + endpoint)
        if res.status_code == 200:
            return res.json()
        return []
    except:
        return []

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NewsGuard",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=JetBrains+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap');

/* Reset & base */
html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0b !important;
    color: #e8e3d9 !important;
}

[data-testid="stAppViewContainer"] {
    font-family: 'DM Sans', sans-serif;
}

/* Hide default Streamlit chrome */
#MainMenu, footer, [data-testid="stToolbar"], header { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }
[data-testid="block-container"] {
    padding: 0 2rem 2rem !important;
    max-width: 1400px !important;
}

/* ── Masthead ── */
.ng-masthead {
    border-bottom: 1px solid #2a2620;
    padding: 2rem 0 1.2rem;
    margin-bottom: 2.5rem;
    display: flex;
    align-items: baseline;
    gap: 1.5rem;
}
.ng-logo {
    font-family: 'Playfair Display', serif;
    font-size: 2.6rem;
    font-weight: 700;
    color: #e8e3d9;
    letter-spacing: -0.02em;
    line-height: 1;
}
.ng-logo span {
    color: #c8974a;
}
.ng-dateline {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: #5a5550;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 4px;
}
.ng-tagline {
    font-size: 0.8rem;
    color: #5a5550;
    font-weight: 300;
    letter-spacing: 0.05em;
    margin-left: auto;
    font-style: italic;
}

/* ── Tab bar ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid #2a2620 !important;
    gap: 0 !important;
    padding: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #5a5550 !important;
    background: transparent !important;
    border: none !important;
    padding: 0.8rem 1.4rem !important;
    border-bottom: 2px solid transparent !important;
    transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
    color: #c8974a !important;
    border-bottom: 2px solid #c8974a !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: #e8e3d9 !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding: 2rem 0 0 !important;
    background: transparent !important;
}

/* ── Search bar ── */
[data-testid="stTextInput"] input {
    background: #111113 !important;
    border: 1px solid #2a2620 !important;
    border-radius: 2px !important;
    color: #e8e3d9 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    padding: 0.6rem 1rem !important;
    transition: border-color 0.2s !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #c8974a !important;
    box-shadow: 0 0 0 3px rgba(200, 151, 74, 0.08) !important;
}
[data-testid="stTextInput"] input::placeholder { color: #3a3530 !important; }
[data-testid="stTextInput"] label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #5a5550 !important;
}

/* ── Buttons ── */
.stButton button {
    background: transparent !important;
    border: 1px solid #2a2620 !important;
    border-radius: 2px !important;
    color: #5a5550 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    padding: 0.5rem 1.2rem !important;
    transition: all 0.2s !important;
}
.stButton button:hover {
    border-color: #c8974a !important;
    color: #c8974a !important;
    background: rgba(200, 151, 74, 0.05) !important;
}

/* ── Article cards ── */
.ng-article {
    border-left: 3px solid #2a2620;
    padding: 1.2rem 0 1.2rem 1.4rem;
    margin-bottom: 1.6rem;
    transition: border-color 0.2s;
}
.ng-article:hover { border-left-color: #c8974a; }
.ng-article h3 {
    font-family: 'Playfair Display', serif !important;
    font-size: 1.25rem !important;
    font-weight: 600 !important;
    color: #e8e3d9 !important;
    margin: 0 0 0.4rem !important;
    line-height: 1.35 !important;
}
.ng-article .meta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: #3a3530;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    display: flex;
    gap: 1.2rem;
    margin-bottom: 0.6rem;
}
.ng-article .url {
    color: #c8974a;
    font-size: 0.8rem;
    word-break: break-all;
}

/* ── Expanders ── */
[data-testid="stExpander"] {
    background: #111113 !important;
    border: 1px solid #1e1c19 !important;
    border-radius: 2px !important;
}
[data-testid="stExpander"] summary {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #3a3530 !important;
}
[data-testid="stExpanderDetails"] {
    font-size: 0.9rem !important;
    color: #9a9590 !important;
    line-height: 1.7 !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: #111113 !important;
    border: 1px solid #1e1c19 !important;
    border-radius: 2px !important;
    padding: 1rem 1.2rem !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.6rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #3a3530 !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Playfair Display', serif !important;
    font-size: 1.6rem !important;
    color: #e8e3d9 !important;
}

/* ── Progress bars ── */
[data-testid="stProgress"] > div {
    background: #1e1c19 !important;
    border-radius: 0 !important;
    height: 3px !important;
}
[data-testid="stProgress"] > div > div {
    background: #c8974a !important;
    border-radius: 0 !important;
}

/* ── Section headers ── */
.ng-section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #3a3530;
    border-bottom: 1px solid #1e1c19;
    padding-bottom: 0.5rem;
    margin-bottom: 1.5rem;
}

/* ── Data frames ── */
[data-testid="stDataFrame"] {
    background: #111113 !important;
    border: 1px solid #1e1c19 !important;
}

/* ── Info/success boxes ── */
[data-testid="stAlert"] {
    background: #111113 !important;
    border-left: 3px solid #c8974a !important;
    color: #9a9590 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.85rem !important;
    border-radius: 0 !important;
}

/* ── Date input ── */
[data-testid="stDateInput"] input {
    background: #111113 !important;
    border: 1px solid #2a2620 !important;
    color: #e8e3d9 !important;
    border-radius: 2px !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stDateInput"] label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.65rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    color: #5a5550 !important;
}

/* ── Sentiment article blocks ── */
.ng-sentiment-card {
    background: #111113;
    border: 1px solid #1e1c19;
    border-radius: 2px;
    padding: 1.4rem;
    margin-bottom: 1.2rem;
}
.ng-sentiment-card h4 {
    font-family: 'Playfair Display', serif;
    font-size: 1.05rem;
    font-weight: 600;
    color: #e8e3d9;
    margin: 0 0 1rem;
}
.ng-stat-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #3a3530;
    margin-bottom: 0.25rem;
}
.ng-stat-value {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.1rem;
    font-weight: 500;
    color: #e8e3d9;
}
.ng-bias-label {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    padding: 0.2rem 0.6rem;
    border-radius: 1px;
    background: rgba(200, 151, 74, 0.12);
    color: #c8974a;
    border: 1px solid rgba(200, 151, 74, 0.3);
}
.ng-divider {
    border: none;
    border-top: 1px solid #1e1c19;
    margin: 0.8rem 0;
}

/* ── Topic chips ── */
.ng-topic-chip {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding: 0.25rem 0.7rem;
    background: rgba(200, 151, 74, 0.08);
    border: 1px solid rgba(200, 151, 74, 0.2);
    color: #c8974a;
    border-radius: 1px;
    margin-right: 0.4rem;
}

/* ── Plotly charts ── */
.js-plotly-plot .plotly .bg {
    fill: transparent !important;
}
</style>
""", unsafe_allow_html=True)

# ── Masthead ─────────────────────────────────────────────────────────────────
now = datetime.now()
st.markdown(f"""
<div class="ng-masthead">
    <div>
        <div class="ng-logo">News<span>Guard</span></div>
        <div class="ng-dateline">{now.strftime('%A, %B %d, %Y — %H:%M')}</div>
    </div>
    <div class="ng-tagline">Intelligence pipeline for the discerning reader</div>
</div>
""", unsafe_allow_html=True)

# ── Control bar ──────────────────────────────────────────────────────────────
col_search, col_btn = st.columns([5, 1])
with col_search:
    query = st.text_input("Search articles", placeholder="Keywords, entities, topics…", label_visibility="collapsed")
with col_btn:
    if st.button("↺  Refresh"):
        try:
            requests.get(BASE_URL + "/refresh")
            st.success("Pipeline executed")
        except:
            st.error("Could not reach backend")

st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

# ── Plotly theme ──────────────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color="#5a5550", size=11),
    xaxis=dict(gridcolor="#1e1c19", linecolor="#2a2620", tickcolor="#2a2620"),
    yaxis=dict(gridcolor="#1e1c19", linecolor="#2a2620", tickcolor="#2a2620"),
    margin=dict(l=0, r=0, t=20, b=0),
    colorway=["#c8974a", "#8b6a35", "#e8b87a", "#5a3d1e", "#f0d4a8"],
)

# ── Tabs ─────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "Scraped", "Preprocessed", "Entities",
    "Topics", "Summaries", "Modeling",
    "Daily Digest", "Sentiment & Bias"
])

# ════════════════ SCRAPED ════════════════
with tabs[0]:
    st.markdown('<div class="ng-section-label">Raw feed — scraped articles</div>', unsafe_allow_html=True)
    data = fetch("/search?q=" + query) if query else fetch("/articles/scraped")
    if not data:
        st.info("No articles available.")
    for a in data:
        pub = a.get("published_at", "")
        try:
            pub = datetime.fromisoformat(pub).strftime("%b %d, %Y · %H:%M")
        except:
            pass
        st.markdown(f"""
        <div class="ng-article">
            <h3>{a.get("title", "Untitled")}</h3>
            <div class="meta">
                <span>{pub}</span>
            </div>
            <div class="url">{a.get("url", "")}</div>
        </div>
        """, unsafe_allow_html=True)
        content = a.get("content", "")
        if content:
            with st.expander("Read content"):
                st.write(content)

# ════════════════ PREPROCESSED ════════════════
with tabs[1]:
    st.markdown('<div class="ng-section-label">NLP pipeline — preprocessed text</div>', unsafe_allow_html=True)
    data = fetch("/articles/preprocessed")
    if not data:
        st.info("No preprocessed articles.")
    for a in data:
        st.markdown(f"""
        <div class="ng-article">
            <h3>{a.get("title", "Untitled")}</h3>
        </div>
        """, unsafe_allow_html=True)
        with st.expander("Processed content"):
            st.write(a.get("processed_content", ""))

# ════════════════ ENTITIES ════════════════
with tabs[2]:
    st.markdown('<div class="ng-section-label">Named entity recognition</div>', unsafe_allow_html=True)
    data = fetch("/entities")

    if "counts" in data:
        df = pd.DataFrame(data["counts"])
        if not df.empty:
            col_t, col_c = st.columns([1, 2])
            with col_t:
                st.dataframe(
                    df.style.set_properties(**{
                        "background-color": "#111113",
                        "color": "#9a9590",
                        "border-color": "#1e1c19",
                        "font-family": "JetBrains Mono, monospace",
                        "font-size": "12px",
                    }),
                    use_container_width=True,
                    hide_index=True,
                )
            with col_c:
                fig = px.bar(
                    df, x="label", y="count",
                    title="",
                )
                fig.update_traces(marker_color="#c8974a", marker_line_width=0)
                fig.update_layout(**PLOTLY_LAYOUT)
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No entity data.")

# ════════════════ TOPICS ════════════════
with tabs[3]:
    st.markdown('<div class="ng-section-label">Topic classification</div>', unsafe_allow_html=True)
    data = fetch("/topics/predicted")
    if not data:
        st.info("No topic predictions.")
    for a in data:
        topic = a.get("predicted_topic", "Unknown")
        st.markdown(f"""
        <div class="ng-article">
            <div class="meta"><span>Predicted topic</span></div>
            <h3>{a.get("title", "Untitled")}</h3>
            <span class="ng-topic-chip">{topic}</span>
        </div>
        """, unsafe_allow_html=True)

# ════════════════ SUMMARIES ════════════════
with tabs[4]:
    st.markdown('<div class="ng-section-label">AI-generated summaries</div>', unsafe_allow_html=True)
    data = fetch("/summaries")
    if not data:
        st.info("No summaries available.")
    for a in data:
        st.markdown(f"""
        <div class="ng-article">
            <h3>{a.get("title", "Untitled")}</h3>
        </div>
        """, unsafe_allow_html=True)
        with st.expander("Read summary"):
            st.write(a.get("summary", ""))

# ════════════════ MODELING ════════════════
with tabs[5]:
    st.markdown('<div class="ng-section-label">Topic modeling — unsupervised</div>', unsafe_allow_html=True)
    raw = fetch("/topics/modeled")
    df = pd.DataFrame(raw)
    if not df.empty and "topic_keywords" in df.columns:
        fig = px.histogram(df, x="topic_keywords", title="")
        fig.update_traces(marker_color="#c8974a", marker_line_width=0)
        fig.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No modeling data.")

# ════════════════ DAILY DIGEST ════════════════
with tabs[6]:
    st.markdown('<div class="ng-section-label">Daily digest — curated briefing</div>', unsafe_allow_html=True)
    data = fetch("/digest/today")
    if not data:
        st.info("No articles in today's digest.")
    for i, a in enumerate(data):
        num = str(i + 1).zfill(2)
        pub = a.get("date", "")
        st.markdown(f"""
        <div class="ng-article">
            <div class="meta">
                <span>#{num}</span>
                <span>{pub}</span>
            </div>
            <h3>{a.get("title", "Untitled")}</h3>
            <div class="url">{a.get("url", "")}</div>
        </div>
        """, unsafe_allow_html=True)
        summary = a.get("summary", "")
        if summary:
            with st.expander("Read summary"):
                st.write(summary)

# ════════════════ SENTIMENT & BIAS ════════════════
with tabs[7]:
    st.markdown('<div class="ng-section-label">Sentiment analysis & media bias detection</div>', unsafe_allow_html=True)

    date = st.date_input("Filter by publication date", value=None)
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    data = fetch(f"/sentiment/filter?date={date}") if date else fetch("/sentiment")
    df = pd.DataFrame(data)

    if df.empty:
        st.info("No sentiment data.")
    else:
        # Aggregate chart
        if "sentiment_textblob" in df.columns:
            try:
                df["polarity"] = df["sentiment_textblob"].apply(
                    lambda x: x.get("polarity", 0) if isinstance(x, dict) else 0
                )
                df["subjectivity"] = df["sentiment_textblob"].apply(
                    lambda x: x.get("subjectivity", 0) if isinstance(x, dict) else 0
                )
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df.get("title", df.index),
                    y=df["polarity"],
                    mode="lines+markers",
                    name="Polarity",
                    line=dict(color="#c8974a", width=1.5),
                    marker=dict(size=5, color="#c8974a"),
                ))
                fig.add_trace(go.Scatter(
                    x=df.get("title", df.index),
                    y=df["subjectivity"],
                    mode="lines+markers",
                    name="Subjectivity",
                    line=dict(color="#5a3d1e", width=1.5, dash="dot"),
                    marker=dict(size=5, color="#5a3d1e"),
                ))
                fig.update_layout(
                    **PLOTLY_LAYOUT,
                    legend=dict(
                        font=dict(family="JetBrains Mono", size=10, color="#5a5550"),
                        bgcolor="rgba(0,0,0,0)",
                        x=0, y=1,
                    ),
                    height=220,
                )
                st.plotly_chart(fig, use_container_width=True)
            except:
                pass

        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

        # Per-article cards
        for _, row in df.iterrows():
            vader = row.get("sentiment_vader") or {}
            tb = row.get("sentiment_textblob") or {}
            bias = row.get("bias") or {}

            comp = vader.get("compound", 0)
            polarity = round(float(tb.get("polarity", 0)), 3)
            subjectivity = round(float(tb.get("subjectivity", 0)), 3)
            bias_label = bias.get("label", "—")
            bias_conf = float(bias.get("confidence", 0))

            # Sentiment direction
            if comp > 0.05:
                sent_icon, sent_color = "↑ Positive", "#4a8c5c"
            elif comp < -0.05:
                sent_icon, sent_color = "↓ Negative", "#8c4a4a"
            else:
                sent_icon, sent_color = "→ Neutral", "#5a5550"

            st.markdown(f"""
            <div class="ng-sentiment-card">
                <h4>{row.get("title", "Untitled")}</h4>
                <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1.2rem;margin-bottom:1rem">
                    <div>
                        <div class="ng-stat-label">VADER compound</div>
                        <div class="ng-stat-value" style="color:{sent_color}">{sent_icon} ({round(comp,3)})</div>
                    </div>
                    <div>
                        <div class="ng-stat-label">Polarity</div>
                        <div class="ng-stat-value">{polarity}</div>
                    </div>
                    <div>
                        <div class="ng-stat-label">Subjectivity</div>
                        <div class="ng-stat-value">{subjectivity}</div>
                    </div>
                </div>
                <hr class="ng-divider">
                <div style="display:flex;align-items:center;justify-content:space-between;margin-top:0.7rem">
                    <div>
                        <div class="ng-stat-label" style="margin-bottom:0.3rem">Media bias</div>
                        <span class="ng-bias-label">{bias_label}</span>
                    </div>
                    <div style="text-align:right">
                        <div class="ng-stat-label" style="margin-bottom:0.3rem">Confidence</div>
                        <div class="ng-stat-value">{round(bias_conf * 100)}%</div>
                    </div>
                </div>
                <div style="margin-top:0.5rem;background:#1e1c19;height:3px;border-radius:0;">
                    <div style="width:{round(bias_conf * 100)}%;height:3px;background:#c8974a;border-radius:0;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # VADER breakdown chart
        try:
            vader_rows = []
            for _, row in df.iterrows():
                v = row.get("sentiment_vader") or {}
                vader_rows.append({
                    "title": str(row.get("title", ""))[:40] + "…",
                    "Positive": v.get("positive", 0),
                    "Neutral": v.get("neutral", 0),
                    "Negative": v.get("negative", 0),
                })
            vdf = pd.DataFrame(vader_rows)
            if not vdf.empty:
                st.markdown('<div class="ng-section-label" style="margin-top:2rem">VADER breakdown by article</div>', unsafe_allow_html=True)
                fig2 = go.Figure()
                for col, color in [("Positive","#4a8c5c"),("Neutral","#3a3530"),("Negative","#8c4a4a")]:
                    fig2.add_trace(go.Bar(
                        name=col,
                        x=vdf["title"],
                        y=vdf[col],
                        marker_color=color,
                        marker_line_width=0,
                    ))
                fig2.update_layout(
                    **PLOTLY_LAYOUT,
                    barmode="stack",
                    height=280,
                    legend=dict(
                        font=dict(family="JetBrains Mono", size=10, color="#5a5550"),
                        bgcolor="rgba(0,0,0,0)",
                        orientation="h", x=0, y=1.05,
                    ),
                )
                st.plotly_chart(fig2, use_container_width=True)
        except:
            pass