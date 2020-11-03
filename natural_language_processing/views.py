from django.http import HttpResponseRedirect
from django.contrib import messages
from rest_framework.parsers import FormParser
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, parser_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import status
from .preprocess import predict
from .models import SentimentReview
from .serializers import SentimentSerializer

# Create your views here.


@api_view(["GET", "POST", "DELETE"])
@parser_classes([FormParser])
@renderer_classes([TemplateHTMLRenderer])
def sentiment_analysis(request):
    if request.method == "GET":
        reviews = SentimentReview.objects.all()
        name = request.query_params.get("review_name", None)
        if name is not None:
            reviews = reviews.filter(reviewname__icontains=name)

        sentiment_serializer = SentimentSerializer(reviews, many=True)

        return Response(
            {"sentiments": sentiment_serializer.data},
            template_name="nlp/sentiment_analysis.html",
            status=status.HTTP_200_OK,
        )

    elif request.method == "POST":
        data = (request.POST).dict()
        review_text = data["review_text"]
        predict_result = predict(review_text)
        data["sentiment"] = predict_result
        if predict_result == "Positive":
            messages.success(request, f"{predict_result}")
        else:
            messages.error(request, f"{predict_result}")
        serializer = SentimentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponseRedirect("/nlp/sentiment-analysis")
        return Response(
            template_name="nlp/sentiment_analysis.html",
            status=status.HTTP_201_CREATED,
        )
    elif request.method == "DELETE":
        deleted = SentimentReview.objects.all().delete()
        return Response(
            {"messages": f"Total {deleted[0]} was successfully deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )
