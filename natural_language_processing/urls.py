from django.urls import re_path

from natural_language_processing import views as nlp_views

urlpatterns = [
    re_path(r"sentiment_review$", nlp_views.review, name="sentiment review"),
]
