from typing import Any

from core.models import HouseRule
from django.views.generic import ListView


class HouseRulesIndexView(ListView):
    model = HouseRule
    template_name = "core/houserules/index.html"

    def get_context_data(self) -> dict[str, Any]:
        context = super().get_context_data()
        if self.request.user.is_authenticated:
            context["header"] = self.request.user.profile.preferred_heading
        else:
            context["header"] = "wod_heading"
        return context
