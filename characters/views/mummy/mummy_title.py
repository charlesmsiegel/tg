from characters.models.mummy.mummy_title import MummyTitle
from django.views.generic import DetailView


class MummyTitleDetailView(DetailView):
    model = MummyTitle
    template_name = "characters/mummy/title/detail.html"
