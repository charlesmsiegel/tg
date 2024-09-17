from django.views.generic import CreateView, DetailView, UpdateView
from items.models.werewolf.fetish import Fetish


class FetishDetailView(DetailView):
    model = Fetish
    template_name = "items/werewolf/fetish/detail.html"


class FetishCreateView(CreateView):
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

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        return form


class FetishUpdateView(UpdateView):
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

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        return form
