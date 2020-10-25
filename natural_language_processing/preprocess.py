import string
import re
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from pathlib import Path

# lemmatizer = WordNetLemmatizer()
translation_table = dict.fromkeys(map(ord, string.punctuation), " ")

# model file path

BASE_PATH = Path(__file__).resolve().parent
MODEL_PATH = Path(BASE_PATH, "nlp_model", "sentiment_model.h5")
TOKENIZER_PATH = Path(BASE_PATH, "nlp_model", "tokenizer.pickle")


def clean_text(text):
    """
    text: a string

    return: modified initial string
    """

    text = text.lower()
    text = text.translate(translation_table)
    text = re.sub(r"[^\x00-\x7F]+", "", text)  # remove non-ascii
    text = re.sub(r"\d+", "", text)
    # tokenize = word_tokenize(text)
    # filtered_token = [
    #     lemmatizer.lemmatize(word)
    #     for word in tokenize
    #     if word not in set(stopwords.words("english"))
    # ]
    # text = " ".join(filtered_token)

    return text


def load_tokenizer(file_path):
    with open(file_path, "rb") as handle:
        tokenizer = pickle.load(handle)

    return tokenizer


def predict(data):
    try:
        model = load_model(MODEL_PATH)
        tokenizer = load_tokenizer(TOKENIZER_PATH)

        cleaned_data = clean_text(data)
        sequences = tokenizer.texts_to_sequences([cleaned_data])
        padded_sequences = pad_sequences(sequences)
        predict_result = (model.predict(padded_sequences) > 0.5).astype("int32")
        if predict_result == 1:
            return "Positive"
        else:
            return "Negative"
    except ValueError as e:
        return e.args[0]
