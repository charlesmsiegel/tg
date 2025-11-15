"""
Reusable view mixins for common patterns across the application.
"""


class ApprovedUserContextMixin:
    """
    Adds is_approved_user to the context automatically.

    This mixin should be used with views that need to check if the current user
    has special permissions for the object being viewed. It requires the view
    to have access to self.object and self.request.user, and to implement
    the check_if_special_user method (typically via SpecialUserMixin).
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_approved_user"] = self.check_if_special_user(
            self.object, self.request.user
        )
        return context


class PlaceholderFormMixin:
    """
    Automatically adds placeholder text to form fields.

    Define placeholder_fields as a dict mapping field names to placeholder text.
    Common fields (name, description) have defaults but can be overridden.

    Example:
        class MyView(PlaceholderFormMixin, CreateView):
            placeholder_fields = {
                "name": "Enter name here",
                "description": "Enter description here",
                "custom_field": "Custom placeholder",
            }
    """

    placeholder_fields = {
        "name": "Enter name here",
        "description": "Enter description here",
    }

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field_name, placeholder in self.placeholder_fields.items():
            if field_name in form.fields:
                form.fields[field_name].widget.attrs.update({
                    "placeholder": placeholder
                })
        return form
