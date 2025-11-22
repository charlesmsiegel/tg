from typing import Any

from core.mixins import EditPermissionMixin, ViewPermissionMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView, UpdateView
from django.views.generic.edit import FormView
from locations.forms.mage.paradox_realm import ParadoxRealmForm
from locations.models.mage import ParadoxRealm, ParadoxObstacle, ParadoxAtmosphere


class ParadoxRealmDetailView(ViewPermissionMixin, DetailView):
    model = ParadoxRealm
    template_name = "locations/mage/paradox_realm/detail.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["obstacles"] = ParadoxObstacle.objects.filter(
            realm=self.object
        ).order_by("order")
        context["atmospheres"] = ParadoxAtmosphere.objects.filter(
            realm=self.object
        )
        return context


class ParadoxRealmListView(ListView):
    model = ParadoxRealm
    ordering = ["name"]
    template_name = "locations/mage/paradox_realm/list.html"


class ParadoxRealmCreateView(LoginRequiredMixin, FormView):
    template_name = "locations/mage/paradox_realm/form.html"
    form_class = ParadoxRealmForm
    success_message = "Paradox Realm '{name}' created successfully!"
    error_message = "Failed to create paradox realm. Please correct the errors below."

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class ParadoxRealmUpdateView(EditPermissionMixin, FormView):
    model = ParadoxRealm
    template_name = "locations/mage/paradox_realm/form.html"
    form_class = ParadoxRealmForm
    success_message = "Paradox Realm '{name}' updated successfully!"
    error_message = "Failed to update paradox realm. Please correct the errors below."

    def get_object(self):
        return ParadoxRealm.objects.get(pk=self.kwargs['pk'])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()
