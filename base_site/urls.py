from django.contrib import admin
from django.urls import re_path, include
from .views import index

urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^blog/", include("blog.urls")),
    re_path(r"^nlp/", include("natural_language_processing.urls")),
    re_path(r"^$", index, name="index"),
]
