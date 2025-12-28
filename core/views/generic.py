from django.shortcuts import get_object_or_404, redirect
from django.views import View


class DictView(View):
    view_mapping = {}
    model_class = None
    key_property = None
    default_redirect = None

    def get_object(self, pk):
        return get_object_or_404(self.model_class, pk=pk)

    def handle_request(self, request, *args, **kwargs):
        obj = self.get_object(kwargs["pk"])
        key = getattr(obj, self.key_property)

        if self.is_valid_key(obj, key):
            return self.view_mapping[key].as_view()(request, *args, **kwargs)

        return self.get_default_redirect(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.handle_request(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.handle_request(request, *args, **kwargs)

    def is_valid_key(self, obj, key):
        return key in self.view_mapping

    def get_default_redirect(self, request, *args, **kwargs):
        if isinstance(self.default_redirect, str):
            return redirect(self.default_redirect)
        elif callable(self.default_redirect):
            return self.default_redirect.as_view()(request, *args, **kwargs)
        raise ValueError("default_redirect must be a URL name or a view callable")


class MultipleFormsetsMixin:
    formsets = {}
    _bound_formsets = None  # Cache for bound formsets during POST

    def get_formset_context(self, formset_class, formset_prefix, bound_formset=None):
        """Generate context and JavaScript code for a given formset."""
        if bound_formset is not None:
            formset = bound_formset
        else:
            kwargs = self.get_formset_kwargs(formset_prefix)
            formset = formset_class(**kwargs)  # Initialize formset

            if len(formset.forms) == 0:
                kwargs["initial"] = [{}]
                formset = formset_class(**kwargs)  # Ensure at least one form exists

        empty_form = formset.empty_form  # Generate the "empty" form for cloning

        context = {
            "formset": formset,
            "formset_prefix": formset_prefix,
            "add_button_id": f"add_{formset_prefix}_form",
            "remove_button_class": f"remove_{formset_prefix}_form",
            "empty_form": empty_form,  # Pass empty form to context
        }

        js_code = f"""
        <script>
        document.getElementById('{context['add_button_id']}').addEventListener('click', function(e) {{
            e.preventDefault();  // Prevent form submission

            var totalForms = document.getElementById('id_{formset_prefix}-TOTAL_FORMS');
            var formCount = parseInt(totalForms.value);
            var emptyForm = document.getElementById('{formset_prefix}_empty_form').innerHTML;
            var newForm = emptyForm.replace(/__prefix__/g, formCount);  // Replace prefix
            document.getElementById('{formset_prefix}_container').insertAdjacentHTML('beforeend', newForm);
            totalForms.value = formCount + 1;
        }});
        </script>
        """

        return context, js_code

    def get_formset_kwargs(self, prefix):
        """
        Get kwargs for creating a formset. Override this method to pass custom
        kwargs like 'instance' for inline formsets.
        """
        kwargs = {"prefix": prefix}
        # If view has self.object (e.g., UpdateView), pass it as instance for inline formsets
        if hasattr(self, "object") and self.object is not None:
            kwargs["instance"] = self.object
        return kwargs

    def get_bound_formsets(self):
        """Create formsets bound to POST data. Caches result for reuse."""
        if self._bound_formsets is not None:
            return self._bound_formsets

        self._bound_formsets = {}
        for prefix, formset_class in self.formsets.items():
            kwargs = self.get_formset_kwargs(prefix)
            formset = formset_class(self.request.POST, **kwargs)
            if len(formset.forms) == 0:
                formset = formset_class(self.request.POST, initial=[{}], **kwargs)
            self._bound_formsets[prefix] = formset

        return self._bound_formsets

    def get_formsets(self):
        """Create and return all formsets defined in the view."""
        formsets_context = {}
        formsets_js = {}

        # Check if we have bound formsets (from POST) to preserve
        bound_formsets = getattr(self, "_bound_formsets", None)

        for prefix, formset_class in self.formsets.items():
            bound_formset = bound_formsets.get(prefix) if bound_formsets else None
            context, js_code = self.get_formset_context(formset_class, prefix, bound_formset)
            formsets_context[f"{prefix}_context"] = context
            formsets_js[f"{prefix}_js"] = js_code

        return formsets_context, formsets_js

    def get_context_data(self, **kwargs):
        """Add formsets and their context to the view context."""
        context = super().get_context_data(**kwargs)
        formsets_context, formsets_js = self.get_formsets()

        context.update(formsets_context)
        context.update(formsets_js)

        return context

    def form_valid(self, form):
        """Override to handle formsets saving logic."""
        # Get bound formsets from POST data
        bound_formsets = self.get_bound_formsets()

        for prefix, formset in bound_formsets.items():
            if not formset.is_valid():
                return self.form_invalid(form)  # Handle invalid formsets
            formset.save()  # Save valid formsets

        return super().form_valid(form)

    def form_invalid(self, form):
        """Ensure bound formsets are preserved in context when form is invalid."""
        # Make sure bound formsets are available for get_context_data
        if self.request.method == "POST" and self._bound_formsets is None:
            self.get_bound_formsets()
        return super().form_invalid(form)

    def get_form_data(self, formset_prefix, blankable=None):
        """
        Return a list of dictionaries containing the input data for all forms in the formset
        identified by the given prefix. The method works with POST data.
        """
        if blankable is None:
            blankable = []
        formset_class = self.formsets.get(formset_prefix)

        if not formset_class:
            return []  # Return an empty list if the formset prefix does not exist

        # Initialize the formset with POST data
        formset = formset_class(self.request.POST, prefix=formset_prefix)

        # Collect data from each form in the formset
        forms_data = []
        for i, form in enumerate(formset.forms):
            sample = {}
            for key in form.fields.keys():
                if f"{formset_prefix}-{i}-{key}" in form.data:
                    sample[key] = form.data[f"{formset_prefix}-{i}-{key}"]
            if sample:
                forms_data.append(sample)
        forms_data = [
            x for x in forms_data if "" not in set([v for k, v in x.items() if k not in blankable])
        ]
        return forms_data
