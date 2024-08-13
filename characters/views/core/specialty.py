from characters.models.core import Specialty
from django.shortcuts import redirect, render
from django.views.generic import CreateView, DetailView, UpdateView


# Create your views here.
class SpecialtyDetailView(DetailView):
    model = Specialty
    template_name = "characters/core/specialty/detail.html"


class SpecialtyCreateView(CreateView):
    model = Specialty
    fields = ["name", "stat"]
    template_name = "characters/core/specialty/form.html"


class SpecialtyUpdateView(UpdateView):
    model = Specialty
    fields = ["name", "stat"]
    template_name = "characters/core/specialty/form.html"