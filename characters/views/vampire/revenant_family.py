from characters.models.vampire.revenant import RevenantFamily
from core.mixins import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class RevenantFamilyDetailView(DetailView):
    model = RevenantFamily
    template_name = "characters/vampire/revenant_family/detail.html"


class RevenantFamilyCreateView(MessageMixin, CreateView):
    model = RevenantFamily
    fields = [
        "name",
        "description",
        "weakness",
        "disciplines",
    ]
    template_name = "characters/vampire/revenant_family/form.html"
    success_message = "Revenant Family created successfully."
    error_message = "There was an error creating the Revenant Family."


class RevenantFamilyUpdateView(MessageMixin, UpdateView):
    model = RevenantFamily
    fields = [
        "name",
        "description",
        "weakness",
        "disciplines",
    ]
    template_name = "characters/vampire/revenant_family/form.html"
    success_message = "Revenant Family updated successfully."
    error_message = "There was an error updating the Revenant Family."


class RevenantFamilyListView(ListView):
    model = RevenantFamily
    ordering = ["name"]
    template_name = "characters/vampire/revenant_family/list.html"
