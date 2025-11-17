from django.views.generic import CreateView, DetailView, ListView, UpdateView
from locations.models.mage.realm import HorizonRealm


class RealmDetailView(DetailView):
    model = HorizonRealm
    template_name = "locations/mage/realm/detail.html"


class RealmListView(ListView):
    model = HorizonRealm
    ordering = ["name"]
    template_name = "locations/mage/realm/list.html"


class RealmCreateView(CreateView):
    model = HorizonRealm
    fields = ["name", "description", "parent"]
    template_name = "locations/mage/realm/form.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        form.fields["parent"].empty_label = "Parent Location"
        return form


class RealmUpdateView(UpdateView):
    model = HorizonRealm
    fields = ["name", "description", "parent"]
    template_name = "locations/mage/realm/form.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        form.fields["parent"].empty_label = "Parent Location"
        return form
