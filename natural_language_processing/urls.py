from django.urls import re_path

from natural_language_processing import views as nlp_views

urlpatterns = [
    re_path(r"^api/Review_API$", nlp_views.review, name="review list"),
]
