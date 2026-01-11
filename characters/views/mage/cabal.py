from django import forms
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from characters.forms.mage.cabal import CabalForm
from characters.models.core.human import Human
from characters.models.mage.cabal import Cabal
from core.mixins import MessageMixin


class CabalDetailView(DetailView):
    model = Cabal
    template_name = "characters/mage/cabal/detail.html"


class CabalCreateView(MessageMixin, CreateView):
    model = Cabal
    form_class = CabalForm
    template_name = "characters/mage/cabal/form.html"
    success_message = "Cabal created successfully."
    error_message = "There was an error creating the Cabal."

    def form_valid(self, form):
        response = super().form_valid(form)
        leader = form.cleaned_data.get("leader")
        if leader:
            self.object.members.add(leader)
        return response

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class CabalUpdateView(MessageMixin, UpdateView):
    model = Cabal
    form_class = CabalForm
    template_name = "characters/mage/cabal/form.html"
    success_message = "Cabal updated successfully."
    error_message = "There was an error updating the Cabal."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # Add a new field to add a new character (a Human object)
        options = Human.objects.filter(chronicle=self.object.chronicle)
        options = options.filter(group__isnull=True)

        form.fields["new_character"] = forms.ModelChoiceField(
            queryset=options,
            required=False,
            label="Add New Member",
            help_text="Select a character to add to this cabal.",
        )
        return form

    def form_valid(self, form):
        # Handle adding the new character to the cabal
        response = super().form_valid(form)
        new_char = form.cleaned_data.get("new_character")
        if new_char:
            self.object.members.add(new_char)
        return response

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class CabalListView(ListView):
    model = Cabal
    ordering = ["name"]
    template_name = "characters/mage/cabal/list.html"

    def get_queryset(self):
        return super().get_queryset().select_related("leader").prefetch_related("members")
