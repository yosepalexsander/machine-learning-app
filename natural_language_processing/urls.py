from django.urls import re_path

from natural_language_processing import views as nlp_views

urlpatterns = [
    re_path(r"review-form/$", nlp_views.review_form, name="review form"),
    re_path(r"review-list/$", nlp_views.review_list, name="review list"),
]
