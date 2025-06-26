import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
from newspaper import Article
from datetime import datetime
import os

def scrape_urls(base_url):
    try:
        response = requests.get(base_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error accessing {base_url}: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    urls = set()

    for link in soup.find_all('a', href=True):
        full_url = urljoin(base_url, link['href'])
        urls.add(full_url)

    return list(urls)

def save_urls_to_json(urls, filename):
    try:
        with open(filename, 'w') as f:
            json.dump(urls, f, indent=4)
        print(f"URLs saved to {filename}")
    except Exception as e:
        print(f"Error saving to {filename}: {e}")

def scrape_and_save_articles(urls_json_path, output_path):
    print("Starting article scraping...")

    # Load all URLs to be scraped
    with open(urls_json_path, 'r', encoding='utf-8') as f:
        all_urls = json.load(f)

    # Load already scraped articles (if any)
    scraped_articles = []
    scraped_urls = set()

    if os.path.exists(output_path):
        try:
            with open(output_path, 'r', encoding='utf-8') as f:
                scraped_articles = json.load(f)
                scraped_urls = {article['url'] for article in scraped_articles}
        except Exception as e:
            print(f"Warning: Could not load existing scraped articles: {e}")

    new_articles = []

    # Scrape only new URLs
    for url in all_urls:
        if url in scraped_urls:
            continue
        try:
            article = Article(url)
            article.download()
            article.parse()
            article.nlp()

            publish_date = article.publish_date
            if publish_date:
                publish_date = publish_date.strftime("%Y-%m-%d %H:%M:%S")
            else:
                publish_date = "Unknown"

            new_articles.append({
                "title": article.title,
                "published_at": publish_date,
                "url": url,
                "content": article.text,
            })

        except Exception as e:
            print(f"Failed to process {url}: {e}")

    total_articles = scraped_articles + new_articles

    # Save updated list
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(total_articles, f, indent=2, ensure_ascii=False)

    print(f"Scraping complete! Added {len(new_articles)} new articles. Total: {len(total_articles)}")

def scrapped_website_with_url(website, url_file, output_file):
    all_urls = scrape_urls(website)
    save_urls_to_json(all_urls, url_file)
    scrape_and_save_articles(url_file, output_file)
