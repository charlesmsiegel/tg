from django import forms
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from characters.models.core.human import Human
from characters.models.demon.conclave import Conclave
from core.mixins import MessageMixin


class ConclaveDetailView(DetailView):
    model = Conclave
    template_name = "characters/demon/conclave/detail.html"


class ConclaveCreateView(MessageMixin, CreateView):
    model = Conclave
    fields = ["name", "description", "leader", "chronicle", "public_info"]
    template_name = "characters/demon/conclave/form.html"
    success_message = "Conclave created successfully."
    error_message = "There was an error creating the Conclave."

    def form_valid(self, form):
        response = super().form_valid(form)
        leader = form.cleaned_data.get("leader")
        if leader:
            self.object.members.add(leader)
        return response


class ConclaveUpdateView(MessageMixin, UpdateView):
    model = Conclave
    fields = ["name", "description", "leader", "chronicle", "public_info"]
    template_name = "characters/demon/conclave/form.html"
    success_message = "Conclave updated successfully."
    error_message = "There was an error updating the Conclave."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # Add a new field to add a new character (a Human object)
        options = Human.objects.filter(chronicle=self.object.chronicle)
        options = options.filter(group__isnull=True)

        form.fields["new_character"] = forms.ModelChoiceField(
            queryset=options,
            required=False,
            label="Add New Member",
            help_text="Select a character to add to this conclave.",
        )
        return form

    def form_valid(self, form):
        response = super().form_valid(form)
        new_char = form.cleaned_data.get("new_character")
        if new_char:
            self.object.members.add(new_char)
        return response


class ConclaveListView(ListView):
    model = Conclave
    ordering = ["name"]
    template_name = "characters/demon/conclave/list.html"
