# from django.views.generic import TemplateView

# from django.views.decorators.cache import never_cache

# # Serve Single Page Application
# Index = never_cache(TemplateView.as_view(template_name="base.html"))

from django.views.generic.base import TemplateView


class Index(TemplateView):
    template_name = "base.html"


class About(TemplateView):
    template_name = "about.html"
