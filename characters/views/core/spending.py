"""Freebie form orchestration; spending rules remain in the existing services."""

from types import SimpleNamespace

from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.views.generic import UpdateView

from characters.chargen import get_workflow
from characters.chargen.transitions import advance
from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.core.background_block import Background, BackgroundRating
from characters.models.core.merit_flaw_block import MeritFlaw
from characters.models.core.statistic import Statistic
from characters.models.mage.focus import Practice, Tenet
from characters.models.mage.sphere import Sphere
from characters.models.vampire.discipline import Discipline
from characters.services.freebie_spending import FreebieSpendingServiceFactory
from characters.views.core.chargen_mixins import ChargenStepMixin
from core.mixins import SpendFreebiesPermissionMixin


class FreebieSpendingView(ChargenStepMixin, SpendFreebiesPermissionMixin, UpdateView):
    """Validate a form, adapt its choices, spend, and advance once when exhausted."""

    example_models = {
        "Attribute": Attribute,
        "Ability": Ability,
        "MeritFlaw": MeritFlaw,
        "Art": Statistic,
        "Realm": Statistic,
        "Discipline": Discipline,
        "Sphere": Sphere,
        "Tenet": Tenet,
        "Practice": Practice,
    }
    category_aliases = {"Rotes": "Rote Points"}

    def resolve_choice(self, model, value, **filters):
        if isinstance(value, model):
            return value
        try:
            return model.objects.get(pk=value, **filters)
        except (model.DoesNotExist, TypeError, ValueError):
            raise ValidationError("Must Choose Trait") from None

    def get_spending_kwargs(self, form):
        data = form.cleaned_data
        category = self.category_aliases.get(data["category"], data["category"])
        example = data.get("example")
        if category in {"Background", "New Background", "Existing Background"}:
            if isinstance(example, BackgroundRating):
                example = self.resolve_choice(BackgroundRating, example.pk, char=self.object)
            elif not isinstance(example, Background):
                raw = str(example or "")
                if raw.startswith("bg_"):
                    example = self.resolve_choice(Background, raw[3:])
                elif raw.startswith(("br_", "bgr_")):
                    example = self.resolve_choice(
                        BackgroundRating, raw.split("_", 1)[1], char=self.object
                    )
                else:
                    raise ValidationError("Invalid background selection")
        elif category in self.example_models:
            example = self.resolve_choice(self.example_models[category], example)
        elif category == "Arete" and isinstance(example, str):
            # The chained form selects the next level, not a Practice object.
            # The service already calculates and validates that level itself.
            example = None
        elif category == "Virtue" and isinstance(example, str):
            # Chained forms identify built-in virtues by their property names.
            if not example:
                raise ValidationError("Must Choose Trait")
            example = SimpleNamespace(name=example.replace("_", " ").title(), property_name=example)
        value = data.get("value")
        if category == "Advantage" and value in (None, ""):
            raise ValidationError("Must Choose Advantage and rating")
        if value not in (None, ""):
            try:
                value = int(value)
            except (ValueError, TypeError):
                raise ValidationError("Invalid trait rating") from None
        kwargs = {
            "category": category,
            "example": example,
            "value": value,
            "note": data.get("note", ""),
            "pooled": data.get("pooled", False),
        }
        if "resonance" in data:
            kwargs["resonance"] = data["resonance"]
        return kwargs

    def form_valid(self, form):
        if not form.is_valid():
            return self.form_invalid(form)
        try:
            kwargs = self.get_spending_kwargs(form)
        except ValidationError as error:
            form.add_error(None, error)
            return self.form_invalid(form)
        service = FreebieSpendingServiceFactory.get_service(self.object)
        result = service.spend(**kwargs)
        if not result.success:
            form.add_error(None, result.error)
            return self.form_invalid(form)
        workflow = get_workflow(self.object.type)
        if (
            self.object.freebies == 0
            and workflow
            and 1 <= self.object.creation_status <= len(workflow.steps)
            and workflow.step(self.object.creation_status).key == "freebies"
        ):
            advance(self.object, user=self.request.user)
        return HttpResponseRedirect(self.get_success_url())
