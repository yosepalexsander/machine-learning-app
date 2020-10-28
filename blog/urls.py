from django.urls import re_path
from blog import views as blog_views

urlpatterns = [
    re_path(r"^post/$", blog_views.post_list, name="post list"),
    re_path(r"^post/(?P<pk>[0-9]+)/$", blog_views.post_detail, name="post detail"),
]
