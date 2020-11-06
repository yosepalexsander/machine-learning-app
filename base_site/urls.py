from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import re_path, include
from django.views.generic.base import RedirectView
from .views import index, About

urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
    re_path(
        r"^nlp/", include(("natural_language_processing.urls", "nlp"), namespace="nlp")
    ),
    re_path(r"^$", index, name="index"),
    re_path(r"^about/$", About.as_view(), name="about"),
    re_path(
        r"^favicon.ico",
        RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")),
    ),
]
