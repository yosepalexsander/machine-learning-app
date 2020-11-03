from django.urls import re_path

from natural_language_processing import views as nlp_views

urlpatterns = [
    re_path(
        r"sentiment-analysis/$", nlp_views.sentiment_analysis, name="sentiment_analysis"
    ),
    # re_path(r"sentiment-reviews/$", nlp_views.reviews, name="sentiment reviews")
]
