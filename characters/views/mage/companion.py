from characters.forms.core.linked_npc import LinkedNPCForm
from characters.forms.core.specialty import SpecialtiesForm
from characters.forms.mage.freebies import CompanionFreebiesForm
from characters.models.core.ability_block import Ability
from characters.models.core.archetype import Archetype
from characters.models.core.attribute_block import Attribute
from characters.models.core.background_block import Background, BackgroundRating
from characters.models.core.human import Human
from characters.models.core.merit_flaw_block import MeritFlaw
from characters.models.core.specialty import Specialty
from characters.models.mage.cabal import Cabal
from characters.models.mage.companion import Advantage, Companion
from characters.models.mage.faction import MageFaction
from characters.models.werewolf.charm import SpiritCharm
from characters.views.core.backgrounds import HumanBackgroundsView
from characters.views.core.generic_background import GenericBackgroundView
from characters.views.core.human import (
    HumanAttributeView,
    HumanCharacterCreationView,
    HumanDetailView,
)
from characters.views.mage.background_views import MtAEnhancementView
from characters.views.mage.mtahuman import MtAHumanAbilityView
from core.forms.language import HumanLanguageForm
from core.mixins import (
    EditPermissionMixin,
    MessageMixin,
    SpecialUserMixin,
    SpendFreebiesPermissionMixin,
    SpendXPPermissionMixin,
    ViewPermissionMixin,
)
from core.models import Language
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import CreateView, FormView, UpdateView
from game.models import ObjectType
from items.forms.mage.wonder import WonderForm
from locations.forms.mage.chantry import ChantrySelectOrCreateForm
from locations.forms.mage.library import LibraryForm
from locations.forms.mage.node import NodeForm
from locations.forms.mage.sanctum import SanctumForm


class CompanionDetailView(HumanDetailView):
    model = Companion
    template_name = "characters/mage/companion/detail.html"


class CompanionCreateView(MessageMixin, CreateView):
    model = Companion
    fields = "__all__"
    template_name = "characters/mage/companion/form.html"
    success_message = "Companion created successfully."
    error_message = "There was an error creating the Companion."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["affiliation"].queryset = MageFaction.objects.top_level()
        form.fields["faction"].queryset = MageFaction.objects.none()
        form.fields["subfaction"].queryset = MageFaction.objects.none()
        return form


class CompanionUpdateView(EditPermissionMixin, UpdateView):
    model = Companion
    fields = "__all__"
    template_name = "characters/mage/companion/form.html"
    success_message = "Companion updated successfully."
    error_message = "There was an error updating the Companion."


class LoadExamplesView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        from core.ajax import dropdown_options_response

        category_choice = request.GET.get("category")
        object_id = request.GET.get("object")
        m = Companion.objects.get(pk=object_id)

        category_choice = request.GET.get("category")
        if category_choice == "Attribute":
            examples = Attribute.objects.all()
            examples = [x for x in examples if getattr(m, x.property_name, 0) < 5]
        elif category_choice == "Ability":
            examples = Ability.objects.order_by("name")
            examples = [
                x
                for x in examples
                if getattr(m, x.property_name, 0) < 4 and hasattr(m, x.property_name)
            ]
        elif category_choice == "New Background":
            examples = Background.objects.filter(property_name__in=m.allowed_backgrounds).order_by(
                "name"
            )
        elif category_choice == "Existing Background":
            examples = [x for x in BackgroundRating.objects.filter(char=m, rating__lt=4)]
        elif category_choice == "MeritFlaw":
            companion, _ = ObjectType.objects.get_or_create(
                name="companion", defaults={"type": "char", "gameline": "mta"}
            )
            examples = MeritFlaw.objects.filter(allowed_types=companion)
            max_flaws = 7
            if m.total_flaws() <= 0:
                if m.companion_type == "familiar":
                    max_flaws += 5
                examples = examples.exclude(max_rating__lt=min(0, -max_flaws - m.total_flaws()))
            examples = examples.exclude(min_rating__gt=m.freebies)
        elif category_choice == "Advantage":
            examples = Advantage.objects.filter(min_rating__lte=m.freebies)
            examples = [x for x in examples if x not in m.advantages.all()]
        elif category_choice == "Charms":
            examples = (
                SpiritCharm.objects.exclude(point_cost=0)
                .filter(point_cost__lte=m.freebies)
                .order_by("name")
            )
            examples = [x for x in examples if x not in m.charms.all()]
        else:
            examples = []

        return dropdown_options_response(examples, label_attr="__str__")


@login_required
def load_companion_values(request):
    from core.ajax import simple_values_response

    advantage = Advantage.objects.get(pk=request.GET.get("example"))
    ratings = [x.value for x in advantage.ratings.all()]
    ratings.sort()
    return simple_values_response(ratings)


class CompanionBasicsView(LoginRequiredMixin, CreateView):
    model = Companion
    fields = [
        "name",
        "nature",
        "demeanor",
        "concept",
        "companion_type",
        "chronicle",
        "image",
        "companion_of",
        "npc",
    ]
    template_name = "characters/mage/companion/basics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["storyteller"] = False
        if self.request.user.profile.is_st():
            context["storyteller"] = True
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["nature"].queryset = Archetype.objects.all().order_by("name")
        form.fields["demeanor"].queryset = Archetype.objects.all().order_by("name")
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["concept"].widget.attrs.update({"placeholder": "Enter concept here"})
        form.fields["image"].required = False
        return form

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CompanionAttributeView(HumanAttributeView):
    model = Companion
    template_name = "characters/mage/companion/chargen.html"

    primary = 6
    secondary = 4
    tertiary = 3


class CompanionAbilityView(MtAHumanAbilityView):
    model = Companion
    template_name = "characters/mage/companion/chargen.html"

    primary = 11
    secondary = 7
    tertiary = 4


class CompanionBackgroundsView(HumanBackgroundsView):
    template_name = "characters/mage/companion/chargen.html"


class CompanionExtrasView(SpecialUserMixin, UpdateView):
    model = Companion
    fields = [
        "date_of_birth",
        "apparent_age",
        "age",
        "description",
        "history",
        "goals",
        "notes",
        "public_info",
    ]
    template_name = "characters/mage/companion/chargen.html"

    def form_valid(self, form):
        self.object.creation_status += 1
        if self.object.companion_type in ["acoylte", "backup"]:
            self.object.freebies = 15
        elif self.object.companion_type in ["consor", "ally"]:
            self.object.freebies = 21
        elif self.object.companion_type in ["familiar"]:
            if self.object.npc == False:
                self.object.freebies = 25
            thaumivore = MeritFlaw.objects.get(name="Thaumivore")
            bond_sharing = Advantage.objects.get(name="Bond-Sharing")
            paradox_nullification = Advantage.objects.get(name="Paradox Nullification")
            self.object.add_mf(thaumivore, -5)
            self.object.spent_freebies.append(
                self.object.freebie_spend_record(thaumivore.name, "meritflaw", -5, cost=-5)
            )

            self.object.add_advantage(bond_sharing, 4)
            self.object.spent_freebies.append(
                self.object.freebie_spend_record(bond_sharing.name, "advantage", 4, cost=4)
            )
            self.object.add_advantage(paradox_nullification, 2)
            self.object.spent_freebies.append(
                self.object.freebie_spend_record(paradox_nullification.name, "advantage", 2, cost=2)
            )

            self.object.add_charm(SpiritCharm.objects.get(name="Airt Sense"))

            self.object.freebies -= 1

        self.object.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["date_of_birth"].widget = forms.DateInput(attrs={"type": "date"})
        form.fields["description"].widget.attrs.update(
            {
                "placeholder": "Describe your character's physical appeareance. Be detailed, this will be visible to other players."
            }
        )
        form.fields["history"].widget.attrs.update(
            {
                "placeholder": "Describe character history/backstory. Include information about their childhood, when and how they Awakened, and how they've interacted with mage society since, particularly mentioning important backgrounds."
            }
        )
        form.fields["goals"].widget.attrs.update(
            {
                "placeholder": "Describe your character's long and short term goals, whether personal, professional, or magical."
            }
        )
        form.fields["notes"].widget.attrs.update({"placeholder": "Notes"})
        form.fields["public_info"].widget.attrs.update(
            {
                "placeholder": "This will be displayed to all players who look at your character, include Fame and anything else that would be publicly seen beyond physical description"
            }
        )
        return form


class CompanionFreebiesView(SpecialUserMixin, UpdateView):
    model = Companion
    form_class = CompanionFreebiesForm
    template_name = "characters/mage/companion/chargen.html"

    def form_valid(self, form):
        if form.data["category"] == "-----":
            form.add_error(None, "Must Choose Freebie Expenditure Type")
            return super().form_invalid(form)
        elif form.data["category"] == "MeritFlaw" and (
            form.data["example"] == "" or form.data["value"] == ""
        ):
            form.add_error(None, "Must Choose Merit/Flaw and rating")
            return super().form_invalid(form)
        elif (
            form.data["category"]
            in [
                "Attribute",
                "Ability",
                "New Background",
                "Existing Background",
            ]
            and form.data["example"] == ""
        ):
            form.add_error(None, "Must Choose Trait")
            return super().form_invalid(form)
        trait_type = form.data["category"].lower()
        if "background" in trait_type:
            trait_type = "background"
        cost = self.object.freebie_cost(trait_type)
        if cost == "rating":
            cost = int(form.data["value"])
        if cost > self.object.freebies:
            form.add_error(None, "Not Enough Freebies!")
            return super().form_invalid(form)
        if form.data["category"] == "Attribute":
            trait = Attribute.objects.get(pk=form.data["example"])
            value = getattr(self.object, trait.property_name) + 1
            self.object.add_attribute(trait.property_name)
            self.object.freebies -= cost
            trait = trait.name
        elif form.data["category"] == "Ability":
            trait = Ability.objects.get(pk=form.data["example"])
            value = getattr(self.object, trait.property_name) + 1
            self.object.add_ability(trait.property_name)
            self.object.freebies -= cost
            trait = trait.name
        elif form.data["category"] == "New Background":
            trait = Background.objects.get(pk=form.data["example"])
            cost *= trait.multiplier
            value = 1
            BackgroundRating.objects.create(
                bg=trait, rating=1, char=self.object, note=form.data["note"]
            )
            self.object.freebies -= cost
            trait = str(trait)
            if form.data["note"]:
                trait += f" ({form.data['note']})"
        elif form.data["category"] == "Existing Background":
            trait = BackgroundRating.objects.get(pk=form.data["example"])
            cost *= trait.bg.multiplier
            value = trait.rating + 1
            trait.rating += 1
            trait.save()
            self.object.freebies -= cost
            trait = str(trait)
        elif form.data["category"] == "Willpower":
            trait = "Willpower"
            cost *= 2
            value = self.object.willpower + 1
            self.object.add_willpower()
            self.object.freebies -= cost
        elif form.data["category"] == "MeritFlaw":
            trait = MeritFlaw.objects.get(pk=form.data["example"])
            value = int(form.data["value"])
            self.object.add_mf(trait, value)
            self.object.freebies -= cost
            trait = trait.name
        elif form.data["category"] == "Advantage":
            trait = Advantage.objects.get(pk=form.data["example"])
            value = int(form.data["value"])
            self.object.add_advantage(trait, value)
            self.object.freebies -= cost
            trait = trait.name
            if trait == "Ferocity":
                r = value // 2
                self.object.rage = r
        elif form.data["category"] == "Charms":
            trait = SpiritCharm.objects.get(pk=form.data["example"])
            cost *= trait.point_cost
            value = cost
            self.object.add_charm(trait)
            self.object.freebies -= cost
            trait = trait.name
        if form.data["category"] != "MeritFlaw":
            self.object.spent_freebies.append(
                self.object.freebie_spend_record(trait, trait_type, value, cost=cost)
            )
        else:
            self.object.spent_freebies.append(
                self.object.freebie_spend_record(trait, trait_type, value, cost=cost)
            )
        if self.object.companion_type == "familiar":
            self.object.essence = self.object.willpower * 5
        if self.object.freebies == 0:
            self.object.creation_status += 1
            if "Language" not in self.object.merits_and_flaws.values_list("name", flat=True):
                self.object.creation_status += 1
                english, _ = Language.objects.get_or_create(name="English")
                self.object.languages.add(english)
            for step in [
                "node",
                "library",
                "wonder",
                "enhancement",
                "sanctum",
                "allies",
            ]:
                bg, _ = Background.objects.get_or_create(
                    property_name=step,
                    defaults={"name": step.replace("_", " ").title()},
                )
                if (
                    BackgroundRating.objects.filter(
                        bg=bg,
                        char=self.object,
                        complete=False,
                    ).count()
                    == 0
                ):
                    self.object.creation_status += 1
                else:
                    self.object.save()
                    break
                self.object.save()
        self.object.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        if form.data["category"] == "-----":
            form.add_error(None, "Must Choose Freebie Expenditure Type")
            return super().form_invalid(form)
        elif form.data["category"] == "MeritFlaw" and (
            form.data["example"] == "" or form.data["value"] == ""
        ):
            form.add_error(None, "Must Choose Merit/Flaw and rating")
            return super().form_invalid(form)
        elif (
            form.data["category"] in ["Attribute", "Ability", "Background"]
            and form.data["example"] == ""
        ):
            form.add_error(None, "Must Choose Trait")
            return super().form_invalid(form)
        return self.form_valid(form)


class CompanionLanguagesView(EditPermissionMixin, FormView):
    form_class = HumanLanguageForm
    template_name = "characters/mage/companion/chargen.html"

    def get_object(self):
        """Return the Human object for permission checking."""
        if not hasattr(self, "object") or self.object is None:
            self.object = get_object_or_404(Human, pk=self.kwargs.get("pk"))
        return self.object

    # Overriding `get_form_kwargs` to pass custom arguments to the form
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        human_pk = self.kwargs.get("pk")
        num_languages = Human.objects.get(pk=human_pk).num_languages()
        kwargs.update({"pk": human_pk, "num_languages": int(num_languages)})
        return kwargs

    # Overriding `form_valid` to handle saving the data
    def form_valid(self, form):
        # Get the human instance from the pased `pk`
        human_pk = self.kwargs.get("pk")
        human = get_object_or_404(Human, pk=human_pk)

        num_languages = form.cleaned_data.get("num_languages", 1)
        for i in range(num_languages):
            language_name = form.cleaned_data.get(f"language_{i}")
            if language_name:
                language, created = Language.objects.get_or_create(name=language_name)
                human.languages.add(language)
        human.creation_status += 1
        human.save()
        return HttpResponseRedirect(human.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = self.get_object()
        return context


class CompanionSpecialtiesView(EditPermissionMixin, FormView):
    form_class = SpecialtiesForm
    template_name = "characters/mage/companion/chargen.html"

    def get_object(self):
        """Return the Companion object for permission checking."""
        if not hasattr(self, "object") or self.object is None:
            self.object = Companion.objects.get(id=self.kwargs["pk"])
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = self.get_object()
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        companion = self.get_object()
        kwargs["object"] = companion
        stats = list(Attribute.objects.all()) + list(Ability.objects.all())
        stats = [x for x in stats if getattr(companion, x.property_name, 0) >= 4] + [
            x
            for x in stats
            if getattr(companion, x.property_name, 0) >= 1
            and x.property_name
            in [
                "arts",
                "athletics",
                "crafts",
                "firearms",
                "larceny",
                "melee",
                "academics",
                "esoterica",
                "lore",
                "politics",
                "science",
            ]
        ]
        kwargs["specialties_needed"] = [x.property_name for x in stats]
        return kwargs

    def form_valid(self, form):
        context = self.get_context_data()
        companion = context["object"]
        for field in form.fields:
            spec = Specialty.objects.get_or_create(name=form.data[field], stat=field)[0]
            companion.specialties.add(spec)
        companion.status = "Sub"
        companion.save()
        return HttpResponseRedirect(companion.get_absolute_url())


class CompanionAlliesView(GenericBackgroundView):
    primary_object_class = Companion
    background_name = "allies"
    form_class = LinkedNPCForm
    template_name = "characters/mage/companion/chargen.html"


class CompanionEnhancementView(MtAEnhancementView):
    template_name = "characters/mage/companion/chargen.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["flaw"].required = True
        return form


class CompanionLibraryView(GenericBackgroundView):
    primary_object_class = Companion
    background_name = "library"
    form_class = LibraryForm
    template_name = "characters/mage/companion/chargen.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        obj = get_object_or_404(self.primary_object_class, pk=self.kwargs.get("pk"))
        form.fields["name"].initial = self.current_background.note or f"{obj.name}'s Library"
        tmp = [obj.affiliation, obj.faction, obj.subfaction]
        tmp = [x.pk for x in tmp if hasattr(x, "pk")]
        form.fields["faction"].queryset = MageFaction.objects.filter(pk__in=tmp)
        return form


class CompanionNodeView(GenericBackgroundView):
    primary_object_class = Companion
    background_name = "node"
    form_class = NodeForm
    template_name = "characters/mage/companion/chargen.html"


class CompanionWonderView(GenericBackgroundView):
    primary_object_class = Companion
    background_name = "wonder"
    form_class = WonderForm
    template_name = "characters/mage/companion/chargen.html"
    multiple_ownership = True


class CompanionSanctumView(GenericBackgroundView):
    primary_object_class = Companion
    background_name = "sanctum"
    form_class = SanctumForm
    template_name = "characters/mage/companion/chargen.html"


class CompanionChantryView(GenericBackgroundView):
    primary_object_class = Companion
    background_name = "chantry"
    form_class = ChantrySelectOrCreateForm
    template_name = "characters/mage/companion/chargen.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["character"] = self.primary_object_class.objects.get(pk=self.kwargs["pk"])
        return kwargs

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.chantry_creation_form.fields["total_points"].initial = self.current_background.rating
        form.chantry_creation_form.fields["total_points"].widget.attrs.update(
            {
                "min": self.current_background.rating,
                "max": self.current_background.rating,
            }
        )
        return form


class CopanionCharacterCreationView(HumanCharacterCreationView):
    view_mapping = {
        1: CompanionAttributeView,
        2: CompanionAbilityView,
        3: CompanionBackgroundsView,
        4: CompanionExtrasView,
        5: CompanionFreebiesView,
        6: CompanionLanguagesView,
        7: CompanionNodeView,
        8: CompanionLibraryView,
        9: CompanionWonderView,
        10: CompanionEnhancementView,
        11: CompanionSanctumView,
        12: CompanionAlliesView,
        13: CompanionChantryView,
        14: CompanionSpecialtiesView,
    }

    model_class = Companion
    key_property = "creation_status"
    default_redirect = CompanionDetailView
