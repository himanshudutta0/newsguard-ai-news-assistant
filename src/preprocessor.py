import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import json
import os

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Load spaCy's English model
nlp = spacy.load("en_core_web_sm")

# Preprocessing function
def preprocess_text(text):
    try:
        text = re.sub(r"http\S+|www\S+|https\S+", "", text)
        text = text.lower()
        tokens = word_tokenize(text)
        stop_words = set(stopwords.words('english'))
        tokens = [word for word in tokens if word not in stop_words and word.isalnum()]
        doc = nlp(' '.join(tokens))
        lemmatized_tokens = [token.lemma_ for token in doc]
        return ' '.join(lemmatized_tokens)
    except Exception as e:
        print(f"Error during text preprocessing: {e}")
        return ""

def preprocess_and_save_articles(input_file, output_file):
    print("Preprocessing...")

    # Load raw articles
    try:
        with open(input_file, 'r') as file:
            raw_articles = json.load(file)
    except FileNotFoundError:
        print(f"Error: The file {input_file} does not exist.")
        return
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from the file {input_file}.")
        return

    # Load already processed articles (if any)
    existing_articles = []
    existing_urls = set()
    if os.path.exists(output_file):
        try:
            with open(output_file, 'r') as outfile:
                existing_articles = json.load(outfile)
                existing_urls = {article['url'] for article in existing_articles}
        except Exception as e:
            print(f"Warning: Couldn't load existing processed articles: {e}")

    new_articles = []

    for article in raw_articles:
        try:
            url = article.get('url', '')
            if url in existing_urls:
                continue  # Skip already processed
            processed_content = preprocess_text(article['content'])
            new_articles.append({
                'title': article.get('title', ''),
                'processed_content': processed_content,
                'url': url
            })
        except KeyError as e:
            print(f"Error: Missing key {e} in article data.")

    if new_articles:
        all_articles = existing_articles + new_articles
        try:
            with open(output_file, 'w') as outfile:
                json.dump(all_articles, outfile, indent=4)
            print(f"Added {len(new_articles)} new articles. Preprocessing complete!")
        except Exception as e:
            print(f"Error saving processed articles to {output_file}: {e}")
    else:
        print("No new articles to preprocess.")

# Example usage
# preprocess_and_save_articles('data/raw_articles.json', 'data/preprocessed.json')
