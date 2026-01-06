"""
Template tags for FormsetManager widget.

Simplified Usage:
    {% load formset_tags %}

    {% formset my_formset prefix="items" add_label="Add Item" %}
        <div class="col-sm">{{ subform.name }}</div>
        <div class="col-sm">{{ subform.quantity }}</div>
    {% endformset %}

That's it! The tag handles:
- Management form
- Container with data attributes
- Looping through existing forms
- Hidden empty form template
- Add button
- JavaScript injection (once per page)
"""

from django import template
from django.utils.safestring import mark_safe

from ..widgets.formset_manager import render_formset_manager_script_once

register = template.Library()


class FormsetNode(template.Node):
    """
    Template node for the {% formset %} block tag.

    Renders a complete dynamic formset with add/remove functionality.
    """

    def __init__(self, formset_var, nodelist, prefix=None, add_label=None,
                 add_class=None, remove_label=None, remove_class=None,
                 wrapper_class=None, show_remove=True, animate=False):
        self.formset_var = formset_var
        self.nodelist = nodelist
        self.prefix = prefix
        self.add_label = add_label
        self.add_class = add_class
        self.remove_label = remove_label
        self.remove_class = remove_class
        self.wrapper_class = wrapper_class
        self.show_remove = show_remove
        self.animate = animate

    def render(self, context):
        # Resolve the formset variable
        formset = self.formset_var.resolve(context)

        # Resolve other variables
        prefix = self.prefix.resolve(context) if self.prefix else formset.prefix
        add_label = self.add_label.resolve(context) if self.add_label else "Add"
        add_class = self.add_class.resolve(context) if self.add_class else ""
        remove_label = self.remove_label.resolve(context) if self.remove_label else "Remove"
        remove_class = self.remove_class.resolve(context) if self.remove_class else "tg-btn btn-danger btn-sm"
        wrapper_class = self.wrapper_class.resolve(context) if self.wrapper_class else "form-row"
        show_remove = self.show_remove.resolve(context) if hasattr(self.show_remove, 'resolve') else self.show_remove
        animate = self.animate.resolve(context) if hasattr(self.animate, 'resolve') else self.animate

        parts = []

        # Management form
        parts.append(str(formset.management_form))

        # Container opening
        animate_attr = ' data-formset-animate="true"' if animate else ''
        parts.append(
            f'<div id="{prefix}_formset" data-formset-container="" '
            f'data-formset-prefix="{prefix}"{animate_attr}>'
        )

        # Render existing forms
        for form in formset:
            parts.append(self._render_form_row(
                context, form, prefix, wrapper_class,
                remove_label, remove_class, show_remove, is_empty=False
            ))

        # Container closing
        parts.append('</div>')

        # Empty form template (hidden)
        parts.append(f'<div id="empty_{prefix}_form" class="d-none">')
        parts.append(self._render_form_row(
            context, formset.empty_form, prefix, wrapper_class,
            remove_label, remove_class, show_remove, is_empty=True
        ))
        parts.append('</div>')

        # Add button
        parts.append(
            f'<button type="button" data-formset-add="{prefix}" '
            f'class="{add_class}">{add_label}</button>'
        )

        # JavaScript (once per page)
        parts.append(render_formset_manager_script_once())

        return mark_safe('\n'.join(parts))

    def _render_form_row(self, context, form, prefix, wrapper_class,
                         remove_label, remove_class, show_remove, is_empty):
        """Render a single form row with the user-provided content."""
        # Push subform into context
        with context.push():
            context['subform'] = form
            context['form'] = form  # Alias for convenience

            # Render the user's nodelist content
            content = self.nodelist.render(context)

        # Build remove button if enabled
        remove_btn = ''
        if show_remove:
            remove_btn = (
                f'<button type="button" data-formset-remove="{prefix}" '
                f'class="{remove_class}">{remove_label}</button>'
            )

        # Wrap in form row div
        return (
            f'<div class="{wrapper_class}" data-formset-form="">'
            f'{content}{remove_btn}</div>'
        )


@register.tag('formset')
def do_formset(parser, token):
    """
    Render a complete dynamic formset.

    Usage:
        {% formset formset_var prefix="prefix" add_label="Add" %}
            {{ subform.field1 }}
            {{ subform.field2 }}
        {% endformset %}

    Arguments:
        formset_var: The Django formset object (required)
        prefix: The formset prefix (optional, defaults to formset.prefix)
        add_label: Text for the add button (default: "Add")
        add_class: CSS class for add button (default: "")
        remove_label: Text for remove buttons (default: "Remove")
        remove_class: CSS class for remove button (default: "tg-btn btn-danger btn-sm")
        wrapper_class: CSS class for form row wrapper (default: "form-row")
        show_remove: Whether to show remove buttons (default: True)
        animate: Whether to animate add/remove (default: False)

    Inside the block, use {{ subform.fieldname }} to render fields.
    """
    bits = token.split_contents()
    tag_name = bits[0]

    if len(bits) < 2:
        raise template.TemplateSyntaxError(
            f"'{tag_name}' tag requires at least one argument (the formset)"
        )

    formset_var = parser.compile_filter(bits[1])

    # Parse keyword arguments
    kwargs = {}
    for bit in bits[2:]:
        if '=' in bit:
            key, value = bit.split('=', 1)
            # Remove quotes if present
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            kwargs[key] = parser.compile_filter(value) if not value.startswith('"') else template.Variable(f'"{value}"')
            # Handle string literals vs variables
            if value in ('True', 'False'):
                kwargs[key] = value == 'True'
            else:
                kwargs[key] = parser.compile_filter(f'"{value}"') if '"' not in value and "'" not in value else parser.compile_filter(value)
        else:
            raise template.TemplateSyntaxError(
                f"'{tag_name}' tag arguments must be in key=value format"
            )

    # Parse the nodelist until {% endformset %}
    nodelist = parser.parse(('endformset',))
    parser.delete_first_token()

    return FormsetNode(
        formset_var=formset_var,
        nodelist=nodelist,
        prefix=kwargs.get('prefix'),
        add_label=kwargs.get('add_label'),
        add_class=kwargs.get('add_class'),
        remove_label=kwargs.get('remove_label'),
        remove_class=kwargs.get('remove_class'),
        wrapper_class=kwargs.get('wrapper_class'),
        show_remove=kwargs.get('show_remove', True),
        animate=kwargs.get('animate', False),
    )


# Keep the simple tags for advanced/custom use cases
@register.simple_tag
def formset_script():
    """Render FormsetManager JS. Only renders once per page."""
    return render_formset_manager_script_once()


@register.simple_tag
def formset_container(prefix, empty_form_id=None, animate=False):
    """Return data attributes for a formset container (advanced use)."""
    attrs = [
        'data-formset-container=""',
        f'data-formset-prefix="{prefix}"',
    ]
    if empty_form_id:
        attrs.append(f'data-formset-empty-form="{empty_form_id}"')
    if animate:
        attrs.append('data-formset-animate="true"')
    return mark_safe(' '.join(attrs))


@register.simple_tag
def formset_add_btn(prefix, label="Add", **kwargs):
    """Render an add button (advanced use)."""
    attrs = [f'data-formset-add="{prefix}"', 'type="button"']
    for key, value in kwargs.items():
        attrs.append(f'{key.replace("_", "-")}="{value}"')
    return mark_safe(f'<button {" ".join(attrs)}>{label}</button>')


@register.simple_tag
def formset_remove_btn(prefix):
    """Return data attributes for a remove button (advanced use)."""
    return mark_safe(f'data-formset-remove="{prefix}"')


@register.simple_tag
def formset_form_wrapper():
    """Return data attribute to mark a form row (advanced use)."""
    return mark_safe('data-formset-form=""')
