from core.mixins import EditPermissionMixin, MessageMixin, ViewPermissionMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, FormView, ListView, UpdateView
from locations.forms.mage.library import LibraryForm
from locations.models.mage.library import Library


class LibraryDetailView(ViewPermissionMixin, DetailView):
    model = Library
    template_name = "locations/mage/library/detail.html"


class LibraryListView(ListView):
    model = Library
    ordering = ["name"]
    template_name = "locations/mage/library/list.html"


class LibraryCreateView(LoginRequiredMixin, MessageMixin, FormView):
    template_name = "locations/mage/library/form.html"
    form_class = LibraryForm
    success_message = "Library '{name}' created successfully!"
    error_message = "Failed to create library. Please correct the errors below."

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class LibraryUpdateView(EditPermissionMixin, MessageMixin, UpdateView):
    model = Library
    fields = ["name", "description", "parent", "rank", "faction", "books"]
    template_name = "locations/mage/library/form.html"
    success_message = "Library '{name}' updated successfully!"
    error_message = "Failed to update library. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update({"placeholder": "Enter description here"})
        return form
