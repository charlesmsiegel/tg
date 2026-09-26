from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic.edit import FormView

from core.mixins import EditPermissionMixin, ViewPermissionMixin, prepare_created_object
from locations.models.mage import ParadoxAtmosphere, ParadoxObstacle, ParadoxRealm
from locations.registry import registry


class _ParadoxRealmDetailView(ViewPermissionMixin, DetailView):

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["obstacles"] = ParadoxObstacle.objects.filter(realm=self.object).order_by("order")
        context["atmospheres"] = ParadoxAtmosphere.objects.filter(realm=self.object)
        return context


ParadoxRealmDetailView = registry.view("locations.ParadoxRealm", "detail")


class _ParadoxRealmCreateView(LoginRequiredMixin, FormView):

    def form_valid(self, form):
        prepare_created_object(form, self.request)
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


ParadoxRealmCreateView = registry.view("locations.ParadoxRealm", "create")


class _ParadoxRealmUpdateView(EditPermissionMixin, FormView):

    def get_object(self):
        return ParadoxRealm.objects.get(pk=self.kwargs["pk"])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.get_object()
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


ParadoxRealmUpdateView = registry.view("locations.ParadoxRealm", "update")


ParadoxRealmListView = registry.view("locations.ParadoxRealm", "list")
