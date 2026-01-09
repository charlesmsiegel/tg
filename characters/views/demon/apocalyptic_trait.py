from characters.models.demon.apocalyptic_form import ApocalypticFormTrait
from core.mixins import MessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class ApocalypticFormTraitDetailView(DetailView):
    model = ApocalypticFormTrait
    template_name = "characters/demon/apocalyptic_trait/detail.html"


class ApocalypticFormTraitCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    model = ApocalypticFormTrait
    fields = [
        "name",
        "description",
        "cost",
        "house",
        "high_torment_only",
    ]
    template_name = "characters/demon/apocalyptic_trait/form.html"
    success_message = "Apocalyptic Form Trait created successfully."
    error_message = "There was an error creating the Apocalyptic Form Trait."


class ApocalypticFormTraitUpdateView(LoginRequiredMixin, MessageMixin, UpdateView):
    model = ApocalypticFormTrait
    fields = [
        "name",
        "description",
        "cost",
        "house",
        "high_torment_only",
    ]
    template_name = "characters/demon/apocalyptic_trait/form.html"
    success_message = "Apocalyptic Form Trait updated successfully."
    error_message = "There was an error updating the Apocalyptic Form Trait."


class ApocalypticFormTraitListView(ListView):
    model = ApocalypticFormTrait
    ordering = ["cost", "name"]
    template_name = "characters/demon/apocalyptic_trait/list.html"

    def get_queryset(self):
        return super().get_queryset().select_related("house")
