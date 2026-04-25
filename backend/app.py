from fastapi import FastAPI, Query
import subprocess
from utils import load_json
from datetime import datetime
import pandas as pd

app = FastAPI(title="NewsGuard API")

# ---------------- ROOT ----------------
@app.get("/")
def root():
    return {"message": "Backend is running"}

# ---------------- PIPELINE ----------------
@app.get("/refresh")
def refresh_pipeline():
    try:
        subprocess.run(["python", "../main.py"], check=True)
        return {"status": "Pipeline executed successfully"}
    except Exception as e:
        return {"error": str(e)}

# ---------------- BASIC DATA ----------------
@app.get("/articles/scraped")
def scraped():
    return load_json("scrapped.json")

@app.get("/articles/preprocessed")
def preprocessed():
    return load_json("preprocessed.json")

@app.get("/summaries")
def summaries():
    return load_json("summarized.json")

@app.get("/topics/predicted")
def predicted_topics():
    return load_json("topic_predicted.json")

@app.get("/topics/modeled")
def topic_modeled():
    return load_json("topic_modeled.json")

@app.get("/sentiment")
def sentiment_bias():
    return load_json("sentiment_bias.json")

# ---------------- SEARCH ----------------
@app.get("/search")
def search(q: str = Query(...)):
    data = load_json("scrapped.json")
    return [
        a for a in data
        if q.lower() in a.get("title", "").lower()
        or q.lower() in a.get("content", "").lower()
    ]

# ---------------- ENTITIES ----------------
@app.get("/entities")
def entities():
    data = load_json("entities.json")

    all_entities = []
    for article in data:
        for label, ents in article.items():
            if label not in ["title", "url"]:
                for e in ents:
                    all_entities.append({"label": label, "entity": e})

    df = pd.DataFrame(all_entities)

    if df.empty:
        return {"entities": [], "counts": []}

    counts = df.groupby("label").size().reset_index(name="count")

    return {
        "entities": df.to_dict(orient="records"),
        "counts": counts.to_dict(orient="records")
    }

# ---------------- DAILY DIGEST ----------------
@app.get("/digest/today")
def today_digest():
    data = load_json("summarized.json")
    today = datetime.now().strftime("%Y-%m-%d")

    return [
        a for a in data
        if a.get("date", "").startswith(today)
    ]

# ---------------- SENTIMENT FILTER ----------------
@app.get("/sentiment/filter")
def sentiment_filter(date: str = None):
    data = load_json("sentiment_bias.json")

    if not date:
        return data

    return [
        a for a in data
        if a.get("date", "").startswith(date)
    ]