import streamlit as st
import json
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import plotly.express as px
import subprocess
import time

# Set page configuration
st.set_page_config(page_title="NewsGuard-AI Powered Multilingual News", layout="wide")


# Load JSON files with caching
@st.cache_data(ttl=60 * 60)  # Cache data for 1 hour to avoid reloading too often
def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading {file_path}: {e}")
        return []


# Function to refresh the data automatically after a certain time interval
def auto_refresh(last_refresh_time):
    current_time = time.time()
    time_diff = current_time - last_refresh_time
    refresh_interval =  5*60  # 5 minutes refresh interval

    if time_diff >= refresh_interval:
        return True, current_time
    else:
        return False, last_refresh_time


# Initialize or update the last refresh time
if 'last_refresh_time' not in st.session_state:
    st.session_state['last_refresh_time'] = time.time()

# Auto refresh condition
refresh_needed, st.session_state['last_refresh_time'] = auto_refresh(st.session_state['last_refresh_time'])

# Manual refresh button
refresh_data = st.button("🔄 Refresh Data")

if refresh_data or refresh_needed:
    with st.spinner("Running main.py..."):
        result = subprocess.run(["python", "main.py"], capture_output=True, text=True)
    # Reload all JSON files when auto-refresh or manual refresh is triggered
    scraped_articles = load_json("data/scrapped.json")
    preprocessed_articles = load_json("data/preprocessed.json")
    entities_data = load_json("data/entities.json")
    predicted_topics_data = load_json("data/topic_predicted.json")
    summarized_articles = load_json("data/summarized.json")
    topic_modeled_data = load_json("data/topic_modeled.json")
    st.success("Data refreshed successfully!")
else:
    # If not refreshed, use cached data
    scraped_articles = load_json("data/scrapped.json")
    preprocessed_articles = load_json("data/preprocessed.json")
    entities_data = load_json("data/entities.json")
    predicted_topics_data = load_json("data/topic_predicted.json")
    summarized_articles = load_json("data/summarized.json")
    topic_modeled_data = load_json("data/topic_modeled.json")


# Helper function for search matching
def match_query(article, keys):
    return any(global_query.lower() in article.get(key, "").lower() for key in keys)


st.title("🗞️ NewsGuard Dashboard")
global_query = st.text_input("🔎 Global Search", "")

# Tabs
tabs = st.tabs([
    "📝 Scraped", "🧹 Preprocessed", "🏷️ Entities", "🔮 Predicted Topics",
    "🧠 Summarized", "📊 Topic Modeling", "📬 Daily Digest", "🧭 Sentiment & Bias"
])

# Tab 1: Scraped
with tabs[0]:
    st.header("📝 Scraped Articles")
    for article in scraped_articles:
        if global_query and not match_query(article, ['title', 'content']):
            continue
        st.subheader(article['title'])
        st.markdown(f"**URL:** [{article['url']}]({article['url']})")
        st.markdown(f"📅 **Date:** {article.get('published_at', 'Unknown')}")
        with st.expander("Content"):
            st.write(article['content'])

# Tab 2: Preprocessed
with tabs[1]:
    st.header("🧹 Preprocessed Content")
    for article in preprocessed_articles:
        if global_query and not match_query(article, ['title', 'processed_content']):
            continue
        st.subheader(article['title'])
        st.markdown(f"**URL:** [{article['url']}]({article['url']})")
        with st.expander("Processed Content"):
            st.write(article['processed_content'])

# Tab 3: Named Entities with Visualization and Filters
with tabs[2]:
    st.markdown("### 🏷️ Named Entities")

    # Prepare entity data for visualization
    all_entities = []
    for article in entities_data:
        for label, entities in article.items():
            if label not in ["title", "url"]:
                for entity in entities:
                    all_entities.append({"title": article["title"], "entity": entity, "label": label})

    df_entities = pd.DataFrame(all_entities)

    # Filter options
    entity_label_filter = st.selectbox("Filter by Entity Type", options=["All"] + list(df_entities['label'].unique()))
    if entity_label_filter != "All":
        df_entities = df_entities[df_entities['label'] == entity_label_filter]

    # Display filtered entities
    st.write(f"Found {len(df_entities)} entities")

    # Visualization: Entity Counts by Type
    entity_counts = df_entities['label'].value_counts().reset_index()
    entity_counts.columns = ['Entity Type', 'Count']

    fig = plt.figure(figsize=(5, 3))
    plt.bar(entity_counts['Entity Type'], entity_counts['Count'], color="skyblue")
    plt.title('Distribution of Named Entity Types')
    plt.xlabel('Entity Type')
    plt.ylabel('Count')
    st.pyplot(fig)

    # Visualization: Entity Distribution (Bar Plot)
    st.markdown("#### Entity Distribution (Bar Plot)")
    entity_dist_fig = px.bar(entity_counts, x='Entity Type', y='Count', title="Entity Type Distribution")
    st.plotly_chart(entity_dist_fig)

    # Show entities list
    st.write("### List of Entities")
    for article in df_entities['title'].unique():
        st.subheader(article)
        filtered_entities = df_entities[df_entities['title'] == article]
        for _, row in filtered_entities.iterrows():
            st.write(f"{row['entity']} - {row['label']}")

# Tab 4: Predicted Topics
with tabs[3]:
    st.header("🔮 Predicted Topics")
    topic_filter = st.multiselect("Filter by Topic", options=sorted(set(a['predicted_topic'] for a in predicted_topics_data)))
    for article in predicted_topics_data:
        if topic_filter and article["predicted_topic"] not in topic_filter:
            continue
        if global_query and not match_query(article, ['title']):
            continue
        st.subheader(article["title"])
        st.markdown(f"**Topic:** `{article['predicted_topic']}`")
        st.markdown(f"**URL:** [{article['url']}]({article['url']})")
        with st.expander("Processed Content"):
            st.write(article["processed_content"])

# Tab 5: Summarized
with tabs[4]:
    st.header("🧠 Summarized Articles")
    for article in summarized_articles:
        if global_query and not match_query(article, ['title', 'summary']):
            continue
        st.subheader(article["title"])
        st.markdown(f"📅 {article.get('date', 'Unknown')} | 🔗 [{article['url']}]({article['url']})")
        with st.expander("Summary"):
            st.write(article["summary"])
        with st.expander("Original Content"):
            st.write(article["content"])

# Tab 6: Topic Modeling
with tabs[5]:
    st.header("📊 Topic Modeling Timeline")
    selected_topic = st.selectbox("Choose Topic", ["All"] + sorted({str(a['topic_keywords']) for a in topic_modeled_data}))
    date_filter = st.date_input("Filter by Date", value=None)

    filtered = []
    for article in topic_modeled_data:
        if selected_topic != "All" and str(article["topic"]) != selected_topic:
            continue
        if date_filter and not article.get("date", "").startswith(str(date_filter)):
            continue
        if global_query and not match_query(article, ['title', 'processed_content']):
            continue
        filtered.append(article)

    for article in filtered:
        st.subheader(article["title"])
        st.markdown(f"📅 {article.get('date', 'Unknown')} | 🔗 [{article['url']}]({article['url']})")
        st.markdown(f"**Topic {article['title']}**: `{article['topic_keywords']}`")
        with st.expander("Processed Content"):
            st.write(article["processed_content"])

    # Topic frequency chart
    if topic_modeled_data:
        df = pd.DataFrame(topic_modeled_data)
        fig = px.histogram(df, x="topic_keywords", title="Topic Distribution")
        st.plotly_chart(fig)

# Tab 7: Daily Digest (with PDF export)
with tabs[6]:
    st.markdown("### 📬 Daily Digest Generator")
    today = datetime.now().strftime("%Y-%m-%d")

    # Filter articles published today
    today_articles = [
        article for article in summarized_articles
        if article.get("date", "").startswith(today)
    ]

    if today_articles:
        for article in today_articles:
            st.subheader(article["title"])
            st.markdown(f"**Date:** {article.get('date')}")
            st.markdown(f"**URL:** [{article['url']}]({article['url']})")
            st.markdown(f"🧠 **Summary:** {article['summary']}")
    else:
        st.info("No articles found for today.")

# Tab 8: Sentiment & Bias Analysis
with tabs[7]:
    st.header("🧭 Sentiment & Bias Analysis")

    # Load from sentiment_bias.json (or use direct data if already loaded)
    sentiment_bias_data = load_json("data/sentiment_bias.json")  # Replace with your actual file path

    if sentiment_bias_data:
        df_sentiment = pd.DataFrame(sentiment_bias_data)
        df_sentiment['formatted_date'] = df_sentiment['date'].replace("Unknown", "1970-01-01")
        df_sentiment['formatted_date'] = pd.to_datetime(df_sentiment['formatted_date'], errors='coerce')

        # Filters
        date_filter = st.date_input("Filter by Date", value=None, key="date_filter_sentiment_bias")
        if date_filter:
            df_sentiment = df_sentiment[df_sentiment['formatted_date'].dt.date == date_filter]

        # Display
        for _, article in df_sentiment.iterrows():
            if global_query and global_query.lower() not in article["title"].lower():
                continue
            st.subheader(article["title"])
            st.markdown(f"📅 **Date:** {article['date']}")
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("#### VADER Sentiment")
                compound_score = article['sentiment_vader']['compound']
                normalized_score = (compound_score + 1) / 2  # Shift from [-1, 1] → [0, 1]
                st.progress(normalized_score, text=f"Compound: {compound_score:.2f}")
                st.write(f"Positive: {article['sentiment_vader']['positive']}")
                st.write(f"Neutral: {article['sentiment_vader']['neutral']}")
                st.write(f"Negative: {article['sentiment_vader']['negative']}")

            with col2:
                st.markdown("#### TextBlob Sentiment")
                st.metric("Polarity", f"{article['sentiment_textblob']['polarity']:.2f}")
                st.metric("Subjectivity", f"{article['sentiment_textblob']['subjectivity']:.2f}")

            with col3:
                st.markdown("#### Bias Detection")
                st.metric("Label", article['bias']['label'])
                st.progress(article['bias']['confidence'], text=f"Confidence: {article['bias']['confidence']:.2f}")

    else:
        st.warning("Sentiment and bias data not available.")
