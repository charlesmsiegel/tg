from characters.models.core import Group
from django.views.generic import CreateView, DetailView, UpdateView


class GroupDetailView(DetailView):
    model = Group
    template_name = "characters/core/group/detail.html"


class GroupCreateView(CreateView):
    model = Group
    fields = ["name", "description", "members", "leader"]
    template_name = "characters/core/group/form.html"


class GroupUpdateView(UpdateView):
    model = Group
    fields = ["name", "description", "members", "leader"]
    template_name = "characters/core/group/form.html"
