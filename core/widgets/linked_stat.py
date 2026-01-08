"""
Linked Stat Widget for Django Forms

A composite widget for editing paired permanent/temporary stats in WoD games.
Displays both values with appropriate controls and validation.
"""

from django import forms
from django.utils.safestring import mark_safe


class LinkedStatWidget(forms.MultiWidget):
    """
    A composite widget for editing linked permanent/temporary stats.

    Displays two number inputs (or selects) side by side, with optional
    labels and visual indicators for the permanent/temporary relationship.

    Usage:
        class WillpowerForm(forms.Form):
            willpower = LinkedStatFormField(
                max_value=10,
                widget=LinkedStatWidget(max_value=10)
            )

    Args:
        max_value: Maximum value for both fields (default 10)
        min_permanent: Minimum permanent value (default 1)
        min_temporary: Minimum temporary value (default 0)
        use_select: Use select dropdowns instead of number inputs
        show_labels: Show 'Permanent' and 'Temporary' labels
        permanent_label: Custom label for permanent field
        temporary_label: Custom label for temporary field
        attrs: Additional HTML attributes
    """

    template_name = "core/widgets/linked_stat.html"

    def __init__(
        self,
        max_value=10,
        min_permanent=1,
        min_temporary=0,
        use_select=False,
        show_labels=True,
        permanent_label="Permanent",
        temporary_label="Temporary",
        attrs=None,
    ):
        self.max_value = max_value
        self.min_permanent = min_permanent
        self.min_temporary = min_temporary
        self.use_select = use_select
        self.show_labels = show_labels
        self.permanent_label = permanent_label
        self.temporary_label = temporary_label

        if use_select:
            perm_choices = [(i, str(i)) for i in range(min_permanent, max_value + 1)]
            temp_choices = [(i, str(i)) for i in range(min_temporary, max_value + 1)]
            widgets = [
                forms.Select(attrs={"class": "form-select linked-stat-permanent"}),
                forms.Select(attrs={"class": "form-select linked-stat-temporary"}),
            ]
            widgets[0].choices = perm_choices
            widgets[1].choices = temp_choices
        else:
            widgets = [
                forms.NumberInput(
                    attrs={
                        "class": "form-control linked-stat-permanent",
                        "min": min_permanent,
                        "max": max_value,
                    }
                ),
                forms.NumberInput(
                    attrs={
                        "class": "form-control linked-stat-temporary",
                        "min": min_temporary,
                        "max": max_value,
                    }
                ),
            ]

        super().__init__(widgets, attrs)

    def decompress(self, value):
        """
        Split a combined value into [permanent, temporary].

        Accepts:
        - tuple/list: (permanent, temporary)
        - dict: {'permanent': x, 'temporary': y}
        - LinkedStatAccessor: extracts permanent/temporary
        - single int: uses as both permanent and temporary
        """
        if value is None:
            return [self.min_permanent, self.min_temporary]

        if isinstance(value, (list, tuple)):
            return list(value[:2])

        if isinstance(value, dict):
            return [
                value.get("permanent", self.min_permanent),
                value.get("temporary", self.min_temporary),
            ]

        # Check for LinkedStatAccessor (duck typing to avoid circular import)
        if hasattr(value, "permanent") and hasattr(value, "temporary"):
            return [value.permanent, value.temporary]

        # Single int - use for both
        if isinstance(value, int):
            return [value, value]

        return [self.min_permanent, self.min_temporary]

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["show_labels"] = self.show_labels
        context["widget"]["permanent_label"] = self.permanent_label
        context["widget"]["temporary_label"] = self.temporary_label
        return context

    def render(self, name, value, attrs=None, renderer=None):
        """
        Render the widget with permanent/temporary inputs.
        """
        if attrs is None:
            attrs = {}

        # Get decompressed values
        values = self.decompress(value)

        # Render each sub-widget
        widgets_html = []
        for i, (widget, val) in enumerate(zip(self.widgets, values)):
            widget_name = f"{name}_{i}"
            widget_id = f"{attrs.get('id', name)}_{i}"
            widget_attrs = {**attrs, "id": widget_id}
            widgets_html.append(widget.render(widget_name, val, widget_attrs, renderer))

        # Build the combined HTML
        html_parts = ['<div class="linked-stat-widget">']

        if self.show_labels:
            html_parts.append(
                f'<div class="linked-stat-row">'
                f'<label class="linked-stat-label">{self.permanent_label}</label>'
                f"{widgets_html[0]}"
                f"</div>"
            )
            html_parts.append(
                f'<div class="linked-stat-row">'
                f'<label class="linked-stat-label">{self.temporary_label}</label>'
                f"{widgets_html[1]}"
                f"</div>"
            )
        else:
            html_parts.append(
                f'<div class="linked-stat-row">'
                f"{widgets_html[0]}"
                f'<span class="linked-stat-separator">/</span>'
                f"{widgets_html[1]}"
                f"</div>"
            )

        html_parts.append("</div>")

        # Add JavaScript for constraint enforcement
        html_parts.append(
            f"""
<script>
(function() {{
    const permInput = document.getElementById('{attrs.get('id', name)}_0');
    const tempInput = document.getElementById('{attrs.get('id', name)}_1');

    function enforceConstraint() {{
        const permVal = parseInt(permInput.value) || 0;
        const tempVal = parseInt(tempInput.value) || 0;

        // Update temporary max to match permanent
        if (tempInput.type === 'number') {{
            tempInput.max = permVal;
        }}

        // Cap temporary at permanent
        if (tempVal > permVal) {{
            tempInput.value = permVal;
        }}
    }}

    permInput.addEventListener('change', enforceConstraint);
    permInput.addEventListener('input', enforceConstraint);
    enforceConstraint();
}})();
</script>
"""
        )

        return mark_safe("".join(html_parts))

    def value_from_datadict(self, data, files, name):
        """Extract the two values from form submission."""
        return [
            widget.value_from_datadict(data, files, f"{name}_{i}")
            for i, widget in enumerate(self.widgets)
        ]


class LinkedStatFormField(forms.MultiValueField):
    """
    A form field for editing linked permanent/temporary stats.

    Usage:
        class CharacterForm(forms.Form):
            willpower = LinkedStatFormField(
                max_value=10,
                min_permanent=1,
                cap_temporary=True,
            )

    Args:
        max_value: Maximum value for both fields
        min_permanent: Minimum permanent value (default 1)
        min_temporary: Minimum temporary value (default 0)
        cap_temporary: Whether temporary must be <= permanent
    """

    def __init__(
        self,
        max_value=10,
        min_permanent=1,
        min_temporary=0,
        cap_temporary=True,
        **kwargs,
    ):
        self.max_value = max_value
        self.min_permanent = min_permanent
        self.min_temporary = min_temporary
        self.cap_temporary = cap_temporary

        fields = [
            forms.IntegerField(
                min_value=min_permanent,
                max_value=max_value,
                required=kwargs.get("required", True),
            ),
            forms.IntegerField(
                min_value=min_temporary,
                max_value=max_value,
                required=kwargs.get("required", True),
            ),
        ]

        # Default widget if not provided
        if "widget" not in kwargs:
            kwargs["widget"] = LinkedStatWidget(
                max_value=max_value,
                min_permanent=min_permanent,
                min_temporary=min_temporary,
            )

        super().__init__(fields=fields, **kwargs)

    def compress(self, data_list):
        """
        Combine the two field values into a dict.

        Returns:
            dict: {'permanent': x, 'temporary': y}
        """
        if not data_list:
            return None

        permanent = data_list[0] if data_list[0] is not None else self.min_permanent
        temporary = data_list[1] if len(data_list) > 1 and data_list[1] is not None else permanent

        # Enforce cap if needed
        if self.cap_temporary and temporary > permanent:
            temporary = permanent

        return {"permanent": permanent, "temporary": temporary}

    def clean(self, value):
        """Validate the combined value."""
        result = super().clean(value)

        if result and self.cap_temporary:
            if result["temporary"] > result["permanent"]:
                raise forms.ValidationError("Temporary value cannot exceed permanent value.")

        return result


class DotsBoxesWidget(forms.Widget):
    """
    A read-only widget that displays linked stats in various WoD styles.

    Supports multiple display modes:
    - "willpower": Two rows - dots (●○) for permanent, boxes (■□) for temporary
    - "pool": Single row of boxes showing current/max (■■■■■□□□□□)
    - "pool_dots": Single row of dots showing current/max (●●●●●○○○○○)

    Usage:
        # Willpower style (two rows)
        {{ form.willpower }}  # ●●●●●●●○○○ / ■■■■■□□□□□

        # Blood pool style (single row, filled = current)
        DotsBoxesWidget(mode="pool")  # ■■■■■□□□□□

        # Large pool with row breaks (10 per row)
        DotsBoxesWidget(mode="pool", row_length=10)
    """

    # Display mode constants
    MODE_WILLPOWER = "willpower"  # Two rows: dots for perm, boxes for temp
    MODE_POOL = "pool"  # Single row: filled boxes = current, empty = remaining
    MODE_POOL_DOTS = "pool_dots"  # Single row: filled dots = current, empty = remaining

    def __init__(self, max_value=10, mode="willpower", row_length=None, attrs=None):
        """
        Initialize the widget.

        Args:
            max_value: Maximum display value (default 10)
            mode: Display mode - "willpower", "pool", or "pool_dots"
            row_length: Max symbols per row for pool modes (default None = no wrapping)
            attrs: Additional HTML attributes
        """
        self.max_value = max_value
        self.mode = mode
        self.row_length = row_length
        super().__init__(attrs)

    def _extract_values(self, value):
        """Extract permanent and temporary values from various input types."""
        if value is None:
            return 0, 0

        if isinstance(value, (list, tuple)):
            permanent = value[0] if len(value) > 0 else 0
            temporary = value[1] if len(value) > 1 else 0
        elif isinstance(value, dict):
            permanent = value.get("permanent", value.get("max", 0))
            temporary = value.get("temporary", value.get("current", 0))
        elif hasattr(value, "permanent") and hasattr(value, "temporary"):
            permanent = value.permanent
            temporary = value.temporary
        else:
            permanent = temporary = int(value) if value else 0

        return permanent, temporary

    def _render_with_rows(self, full_str, row_length):
        """Split a string into rows of specified length."""
        if row_length is None or row_length <= 0 or len(full_str) <= row_length:
            return f'<span class="dots">{full_str}</span>'

        rows = []
        for i in range(0, len(full_str), row_length):
            row = full_str[i : i + row_length]
            rows.append(f'<span class="dots">{row}</span>')
        return "<br>".join(rows)

    def render(self, name, value, attrs=None, renderer=None):
        """Render the stat display."""
        permanent, temporary = self._extract_values(value)

        if self.mode == self.MODE_POOL:
            # Blood pool style: single row of boxes, filled = current
            # Display up to the max (permanent) capacity
            display_max = min(permanent, self.max_value) if permanent > 0 else self.max_value
            current = min(temporary, display_max)
            boxes = "■" * current + "□" * (display_max - current)
            boxes_html = self._render_with_rows(boxes, self.row_length)

            html = f"""
<div class="linked-stat-display pool-display" title="Current: {temporary} / Max: {permanent}">
    {boxes_html}
</div>
"""
        elif self.mode == self.MODE_POOL_DOTS:
            # Pool style with dots instead of boxes
            display_max = min(permanent, self.max_value) if permanent > 0 else self.max_value
            current = min(temporary, display_max)
            dots = "●" * current + "○" * (display_max - current)
            dots_html = self._render_with_rows(dots, self.row_length)

            html = f"""
<div class="linked-stat-display pool-display" title="Current: {temporary} / Max: {permanent}">
    {dots_html}
</div>
"""
        else:
            # Willpower style: two rows
            # Generate dots (●○) for permanent
            perm_display = min(permanent, self.max_value)
            dots = "●" * perm_display + "○" * (self.max_value - perm_display)

            # Generate boxes (■□) for temporary
            temp_display = min(temporary, self.max_value)
            boxes = "■" * temp_display + "□" * (self.max_value - temp_display)

            html = f"""
<div class="linked-stat-display willpower-display">
    <div class="stat-dots" title="Permanent: {permanent}"><span class="dots">{dots}</span></div>
    <div class="stat-boxes" title="Temporary: {temporary}"><span class="dots">{boxes}</span></div>
</div>
"""
        return mark_safe(html)

    def value_from_datadict(self, data, files, name):
        """This widget is read-only, return None."""
        return None


class PoolWidget(DotsBoxesWidget):
    """
    Convenience widget for blood pool style display.

    Shows filled squares for current, empty for remaining capacity.
    Supports row_length for large pools (e.g., elder vampires with 50 blood).

    Examples:
        PoolWidget()  # ■■■■■■■□□□
        PoolWidget(max_value=50, row_length=10)  # 5 rows of 10
    """

    def __init__(self, max_value=10, use_dots=False, row_length=None, attrs=None):
        """
        Initialize the pool widget.

        Args:
            max_value: Maximum pool size (default 10)
            use_dots: Use dots instead of boxes (default False)
            row_length: Symbols per row, None for single row (default None)
            attrs: Additional HTML attributes
        """
        mode = DotsBoxesWidget.MODE_POOL_DOTS if use_dots else DotsBoxesWidget.MODE_POOL
        super().__init__(max_value=max_value, mode=mode, row_length=row_length, attrs=attrs)
