from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView

from core.mixins import (
    MessageMixin,
    prepare_created_object,
)
from locations.registry import registry


class _DemesneCreateView(LoginRequiredMixin, MessageMixin, FormView):

    def form_valid(self, form):
        prepare_created_object(form, self.request)
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


DemesneCreateView = registry.view("locations.Demesne", "create")


DemesneDetailView = registry.view("locations.Demesne", "detail")
DemesneListView = registry.view("locations.Demesne", "list")
DemesneUpdateView = registry.view("locations.Demesne", "update")
