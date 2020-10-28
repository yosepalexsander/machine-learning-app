from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, parser_classes, renderer_classes
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer

# from sklearn.feature_extraction.text import TfidfVectorizer

# Create your views here.
from .preprocess import predict
from .models import SentimentReview
from .serializers import SentimentSerializer

# from .form import ReviewForm


@api_view(["GET", "POST", "DELETE"])
@parser_classes([JSONParser])
@renderer_classes([TemplateHTMLRenderer])
def review(request):
    if request.method == "GET":
        reviews = SentimentReview.objects.all()
        name = request.query_params.get("review_name", None)
        if name is not None:
            reviews = reviews.filter(reviewname__icontains=name)

        sentiment_serializer = SentimentSerializer(reviews, many=True)
        return Response(
            {"sentiments": sentiment_serializer.data},
            template_name="nlp_form.html",
            status=status.HTTP_200_OK,
        )

    elif request.method == "POST":
        review_data = request.data
        predicted_sentiment = predict(review_data["review_text"])
        review_data["sentiment"] = predicted_sentiment
        print(review_data)
        sentiment_serializer = SentimentSerializer(data=review_data)
        if sentiment_serializer.is_valid():
            sentiment_serializer.save()
            return Response(
                {review_data},
                template_name="nlp_form.html",
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"error": sentiment_serializer.errors},
            template_name="nlp_form.html",
            status=status.HTTP_400_BAD_REQUEST,
        )

    elif request.method == "DELETE":
        total_deleted = SentimentReview.objects.all().delete()
        return Response(
            {"message": f"{total_deleted[0]} Reviews were deleted successfully!"},
            status.HTTP_204_NO_CONTENT,
        )


# def review_form(request):
#     form = ReviewForm(request.POST)
#     if form.is_valid():
#         review_name = form.cleaned_data['review_name']
#         review_text = form.cleaned_data['review_text']
#         result = predict(review_text)

#         messages.succes(request, f"Sentiment for reviews is: {result}")
#       form = ReviewForm()

#     return Response({'form': form}, template_name="nlp_form.html")
