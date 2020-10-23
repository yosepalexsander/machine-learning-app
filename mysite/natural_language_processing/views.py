from sklearn.externals import joblib

# import numpy as np
# import pandas as pd
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework import status, viewsets

# from sklearn.feature_extraction.text import TfidfVectorizer

# Create your views here.
from .preprocess import clean_text
from .models import SentimentModel
from .serializers import SentimentSerializer


class SentimentView(viewsets.ModelViewSet):
    queryset = SentimentModel.objects.all()
    serializer_class = SentimentSerializer


@api_view(["GET", "POST", "DELETE"])
def review(request):
    if request.method == "GET":
        reviews = SentimentModel.objects.all()
        name = request.query_params.get("reviewname", None)
        if name is not None:
            reviews = reviews.filter(reviewname__icontains=name)

        sentiment_serializer = SentimentSerializer(reviews, many=True)
        return Response(sentiment_serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        review_data = JSONParser().parse(request)
        sentiment_serializer = SentimentSerializer(data=review_data)
        if sentiment_serializer.is_valid():
            predicted_sentiment = sentiment(review_data)
            sentiment_serializer.save()
            return Response(predicted_sentiment, status=status.HTTP_202_ACCEPTED)
        return Response(sentiment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        total_deleted = SentimentModel.objects.all().delete()
        return Response(
            {"message": f"{total_deleted[0]} Reviews were deleted successfully!"},
            status.HTTP_204_NO_CONTENT,
        )


def sentiment(data):
    try:
        vectorizer = joblib.load(
            open(
                "C:\\Users\\USER\\web-app\\mysite\\natural_language_processing\\nlp_model\\Vectorizer.pickle"
            )
        )
        model = joblib.load(
            open(
                "C:\\Users\\USER\\web-app\\mysite\\natural_language_processing\\nlp_model\\LogisticRegression.pickle"
            )
        )
        review_name = data["reviewname"]
        cleaned_data = clean_text(data["reviewtext"])
        features = vectorizer.transform([cleaned_data])
        predicted = model.predict(features)
        if predicted == 1:
            sentiment = "Positive"
            return {"name": review_name, "sentiment": sentiment}
        else:
            sentiment = "Negative"
            return {"name": review_name, "sentiment": sentiment}
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)
