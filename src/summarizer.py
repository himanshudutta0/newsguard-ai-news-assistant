import json
import os
from transformers import pipeline

# Use CPU only by setting device to -1
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)

def summarize(text, max_length=130, min_length=30):
    try:
        # Truncate text to avoid exceeding token limits
        text = text[:1024 * 4]  # Limit text to 4KB (BART max token length)

        # Generate summary using BART
        summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        print("Error summarizing:", e)
        return ""

def summarize_articles(input_path, output_path):
    try:
        # Load the input JSON file
        with open(input_path, "r", encoding="utf-8") as f:
            input_articles = json.load(f)
    except Exception as e:
        print("Error loading input file:", e)
        return

    # Load previously summarized articles
    existing_articles = []
    existing_urls = set()

    if os.path.exists(output_path):
        try:
            with open(output_path, "r", encoding="utf-8") as f:
                existing_articles = json.load(f)
                existing_urls = {a['url'] for a in existing_articles}
        except Exception as e:
            print("Warning: Could not load existing output file:", e)

    # Filter out already summarized articles
    new_articles = [a for a in input_articles if a.get("url") not in existing_urls and a.get("content", "").strip()]

    if not new_articles:
        print("No new articles to summarize.")
        return

    print(f"Summarizing {len(new_articles)} new articles...")

    summarized = []
    for idx, article in enumerate(new_articles):
        title = article.get("title", f"Untitled {idx}")
        content = article.get("content", "")
        url = article.get("url", "")
        date = article.get("published_at", "")

        # Summarize the article content
        summary = summarize(content)

        # Append summarized result
        summarized.append({
            "title": title,
            "content": content,
            "summary": summary,
            "url": url,
            "date": date
        })

    # Combine existing and new summaries
    all_summaries = existing_articles + summarized

    try:
        # Save the summarized articles to an output file
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(all_summaries, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print("Error writing to output file:", e)

    print(f"Summarization complete! Saved {len(summarized)} new summaries to {output_path}")
