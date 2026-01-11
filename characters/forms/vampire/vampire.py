from characters.models.vampire.clan import VampireClan
from characters.models.vampire.path import Path
from characters.models.vampire.sect import VampireSect
from characters.models.vampire.vampire import Vampire
from django import forms


class VampireCreationForm(forms.ModelForm):
    class Meta:
        model = Vampire
        fields = [
            "name",
            "nature",
            "demeanor",
            "concept",
            "clan",
            "sect",
            "sire",
            "path",
            "chronicle",
            "image",
            "npc",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        # Set up querysets
        self.fields["clan"].queryset = VampireClan.objects.filter(is_bloodline=False)
        self.fields["sect"].queryset = VampireSect.objects.all()
        self.fields["path"].queryset = Path.objects.all()
        self.fields["sire"].queryset = Vampire.objects.none()

        # Placeholders
        self.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        self.fields["concept"].widget.attrs.update({"placeholder": "Enter concept here"})
        self.fields["image"].required = False
        self.fields["sire"].required = False
        self.fields["path"].required = False

        if self.is_bound:
            self.fields["sire"].queryset = Vampire.objects.all()

    def _post_clean(self):
        """Override to set path_rating before model validation runs."""
        from django.forms.models import construct_instance

        opts = self._meta
        exclude = self._get_validation_exclusions()

        # Construct instance first
        try:
            self.instance = construct_instance(
                self, self.instance, opts.fields, opts.exclude
            )
        except ValueError as e:
            self._update_errors(e)
            return

        # Set path_rating if a path is selected
        if self.instance.path and self.instance.path_rating < 4:
            self.instance.path_rating = 4

        # Now run model validation
        try:
            self.instance.full_clean(exclude=exclude, validate_unique=False)
        except forms.ValidationError as e:
            self._update_errors(e)

        try:
            self.validate_unique()
        except forms.ValidationError as e:
            self._update_errors(e)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.owner = self.user
        if commit:
            instance.save()
        return instance
