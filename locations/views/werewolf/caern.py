from django.views.generic import CreateView, DetailView, UpdateView
from locations.models.werewolf.caern import Caern


class CaernDetailView(DetailView):
    model = Caern
    template_name = "locations/werewolf/caern/detail.html"


class CaernCreateView(CreateView):
    model = Caern
    fields = [
        "name",
        "parent",
        "description",
        "rank",
        "caern_type",
    ]
    template_name = "locations/werewolf/caern/form.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        form.fields["parent"].empty_label = "Parent Location"
        return form


class CaernUpdateView(UpdateView):
    model = Caern
    fields = [
        "name",
        "description",
        "parent",
        "rank",
        "caern_type",
    ]
    template_name = "locations/werewolf/caern/form.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        form.fields["parent"].empty_label = "Parent Location"
        return form
