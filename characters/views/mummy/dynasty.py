from characters.models.mummy.dynasty import Dynasty
from django.views.generic import DetailView


class DynastyDetailView(DetailView):
    model = Dynasty
    template_name = "characters/mummy/dynasty/detail.html"
