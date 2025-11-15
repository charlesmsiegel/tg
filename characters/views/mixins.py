"""
Reusable view mixins and base classes for character views.
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, FormView, UpdateView
from core.views.approved_user_mixin import SpecialUserMixin
from characters.models.core.human import Human
from core.models import Language


class CharacterBasicsView(LoginRequiredMixin, FormView):
    """
    Base view for character creation basics forms.

    Subclasses must define:
    - form_class: The form to use for character creation
    - template_name: The template to render
    """

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["storyteller"] = False
        if self.request.user.profile.is_st():
            context["storyteller"] = True
        return context


class CharacterLanguagesView(SpecialUserMixin, FormView):
    """
    Base view for character language selection during creation.

    Subclasses must define:
    - form_class: The language form to use
    - template_name: The template to render
    - model: The character model class (e.g., MtAHuman, WtAHuman)
    """

    def dispatch(self, request, *args, **kwargs):
        obj = get_object_or_404(Human, pk=kwargs.get("pk"))
        if "Language" not in obj.merits_and_flaws.values_list("name", flat=True):
            obj.languages.add(Language.objects.get(name="English"))
            obj.creation_status += 1
            obj.save()
            return HttpResponseRedirect(obj.get_absolute_url())
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        human_pk = self.kwargs.get("pk")
        num_languages = Human.objects.get(pk=human_pk).num_languages()
        kwargs.update({"pk": human_pk, "num_languages": int(num_languages)})
        return kwargs

    def form_valid(self, form):
        human_pk = self.kwargs.get("pk")
        human = get_object_or_404(Human, pk=human_pk)
        num_languages = human.num_languages()
        human.languages.add(Language.objects.get(name="English"))
        for i in range(num_languages):
            language_name = form.cleaned_data.get(f"language_{i+1}")
            if language_name:
                language, created = Language.objects.get_or_create(name=language_name)
                human.languages.add(language)
        human.creation_status += 1
        human.save()
        return HttpResponseRedirect(human.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = get_object_or_404(Human, pk=self.kwargs.get("pk"))
        context["is_approved_user"] = self.check_if_special_user(
            context["object"], self.request.user
        )
        return context


class CharacterSpecialtiesView(SpecialUserMixin, FormView):
    """
    Base view for character specialty selection during creation.

    Subclasses must define:
    - form_class: The specialties form to use
    - template_name: The template to render
    - model: The character model class
    """

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["pk"] = self.kwargs.get("pk")
        return kwargs

    def form_valid(self, form):
        from characters.models.core.specialty import Specialty

        human_pk = self.kwargs.get("pk")
        human = get_object_or_404(Human, pk=human_pk)
        for ability in form.fields:
            specialty_name = form.cleaned_data.get(ability)
            if specialty_name and specialty_name != "":
                specialty, created = Specialty.objects.get_or_create(
                    name=specialty_name, ability=ability
                )
                human.specialties.add(specialty)
        human.creation_status += 1
        human.save()
        return HttpResponseRedirect(human.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = get_object_or_404(Human, pk=self.kwargs.get("pk"))
        context["is_approved_user"] = self.check_if_special_user(
            context["object"], self.request.user
        )
        return context


class CharacterExtrasView(SpecialUserMixin, UpdateView):
    """
    Base view for character extras (age, appearance, history, etc.).

    Subclasses must define:
    - model: The character model class
    - template_name: The template to render
    - fields: The fields to include (or use extras_fields attribute)
    """

    # Common extras fields that most character types use
    extras_fields = [
        "age",
        "apparent_age",
        "date_of_birth",
        "apparent_date_of_birth",
        "hair",
        "eyes",
        "ethnicity",
        "nationality",
        "height",
        "weight",
        "sex",
        "description",
        "childhood",
        "history",
        "goals",
        "notes",
        "public_info",
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_approved_user"] = self.check_if_special_user(
            self.object, self.request.user
        )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        if context["is_approved_user"]:
            self.object = form.save(commit=False)
            self.object.creation_status += 1
            self.object.save()
            return HttpResponseRedirect(self.object.get_absolute_url())
        return redirect(self.object.get_absolute_url())

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Add placeholders to common fields
        if "description" in form.fields:
            form.fields["description"].widget.attrs.update({
                "placeholder": "Describe your character's appearance"
            })
        if "childhood" in form.fields:
            form.fields["childhood"].widget.attrs.update({
                "placeholder": "Describe your character's childhood"
            })
        if "history" in form.fields:
            form.fields["history"].widget.attrs.update({
                "placeholder": "Describe your character's history"
            })
        if "goals" in form.fields:
            form.fields["goals"].widget.attrs.update({
                "placeholder": "What are your character's goals?"
            })
        if "notes" in form.fields:
            form.fields["notes"].widget.attrs.update({
                "placeholder": "Additional notes about your character"
            })
        return form
