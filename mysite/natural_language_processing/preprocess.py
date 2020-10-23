import string
import re

# lemmatizer = WordNetLemmatizer()
translation_table = dict.fromkeys(map(ord, string.punctuation), " ")


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
