from django.views.generic import DetailView

from locations.models.mummy.cult_temple import CultTemple
from locations.models.mummy.sanctuary import UndergroundSanctuary
from locations.models.mummy.tomb import Tomb


class TombDetailView(DetailView):
    model = Tomb
    template_name = "locations/mummy/tomb/detail.html"


class CultTempleDetailView(DetailView):
    model = CultTemple
    template_name = "locations/mummy/cult_temple/detail.html"


class UndergroundSanctuaryDetailView(DetailView):
    model = UndergroundSanctuary
    template_name = "locations/mummy/sanctuary/detail.html"
