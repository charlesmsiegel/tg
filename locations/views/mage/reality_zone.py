from core.views.message_mixin import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from locations.models.mage.reality_zone import RealityZone, ZoneRating


class RealityZoneDetailView(DetailView):
    model = RealityZone
    template_name = "locations/mage/reality_zone/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["positive_practices"] = ZoneRating.objects.filter(
            zone=self.object, rating__gt=0
        )
        context["negative_practices"] = ZoneRating.objects.filter(
            zone=self.object, rating__lt=0
        )
        return context


class RealityZoneCreateView(MessageMixin, CreateView):
    model = RealityZone
    fields = ["name", "description", "practices"]
    template_name = "locations/mage/reality_zone/form.html"
    success_message = "Reality Zone '{name}' created successfully!"
    error_message = "Failed to create reality zone. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        return form


class RealityZoneUpdateView(MessageMixin, UpdateView):
    model = RealityZone
    fields = ["name", "description", "practices"]
    template_name = "locations/mage/reality_zone/form.html"
    success_message = "Reality Zone '{name}' updated successfully!"
    error_message = "Failed to update reality zone. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        return form


class RealityZoneListView(ListView):
    model = RealityZone
    ordering = ["name"]
    template_name = "locations/mage/reality_zone/list.html"
