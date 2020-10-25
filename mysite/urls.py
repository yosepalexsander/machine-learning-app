from django.contrib import admin
from django.urls import re_path, include

urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^", include("blog.urls")),
    re_path(r"^", include("natural_language_processing.urls")),
]
