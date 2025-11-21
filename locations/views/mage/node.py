from typing import Any

from core.views.message_mixin import MessageMixin
from django.views.generic import DetailView, ListView, UpdateView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.mixins import ViewPermissionMixin, EditPermissionMixin
from locations.forms.mage.node import NodeForm
from locations.models.mage import Node, NodeMeritFlawRating, NodeResonanceRating


class NodeDetailView(ViewPermissionMixin, DetailView):
    model = Node
    template_name = "locations/mage/node/detail.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["resonance"] = NodeResonanceRating.objects.filter(
            node=self.object
        ).order_by("resonance__name")
        context["merits_and_flaws"] = NodeMeritFlawRating.objects.filter(
            node=self.object
        ).order_by("mf__name")
        return context


class NodeListView(ListView):
    model = Node
    ordering = ["name"]
    template_name = "locations/mage/node/list.html"


class NodeCreateView(LoginRequiredMixin, FormView):
    template_name = "locations/mage/node/form.html"
    form_class = NodeForm
    success_message = "Node '{name}' created successfully!"
    error_message = "Failed to create node. Please correct the errors below."

    def form_valid(self, form):
        self.object = form.save()
        return super(NodeCreateView, self).form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class NodeUpdateView(EditPermissionMixin, UpdateView):
    model = Node
    fields = [
        "name",
        "parent",
        "reality_zone",
        "description",
        "rank",
        "size",
        "quintessence_per_week",
        "quintessence_form",
        "tass_per_week",
        "tass_form",
        "merits_and_flaws",
        "resonance",
    ]
    template_name = "locations/mage/node/form.html"
    success_message = "Node '{name}' updated successfully!"
    error_message = "Failed to update node. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        return form
