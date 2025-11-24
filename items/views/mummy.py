from django.views.generic import DetailView

from items.models.mummy.relic import MummyRelic
from items.models.mummy.ushabti import Ushabti
from items.models.mummy.vessel import Vessel


class MummyRelicDetailView(DetailView):
    model = MummyRelic
    template_name = "items/mummy/relic/detail.html"


class VesselDetailView(DetailView):
    model = Vessel
    template_name = "items/mummy/vessel/detail.html"


class UshabtiDetailView(DetailView):
    model = Ushabti
    template_name = "items/mummy/ushabti/detail.html"
