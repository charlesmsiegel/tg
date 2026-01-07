"""
Create or Select Widget for Django

A composite widget that renders a toggle checkbox along with auto-injected
JavaScript to switch between "select existing" and "create new" modes.

Self-contained: automatically injects JavaScript when rendered.
No {{ form.media }} or static file configuration needed.
"""

from django import forms
from django.utils.safestring import mark_safe

# The JavaScript code, embedded directly so no static files or {{ form.media }} needed
CREATE_OR_SELECT_JS = """
(function() {
    'use strict';

    // Prevent double-initialization
    if (window.CreateOrSelect) return;

    class CreateOrSelectManager {
        constructor() {
            this.initialized = new WeakSet();
        }

        init() {
            document.querySelectorAll('[data-create-or-select-toggle]').forEach(toggle => {
                if (!this.initialized.has(toggle)) {
                    this.registerToggle(toggle);
                    this.initialized.add(toggle);
                }
            });
        }

        registerToggle(toggle) {
            const groupId = toggle.dataset.createOrSelectGroup;
            const selectContainer = document.querySelector(
                `[data-create-or-select-container="${groupId}"][data-create-or-select-mode="select"]`
            );
            const createContainer = document.querySelector(
                `[data-create-or-select-container="${groupId}"][data-create-or-select-mode="create"]`
            );

            if (!selectContainer || !createContainer) {
                console.warn(`CreateOrSelect: Missing containers for group "${groupId}"`);
                return;
            }

            // Store references on the toggle
            toggle._selectContainer = selectContainer;
            toggle._createContainer = createContainer;

            // Set initial state
            this.updateVisibility(toggle);

            // Listen for changes
            toggle.addEventListener('change', () => this.updateVisibility(toggle));
        }

        updateVisibility(toggle) {
            const selectContainer = toggle._selectContainer;
            const createContainer = toggle._createContainer;

            if (toggle.checked) {
                // Create mode: hide select, show create
                selectContainer.classList.add('d-none');
                createContainer.classList.remove('d-none');
            } else {
                // Select mode: show select, hide create
                selectContainer.classList.remove('d-none');
                createContainer.classList.add('d-none');
            }
        }

        // Programmatic toggle
        setMode(groupId, createMode) {
            const toggle = document.querySelector(
                `[data-create-or-select-toggle][data-create-or-select-group="${groupId}"]`
            );
            if (toggle) {
                toggle.checked = createMode;
                this.updateVisibility(toggle);
            }
        }

        getMode(groupId) {
            const toggle = document.querySelector(
                `[data-create-or-select-toggle][data-create-or-select-group="${groupId}"]`
            );
            return toggle ? toggle.checked : null;
        }
    }

    window.CreateOrSelect = new CreateOrSelectManager();

    const init = () => window.CreateOrSelect.init();

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Re-init for htmx/Turbo/dynamic content
    document.addEventListener('htmx:afterSwap', init);
    document.addEventListener('turbo:render', init);
    document.addEventListener('turbo:frame-load', init);
})();
"""


class CreateOrSelectWidget(forms.CheckboxInput):
    """
    A checkbox widget that toggles visibility between select and create containers.

    Self-contained: automatically injects JavaScript when rendered.
    No {{ form.media }} or static file configuration needed.

    Usage in template:
        <div data-create-or-select-container="{{ form.field_name.name }}" data-create-or-select-mode="select">
            {{ form.select_field }}
        </div>
        <div data-create-or-select-container="{{ form.field_name.name }}" data-create-or-select-mode="create">
            {{ form.create_fields }}
        </div>

    Or use the simpler template tags provided by this module.
    """

    # Track if JS has been rendered in this request
    _js_rendered = False

    def __init__(self, group_name=None, create_label="Create new", attrs=None):
        """
        Initialize the widget.

        Args:
            group_name: Optional custom group name. If not provided, uses the field name.
            create_label: Label text for the checkbox (displayed next to toggle)
            attrs: Additional HTML attributes for the checkbox
        """
        self.group_name = group_name
        self.create_label = create_label
        super().__init__(attrs=attrs)

    def get_group_name(self, name):
        """Get the group name for this toggle, deriving from field name if not set."""
        return self.group_name or name

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        return attrs

    def render(self, name, value, attrs=None, renderer=None):
        # Add data attributes for the toggle
        if attrs is None:
            attrs = {}

        group_name = self.get_group_name(name)
        attrs["data-create-or-select-toggle"] = "true"
        attrs["data-create-or-select-group"] = group_name

        existing = attrs.get("class", "")
        attrs["class"] = f"{existing} create-or-select-toggle".strip()

        # Render the standard checkbox
        checkbox_html = super().render(name, value, attrs, renderer)

        parts = [checkbox_html]

        # Inject JavaScript (only once per page)
        if not CreateOrSelectWidget._js_rendered:
            CreateOrSelectWidget._js_rendered = True
            parts.append(f"<script data-create-or-select-js>{CREATE_OR_SELECT_JS}</script>")

        # Add a micro-script to re-initialize (handles dynamic/AJAX-loaded forms)
        parts.append("<script>if(window.CreateOrSelect)window.CreateOrSelect.init();</script>")

        return mark_safe("".join(parts))

    @classmethod
    def reset_js_rendered(cls):
        """Reset the JS rendered flag. Called automatically between requests."""
        cls._js_rendered = False


# Reset flag between requests using Django's request_finished signal
try:
    from django.core.signals import request_finished

    request_finished.connect(lambda sender, **kwargs: CreateOrSelectWidget.reset_js_rendered())
except ImportError:
    pass
