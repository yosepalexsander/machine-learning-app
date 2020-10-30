from django.urls import re_path

from natural_language_processing import views as nlp_views

urlpatterns = [
    re_path(r"sentiment-review/$", nlp_views.review_form, name="review form"),
    # re_path(r"sentiment-reviews/$", nlp_views.reviews, name="sentiment reviews")
]
