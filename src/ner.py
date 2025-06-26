import spacy
import json
import os
from collections import defaultdict

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")


def extract_named_entities(text):
    doc = nlp(text)
    entities = defaultdict(list)
    for ent in doc.ents:
        entities[ent.label_].append(ent.text)
    return entities


def extract_entities_and_save(input_file, output_file):
    print("Extracting Named Entities")

    # Load preprocessed articles
    with open(input_file, 'r', encoding='utf-8') as infile:
        articles = json.load(infile)

    # Load already processed NER results (if exists)
    ner_results = []
    processed_urls = set()

    if os.path.exists(output_file):
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                ner_results = json.load(f)
                processed_urls = {entry['url'] for entry in ner_results}
        except Exception as e:
            print(f"Warning: Could not load existing NER file: {e}")

    new_ner_results = []

    for article in articles:
        url = article.get('url', '')
        if not url or url in processed_urls:
            continue

        content = article.get('processed_content', '')
        if not content:
            continue

        entities = extract_named_entities(content)

        article_entities = {
            'title': article.get('title', ''),
            'url': url,
            'PERSON': entities.get('PERSON', []),
            'ORG': entities.get('ORG', []),
            'GPE': entities.get('GPE', []),
            'DATE': entities.get('DATE', []),
            'MONEY': entities.get('MONEY', []),
            'LOC': entities.get('LOC', []),
            'EVENT': entities.get('EVENT', [])
        }

        new_ner_results.append(article_entities)

    # Combine old and new results
    ner_results += new_ner_results

    # Save updated results
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(ner_results, outfile, indent=4)

    print(f"Entities Extracted and Saved: {len(new_ner_results)} new articles processed")
