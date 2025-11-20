"""Mixins for adding Django messages to views."""

from django.contrib import messages


class SuccessMessageMixin:
    """
    Mixin to add a success message when a form is successfully saved.

    Usage:
        class MyCreateView(SuccessMessageMixin, CreateView):
            model = MyModel
            success_message = "{name} created successfully!"

    The success_message can use field names from the object in curly braces.
    For safety, it only allows access to string fields and limits length.
    """

    success_message = ""

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.success_message:
            message = self.get_success_message(form.cleaned_data)
            if message:
                messages.success(self.request, message)
        return response

    def get_success_message(self, cleaned_data):
        """
        Generate the success message from the template string.
        Uses self.object for formatting to ensure we have saved data.
        """
        if not self.success_message:
            return ""

        # Get safe formatting dict from object
        format_dict = self.get_message_format_dict()

        try:
            return self.success_message.format(**format_dict)
        except (KeyError, AttributeError, ValueError):
            # Fallback to unformatted message if formatting fails
            return self.success_message

    def get_message_format_dict(self):
        """
        Create a dictionary of safe values for message formatting.
        Only includes basic string representations to avoid security issues.
        """
        if not hasattr(self, 'object') or not self.object:
            return {}

        format_dict = {}

        # Add common safe attributes
        safe_attrs = ['name', 'id', 'pk']
        for attr in safe_attrs:
            if hasattr(self.object, attr):
                value = getattr(self.object, attr)
                # Convert to string and limit length for safety
                format_dict[attr] = str(value)[:100]

        # Add model name for generic messages
        format_dict['model_name'] = self.object._meta.verbose_name
        format_dict['model_name_plural'] = self.object._meta.verbose_name_plural

        return format_dict


class ErrorMessageMixin:
    """
    Mixin to add error messages when form validation fails.

    Usage:
        class MyCreateView(ErrorMessageMixin, CreateView):
            model = MyModel
            error_message = "Please correct the errors below."
    """

    error_message = "Please correct the errors below."

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.error_message:
            messages.error(self.request, self.error_message)
        return response


class MessageMixin(SuccessMessageMixin, ErrorMessageMixin):
    """
    Combined mixin for both success and error messages.

    Usage:
        class MyCreateView(MessageMixin, CreateView):
            model = MyModel
            success_message = "{name} created successfully!"
            error_message = "Failed to create {model_name}. Please check the form."
    """
    pass


class DeleteMessageMixin:
    """
    Mixin to add a success message when an object is deleted.

    Usage:
        class MyDeleteView(DeleteMessageMixin, DeleteView):
            model = MyModel
            success_message = "{name} deleted successfully!"
    """

    success_message = ""

    def delete(self, request, *args, **kwargs):
        # Store object info before deletion
        self.object = self.get_object()
        object_name = str(self.object)

        # Format success message before deleting object
        if self.success_message:
            format_dict = {'name': object_name[:100], 'pk': self.object.pk}
            try:
                message = self.success_message.format(**format_dict)
            except (KeyError, ValueError):
                message = self.success_message
            messages.success(request, message)

        return super().delete(request, *args, **kwargs)
