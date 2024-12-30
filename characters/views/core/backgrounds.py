from characters.forms.core.backgroundform import BackgroundRatingFormSet
from characters.models.core.background_block import Background
from characters.models.core.human import Human
from core.views.approved_user_mixin import SpecialUserMixin
from django.views.generic import FormView


class HumanBackgroundsView(SpecialUserMixin, FormView):
    form_class = BackgroundRatingFormSet
    template_name = "characters/core/human/chargen.html"

    def get_success_url(self):
        return Human.objects.get(pk=self.kwargs["pk"]).get_absolute_url()

    def form_valid(self, form):
        self.get_context_data()
        total_bg = sum(
            [
                f.cleaned_data["rating"] * f.cleaned_data["bg"].multiplier
                for f in form
                if "rating" in f.cleaned_data.keys() and "bg" in f.cleaned_data.keys()
            ]
        )
        if total_bg != self.object.background_points:
            for f in form:
                f.add_error(
                    None,
                    f"Backgrounds must total {self.object.background_points} points",
                )
            return super().form_invalid(form)
        form.save()
        self.object.creation_status += 1
        self.object.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["character"] = Human.objects.get(pk=self.kwargs["pk"])
        return kwargs

    def get_form(self, form_class=None):
        form_class = self.get_form_class()
        return form_class(**self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = Human.objects.get(pk=self.kwargs["pk"])
        context["object"] = self.object
        context["is_approved_user"] = self.check_if_special_user(
            self.object, self.request.user
        )
        for form in context["form"]:
            form.fields["bg"].queryset = Background.objects.filter(
                property_name__in=self.object.allowed_backgrounds
            )

        empty_form = context["form"].empty_form
        empty_form.fields["bg"].queryset = Background.objects.filter(
            property_name__in=self.object.allowed_backgrounds
        )
        context["empty_form"] = empty_form
        return context
