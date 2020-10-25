from django.contrib import admin
from django.urls import re_path, include

urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^api/", include("blog.urls")),
    re_path(r"^api/", include("natural_language_processing.urls")),
]
