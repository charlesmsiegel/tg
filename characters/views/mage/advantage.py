from django.views.generic import DetailView

from characters.models.mage.companion import Advantage
from characters.views.core.known_by import KnownByMixin


class AdvantageDetailView(KnownByMixin, DetailView):
    model = Advantage
    template_name = "characters/mage/advantage/detail.html"
