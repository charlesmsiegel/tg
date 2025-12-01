from characters.models.werewolf.gift import Gift, GiftPermission
from core.mixins import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class GiftDetailView(DetailView):
    model = Gift
    template_name = "characters/werewolf/gift/detail.html"


class GiftCreateView(MessageMixin, CreateView):
    model = Gift
    fields = ["name", "rank", "description"]
    template_name = "characters/werewolf/gift/form.html"
    success_message = "Gift created successfully."
    error_message = "There was an error creating the Gift."


class GiftUpdateView(MessageMixin, UpdateView):
    model = Gift
    fields = ["name", "rank", "description"]
    template_name = "characters/werewolf/gift/form.html"
    success_message = "Gift updated successfully."
    error_message = "There was an error updating the Gift."


class GiftListView(ListView):
    model = Gift
    ordering = ["name"]
    template_name = "characters/werewolf/gift/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get unique shifter types for filtering
        context["shifter_types"] = (
            GiftPermission.objects.values_list("shifter", flat=True).distinct().order_by("shifter")
        )
        # Get all permissions for more specific filtering
        context["gift_permissions"] = GiftPermission.objects.all().order_by("shifter", "condition")
        # Get unique ranks
        context["ranks"] = Gift.objects.values_list("rank", flat=True).distinct().order_by("rank")
        return context
