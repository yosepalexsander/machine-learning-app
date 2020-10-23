from django.urls import re_path, path, include
from natural_language_processing import views as nlp_views
from rest_framework import routers

router = routers.DefaultRouter()
router.register("Review_API", nlp_views.SentimentView)
urlpatterns = [
    path("api/", include(router.urls)),
    re_path(r"^api/review$", nlp_views.review, name="review list"),
]
