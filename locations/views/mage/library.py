from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView

from core.mixins import (
    MessageMixin,
    prepare_created_object,
)
from locations.registry import registry


class _LibraryCreateView(LoginRequiredMixin, MessageMixin, FormView):

    def form_valid(self, form):
        prepare_created_object(form, self.request)
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


LibraryCreateView = registry.view("locations.Library", "create")


LibraryDetailView = registry.view("locations.Library", "detail")
LibraryListView = registry.view("locations.Library", "list")
LibraryUpdateView = registry.view("locations.Library", "update")
