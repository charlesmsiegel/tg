from typing import Any

from django.conf import settings
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from core.mixins import MessageMixin
from core.models import HouseRule


def group_rules_by_gameline(rules):
    """[{"code", "label", "rules"}] in settings.GAMELINES order, rules for all lines first.

    Gamelines with no rules are left out; each group keeps the order it was given.
    """
    groups = {code: [] for code in settings.GAMELINES}
    for rule in rules:
        groups.setdefault(rule.gameline, []).append(rule)
    return [
        {
            "code": code,
            "label": (
                "All lines"
                if code == "wod"
                else settings.GAMELINES.get(code, {}).get("name", code).split(":")[0]
            ),
            "rules": rules_for_line,
        }
        for code, rules_for_line in groups.items()
        if rules_for_line
    ]


class HouseRulesIndexView(ListView):
    model = HouseRule
    template_name = "core/houserules/index.html"

    def get_queryset(self):
        return (
            HouseRule.objects.select_related("chronicle")
            .prefetch_related("sources__book")
            .order_by("name")
        )

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["header"] = self.request.user.profile.preferred_heading
        else:
            context["header"] = "wod_heading"
        context["rule_groups"] = group_rules_by_gameline(context["object_list"])
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
