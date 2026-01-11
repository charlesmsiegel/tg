from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import FormView

from characters.models.core.human import Human
from core.mixins import (
    SpendFreebiesPermissionMixin,
)


class GenericBackgroundView(SpendFreebiesPermissionMixin, FormView):
    primary_object_class = Human
    background_name = ""
    multiple_ownership = False
    is_owned = True

    def get_object(self):
        """Return the primary object for permission checking."""
        if not hasattr(self, "object") or self.object is None:
            self.object = get_object_or_404(self.primary_object_class, pk=self.kwargs.get("pk"))
        return self.object

    def special_valid_action(self, background_object):
        return None

    def form_valid(self, form):
        content = self.get_context_data()
        primary_object = content["object"]
        background_object = form.save()
        if self.is_owned:
            if self.multiple_ownership:
                background_object.owned_by.add(primary_object)
            else:
                background_object.owned_by = primary_object
        background_object.owner = primary_object.owner
        background_object.chronicle = primary_object.chronicle
        background_object.status = "Sub"
        self.special_valid_action(background_object)
        background_object.save()

        self.current_background.note = background_object.name
        self.current_background.url = background_object.get_absolute_url()
        self.current_background.complete = True
        self.current_background.save()
        return HttpResponseRedirect(primary_object.get_absolute_url())

    def get_form_kwargs(self):
        """Add obj and npc_role to form kwargs for LinkedNPCForm."""
        kwargs = super().get_form_kwargs()
        obj = get_object_or_404(self.primary_object_class, pk=self.kwargs.get("pk"))
        kwargs["obj"] = obj
        kwargs["npc_role"] = self.background_name
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = self.get_object()
        context["current_background"] = (
            context["object"]
            .backgrounds.filter(bg__property_name=self.background_name, complete=False)
            .first()
        )
        return context

    def get_form(self, form_class=None):
        obj = get_object_or_404(self.primary_object_class, pk=self.kwargs.get("pk"))
        self.current_background = obj.backgrounds.filter(
            bg__property_name=self.background_name, complete=False
        ).first()
        form = super().get_form(form_class)

        # Pass the background_name as npc_role to LinkedNPCForm
        if hasattr(form, "npc_role"):
            form.npc_role = self.background_name

        # Set initial rank if the form has a rank field
        if "rank" in form.fields.keys():
            form.fields["rank"].initial = self.current_background.rating
            form.fields["rank"].widget.attrs.update(
                {
                    "min": self.current_background.rating,
                    "max": self.current_background.rating,
                }
            )
        return form

    def dispatch(self, request, *args, **kwargs):
        obj = get_object_or_404(self.primary_object_class, pk=kwargs.get("pk"))
        if not obj.backgrounds.filter(
            bg__property_name=self.background_name, complete=False
        ).exists():
            obj.creation_status += 1
            obj.save()
            return HttpResponseRedirect(obj.get_absolute_url())
        return super().dispatch(request, *args, **kwargs)
