from django.contrib import admin
from django.urls import re_path, include
from .views import index, About

urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
    re_path(
        r"^nlp/", include(("natural_language_processing.urls", "nlp"), namespace="nlp")
    ),
    re_path(r"^$", index, name="index"),
    re_path(r"^about/$", About.as_view(), name="about"),
]
