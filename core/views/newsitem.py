from django.views.generic import CreateView, DetailView, ListView, UpdateView

from core.mixins import MessageMixin
from core.models import NewsItem


class NewsItemDetailView(DetailView):
    model = NewsItem
    template_name = "core/newsitem/detail.html"


class NewsItemListView(ListView):
    model = NewsItem
    ordering = ["-date"]
    template_name = "core/newsitem/list.html"


class NewsItemCreateView(MessageMixin, CreateView):
    model = NewsItem
    fields = ["title", "content", "date"]
    template_name = "core/newsitem/form.html"
    success_message = "News item created successfully."
    error_message = "Error creating news item."


class NewsItemUpdateView(MessageMixin, UpdateView):
    model = NewsItem
    fields = ["title", "content", "date"]
    template_name = "core/newsitem/form.html"
    success_message = "News item updated successfully."
    error_message = "Error updating news item."
