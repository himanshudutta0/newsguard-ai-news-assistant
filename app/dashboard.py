import streamlit as st
import json
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import subprocess
import time

st.set_page_config(
    page_title="NewsGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Page background */
.stApp {
    background: #0d0f14;
    color: #e8e6e0;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #13161d !important;
    border-right: 1px solid #1f2330;
}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] label {
    color: #8a8fa0 !important;
    font-size: 12px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* Header */
.ng-header {
    display: flex;
    align-items: baseline;
    gap: 14px;
    padding: 2rem 0 0.5rem;
    border-bottom: 1px solid #1f2330;
    margin-bottom: 1.5rem;
}
.ng-logo {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    color: #e8e6e0;
    line-height: 1;
}
.ng-logo span { color: #4f8fff; }
.ng-tagline {
    font-size: 12px;
    color: #4a4f60;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: transparent;
    border-bottom: 1px solid #1f2330;
    gap: 0;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'DM Sans', sans-serif;
    font-size: 13px;
    font-weight: 500;
    color: #4a4f60;
    padding: 10px 20px;
    border-radius: 0;
    border-bottom: 2px solid transparent;
    transition: all 0.15s;
    letter-spacing: 0.02em;
}
.stTabs [aria-selected="true"] {
    color: #4f8fff !important;
    border-bottom: 2px solid #4f8fff !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab"]:hover { color: #a0a8c0 !important; }
.stTabs [data-baseweb="tab-panel"] { padding-top: 1.5rem; }

/* Article cards */
.ng-card {
    background: #13161d;
    border: 1px solid #1f2330;
    border-radius: 10px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
}
.ng-card:hover { border-color: #2d3250; }
.ng-card-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.1rem;
    color: #e8e6e0;
    margin-bottom: 6px;
    line-height: 1.4;
}
.ng-card-meta {
    font-size: 12px;
    color: #4a4f60;
    letter-spacing: 0.04em;
    margin-bottom: 10px;
}
.ng-card-meta a { color: #4f8fff; text-decoration: none; }
.ng-card-meta a:hover { text-decoration: underline; }
.ng-tag {
    display: inline-block;
    background: #1a1f2e;
    border: 1px solid #2a3050;
    color: #7a90c0;
    font-size: 11px;
    font-weight: 500;
    padding: 3px 9px;
    border-radius: 4px;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-right: 6px;
}
.ng-tag-blue { border-color: #1a3a6e; color: #4f8fff; background: #0d1a30; }
.ng-tag-green { border-color: #1a3a2e; color: #3fcf8e; background: #0d201a; }
.ng-tag-amber { border-color: #3a2a0d; color: #c09020; background: #1e1808; }
.ng-tag-red { border-color: #3a1010; color: #e05050; background: #1e0a0a; }

/* Metric row */
.ng-metrics {
    display: flex;
    gap: 12px;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
}
.ng-metric {
    flex: 1;
    min-width: 120px;
    background: #13161d;
    border: 1px solid #1f2330;
    border-radius: 10px;
    padding: 1rem 1.25rem;
}
.ng-metric-label {
    font-size: 11px;
    color: #4a4f60;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 6px;
}
.ng-metric-value {
    font-size: 1.6rem;
    font-weight: 600;
    color: #e8e6e0;
    line-height: 1;
}
.ng-metric-sub {
    font-size: 11px;
    color: #3fcf8e;
    margin-top: 4px;
}

/* Expanders */
details summary {
    font-size: 12px;
    color: #4a4f60;
    cursor: pointer;
    letter-spacing: 0.04em;
    margin-top: 8px;
}
details summary:hover { color: #8a8fa0; }

/* Search bar */
.stTextInput > div > div > input {
    background: #13161d !important;
    border: 1px solid #1f2330 !important;
    border-radius: 8px !important;
    color: #e8e6e0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    padding: 10px 14px !important;
}
.stTextInput > div > div > input:focus {
    border-color: #4f8fff !important;
    box-shadow: 0 0 0 1px #4f8fff20 !important;
}

/* Buttons */
.stButton > button {
    background: #1a1f2e !important;
    border: 1px solid #2d3250 !important;
    color: #7a90c0 !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 8px 16px !important;
    transition: all 0.15s !important;
}
.stButton > button:hover {
    border-color: #4f8fff !important;
    color: #4f8fff !important;
    background: #0d1a30 !important;
}

/* Selectbox & multiselect */
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: #13161d !important;
    border: 1px solid #1f2330 !important;
    border-radius: 8px !important;
    color: #e8e6e0 !important;
}

/* Section headers */
.ng-section-header {
    font-family: 'DM Serif Display', serif;
    font-size: 1.4rem;
    color: #e8e6e0;
    margin-bottom: 1.25rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #1f2330;
}

/* Entity pill */
.ng-entity {
    display: inline-block;
    margin: 3px 4px 3px 0;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
}

/* Divider */
.ng-divider { border: none; border-top: 1px solid #1f2330; margin: 1rem 0; }

/* Sentiment progress */
.ng-progress-wrap {
    background: #1a1f2e;
    border-radius: 4px;
    height: 6px;
    margin-top: 4px;
}
.ng-progress-fill {
    height: 6px;
    border-radius: 4px;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0d0f14; }
::-webkit-scrollbar-thumb { background: #1f2330; border-radius: 3px; }

/* Info/warning boxes */
.ng-info {
    background: #0d1a30;
    border: 1px solid #1a3a6e;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    color: #7a90c0;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# ── Data Loading ──────────────────────────────────────────────────────────────
@st.cache_data(ttl=60 * 60)
def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []

def auto_refresh(last_refresh_time):
    diff = time.time() - last_refresh_time
    if diff >= 300:
        return True, time.time()
    return False, last_refresh_time

if 'last_refresh_time' not in st.session_state:
    st.session_state['last_refresh_time'] = time.time()

refresh_needed, st.session_state['last_refresh_time'] = auto_refresh(
    st.session_state['last_refresh_time']
)

def load_all():
    return {
        "scraped": load_json("data/scrapped.json"),
        "preprocessed": load_json("data/preprocessed.json"),
        "entities": load_json("data/entities.json"),
        "predicted": load_json("data/topic_predicted.json"),
        "summarized": load_json("data/summarized.json"),
        "topic_modeled": load_json("data/topic_modeled.json"),
        "sentiment_bias": load_json("data/sentiment_bias.json"),
    }

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 1.5rem 0 1rem;'>
        <div style='font-family: DM Serif Display, serif; font-size: 1.3rem; color: #e8e6e0;'>
            News<span style='color:#4f8fff'>Guard</span>
        </div>
        <div style='font-size: 11px; color: #3a3f50; letter-spacing: 0.1em; text-transform: uppercase; margin-top: 2px;'>
            AI Intelligence Platform
        </div>
    </div>
    <hr style='border: none; border-top: 1px solid #1f2330; margin-bottom: 1.25rem;'>
    """, unsafe_allow_html=True)

    if st.button("↻  Refresh Data", use_container_width=True):
        with st.spinner("Fetching latest articles..."):
            result = subprocess.run(["python", "main.py"], capture_output=True, text=True)
        load_json.clear()
        st.success("Data refreshed!")

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown("**NAVIGATION**")
    global_query = st.text_input("", placeholder="Search all articles…", label_visibility="collapsed")

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown("**LAST UPDATED**")
    st.markdown(f"<div style='font-size:13px;color:#4a4f60'>{datetime.now().strftime('%b %d, %Y · %H:%M')}</div>",
                unsafe_allow_html=True)

data = load_all()

# ── Match helper ──────────────────────────────────────────────────────────────
def match(article, keys):
    if not global_query:
        return True
    q = global_query.lower()
    return any(q in str(article.get(k, "")).lower() for k in keys)

def plotly_theme():
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color="#8a8fa0", size=12),
        margin=dict(l=0, r=0, t=30, b=0),
    )

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='ng-header'>
    <div class='ng-logo'>News<span>Guard</span></div>
    <div class='ng-tagline'>AI-Powered Multilingual Intelligence</div>
</div>
""", unsafe_allow_html=True)

# ── Metric Strip ──────────────────────────────────────────────────────────────
s = data["scraped"]
sb = data["sentiment_bias"]
topics = [a.get("predicted_topic", "") for a in data["predicted"]]
unique_topics = len(set(topics)) if topics else 0

pos_count = sum(1 for a in sb if a.get("sentiment_vader", {}).get("compound", 0) > 0.05)
neg_count = sum(1 for a in sb if a.get("sentiment_vader", {}).get("compound", 0) < -0.05)

st.markdown(f"""
<div class='ng-metrics'>
    <div class='ng-metric'>
        <div class='ng-metric-label'>Articles Scraped</div>
        <div class='ng-metric-value'>{len(s)}</div>
        <div class='ng-metric-sub'>Today</div>
    </div>
    <div class='ng-metric'>
        <div class='ng-metric-label'>Topics Detected</div>
        <div class='ng-metric-value'>{unique_topics}</div>
    </div>
    <div class='ng-metric'>
        <div class='ng-metric-label'>Positive Tone</div>
        <div class='ng-metric-value'>{pos_count}</div>
        <div class='ng-metric-sub' style='color:#3fcf8e'>Articles</div>
    </div>
    <div class='ng-metric'>
        <div class='ng-metric-label'>Negative Tone</div>
        <div class='ng-metric-value'>{neg_count}</div>
        <div class='ng-metric-sub' style='color:#e05050'>Articles</div>
    </div>
    <div class='ng-metric'>
        <div class='ng-metric-label'>Summarized</div>
        <div class='ng-metric-value'>{len(data["summarized"])}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "Scraped", "Preprocessed", "Entities",
    "Topics", "Summaries", "Topic Model",
    "Daily Digest", "Sentiment & Bias"
])

# ─── Tab 1: Scraped ────────────────────────────────────────────────────────
with tabs[0]:
    st.markdown("<div class='ng-section-header'>Scraped Articles</div>", unsafe_allow_html=True)
    articles = [a for a in data["scraped"] if match(a, ['title', 'content'])]
    st.markdown(f"<div style='font-size:12px;color:#4a4f60;margin-bottom:1rem'>{len(articles)} articles found</div>",
                unsafe_allow_html=True)
    for a in articles:
        date_str = a.get('published_at', 'Unknown date')
        st.markdown(f"""
        <div class='ng-card'>
            <div class='ng-card-title'>{a.get('title','Untitled')}</div>
            <div class='ng-card-meta'>
                📅 {date_str} &nbsp;·&nbsp; 🔗 <a href='{a.get('url','')}' target='_blank'>{a.get('url','')[:60]}…</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
        with st.expander("Read content"):
            st.write(a.get('content', ''))

# ─── Tab 2: Preprocessed ──────────────────────────────────────────────────
with tabs[1]:
    st.markdown("<div class='ng-section-header'>Preprocessed Content</div>", unsafe_allow_html=True)
    articles = [a for a in data["preprocessed"] if match(a, ['title', 'processed_content'])]
    for a in articles:
        st.markdown(f"""
        <div class='ng-card'>
            <div class='ng-card-title'>{a.get('title','Untitled')}</div>
            <div class='ng-card-meta'>🔗 <a href='{a.get('url','')}' target='_blank'>{a.get('url','')[:70]}</a></div>
        </div>
        """, unsafe_allow_html=True)
        with st.expander("Processed content"):
            st.write(a.get('processed_content', ''))

# ─── Tab 3: Entities ──────────────────────────────────────────────────────
with tabs[2]:
    st.markdown("<div class='ng-section-header'>Named Entity Recognition</div>", unsafe_allow_html=True)

    all_entities = []
    for article in data["entities"]:
        for label, entities in article.items():
            if label not in ["title", "url"]:
                for entity in (entities or []):
                    all_entities.append({"title": article.get("title",""), "entity": entity, "label": label})

    if all_entities:
        df_e = pd.DataFrame(all_entities)

        col_filter, col_chart = st.columns([1, 2])
        with col_filter:
            label_opts = ["All"] + sorted(df_e['label'].unique().tolist())
            chosen_label = st.selectbox("Filter by type", label_opts)

        filtered_df = df_e if chosen_label == "All" else df_e[df_e['label'] == chosen_label]

        counts = filtered_df['label'].value_counts().reset_index()
        counts.columns = ['Entity Type', 'Count']

        with col_chart:
            fig = go.Figure(go.Bar(
                x=counts['Entity Type'], y=counts['Count'],
                marker_color='#4f8fff',
                marker_line_width=0,
            ))
            fig.update_layout(**plotly_theme(), height=200)
            fig.update_xaxes(showgrid=False, tickfont=dict(size=11))
            fig.update_yaxes(showgrid=True, gridcolor='#1f2330')
            st.plotly_chart(fig, use_container_width=True)

        ENTITY_COLORS = {
            "PERSON": "ng-tag-blue", "ORG": "ng-tag-green",
            "GPE": "ng-tag-amber", "DATE": "ng-tag",
            "LOC": "ng-tag-amber", "MONEY": "ng-tag-green",
        }

        for title in filtered_df['title'].unique():
            st.markdown(f"<div class='ng-card'><div class='ng-card-title'>{title}</div>", unsafe_allow_html=True)
            rows = filtered_df[filtered_df['title'] == title]
            pills = "".join(
                f"<span class='ng-entity ng-tag {ENTITY_COLORS.get(r[\"label\"], \"ng-tag\")}'>{r['entity']} <span style='opacity:0.5;font-size:10px'>{r['label']}</span></span>"
                for _, r in rows.iterrows()
            )
            st.markdown(f"{pills}</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='ng-info'>No entity data available.</div>", unsafe_allow_html=True)

# ─── Tab 4: Predicted Topics ──────────────────────────────────────────────
with tabs[3]:
    st.markdown("<div class='ng-section-header'>Predicted Topics</div>", unsafe_allow_html=True)

    all_topics = sorted({a.get('predicted_topic','') for a in data["predicted"] if a.get('predicted_topic')})
    col1, col2 = st.columns([1, 3])
    with col1:
        topic_filter = st.multiselect("Filter topics", all_topics, placeholder="All topics")

    filtered = [
        a for a in data["predicted"]
        if (not topic_filter or a.get("predicted_topic") in topic_filter)
        and match(a, ['title'])
    ]

    if all_topics and data["predicted"]:
        topic_counts = pd.Series([a.get('predicted_topic','') for a in data["predicted"]]).value_counts()
        fig = go.Figure(go.Bar(
            x=topic_counts.index.tolist(),
            y=topic_counts.values.tolist(),
            marker_color='#3fcf8e',
            marker_line_width=0,
        ))
        fig.update_layout(**plotly_theme(), height=180)
        fig.update_xaxes(showgrid=False, tickangle=-20, tickfont=dict(size=11))
        fig.update_yaxes(showgrid=True, gridcolor='#1f2330')
        st.plotly_chart(fig, use_container_width=True)

    for a in filtered:
        st.markdown(f"""
        <div class='ng-card'>
            <div class='ng-card-title'>{a.get('title','Untitled')}</div>
            <div class='ng-card-meta' style='margin-bottom:8px'>
                🔗 <a href='{a.get('url','')}' target='_blank'>{a.get('url','')[:60]}</a>
            </div>
            <span class='ng-tag ng-tag-blue'>{a.get('predicted_topic','—')}</span>
        </div>
        """, unsafe_allow_html=True)
        with st.expander("Processed content"):
            st.write(a.get('processed_content', ''))

# ─── Tab 5: Summarized ────────────────────────────────────────────────────
with tabs[4]:
    st.markdown("<div class='ng-section-header'>Article Summaries</div>", unsafe_allow_html=True)
    articles = [a for a in data["summarized"] if match(a, ['title', 'summary'])]
    for a in articles:
        st.markdown(f"""
        <div class='ng-card'>
            <div class='ng-card-title'>{a.get('title','Untitled')}</div>
            <div class='ng-card-meta'>📅 {a.get('date','Unknown')} &nbsp;·&nbsp;
            🔗 <a href='{a.get('url','')}' target='_blank'>{a.get('url','')[:55]}…</a></div>
            <div style='font-size:14px;color:#c0c4d0;line-height:1.65;margin-top:6px'>
                {a.get('summary','')}
            </div>
        </div>
        """, unsafe_allow_html=True)
        with st.expander("Original content"):
            st.write(a.get('content', ''))

# ─── Tab 6: Topic Modeling ────────────────────────────────────────────────
with tabs[5]:
    st.markdown("<div class='ng-section-header'>Topic Modeling Timeline</div>", unsafe_allow_html=True)
    tm_data = data["topic_modeled"]

    col1, col2 = st.columns(2)
    with col1:
        kw_opts = ["All"] + sorted({str(a.get('topic_keywords','')) for a in tm_data})
        selected_kw = st.selectbox("Topic keywords", kw_opts)
    with col2:
        date_f = st.date_input("Filter by date", value=None)

    filtered_tm = [
        a for a in tm_data
        if (selected_kw == "All" or str(a.get("topic_keywords","")) == selected_kw)
        and (not date_f or str(a.get("date","")).startswith(str(date_f)))
        and match(a, ['title','processed_content'])
    ]

    if tm_data:
        df_tm = pd.DataFrame(tm_data)
        kw_counts = df_tm['topic_keywords'].astype(str).value_counts().head(12)
        fig = go.Figure(go.Bar(
            x=kw_counts.values.tolist(), y=kw_counts.index.tolist(),
            orientation='h',
            marker_color='#c09020',
            marker_line_width=0,
        ))
        fig.update_layout(**plotly_theme(), height=300)
        fig.update_xaxes(showgrid=True, gridcolor='#1f2330')
        fig.update_yaxes(showgrid=False, tickfont=dict(size=11))
        st.plotly_chart(fig, use_container_width=True)

    for a in filtered_tm:
        st.markdown(f"""
        <div class='ng-card'>
            <div class='ng-card-title'>{a.get('title','Untitled')}</div>
            <div class='ng-card-meta'>📅 {a.get('date','Unknown')} &nbsp;·&nbsp;
            🔗 <a href='{a.get('url','')}' target='_blank'>{a.get('url','')[:55]}…</a></div>
            <span class='ng-tag ng-tag-amber'>{str(a.get('topic_keywords',''))[:60]}</span>
        </div>
        """, unsafe_allow_html=True)
        with st.expander("Processed content"):
            st.write(a.get('processed_content',''))

# ─── Tab 7: Daily Digest ──────────────────────────────────────────────────
with tabs[6]:
    st.markdown("<div class='ng-section-header'>Daily Digest</div>", unsafe_allow_html=True)
    today = datetime.now().strftime("%Y-%m-%d")
    today_articles = [a for a in data["summarized"] if a.get("date","").startswith(today)]

    if today_articles:
        st.markdown(f"""
        <div style='font-size:12px;color:#4a4f60;margin-bottom:1.5rem'>
            {datetime.now().strftime("%A, %B %d, %Y")} · {len(today_articles)} articles
        </div>
        """, unsafe_allow_html=True)
        for i, a in enumerate(today_articles, 1):
            st.markdown(f"""
            <div class='ng-card'>
                <div style='display:flex;align-items:baseline;gap:10px'>
                    <span style='font-family:DM Serif Display,serif;font-size:1.5rem;color:#2a3050'>{i:02d}</span>
                    <div>
                        <div class='ng-card-title'>{a.get('title','Untitled')}</div>
                        <div class='ng-card-meta'>🔗 <a href='{a.get('url','')}' target='_blank'>{a.get('url','')[:60]}</a></div>
                        <div style='font-size:14px;color:#c0c4d0;line-height:1.65;margin-top:6px'>{a.get('summary','')}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("<div class='ng-info'>No articles found for today. Run a refresh to fetch the latest.</div>",
                    unsafe_allow_html=True)

# ─── Tab 8: Sentiment & Bias ──────────────────────────────────────────────
with tabs[7]:
    st.markdown("<div class='ng-section-header'>Sentiment & Bias Analysis</div>", unsafe_allow_html=True)
    sb_data = data["sentiment_bias"]

    if sb_data:
        df_sb = pd.DataFrame(sb_data)
        df_sb['_date'] = pd.to_datetime(df_sb['date'].replace("Unknown", "1970-01-01"), errors='coerce')

        col1, col2 = st.columns([1, 3])
        with col1:
            date_sb = st.date_input("Filter by date", value=None, key="sb_date")
        if date_sb:
            df_sb = df_sb[df_sb['_date'].dt.date == date_sb]

        # Aggregate charts
        if len(df_sb) > 0:
            compounds = [a.get('sentiment_vader', {}).get('compound', 0) for a in sb_data]
            labels = [a.get('title','')[:35]+'…' for a in sb_data]
            colors = ['#3fcf8e' if c > 0.05 else '#e05050' if c < -0.05 else '#4a4f60' for c in compounds]

            fig = go.Figure(go.Bar(
                x=labels, y=compounds,
                marker_color=colors,
                marker_line_width=0,
            ))
            fig.update_layout(**plotly_theme(), height=220)
            fig.update_xaxes(showgrid=False, tickangle=-30, tickfont=dict(size=10))
            fig.update_yaxes(showgrid=True, gridcolor='#1f2330', zeroline=True, zerolinecolor='#2d3250')
            st.plotly_chart(fig, use_container_width=True)

        for _, row in df_sb.iterrows():
            if global_query and global_query.lower() not in str(row.get('title','')).lower():
                continue

            vader = row.get('sentiment_vader', {})
            textblob = row.get('sentiment_textblob', {})
            bias = row.get('bias', {})
            compound = vader.get('compound', 0)
            tone_color = '#3fcf8e' if compound > 0.05 else '#e05050' if compound < -0.05 else '#8a8fa0'
            tone_label = 'Positive' if compound > 0.05 else 'Negative' if compound < -0.05 else 'Neutral'
            bias_label = bias.get('label', '—')
            bias_conf = bias.get('confidence', 0)

            st.markdown(f"""
            <div class='ng-card'>
                <div style='display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px'>
                    <div class='ng-card-title' style='flex:1'>{row.get('title','Untitled')}</div>
                    <span class='ng-tag' style='color:{tone_color};border-color:{tone_color}20;background:{tone_color}10'>{tone_label}</span>
                </div>
                <div class='ng-card-meta'>📅 {row.get('date','Unknown')}</div>
                <div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;margin-top:12px'>
                    <div>
                        <div style='font-size:11px;color:#4a4f60;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px'>VADER</div>
                        <div style='font-size:1.1rem;font-weight:600;color:{tone_color}'>{compound:+.2f}</div>
                        <div style='font-size:12px;color:#4a4f60;margin-top:4px'>
                            +{vader.get('positive',0):.2f} / ~{vader.get('neutral',0):.2f} / -{vader.get('negative',0):.2f}
                        </div>
                    </div>
                    <div>
                        <div style='font-size:11px;color:#4a4f60;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px'>TextBlob</div>
                        <div style='font-size:1.1rem;font-weight:600;color:#c0c4d0'>
                            {textblob.get('polarity',0):+.2f}
                        </div>
                        <div style='font-size:12px;color:#4a4f60;margin-top:4px'>
                            Subjectivity: {textblob.get('subjectivity',0):.2f}
                        </div>
                    </div>
                    <div>
                        <div style='font-size:11px;color:#4a4f60;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px'>Bias</div>
                        <div style='font-size:1.1rem;font-weight:600;color:#c09020'>{bias_label}</div>
                        <div style='font-size:12px;color:#4a4f60;margin-top:4px'>Confidence: {bias_conf:.0%}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("<div class='ng-info'>Sentiment and bias data not yet available. Run a refresh.</div>",
                    unsafe_allow_html=True)
