from accounts.models import Profile
from characters.models.core.human import Human
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUSerCreationForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def is_valid(self):
        if self.data["username"] == self.data["email"]:
            self.add_error(None, "Username and Email must be distinct")
            return False
        return super().is_valid()

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


class SceneXP(forms.Form):
    def __init__(self, *args, **kwargs):
        self.scene = kwargs.pop("scene")
        super().__init__(*args, **kwargs)
        for character in self.scene.characters.filter(npc=False):
            self.fields[f"{character.name}"] = forms.BooleanField(required=False)

    def save(self):
        self.scene.xp_given = True
        self.scene.save()
        for char in self.cleaned_data.keys():
            if self.cleaned_data[char]:
                char.xp += 1
                char.save()

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data = {
            self.scene.characters.get(name=k): v for k, v in cleaned_data.items()
        }
        for key1 in cleaned_data.keys():
            for key2 in self.data.keys():
                if key1.name in key2:
                    cleaned_data[key1] = True
        return cleaned_data


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
        for char in self.cleaned_data.keys():
            total_gain = self.cleaned_data[char]["duration"]
            if self.cleaned_data[char]["success"]:
                total_gain += 1
            if self.cleaned_data[char]["danger"]:
                total_gain += 1
            if self.cleaned_data[char]["growth"]:
                total_gain += 1
            if self.cleaned_data[char]["drama"]:
                total_gain += 1
            char.xp += total_gain
            char.save()
        self.story.xp_given = True
        self.story.save()

    def clean(self):
        cleaned_data = super().clean()
        tmp = {}
        for char in self.char_list:
            relevant_data = {k: v for k, v in self.data.items() if char.name in k}
            char_dict = {
                "success": False,
                "danger": False,
                "growth": False,
                "drama": False,
                "duration": 0,
            }
            for item in relevant_data.keys():
                keyname = item.split("-")[-1]
                if keyname != "duration":
                    char_dict[keyname] = (
                        relevant_data[f"story_{self.story.pk}-{char.name}-{keyname}"]
                        == "on"
                    )
                else:
                    char_dict[keyname] = int(
                        relevant_data[f"story_{self.story.pk}-{char.name}-{keyname}"]
                    )

            tmp[char] = char_dict
        return tmp


class FreebieAwardForm(forms.Form):
    backstory_freebies = forms.IntegerField(min_value=0, max_value=15, initial=0)

    def __init__(self, *args, **kwargs):
        self.character = kwargs.pop("character")
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        self.character.freebies += self.cleaned_data["backstory_freebies"]
        self.character.freebies_approved = True
        self.character.save()
        return self.character
