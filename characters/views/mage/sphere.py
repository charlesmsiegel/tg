from django.views.generic import CreateView, UpdateView

from characters.models.mage import Sphere
from core.mixins import MessageMixin
from core.views import CachedDetailView, CachedListView


class SphereDetailView(CachedDetailView):
    model = Sphere
    template_name = "characters/mage/sphere/detail.html"


class SphereCreateView(MessageMixin, CreateView):
    model = Sphere
    fields = ["name", "property_name"]
    template_name = "characters/mage/sphere/form.html"
    success_message = "Sphere created successfully."
    error_message = "There was an error creating the Sphere."


class SphereUpdateView(MessageMixin, UpdateView):
    model = Sphere
    fields = ["name", "property_name"]
    template_name = "characters/mage/sphere/form.html"
    success_message = "Sphere updated successfully."
    error_message = "There was an error updating the Sphere."


class SphereListView(CachedListView):
    model = Sphere
    ordering = ["name"]
    template_name = "characters/mage/sphere/list.html"
