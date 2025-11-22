from characters.models.werewolf.garou import Werewolf
from characters.models.werewolf.gift import GiftPermission
from django import forms
from django.core.exceptions import ValidationError


class WerewolfCreationForm(forms.ModelForm):
    class Meta:
        model = Werewolf
        fields = [
            "name",
            "concept",
            "chronicle",
            "breed",
            "auspice",
            "tribe",
            "image",
            "npc",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        self.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        self.fields["concept"].widget.attrs.update(
            {"placeholder": "Enter concept here"}
        )
        self.fields["image"].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:  # If we have a user
            instance.owner = self.user
        if commit:
            instance.save()
        return instance


class WerewolfGiftsForm(forms.ModelForm):
    """Form for selecting starting Gifts during character creation."""

    class Meta:
        model = Werewolf
        fields = ["gifts"]

    def clean_gifts(self):
        """Validate that exactly 3 gifts are selected: one from breed, auspice, and tribe."""
        gifts = self.cleaned_data.get("gifts")

        if not gifts:
            raise ValidationError("You must select gifts.")

        # Check total count
        if gifts.count() != 3:
            raise ValidationError("You must select exactly 3 starting Gifts.")

        # Get the character instance
        instance = self.instance

        # Check that character has required attributes
        if not instance.tribe:
            raise ValidationError("You must have a tribe to select starting Gifts.")

        # Get permission objects
        breed_perm = GiftPermission.objects.get_or_create(
            shifter="werewolf", condition=instance.breed
        )[0]
        auspice_perm = GiftPermission.objects.get_or_create(
            shifter="werewolf", condition=instance.auspice
        )[0]
        tribe_perm = GiftPermission.objects.get_or_create(
            shifter="werewolf", condition=instance.tribe.name
        )[0]

        # Count gifts from each category
        breed_count = sum(1 for gift in gifts if breed_perm in gift.allowed.all())
        auspice_count = sum(1 for gift in gifts if auspice_perm in gift.allowed.all())
        tribe_count = sum(1 for gift in gifts if tribe_perm in gift.allowed.all())

        # Validate distribution
        if breed_count != 1 or auspice_count != 1 or tribe_count != 1:
            raise ValidationError(
                "You must select exactly one Gift from your Breed, one from your Auspice, "
                "and one from your Tribe."
            )

        return gifts


class WerewolfHistoryForm(forms.ModelForm):
    """Form for entering First Change history during character creation."""

    class Meta:
        model = Werewolf
        fields = ["first_change", "age_of_first_change"]

    def clean_first_change(self):
        """Validate that First Change description is provided."""
        first_change = self.cleaned_data.get("first_change")

        if not first_change or first_change.strip() == "":
            raise ValidationError("You must describe your First Change.")

        return first_change

    def clean_age_of_first_change(self):
        """Validate that age of First Change is valid."""
        age_of_first_change = self.cleaned_data.get("age_of_first_change")

        if age_of_first_change is None:
            raise ValidationError("Age of First Change is required.")

        if age_of_first_change <= 0:
            raise ValidationError("Age of First Change must be greater than 0.")

        # Validate against current age (instance must exist)
        if self.instance and self.instance.age:
            if age_of_first_change >= self.instance.age:
                raise ValidationError(
                    f"Age of First Change must be less than current age ({self.instance.age})."
                )

        return age_of_first_change
