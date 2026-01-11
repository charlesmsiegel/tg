from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView

from characters.models.core import Group
from core.mixins import MessageMixin


class GroupDetailView(LoginRequiredMixin, DetailView):
    model = Group
    template_name = "characters/core/group/detail.html"


class GroupCreateView(MessageMixin, CreateView):
    model = Group
    fields = ["name", "description", "members", "leader"]
    template_name = "characters/core/group/form.html"
    success_message = "Group '{name}' created successfully!"
    error_message = "Failed to create Group. Please correct the errors below."


class GroupUpdateView(MessageMixin, UpdateView):
    model = Group
    fields = ["name", "description", "members", "leader"]
    template_name = "characters/core/group/form.html"
    success_message = "Group '{name}' updated successfully!"
    error_message = "Failed to update Group. Please correct the errors below."
