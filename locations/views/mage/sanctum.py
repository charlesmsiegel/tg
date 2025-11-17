from django.views.generic import DetailView, FormView, ListView, UpdateView
from locations.forms.mage.sanctum import SanctumForm
from locations.models.mage.sanctum import Sanctum


class SanctumDetailView(DetailView):
    model = Sanctum
    template_name = "locations/mage/sanctum/detail.html"


class SanctumListView(ListView):
    model = Sanctum
    ordering = ["name"]
    template_name = "locations/mage/sanctum/list.html"


class SanctumCreateView(FormView):
    form_class = SanctumForm
    template_name = "locations/mage/sanctum/form.html"

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class SanctumUpdateView(UpdateView):
    model = Sanctum
    fields = ["name", "description", "parent"]
    template_name = "locations/mage/sanctum/form.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        form.fields["parent"].empty_label = "Parent Location"
        return form
