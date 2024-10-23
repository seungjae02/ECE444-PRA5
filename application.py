from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle
from flask import Flask, render_template, request
import logging
import time

application = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@application.route("/")
def index():
    return render_template("index.html")
    
@application.route("/check", methods=["POST"])
def check_text():
    for _ in range(100):
        start_time = time.time()

        loaded_model = None
        with open('basic_classifier.pkl', 'rb') as fid:
            loaded_model = pickle.load(fid)

        vectorizer = None
        with open('count_vectorizer.pkl', 'rb') as vd:
            vectorizer = pickle.load(vd)
        # predict fake news
        text_input = request.form["text"]
        prediction = loaded_model.predict(vectorizer.transform([text_input]))[0]

        end_time = time.time()
        delta = end_time - start_time

        application.logger.info(delta)

    return render_template("index.html", prediction=(prediction == 'FAKE'))

if __name__ == "__main__":
    application.run(port=5000, debug=True)