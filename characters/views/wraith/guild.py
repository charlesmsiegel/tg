from characters.models.wraith.guild import Guild
from core.mixins import MessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class GuildDetailView(DetailView):
    model = Guild
    template_name = "characters/wraith/guild/detail.html"


class GuildCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    model = Guild
    fields = ["name", "description", "guild_type", "willpower"]
    template_name = "characters/wraith/guild/form.html"
    success_message = "Guild created successfully."
    error_message = "There was an error creating the Guild."


class GuildUpdateView(LoginRequiredMixin, MessageMixin, UpdateView):
    model = Guild
    fields = ["name", "description", "guild_type", "willpower"]
    template_name = "characters/wraith/guild/form.html"
    success_message = "Guild updated successfully."
    error_message = "There was an error updating the Guild."


class GuildListView(ListView):
    model = Guild
    ordering = ["guild_type", "name"]
    template_name = "characters/wraith/guild/list.html"
