import string
import re
import pickle
from pathlib import Path

# lemmatizer = WordNetLemmatizer()
translation_table = dict.fromkeys(map(ord, string.punctuation), " ")

# model file path
BASE_PATH = Path(__file__).resolve().parent
MODEL_PATH = Path(BASE_PATH, "nlp_model", "NaiveBayes.pickle")
VECTORIZER_PATH = Path(BASE_PATH, "nlp_model", "Tfidf.pickle")


def clean_text(text):
    """
    text: a string

    return: modified initial string
    """

    text = text.lower()
    text = text.translate(translation_table)  # remove non-ascii
    text = re.sub(r"\d+", "", text)

    return text


def load_tokenizer(file_path):
    with open(file_path, "rb") as handle:
        vectorizer = pickle.load(handle)

    return vectorizer


def load_model(file_path):
    with open(file_path, "rb") as handle:
        model = pickle.load(handle)

    return model


def predict(data):
    try:
        model = load_model(MODEL_PATH)
        vectorizer = load_tokenizer(VECTORIZER_PATH)
        cleaned_data = clean_text(data)
        sequences = vectorizer.transform([cleaned_data])
        predict_result = model.predict(sequences)[0]
        if predict_result == 1:
            return "Positive"
        else:
            return "Negative"
    except ValueError as e:
        return e.args[0]
