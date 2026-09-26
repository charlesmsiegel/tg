from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic.edit import FormView

from core.mixins import (
    MessageMixin,
    ViewPermissionMixin,
    prepare_created_object,
)
from locations.models.mage import NodeMeritFlawRating, NodeResonanceRating
from locations.registry import registry


class _NodeDetailView(ViewPermissionMixin, DetailView):

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


NodeDetailView = registry.view("locations.Node", "detail")


class _NodeCreateView(LoginRequiredMixin, MessageMixin, FormView):

    def form_valid(self, form):
        prepare_created_object(form, self.request)
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


NodeCreateView = registry.view("locations.Node", "create")


NodeListView = registry.view("locations.Node", "list")
NodeUpdateView = registry.view("locations.Node", "update")
