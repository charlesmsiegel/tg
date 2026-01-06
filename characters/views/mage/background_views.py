from typing import Any

from characters.forms.mage.enhancements import EnhancementForm
from characters.models.core.background_block import Background, BackgroundRating
from characters.models.core.human import Human
from core.mixins import SpendFreebiesPermissionMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import FormView


class MtAEnhancementView(SpendFreebiesPermissionMixin, FormView):
    form_class = EnhancementForm
    template_name = "characters/mage/mage/chargen.html"

    potential_skip = [
        "sanctum",
        "allies",
    ]

    def get_object(self):
        """Return the Human object for permission checking."""
        if not hasattr(self, "object") or self.object is None:
            self.object = get_object_or_404(Human, pk=self.kwargs.get("pk"))
        return self.object

    def dispatch(self, request, *args, **kwargs):
        obj = get_object_or_404(Human, pk=kwargs.get("pk"))
        if not obj.backgrounds.filter(bg__property_name="enhancement", complete=False).exists():
            obj.creation_status += 1
            obj.save()
            return HttpResponseRedirect(obj.get_absolute_url())
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        obj = Human.objects.get(id=self.kwargs["pk"])
        enhancement_bg, _ = Background.objects.get_or_create(
            property_name="enhancement", defaults={"name": "Enhancement"}
        )
        self.current_enhancement = BackgroundRating.objects.filter(
            char=obj,
            bg=enhancement_bg,
            complete=False,
        ).first()
        kwargs["rank"] = self.current_enhancement.rating
        return kwargs

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        obj = get_object_or_404(Human, pk=self.kwargs.get("pk"))
        enhancement_bg, _ = Background.objects.get_or_create(
            property_name="enhancement", defaults={"name": "Enhancement"}
        )
        self.current_enhancement = BackgroundRating.objects.filter(
            char=obj,
            bg=enhancement_bg,
            complete=False,
        ).first()
        return form

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["object"] = self.get_object()
        context["current_enhancement"] = self.current_enhancement
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        obj = context["object"]
        # Save the form data
        form.save(char=obj)

        # Check if there are more enhancements to complete
        enhancement_bg, _ = Background.objects.get_or_create(
            property_name="enhancement", defaults={"name": "Enhancement"}
        )
        if (
            BackgroundRating.objects.filter(
                char=obj,
                bg=enhancement_bg,
                complete=False,
            ).count()
            == 0
        ):
            obj.creation_status += 1
            obj.save()
            for step in self.potential_skip:
                bg, _ = Background.objects.get_or_create(
                    property_name=step,
                    defaults={"name": step.replace("_", " ").title()},
                )
                if (
                    BackgroundRating.objects.filter(
                        bg=bg,
                        char=obj,
                        complete=False,
                    ).count()
                    == 0
                ):
                    obj.creation_status += 1
                else:
                    obj.save()
                    break
            obj.save()
        return HttpResponseRedirect(obj.get_absolute_url())
