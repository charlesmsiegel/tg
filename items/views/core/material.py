from django.views.generic import CreateView, DetailView, ListView, UpdateView
from items.models.core import Material


class MaterialDetailView(DetailView):
    model = Material
    template_name = "items/core/material/detail.html"


class MaterialCreateView(CreateView):
    model = Material
    fields = "__all__"
    template_name = "items/core/material/form.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update(
            {"placeholder": "Enter name here", "rows": 1}
        )
        return form


class MaterialUpdateView(UpdateView):
    model = Material
    fields = "__all__"
    template_name = "items/core/material/form.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update(
            {"placeholder": "Enter name here", "rows": 1}
        )
        return form


class MaterialListView(ListView):
    model = Material
    ordering = ["name"]
    template_name = "items/core/material/list.html"
