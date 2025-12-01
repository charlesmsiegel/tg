from characters.models.core import CharacterModel
from django import forms
from game.models import Story, WeeklyXPRequest
from locations.models.core import LocationModel


class SceneCreationForm(forms.Form):
    name = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"placeholder": "Scene Title"})
    )
    location = forms.ModelChoiceField(
        queryset=LocationModel.objects.order_by("name"), empty_label="Scene Location"
    )
    date_of_scene = forms.CharField(max_length=100, widget=forms.DateInput(attrs={"type": "date"}))

    def __init__(self, *args, **kwargs):
        chronicle = kwargs.pop("chronicle")
        super().__init__(*args, **kwargs)
        self.fields["location"].queryset = LocationModel.objects.filter(
            chronicle=chronicle
        ).order_by("name")


class AddCharForm(forms.Form):
    character_to_add = forms.ModelChoiceField(
        queryset=CharacterModel.objects.none(), empty_label="Add Character"
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        scene = kwargs.pop("scene")
        super().__init__(*args, **kwargs)
        self.fields["character_to_add"].queryset = CharacterModel.objects.filter(
            owner=user, chronicle=scene.chronicle
        ).exclude(pk__in=scene.characters.all())


class PostForm(forms.Form):
    character = forms.ModelChoiceField(
        queryset=CharacterModel.objects.none(), empty_label="Character Select"
    )
    display_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.Textarea(
            attrs={"placeholder": "Display Name (Optional)", "rows": 1, "cols": 25}
        ),
    )
    message = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Message"}))

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        scene = kwargs.pop("scene")
        super().__init__(*args, **kwargs)
        self.fields["character"].queryset = CharacterModel.objects.filter(
            owner=user,
            chronicle=scene.chronicle,
            pk__in=scene.characters.all(),
        )

    def clean(self):
        cleaned_data = super().clean()

        if "character" in self.errors.keys():
            del self.errors["character"]

        message = cleaned_data.get("message")

        # Validate the message content (example: no prohibited words or empty message)
        if not message or len(message.strip()) == 0:
            raise forms.ValidationError("The message cannot be empty.")
        return cleaned_data


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ("name",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"placeholder": "Story Name"})


class JournalEntryForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    message = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Message"}))

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop("instance")
        super().__init__(*args, **kwargs)
        self.fields["message"].widget.attrs.update({"placeholder": "Journal Entry"})

    def save(self, commit=True):
        return self.instance.add_post(self.cleaned_data["date"], self.cleaned_data["message"])


class STResponseForm(forms.Form):
    st_message = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Message"}))

    def __init__(self, *args, **kwargs):
        self.entry = kwargs.pop("entry")
        super().__init__(*args, **kwargs)
        self.fields["st_message"].widget.attrs.update({"placeholder": "Journal Response"})

    def save(self, commit=True):
        self.entry.st_message = self.cleaned_data["st_message"]
        self.entry.save()


class WeeklyXPRequestForm(forms.ModelForm):
    class Meta:
        model = WeeklyXPRequest
        fields = [
            "finishing",
            "learning",
            "rp",
            "focus",
            "standingout",
            "learning_scene",
            "rp_scene",
            "focus_scene",
            "standingout_scene",
        ]

    def __init__(self, *args, **kwargs):
        self.character = kwargs.pop("character", None)
        self.week = kwargs.pop("week", None)
        super().__init__(*args, **kwargs)
        self.fields["learning_scene"].queryset = (
            self.week.finished_scenes().filter(characters=self.character) if self.week else None
        )
        self.fields["rp_scene"].queryset = (
            self.week.finished_scenes().filter(characters=self.character) if self.week else None
        )
        self.fields["focus_scene"].queryset = (
            self.week.finished_scenes().filter(characters=self.character) if self.week else None
        )
        self.fields["standingout_scene"].queryset = (
            self.week.finished_scenes().filter(characters=self.character) if self.week else None
        )
        self.fields["finishing"].required = False
        self.fields["learning_scene"].required = False
        self.fields["rp_scene"].required = False
        self.fields["focus_scene"].required = False
        self.fields["standingout_scene"].required = False

    def player_save(self, commit=True):
        if not self.instance.pk:
            self.instance = super().save(commit=False)
        self.instance.finishing = True
        self.instance.week = self.week
        self.instance.character = self.character
        if commit:
            self.instance.save()
        return self.instance

    def st_save(self, commit=True):
        # Directly modify the instance bound to the form
        self.instance.approved = True
        self.instance.finishing = self.cleaned_data["finishing"]
        self.instance.learning = self.cleaned_data["learning"]
        self.instance.rp = self.cleaned_data["rp"]
        self.instance.focus = self.cleaned_data["focus"]
        self.instance.standingout = self.cleaned_data["standingout"]

        # Update character XP based on the form fields
        xp_increase = sum(
            [
                self.instance.finishing,
                self.instance.learning,
                self.instance.rp,
                self.instance.focus,
                self.instance.standingout,
            ]
        )
        self.character.xp += xp_increase
        self.character.save()

        if commit:
            self.instance.save()
        return self.instance

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data["learning"]:
            if cleaned_data["learning_scene"] is None:
                raise forms.ValidationError("Must include scene for any XP claimed")
        if cleaned_data["rp"]:
            if cleaned_data["rp_scene"] is None:
                raise forms.ValidationError("Must include scene for any XP claimed")
        if cleaned_data["focus"]:
            if cleaned_data["focus_scene"] is None:
                raise forms.ValidationError("Must include scene for any XP claimed")
        if cleaned_data["standingout"]:
            if cleaned_data["standingout_scene"] is None:
                raise forms.ValidationError("Must include scene for any XP claimed")
        return cleaned_data
