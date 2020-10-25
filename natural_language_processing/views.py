# import numpy as np
# import pandas as pd
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, parser_classes
from rest_framework import status

# from sklearn.feature_extraction.text import TfidfVectorizer

# Create your views here.
from .preprocess import predict

from .models import SentimentReview
from .serializers import SentimentSerializer


@api_view(["GET", "POST", "DELETE"])
@parser_classes([JSONParser])
def review(request):
    if request.method == "GET":
        reviews = SentimentReview.objects.all()
        name = request.query_params.get("review_name", None)
        if name is not None:
            reviews = reviews.filter(reviewname__icontains=name)

        Sentiment_serializer = SentimentSerializer(reviews, many=True)
        return Response(Sentiment_serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        review_data = request.data
        predicted_sentiment = predict(review_data["review_text"])
        review_data["sentiment"] = predicted_sentiment
        print(review_data)
        sentiment_serializer = SentimentSerializer(data=review_data)
        if sentiment_serializer.is_valid():
            sentiment_serializer.save()
            return Response(sentiment_serializer.data, status=status.HTTP_201_CREATED)
        return Response(sentiment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        total_deleted = SentimentReview.objects.all().delete()
        return Response(
            {"message": f"{total_deleted[0]} Reviews were deleted successfully!"},
            status.HTTP_204_NO_CONTENT,
        )
