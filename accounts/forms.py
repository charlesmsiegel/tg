from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from accounts.models import Profile
from characters.models.core.human import Human


class CustomAuthenticationForm(AuthenticationForm):
    """Custom authentication form with tg-form-control styling"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add tg-form-control class to all fields
        self.fields["username"].widget.attrs.update(
            {"class": "tg-form-control", "placeholder": "Enter your username"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "tg-form-control", "placeholder": "Enter your password"}
        )


class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form with email field and tg-form-control styling."""

    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add tg-form-control class to all fields
        for field_name in self.fields:
            existing_classes = self.fields[field_name].widget.attrs.get("class", "")
            if existing_classes:
                self.fields[field_name].widget.attrs[
                    "class"
                ] = f"{existing_classes} tg-form-control"
            else:
                self.fields[field_name].widget.attrs["class"] = "tg-form-control"

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")

        if username and email and username == email:
            raise forms.ValidationError("Username and Email must be distinct")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "preferred_heading",
            "theme",
            "highlight_text",
            "discord_id",
            "lines",
            "veils",
            "discord_toggle",
            "lines_toggle",
            "veils_toggle",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["discord_id"].required = False

        # Add tg-form-control class to text inputs and selects
        for field_name, field in self.fields.items():
            if field_name in [
                "preferred_heading",
                "theme",
                "discord_id",
                "lines",
                "veils",
            ]:
                field.widget.attrs.update({"class": "tg-form-control"})
            elif field_name in [
                "highlight_text",
                "discord_toggle",
                "lines_toggle",
                "veils_toggle",
            ]:
                field.widget.attrs.update({"class": "tg-form-check-input"})


class SceneXP(forms.Form):
    """Form for awarding XP to characters in a scene."""

    def __init__(self, *args, **kwargs):
        self.scene = kwargs.pop("scene")
        super().__init__(*args, **kwargs)
        for character in self.scene.characters.player_characters():
            self.fields[f"{character.name}"] = forms.BooleanField(required=False)

    def save(self):
        """Save XP awards using the Scene model's business logic."""
        self.scene.award_xp(self.cleaned_data)

    def clean(self):
        cleaned_data = super().clean()
        # Map character names to Character objects, preserving the boolean value
        return {self.scene.characters.get(name=k): v for k, v in cleaned_data.items()}


class StoryXP(forms.Form):
    def __init__(self, *args, **kwargs):
        self.story = kwargs.pop("story")
        super().__init__(*args, **kwargs)
        self.char_list = Human.objects.filter(status="App")
        for char in self.char_list:
            for topic in ["success", "danger", "growth", "drama"]:
                self.fields[f"{char.name}-{topic}"] = forms.BooleanField(required=False)
            self.fields[f"{char.name}-duration"] = forms.IntegerField(
                initial=0, required=False, widget=forms.NumberInput(attrs={"size": "5"})
            )

    def save(self, commit=True):
        """Save XP awards using the Story model's business logic."""
        self.story.award_xp(self.cleaned_data)

    def clean(self):
        cleaned_data = super().clean()
        result = {}
        for char in self.char_list:
            # Use cleaned_data with proper field names instead of raw self.data
            result[char] = {
                "success": cleaned_data.get(f"{char.name}-success", False),
                "danger": cleaned_data.get(f"{char.name}-danger", False),
                "growth": cleaned_data.get(f"{char.name}-growth", False),
                "drama": cleaned_data.get(f"{char.name}-drama", False),
                "duration": cleaned_data.get(f"{char.name}-duration") or 0,
            }
        return result


class FreebieAwardForm(forms.Form):
    backstory_freebies = forms.IntegerField(min_value=0, max_value=15, initial=0)

    def __init__(self, *args, **kwargs):
        self.character = kwargs.pop("character")
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        """Save freebie awards using the Character model's business logic."""
        return self.character.award_backstory_freebies(self.cleaned_data["backstory_freebies"])
