import json
import joblib
import os

def predict_topics_and_save(input_file, output_file, model_file, vectorizer_file):
    print("Predicting Topics")

    class_names = ['unknown', 'World', 'Sports', 'Business', 'Sci/Technology']

    # Step 1: Load input articles
    with open(input_file, 'r', encoding='utf-8') as file:
        articles = json.load(file)

    # Step 2: Load existing predictions (if output file exists)
    existing_articles = []
    existing_urls = set()

    if os.path.exists(output_file):
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                existing_articles = json.load(f)
                existing_urls = {a['url'] for a in existing_articles}
        except Exception as e:
            print(f"Warning: Could not load existing topic predictions: {e}")

    # Step 3: Load model and vectorizer
    classifier = joblib.load(model_file)
    vectorizer = joblib.load(vectorizer_file)

    # Step 4: Predict topics for new articles
    new_predictions = []

    for article in articles:
        url = article.get('url', '')
        if not url or url in existing_urls:
            continue  # Skip already processed articles

        content = article.get('processed_content', '')
        if not content:
            continue

        content_vector = vectorizer.transform([content])
        predicted_topic_index = classifier.predict(content_vector)
        predicted_topic = class_names[int(predicted_topic_index[0])]

        article['predicted_topic'] = predicted_topic
        new_predictions.append(article)

    # Step 5: Combine old and new, then save
    all_articles = existing_articles + new_predictions

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(all_articles, file, indent=4)

    print(f"Predicted Successfully: {len(new_predictions)} new articles processed")
