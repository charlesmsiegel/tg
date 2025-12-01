from core.models import NewsItem
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import ListView


@method_decorator(cache_page(60 * 5), name="dispatch")  # Cache for 5 minutes
class HomeListView(ListView):
    model = NewsItem
    template_name = "core/index.html"
    context_object_name = "news"
    ordering = ["-date"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context
