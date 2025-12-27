from characters.models.core.human import Human
from characters.models.wraith.circle import Circle
from core.mixins import MessageMixin
from django import forms
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class CircleDetailView(DetailView):
    model = Circle
    template_name = "characters/wraith/circle/detail.html"


class CircleCreateView(MessageMixin, CreateView):
    model = Circle
    fields = ["name", "description", "leader", "chronicle", "public_info"]
    template_name = "characters/wraith/circle/form.html"
    success_message = "Circle created successfully."
    error_message = "There was an error creating the Circle."

    def form_valid(self, form):
        response = super().form_valid(form)
        leader = form.cleaned_data.get("leader")
        if leader:
            self.object.members.add(leader)
        return response


class CircleUpdateView(MessageMixin, UpdateView):
    model = Circle
    fields = ["name", "description", "leader", "chronicle", "public_info"]
    template_name = "characters/wraith/circle/form.html"
    success_message = "Circle updated successfully."
    error_message = "There was an error updating the Circle."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # Add a new field to add a new character (a Human object)
        options = Human.objects.filter(chronicle=self.object.chronicle)
        options = options.filter(group__isnull=True)

        form.fields["new_character"] = forms.ModelChoiceField(
            queryset=options,
            required=False,
            label="Add New Member",
            help_text="Select a character to add to this circle.",
        )
        return form

    def form_valid(self, form):
        # Handle adding the new character to the circle
        response = super().form_valid(form)
        new_char = form.cleaned_data.get("new_character")
        if new_char:
            self.object.members.add(new_char)
        return response


class CircleListView(ListView):
    model = Circle
    ordering = ["name"]
    template_name = "characters/wraith/circle/list.html"

    def get_queryset(self):
        return super().get_queryset().select_related("leader").prefetch_related("members")
