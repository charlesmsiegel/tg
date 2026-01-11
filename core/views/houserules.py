from typing import Any

from django.views.generic import CreateView, DetailView, ListView, UpdateView

from core.mixins import MessageMixin
from core.models import HouseRule


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


class HouseRuleDetailView(DetailView):
    model = HouseRule
    template_name = "core/houserules/detail.html"


class HouseRuleCreateView(MessageMixin, CreateView):
    model = HouseRule
    fields = ["name", "description", "chronicle", "gameline"]
    template_name = "core/houserules/form.html"
    success_message = "House rule created successfully."
    error_message = "Error creating house rule."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update({"placeholder": "Enter description here"})
        return form


class HouseRuleUpdateView(MessageMixin, UpdateView):
    model = HouseRule
    fields = ["name", "description", "chronicle", "gameline"]
    template_name = "core/houserules/form.html"
    success_message = "House rule updated successfully."
    error_message = "Error updating house rule."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update({"placeholder": "Enter description here"})
        return form
