from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from characters.models.wraith.guild import Guild
from core.mixins import MessageMixin


@method_decorator(cache_page(60 * 15), name="dispatch")
class GuildDetailView(DetailView):
    model = Guild
    template_name = "characters/wraith/guild/detail.html"


class GuildCreateView(MessageMixin, CreateView):
    model = Guild
    fields = ["name", "description", "guild_type", "willpower"]
    template_name = "characters/wraith/guild/form.html"
    success_message = "Guild created successfully."
    error_message = "There was an error creating the Guild."


class GuildUpdateView(MessageMixin, UpdateView):
    model = Guild
    fields = ["name", "description", "guild_type", "willpower"]
    template_name = "characters/wraith/guild/form.html"
    success_message = "Guild updated successfully."
    error_message = "There was an error updating the Guild."


@method_decorator(cache_page(60 * 15), name="dispatch")
class GuildListView(ListView):
    model = Guild
    ordering = ["guild_type", "name"]
    template_name = "characters/wraith/guild/list.html"
