from django.views.generic import DetailView

from characters.models.mage.companion import Advantage


class AdvantageDetailView(DetailView):
    model = Advantage
    template_name = "characters/mage/advantage/detail.html"
