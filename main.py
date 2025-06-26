from src.scraper import scrapped_website_with_url
from src.preprocessor import preprocess_and_save_articles
from src.ner import extract_entities_and_save
from src.topic_classifier import predict_topics_and_save
from src.topic_modeler import assign_topics_with_nmf_and_save
from src.summarizer import summarize_articles
from src.sentiment_and_bias import sentiment_bias_analyze_and_save

if __name__ == "__main__":

    # scrapping articles from urls
    scrapped_website_with_url("https://www.thehindu.com/news/", "urls/urls.json", "data/scrapped.json")

    # preprocessing
    preprocess_and_save_articles("data/scrapped.json", "data/preprocessed.json")

    # name entity recognition
    extract_entities_and_save('data/preprocessed.json', 'data/entities.json')

    # topic predicting
    predict_topics_and_save(
        input_file='data/preprocessed.json',
        output_file='data/topic_predicted.json',
        model_file='models/news_classifier_model.pkl',
        vectorizer_file='models/news_classifier_tfidf_vectorizer.pkl'
    )

    # topic modeling
    assign_topics_with_nmf_and_save("data/preprocessed.json", "data/topic_modeled.json")

    # summarizer
    summarize_articles("data/scrapped.json", "data/summarized.json")

    # sentiment and bias
    sentiment_bias_analyze_and_save("data/scrapped.json", "data/sentiment_bias.json")

