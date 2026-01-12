
from characters.forms.core.freebies import HumanFreebiesForm


class WraithFreebiesForm(HumanFreebiesForm):
    """Freebie form for Wraith characters with Wraith-specific categories."""

    def __init__(self, *args, suggestions=None, **kwargs):
        super().__init__(*args, **kwargs)

        # No need to add custom category choices here - categories are determined
        # dynamically by get_category_functions() in the view
