import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

def assign_topics_with_nmf_and_save(input_path, output_path, num_topics=5, num_top_words=10):
    # Load input articles
    with open(input_path, "r", encoding='utf-8') as f:
        input_articles = json.load(f)

    # Load existing output (if exists)
    existing_articles = []
    existing_urls = set()

    if os.path.exists(output_path):
        try:
            with open(output_path, "r", encoding='utf-8') as f:
                existing_articles = json.load(f)
                existing_urls = {a['url'] for a in existing_articles}
        except Exception as e:
            print(f"Warning: Could not load existing output file: {e}")

    # Filter new articles only
    new_articles = [a for a in input_articles if a.get("url") not in existing_urls and a.get("processed_content")]

    if not new_articles:
        print("No new articles to process.")
        return

    print(f"Processing {len(new_articles)} new articles with NMF")

    # Extract text for NMF
    texts = [article["processed_content"] for article in new_articles]

    # Dynamically set min_df based on the number of documents
    num_docs = len(texts)
    min_df = 2 if num_docs >= 10 else 1  # Set min_df to 1 for fewer documents
    max_df = 0.95

    # TF-IDF vectorization
    vectorizer = TfidfVectorizer(max_df=max_df, min_df=min_df, stop_words='english')
    tfidf = vectorizer.fit_transform(texts)

    # Fit NMF model
    nmf = NMF(n_components=num_topics, random_state=42)
    W = nmf.fit_transform(tfidf)
    H = nmf.components_

    # Extract topic keywords
    feature_names = vectorizer.get_feature_names_out()
    topic_keywords = []
    for topic_idx, topic_weights in enumerate(H):
        top_words = [feature_names[i] for i in topic_weights.argsort()[:-num_top_words - 1:-1]]
        topic_keywords.append(top_words)

    # Assign topic to each article
    for i, article in enumerate(new_articles):
        topic_idx = int(W[i].argmax())
        article["topic_keywords"] = ", ".join(topic_keywords[topic_idx])

    # Combine and save
    all_articles = existing_articles + new_articles
    with open(output_path, "w", encoding='utf-8') as f:
        json.dump(all_articles, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(new_articles)} new topic assignments to '{output_path}'")
