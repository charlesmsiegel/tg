from characters.models.changeling.changeling import Changeling
from characters.models.core.merit_flaw_block import MeritFlawRating
from core.views.approved_user_mixin import SpecialUserMixin
from django.views.generic import CreateView, DetailView, UpdateView


class ChangelingDetailView(SpecialUserMixin, DetailView):
    model = Changeling
    template_name = "characters/changeling/changeling/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        specialties = {}
        for attribute in self.object.get_attributes():
            specialties[attribute] = ", ".join(
                [x.name for x in self.object.specialties.filter(stat=attribute)]
            )
        for ability in self.object.get_abilities():
            specialties[ability] = ", ".join(
                [x.name for x in self.object.specialties.filter(stat=ability)]
            )
        for key, value in specialties.items():
            context[f"{key}_spec"] = value

        context["merits_and_flaws"] = MeritFlawRating.objects.order_by(
            "mf__name"
        ).filter(character=self.object)
        context["is_approved_user"] = self.check_if_special_user(
            self.object, self.request.user
        )
        return context


class ChangelingCreateView(CreateView):
    model = Changeling
    fields = [
        "name",
        "description",
        "strength",
        "dexterity",
        "stamina",
        "perception",
        "intelligence",
        "wits",
        "charisma",
        "manipulation",
        "appearance",
        "alertness",
        "athletics",
        "brawl",
        "empathy",
        "expression",
        "intimidation",
        "streetwise",
        "subterfuge",
        "crafts",
        "drive",
        "etiquette",
        "firearms",
        "melee",
        "stealth",
        "academics",
        "computer",
        "investigation",
        "medicine",
        "science",
        "willpower",
        "age",
        "apparent_age",
        "history",
        "goals",
        "notes",
        "kenning",
        "leadership",
        "animal_ken",
        "larceny",
        "performance",
        "survival",
        "enigmas",
        "gremayre",
        "law",
        "politics",
        "technology",
        "court",
        "seeming",
        "autumn",
        "chicanery",
        "chronos",
        "contract",
        "dragons_ire",
        "legerdemain",
        "metamorphosis",
        "naming",
        "oneiromancy",
        "primal",
        "pyretics",
        "skycraft",
        "soothsay",
        "sovereign",
        "spring",
        "summer",
        "wayfare",
        "winter",
        "actor",
        "fae",
        "nature_realm",
        "prop",
        "scene",
        "time",
        "banality",
        "glamour",
        "musing_threshold",
        "ravaging_threshold",
        "antithesis",
        "true_name",
        "date_ennobled",
        "crysalis",
        "date_of_crysalis",
        "fae_mien",
    ]
    template_name = "characters/changeling/changeling/form.html"


class ChangelingUpdateView(SpecialUserMixin, UpdateView):
    model = Changeling
    fields = [
        "name",
        "description",
        "strength",
        "dexterity",
        "stamina",
        "perception",
        "intelligence",
        "wits",
        "charisma",
        "manipulation",
        "appearance",
        "alertness",
        "athletics",
        "brawl",
        "empathy",
        "expression",
        "intimidation",
        "streetwise",
        "subterfuge",
        "crafts",
        "drive",
        "etiquette",
        "firearms",
        "melee",
        "stealth",
        "academics",
        "computer",
        "investigation",
        "medicine",
        "science",
        "willpower",
        "age",
        "apparent_age",
        "history",
        "goals",
        "notes",
        "kenning",
        "leadership",
        "animal_ken",
        "larceny",
        "performance",
        "survival",
        "enigmas",
        "gremayre",
        "law",
        "politics",
        "technology",
        "court",
        "seeming",
        "autumn",
        "chicanery",
        "chronos",
        "contract",
        "dragons_ire",
        "legerdemain",
        "metamorphosis",
        "naming",
        "oneiromancy",
        "primal",
        "pyretics",
        "skycraft",
        "soothsay",
        "sovereign",
        "spring",
        "summer",
        "wayfare",
        "winter",
        "actor",
        "fae",
        "nature_realm",
        "prop",
        "scene",
        "time",
        "banality",
        "glamour",
        "musing_threshold",
        "ravaging_threshold",
        "antithesis",
        "true_name",
        "date_ennobled",
        "crysalis",
        "date_of_crysalis",
        "fae_mien",
    ]
    template_name = "characters/changeling/changeling/form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_approved_user"] = self.check_if_special_user(
            self.object, self.request.user
        )
        return context
