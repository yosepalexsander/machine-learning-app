from django.shortcuts import redirect, get_object_or_404
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.decorators import api_view, parser_classes, renderer_classes
from rest_framework import status
from .preprocess import predict
from .models import SentimentReview
from .serializers import SentimentSerializer

# Create your views here.


@api_view(["GET", "POST"])
@parser_classes([FormParser])
@renderer_classes([TemplateHTMLRenderer])
def review_form(request, pk):
    if request.method == "GET":
        review = get_object_or_404(SentimentReview, pk=pk)
        serializer = SentimentSerializer(review)
        return Response(
            {"serializer": serializer, "review": review},
            template_name="nlp__review_form.html",
        )

    elif request.method == "POST":
        review = get_object_or_404(SentimentReview, pk=pk)
        review_data = request.data
        predicted_sentiment = predict(review_data["review_text"])
        review_data["sentiment"] = predicted_sentiment
        print(review_data)
        sentiment_serializer = SentimentSerializer(review, data=review_data)
        if not sentiment_serializer.is_valid():
            return Response(
                {"serializer": sentiment_serializer, "review": review},
                status=status.HTTP_400_BAD_REQUEST,
            )
        sentiment_serializer.save()
        return redirect("/nlp/review-list")


@api_view(["GET"])
@parser_classes([FormParser])
@renderer_classes([TemplateHTMLRenderer])
def review_list(request):
    if request.method == "GET":
        reviews = SentimentReview.objects.all()
        name = request.query_params.get("review_name", None)
        if name is not None:
            reviews = reviews.filter(reviewname__icontains=name)

        sentiment_serializer = SentimentSerializer(reviews, many=True)
        return Response(
            {"sentiments": sentiment_serializer.data},
            template_name="nlp__review_list.html",
            status=status.HTTP_200_OK,
        )
