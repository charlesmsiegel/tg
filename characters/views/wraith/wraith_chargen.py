from typing import Any

from characters.forms.core.linked_npc import LinkedNPCForm
from characters.forms.core.specialty import SpecialtiesForm
from characters.forms.wraith.fetter import FetterForm
from characters.forms.wraith.freebies import WraithFreebiesForm
from characters.forms.wraith.passion import PassionForm
from characters.forms.wraith.wraith import WraithCreationForm
from characters.models.core.human import Human
from characters.models.core.specialty import Specialty
from characters.models.wraith.shadow_archetype import ShadowArchetype
from characters.models.wraith.thorn import Thorn
from characters.models.wraith.wraith import Wraith
from characters.views.core.backgrounds import HumanBackgroundsView
from characters.views.core.generic_background import GenericBackgroundView
from characters.views.core.human import (
    HumanAttributeView,
    HumanCharacterCreationView,
    HumanFreebieFormPopulationView,
    HumanFreebiesView,
)
from characters.views.wraith.wtohuman import WtOHumanAbilityView
from core.forms.language import HumanLanguageForm
from core.mixins import (
    EditPermissionMixin,
    SpecialUserMixin,
    SpendFreebiesPermissionMixin,
    SpendXPPermissionMixin,
    ViewPermissionMixin,
)
from core.models import Language
from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import FormView, UpdateView


class WraithBasicsView(LoginRequiredMixin, FormView):
    form_class = WraithCreationForm
    template_name = "characters/wraith/wraith/basics.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["storyteller"] = self.request.user.profile.is_st()
        return context

    def form_valid(self, form):
        self.object = form.save()
        # Set initial values based on guild
        if self.object.guild:
            self.object.willpower = self.object.guild.willpower
        self.object.save()
        messages.success(
            self.request,
            f"Wraith '{self.object.name}' created successfully! Continue with character creation.",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors in the form below.")
        return super().form_invalid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class WraithAttributeView(HumanAttributeView):
    model = Wraith
    template_name = "characters/wraith/wraith/chargen.html"

    primary = 7
    secondary = 5
    tertiary = 3


class WraithAbilityView(WtOHumanAbilityView):
    model = Wraith
    template_name = "characters/wraith/wraith/chargen.html"

    primary = 13
    secondary = 9
    tertiary = 5


class WraithBackgroundsView(HumanBackgroundsView):
    model = Wraith
    template_name = "characters/wraith/wraith/chargen.html"


class WraithArcanosView(SpecialUserMixin, UpdateView):
    model = Wraith
    fields = [
        "argos",
        "castigate",
        "embody",
        "fatalism",
        "flux",
        "inhabit",
        "keening",
        "lifeweb",
        "moliate",
        "mnemosynis",
        "outrage",
        "pandemonium",
        "phantasm",
        "usury",
        "intimation",
    ]
    template_name = "characters/wraith/wraith/chargen.html"

    def form_valid(self, form):
        # Validate that total arcanoi is exactly 5
        arcanoi_total = sum(form.cleaned_data.get(field, 0) for field in self.fields)

        if arcanoi_total != 5:
            form.add_error(
                None,
                f"Arcanoi must total exactly 5 dots (currently {arcanoi_total})",
            )
            messages.error(
                self.request,
                f"Arcanoi allocation error: You must spend exactly 5 dots. You have {arcanoi_total}.",
            )
            return self.form_invalid(form)

        # Validate that no arcanos exceeds 5
        for field in self.fields:
            if form.cleaned_data.get(field, 0) > 5:
                form.add_error(field, "Arcanoi cannot exceed 5 dots")
                messages.error(self.request, "Each Arcanos cannot exceed 5 dots.")
                return self.form_invalid(form)

        self.object.creation_status += 1
        self.object.save()
        messages.success(self.request, "Arcanoi allocated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        if not self.request._messages._queued_messages:
            messages.error(self.request, "Please correct the errors in the form below.")
        return super().form_invalid(form)


class WraithShadowView(SpecialUserMixin, UpdateView):
    model = Wraith
    fields = ["shadow_archetype"]
    template_name = "characters/wraith/wraith/chargen.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["shadow_archetypes"] = ShadowArchetype.objects.all()
        context["thorns"] = Thorn.objects.all()
        return context

    def form_valid(self, form):
        # Shadow archetype is required
        if not form.cleaned_data.get("shadow_archetype"):
            form.add_error("shadow_archetype", "Shadow Archetype is required")
            messages.error(self.request, "You must select a Shadow Archetype to continue.")
            return self.form_invalid(form)

        self.object.creation_status += 1
        self.object.save()
        messages.success(self.request, "Shadow Archetype selected successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        if not self.request._messages._queued_messages:
            messages.error(self.request, "Please correct the errors in the form below.")
        return super().form_invalid(form)


class WraithPassionsView(EditPermissionMixin, FormView):
    form_class = PassionForm
    template_name = "characters/wraith/wraith/chargen.html"

    def get_object(self):
        """Return the Wraith object for permission checking."""
        if not hasattr(self, "object") or self.object is None:
            self.object = get_object_or_404(Wraith, pk=self.kwargs.get("pk"))
        return self.object

    def dispatch(self, request, *args, **kwargs):
        obj = get_object_or_404(Wraith, pk=kwargs.get("pk"))
        # If they already have the right number of passion points, skip this
        if obj.has_passions():
            obj.creation_status += 1
            obj.save()
            return HttpResponseRedirect(obj.get_absolute_url())
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = get_object_or_404(Wraith, pk=self.kwargs.get("pk"))
        context["is_approved_user"] = self.check_if_special_user(
            context["object"], self.request.user
        )
        context["passion_points_total"] = context["object"].passion_points
        context["passion_points_spent"] = context["object"].total_passion_rating()
        context["passion_points_remaining"] = (
            context["passion_points_total"] - context["passion_points_spent"]
        )
        return context

    def form_valid(self, form):
        wraith = get_object_or_404(Wraith, pk=self.kwargs.get("pk"))

        # Check if adding this passion would exceed the limit
        current_total = wraith.total_passion_rating()
        new_rating = form.cleaned_data["rating"]

        if current_total + new_rating > wraith.passion_points:
            form.add_error(
                "rating",
                f"Cannot exceed {wraith.passion_points} total passion points. "
                f"You have {wraith.passion_points - current_total} remaining.",
            )
            messages.error(
                self.request,
                f"Cannot exceed {wraith.passion_points} total passion points. "
                f"You have {wraith.passion_points - current_total} remaining.",
            )
            return self.form_invalid(form)

        # Add the passion
        wraith.add_passion(
            emotion=form.cleaned_data["emotion"],
            description=form.cleaned_data["description"],
            rating=new_rating,
            is_dark=form.cleaned_data.get("is_dark_passion", False),
        )

        # If we've hit the exact total, move to next stage
        if wraith.has_passions():
            wraith.creation_status += 1
            wraith.save()
            messages.success(self.request, "All Passions allocated successfully!")
        else:
            messages.success(
                self.request,
                f"Passion added successfully! {wraith.passion_points - wraith.total_passion_rating()} points remaining.",
            )

        return HttpResponseRedirect(wraith.get_absolute_url())

    def form_invalid(self, form):
        if not self.request._messages._queued_messages:
            messages.error(self.request, "Please correct the errors in the form below.")
        return super().form_invalid(form)


class WraithFettersView(EditPermissionMixin, FormView):
    form_class = FetterForm
    template_name = "characters/wraith/wraith/chargen.html"

    def get_object(self):
        """Return the Wraith object for permission checking."""
        if not hasattr(self, "object") or self.object is None:
            self.object = get_object_or_404(Wraith, pk=self.kwargs.get("pk"))
        return self.object

    def dispatch(self, request, *args, **kwargs):
        obj = get_object_or_404(Wraith, pk=kwargs.get("pk"))
        # If they already have the right number of fetter points, skip this
        if obj.has_fetters():
            obj.creation_status += 1
            obj.save()
            return HttpResponseRedirect(obj.get_absolute_url())
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = get_object_or_404(Wraith, pk=self.kwargs.get("pk"))
        context["is_approved_user"] = self.check_if_special_user(
            context["object"], self.request.user
        )
        context["fetter_points_total"] = context["object"].fetter_points
        context["fetter_points_spent"] = context["object"].total_fetter_rating()
        context["fetter_points_remaining"] = (
            context["fetter_points_total"] - context["fetter_points_spent"]
        )
        return context

    def form_valid(self, form):
        wraith = get_object_or_404(Wraith, pk=self.kwargs.get("pk"))

        # Check if adding this fetter would exceed the limit
        current_total = wraith.total_fetter_rating()
        new_rating = form.cleaned_data["rating"]

        if current_total + new_rating > wraith.fetter_points:
            form.add_error(
                "rating",
                f"Cannot exceed {wraith.fetter_points} total fetter points. "
                f"You have {wraith.fetter_points - current_total} remaining.",
            )
            messages.error(
                self.request,
                f"Cannot exceed {wraith.fetter_points} total fetter points. "
                f"You have {wraith.fetter_points - current_total} remaining.",
            )
            return self.form_invalid(form)

        # Add the fetter
        wraith.add_fetter(
            fetter_type=form.cleaned_data["fetter_type"],
            description=form.cleaned_data["description"],
            rating=new_rating,
        )

        # If we've hit the exact total, move to next stage
        if wraith.has_fetters():
            wraith.creation_status += 1
            wraith.save()
            messages.success(self.request, "All Fetters allocated successfully!")
        else:
            messages.success(
                self.request,
                f"Fetter added successfully! {wraith.fetter_points - wraith.total_fetter_rating()} points remaining.",
            )

        return HttpResponseRedirect(wraith.get_absolute_url())

    def form_invalid(self, form):
        if not self.request._messages._queued_messages:
            messages.error(self.request, "Please correct the errors in the form below.")
        return super().form_invalid(form)


class WraithExtrasView(SpecialUserMixin, UpdateView):
    model = Wraith
    fields = [
        "date_of_birth",
        "apparent_age",
        "age",
        "age_at_death",
        "death_description",
        "description",
        "history",
        "goals",
        "notes",
        "public_info",
    ]
    template_name = "characters/wraith/wraith/chargen.html"

    def form_valid(self, form):
        # Validate that death-related fields are filled
        if not form.cleaned_data.get("age_at_death"):
            form.add_error("age_at_death", "Age at death is required")
            messages.error(self.request, "Age at death is required for Wraith characters.")
            return self.form_invalid(form)

        if not form.cleaned_data.get("death_description"):
            form.add_error("death_description", "Death description is required")
            messages.error(self.request, "Death description is required for Wraith characters.")
            return self.form_invalid(form)

        self.object.creation_status += 1
        self.object.save()
        messages.success(self.request, "Character details saved successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        if not self.request._messages._queued_messages:
            messages.error(self.request, "Please correct the errors in the form below.")
        return super().form_invalid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["date_of_birth"].widget = forms.DateInput(attrs={"type": "date"})
        form.fields["description"].widget.attrs.update(
            {
                "placeholder": "Describe your character's physical appearance (as a wraith). Be detailed, this will be visible to other players."
            }
        )
        form.fields["death_description"].widget.attrs.update(
            {
                "placeholder": "Describe how your character died. This is crucial for understanding your wraith's nature."
            }
        )
        form.fields["history"].widget.attrs.update(
            {
                "placeholder": "Describe character history/backstory from when they were alive and how they've adapted to being a wraith."
            }
        )
        form.fields["goals"].widget.attrs.update(
            {"placeholder": "Describe your character's long and short term goals as a wraith."}
        )
        form.fields["notes"].widget.attrs.update({"placeholder": "Notes"})
        form.fields["public_info"].widget.attrs.update(
            {"placeholder": "This will be displayed to all players who look at your character."}
        )
        return form


class WraithFreebiesView(HumanFreebiesView):
    model = Wraith
    form_class = WraithFreebiesForm
    template_name = "characters/wraith/wraith/chargen.html"

    def get_category_functions(self):
        d = super().get_category_functions()
        d.update(
            {
                "arcanos": self.object.arcanos_freebies,
                "pathos": self.object.pathos_freebies,
                "passion": self.object.passion_freebies,
                "fetter": self.object.fetter_freebies,
                "corpus": self.object.corpus_freebies,
            }
        )
        return d


class WraithFreebieFormPopulationView(HumanFreebieFormPopulationView):
    primary_class = Wraith

    def category_method_map(self):
        base_map = super().category_method_map()
        base_map.update(
            {
                "Arcanos": self.arcanos_options,
                "Pathos": self.pathos_options,
                "Passion": self.passion_options,
                "Fetter": self.fetter_options,
                "Corpus": self.corpus_options,
            }
        )
        return base_map

    def arcanos_options(self, wraith):
        """Return available arcanoi for freebie spending."""
        arcanoi = wraith.get_arcanoi()
        return [
            (name.replace("_", " ").title(), name) for name, value in arcanoi.items() if value < 5
        ]

    def pathos_options(self, wraith):
        """Return pathos option if it can be increased."""
        if wraith.pathos_permanent < 10:
            return [("Pathos", "pathos")]
        return []

    def passion_options(self, wraith):
        """Return passion as an option."""
        return [("New Passion", "passion")]

    def fetter_options(self, wraith):
        """Return fetter as an option."""
        return [("New Fetter", "fetter")]

    def corpus_options(self, wraith):
        """Return corpus option if it can be increased."""
        if wraith.corpus < 10:
            return [("Corpus", "corpus")]
        return []


class WraithLanguagesView(EditPermissionMixin, FormView):
    form_class = HumanLanguageForm
    template_name = "characters/wraith/wraith/chargen.html"

    def get_object(self):
        """Return the Human object for permission checking."""
        if not hasattr(self, "object") or self.object is None:
            self.object = get_object_or_404(Human, pk=self.kwargs.get("pk"))
        return self.object

    def dispatch(self, request, *args, **kwargs):
        obj = get_object_or_404(Human, pk=kwargs.get("pk"))
        if "Language" not in obj.merits_and_flaws.values_list("name", flat=True):
            english, _ = Language.objects.get_or_create(name="English")
            obj.languages.add(english)
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
        english, _ = Language.objects.get_or_create(name="English")
        human.languages.add(english)
        for i in range(num_languages):
            language_name = form.cleaned_data.get(f"language_{i+1}")
            if language_name:
                language, created = Language.objects.get_or_create(name=language_name)
                human.languages.add(language)
        human.creation_status += 1
        human.save()
        messages.success(self.request, "Languages added successfully!")
        return HttpResponseRedirect(human.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = get_object_or_404(Human, pk=self.kwargs.get("pk"))
        context["is_approved_user"] = self.check_if_special_user(
            context["object"], self.request.user
        )
        return context


class WraithAlliesView(GenericBackgroundView):
    primary_object_class = Wraith
    background_name = "allies"
    form_class = LinkedNPCForm
    template_name = "characters/wraith/wraith/chargen.html"


class WraithMentorView(GenericBackgroundView):
    primary_object_class = Wraith
    background_name = "mentor"
    form_class = LinkedNPCForm
    template_name = "characters/wraith/wraith/chargen.html"


class WraithContactsView(GenericBackgroundView):
    primary_object_class = Wraith
    background_name = "contacts"
    form_class = LinkedNPCForm
    template_name = "characters/wraith/wraith/chargen.html"


class WraithSpecialtiesView(EditPermissionMixin, FormView):
    form_class = SpecialtiesForm
    template_name = "characters/wraith/wraith/chargen.html"

    def get_object(self):
        """Return the Wraith object for permission checking."""
        if not hasattr(self, "object") or self.object is None:
            self.object = Wraith.objects.get(id=self.kwargs["pk"])
        return self.object

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["object"] = self.get_object()
        context["is_approved_user"] = self.check_if_special_user(
            context["object"], self.request.user
        )
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        wraith = Wraith.objects.get(id=self.kwargs["pk"])
        kwargs["object"] = wraith
        kwargs["specialties_needed"] = wraith.needed_specialties()
        return kwargs

    def form_valid(self, form):
        context = self.get_context_data()
        wraith = context["object"]
        for field in form.fields:
            spec = Specialty.objects.get_or_create(name=form.data[field], stat=field)[0]
            wraith.specialties.add(spec)
        wraith.status = "Sub"
        wraith.save()
        messages.success(self.request, f"Wraith '{wraith.name}' submitted for approval!")
        return HttpResponseRedirect(wraith.get_absolute_url())


class WraithCharacterCreationView(HumanCharacterCreationView):
    view_mapping = {
        1: WraithAttributeView,
        2: WraithAbilityView,
        3: WraithBackgroundsView,
        4: WraithArcanosView,
        5: WraithShadowView,
        6: WraithPassionsView,
        7: WraithFettersView,
        8: WraithExtrasView,
        9: WraithFreebiesView,
        10: WraithLanguagesView,
        11: WraithAlliesView,
        12: WraithMentorView,
        13: WraithContactsView,
        14: WraithSpecialtiesView,
    }
    model_class = Wraith
    key_property = "creation_status"
    default_redirect = lambda self, pk: HttpResponseRedirect(
        Wraith.objects.get(pk=pk).get_absolute_url()
    )
