# app.py

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from flask import Flask, render_template, request

app = Flask(__name__)

# Load NLTK data
nltk.download("vader_lexicon")
nltk.download("stopwords")
nltk.download("punkt")
nltk.download("punkt_tab")

# Initialize sentiment analyzer
sia = SentimentIntensityAnalyzer()


# Function to detect fake news
def detect_fake_news(text):
    # Tokenize text
    tokens = word_tokenize(text)

    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    tokens = [t for t in tokens if t.lower() not in stop_words]

    # Analyze sentiment
    sentiment = sia.polarity_scores(" ".join(tokens))

    # Determine fake news probability
    if sentiment["compound"] < -0.5:
        return "Fake News", 0.8
    elif sentiment["compound"] > 0.5:
        return "Real News", 0.8
    else:
        return "Unknown", 0.5


# Route for index page
@app.route("/")
def index():
    return render_template("index.html")


# Route for fake news detection
@app.route("/detect", methods=["POST"])
def detect():
    text = request.form["text"]
    result, confidence = detect_fake_news(text)
    return render_template("result.html", result=result, confidence=confidence)


if __name__ == "__main__":
    app.run(debug=True)
