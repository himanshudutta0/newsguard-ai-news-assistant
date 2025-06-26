import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from transformers import BertTokenizer, BertForSequenceClassification
import torch

# Initialize VADER Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# Load pre-trained BERT model and tokenizer (fine-tuned for bias detection)
model_name = "bert-base-uncased"  # Replace with your fine-tuned model path
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)


def analyze_sentiment(text):
    sentiment = analyzer.polarity_scores(text)
    return sentiment


def analyze_sentiment_textblob(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment
    return sentiment


def detect_bias(text):
    # Tokenize the input text
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)

    # Make prediction with the model
    with torch.no_grad():
        outputs = model(**inputs)

    # Get the predicted label (bias class) and logits
    logits = outputs.logits
    bias_label = torch.argmax(logits, dim=1).item()  # 0: No Bias, 1: Bias
    bias_confidence = torch.nn.functional.softmax(logits, dim=1)[0][bias_label].item()

    return bias_label, bias_confidence, logits


def process_article(article):
    text = article.get('content', '')  # Ensure the content is there

    # Sentiment analysis using both VADER and TextBlob
    sentiment_vader = analyze_sentiment(text)
    sentiment_textblob = analyze_sentiment_textblob(text)

    # Bias detection
    bias_label, bias_confidence, logits = detect_bias(text)

    # Create a detailed result dictionary with sentiment and bias info
    result = {
        "title": article.get('title', ''),
        "date": article.get('published_at', ''),

        # Sentiment details (VADER and TextBlob)
        "sentiment_vader": {
            "positive": sentiment_vader.get('pos', 0),
            "neutral": sentiment_vader.get('neu', 0),
            "negative": sentiment_vader.get('neg', 0),
            "compound": sentiment_vader.get('compound', 0)
        },
        "sentiment_textblob": {
            "polarity": sentiment_textblob.polarity,
            "subjectivity": sentiment_textblob.subjectivity
        },

        # Bias detection details
        "bias": {
            "label": "Bias" if bias_label == 1 else "No Bias",
            "confidence": bias_confidence,
            "logits": logits.tolist()  # Include the logits for debugging
        }
    }

    return result


def sentiment_bias_analyze_and_save(input_file, output_file):
    # Load the scraped articles
    with open(input_file, 'r') as f:
        scraped_articles = json.load(f)

    # Process each article and analyze sentiment and bias
    results = []
    for article in scraped_articles:
        result = process_article(article)
        results.append(result)

    # Save the results to sentiment_and_bias.json
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4)

    print(f"Sentiment and bias data saved to {output_file}")
