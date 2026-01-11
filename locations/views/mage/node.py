from typing import Any

from core.mixins import EditPermissionMixin, MessageMixin, ViewPermissionMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView, UpdateView
from django.views.generic.edit import FormView
from locations.forms.mage.node import NodeForm
from locations.models.mage import Node, NodeMeritFlawRating, NodeResonanceRating


class NodeDetailView(ViewPermissionMixin, DetailView):
    model = Node
    template_name = "locations/mage/node/detail.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["resonance"] = (
            NodeResonanceRating.objects.filter(node=self.object)
            .select_related("resonance")
            .order_by("resonance__name")
        )
        context["merits_and_flaws"] = (
            NodeMeritFlawRating.objects.filter(node=self.object)
            .select_related("mf")
            .order_by("mf__name")
        )
        return context


class NodeListView(ListView):
    model = Node
    ordering = ["name"]
    template_name = "locations/mage/node/list.html"


class NodeCreateView(LoginRequiredMixin, MessageMixin, FormView):
    template_name = "locations/mage/node/form.html"
    form_class = NodeForm
    success_message = "Node '{name}' created successfully!"
    error_message = "Failed to create node. Please correct the errors below."

    def form_valid(self, form):
        self.object = form.save()
        return super(NodeCreateView, self).form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class NodeUpdateView(EditPermissionMixin, MessageMixin, UpdateView):
    model = Node
    form_class = NodeForm
    template_name = "locations/mage/node/form.html"
    success_message = "Node '{name}' updated successfully!"
    error_message = "Failed to update node. Please correct the errors below."
