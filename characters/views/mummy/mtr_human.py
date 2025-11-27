from typing import Any

from characters.models.mummy.mtr_human import MtRHuman
from characters.views.core.human import HumanDetailView


class MtRHumanDetailView(HumanDetailView):
    model = MtRHuman
    template_name = "characters/mummy/mtrhuman/detail.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context
