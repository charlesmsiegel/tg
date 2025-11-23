from core.mixins import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from items.models.werewolf.talen import Talen


class TalenDetailView(DetailView):
    model = Talen
    template_name = "items/werewolf/talen/detail.html"


class TalenListView(ListView):
    model = Talen
    ordering = ["name"]
    template_name = "items/werewolf/talen/list.html"


class TalenCreateView(MessageMixin, CreateView):
    model = Talen
    fields = [
        "name",
        "rank",
        "background_cost",
        "quintessence_max",
        "description",
        "gnosis",
        "spirit",
    ]
    template_name = "items/werewolf/talen/form.html"
    success_message = "Talen '{name}' created successfully!"
    error_message = "Failed to create Talen. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        return form


class TalenUpdateView(MessageMixin, UpdateView):
    model = Talen
    fields = [
        "name",
        "rank",
        "background_cost",
        "quintessence_max",
        "description",
        "gnosis",
        "spirit",
    ]
    template_name = "items/werewolf/talen/form.html"
    success_message = "Talen '{name}' updated successfully!"
    error_message = "Failed to update Talen. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        return form
