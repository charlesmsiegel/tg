from chained_select import ChainedChoiceField, ChainedSelectMixin
from core.constants import GameLine
from django import forms
from game.models import ObjectType


class ItemCreationForm(ChainedSelectMixin, forms.Form):
    gameline = ChainedChoiceField(
        choices=[],
        label="Game Line",
    )
    item_type = ChainedChoiceField(
        parent_field="gameline",
        choices_map={},
        label="Item Type",
    )
    name = forms.CharField(
        max_length=100,
        label="Name",
        required=False,
    )
    rank = forms.IntegerField(
        initial=1,
        max_value=5,
    )

    def _format_label(self, name):
        """Format item type labels."""
        # Special cases
        special_labels = {
            "sorcerer_artifact": "Sorcerer Artifact",
            "vampire_artifact": "Vampire Artifact",
        }

        if name in special_labels:
            return special_labels[name]

        # Default: title case with underscores replaced
        return name.replace("_", " ").title()

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user and user.is_authenticated:
            if user.profile.is_st():
                # For STs, show all gamelines and item types
                gamelines_with_items = set()
                all_item_types = ObjectType.objects.filter(type="obj")

                for obj in all_item_types:
                    gamelines_with_items.add(obj.gameline)

                # Create gameline choices
                gameline_choices = [
                    (code, name) for code, name in GameLine.CHOICES if code in gamelines_with_items
                ]
                self.fields["gameline"].choices = gameline_choices

                # Build choices_map for ChainedChoiceField
                choices_map = {}
                for obj in all_item_types:
                    if obj.gameline not in choices_map:
                        choices_map[obj.gameline] = []
                    choices_map[obj.gameline].append((obj.name, self._format_label(obj.name)))

                # Sort each gameline's types by label
                for gameline in choices_map:
                    choices_map[gameline].sort(key=lambda x: x[1])

                self.fields["item_type"].choices_map = choices_map
            else:
                # For regular users, only show mage gameline
                self.fields["gameline"].choices = [("mta", "Mage: the Ascension")]

                mage_items = ObjectType.objects.filter(type="obj", gameline="mta")

                choices_map = {
                    "mta": sorted(
                        [(obj.name, self._format_label(obj.name)) for obj in mage_items],
                        key=lambda x: x[1],
                    )
                }
                self.fields["item_type"].choices_map = choices_map

            # Re-run chain setup after choices are configured
            self._setup_chains()
