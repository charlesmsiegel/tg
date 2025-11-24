from typing import Any

from characters.models.mummy.mummy import Mummy
from characters.views.core.human import HumanDetailView
from core.mixins import ApprovedUserContextMixin


class MummyDetailView(ApprovedUserContextMixin, HumanDetailView):
    model = Mummy
    template_name = "characters/mummy/mummy/detail.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["hekau"] = self.object.get_hekau()
        if self.object.dynasty:
            context["dynasty"] = self.object.dynasty
        return context
