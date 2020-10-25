from rest_framework import serializers

from .models import SentimentReview


class SentimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SentimentReview
        fields = ("id", "review_name", "review_text", "sentiment")
