from core.mixins import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from items.models.werewolf.fetish import Fetish


class FetishDetailView(DetailView):
    model = Fetish
    template_name = "items/werewolf/fetish/detail.html"


class FetishListView(ListView):
    model = Fetish
    ordering = ["name"]
    template_name = "items/werewolf/fetish/list.html"


class FetishCreateView(MessageMixin, CreateView):
    model = Fetish
    fields = [
        "name",
        "rank",
        "background_cost",
        "quintessence_max",
        "description",
        "gnosis",
        "spirit",
    ]
    template_name = "items/werewolf/fetish/form.html"
    success_message = "Fetish '{name}' created successfully!"
    error_message = "Failed to create fetish. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        return form


class FetishUpdateView(MessageMixin, UpdateView):
    model = Fetish
    fields = [
        "name",
        "rank",
        "background_cost",
        "quintessence_max",
        "description",
        "gnosis",
        "spirit",
    ]
    template_name = "items/werewolf/fetish/form.html"
    success_message = "Fetish '{name}' updated successfully!"
    error_message = "Failed to update fetish. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        return form
