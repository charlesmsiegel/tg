"""
Formset Manager Widget for Django

A self-contained widget that handles dynamic formset management with add/remove functionality.
No external JavaScript files needed - all JS is embedded and auto-initialized.

Features:
- Dynamic form addition by cloning empty form template
- Form removal via DELETE checkbox or DOM removal
- Automatic re-initialization of dependent widgets (ChainedSelect, ConditionalFields)
- Proper Django formset prefix handling
- Optional smooth animations
- Data attribute-driven configuration
"""

from django.utils.safestring import mark_safe

# The JavaScript code, embedded directly so no static files needed
FORMSET_MANAGER_JS = """
(function() {
    'use strict';

    // Prevent double-initialization
    if (window.FormsetManager) return;

    class FormsetManagerClass {
        constructor() {
            this.formsets = {};
            this.initialized = new WeakSet();
        }

        /**
         * Initialize all formset containers on the page.
         * Call this after adding new content via AJAX/HTMX.
         */
        init() {
            document.querySelectorAll('[data-formset-container]').forEach(container => {
                if (!this.initialized.has(container)) {
                    this.registerFormset(container);
                    this.initialized.add(container);
                }
            });

            // Bind add buttons
            document.querySelectorAll('[data-formset-add]').forEach(btn => {
                if (!this.initialized.has(btn)) {
                    this.bindAddButton(btn);
                    this.initialized.add(btn);
                }
            });

            // Bind remove buttons (including ones in existing forms)
            document.querySelectorAll('[data-formset-remove]').forEach(btn => {
                if (!this.initialized.has(btn)) {
                    this.bindRemoveButton(btn);
                    this.initialized.add(btn);
                }
            });
        }

        /**
         * Register a formset container for management.
         */
        registerFormset(container) {
            const prefix = container.dataset.formsetPrefix;
            if (!prefix) {
                console.error('FormsetManager: Container missing data-formset-prefix');
                return;
            }

            const emptyFormId = container.dataset.formsetEmptyForm || `empty_${prefix}_form`;
            const emptyFormEl = document.getElementById(emptyFormId);

            if (!emptyFormEl) {
                console.error(`FormsetManager: Empty form template not found: #${emptyFormId}`);
                return;
            }

            this.formsets[prefix] = {
                container: container,
                emptyForm: emptyFormEl,
                animate: container.dataset.formsetAnimate === 'true'
            };
        }

        /**
         * Bind click handler to an add button.
         */
        bindAddButton(btn) {
            const prefix = btn.dataset.formsetAdd;
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                this.addForm(prefix);
            });
        }

        /**
         * Bind click handler to a remove button.
         */
        bindRemoveButton(btn) {
            const prefix = btn.dataset.formsetRemove;
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                this.removeForm(btn, prefix);
            });
        }

        /**
         * Add a new form to the formset.
         */
        addForm(prefix) {
            const totalFormsInput = document.getElementById(`id_${prefix}-TOTAL_FORMS`);
            if (!totalFormsInput) {
                console.error(`FormsetManager: TOTAL_FORMS input not found for prefix: ${prefix}`);
                return;
            }

            const formsetInfo = this.formsets[prefix];
            if (!formsetInfo) {
                console.error(`FormsetManager: Formset not registered for prefix: ${prefix}`);
                return;
            }

            const currentCount = parseInt(totalFormsInput.value, 10);
            const newIndex = currentCount;

            // Clone the empty form template HTML and replace __prefix__ placeholders
            let newFormHtml = formsetInfo.emptyForm.innerHTML;
            newFormHtml = newFormHtml.replace(/__prefix__/g, newIndex);

            // Create wrapper div and insert
            const wrapper = document.createElement('div');
            wrapper.innerHTML = newFormHtml;
            const newFormEl = wrapper.firstElementChild || wrapper;

            // Apply animation if enabled
            if (formsetInfo.animate) {
                newFormEl.style.opacity = '0';
                newFormEl.style.transform = 'translateY(-10px)';
            }

            formsetInfo.container.appendChild(newFormEl);

            // Update TOTAL_FORMS
            totalFormsInput.value = newIndex + 1;

            // Animate in
            if (formsetInfo.animate) {
                requestAnimationFrame(() => {
                    newFormEl.style.transition = 'opacity 0.2s ease, transform 0.2s ease';
                    newFormEl.style.opacity = '1';
                    newFormEl.style.transform = 'translateY(0)';
                });
            }

            // Re-initialize widgets
            this.reinitializeWidgets(newFormEl);

            // Re-bind remove buttons in the new form
            newFormEl.querySelectorAll('[data-formset-remove]').forEach(btn => {
                if (!this.initialized.has(btn)) {
                    this.bindRemoveButton(btn);
                    this.initialized.add(btn);
                }
            });

            // Dispatch custom event for extensibility
            const event = new CustomEvent('formset:added', {
                bubbles: true,
                detail: { prefix, index: newIndex, form: newFormEl }
            });
            formsetInfo.container.dispatchEvent(event);

            return newFormEl;
        }

        /**
         * Remove a form from the formset.
         * If the form has a DELETE checkbox (for existing db records), check it.
         * Otherwise, remove the form from DOM entirely.
         */
        removeForm(removeBtn, prefix) {
            // Find the form row - look for closest element with data-formset-form or common class patterns
            const formRow = removeBtn.closest('[data-formset-form]') ||
                           removeBtn.closest('.form-row') ||
                           removeBtn.closest('.formset-row') ||
                           removeBtn.closest('[class*="-row"]') ||
                           removeBtn.parentElement.parentElement;

            if (!formRow) {
                console.error('FormsetManager: Could not find form row to remove');
                return;
            }

            // Look for a DELETE checkbox in this form row
            const deleteCheckbox = formRow.querySelector('input[type="checkbox"][name$="-DELETE"]');

            const formsetInfo = this.formsets[prefix];
            const animate = formsetInfo ? formsetInfo.animate : false;

            if (deleteCheckbox) {
                // Mark for deletion and hide
                deleteCheckbox.checked = true;
                if (animate) {
                    formRow.style.transition = 'opacity 0.2s ease, max-height 0.2s ease';
                    formRow.style.opacity = '0';
                    formRow.style.maxHeight = '0';
                    formRow.style.overflow = 'hidden';
                    setTimeout(() => {
                        formRow.style.display = 'none';
                    }, 200);
                } else {
                    formRow.style.display = 'none';
                }
            } else {
                // New form (not in database yet) - remove from DOM entirely
                // Also decrement TOTAL_FORMS if this is a new form
                if (animate) {
                    formRow.style.transition = 'opacity 0.2s ease, transform 0.2s ease';
                    formRow.style.opacity = '0';
                    formRow.style.transform = 'translateY(-10px)';
                    setTimeout(() => {
                        formRow.remove();
                        if (prefix) {
                            this.reindexForms(prefix);
                        }
                    }, 200);
                } else {
                    formRow.remove();
                    if (prefix) {
                        this.reindexForms(prefix);
                    }
                }
            }

            // Dispatch custom event
            const event = new CustomEvent('formset:removed', {
                bubbles: true,
                detail: { prefix, form: formRow, deleted: !!deleteCheckbox }
            });
            document.dispatchEvent(event);
        }

        /**
         * Re-index forms after removal to maintain proper ordering.
         * This is only needed for forms without DELETE checkboxes.
         */
        reindexForms(prefix) {
            const formsetInfo = this.formsets[prefix];
            if (!formsetInfo) return;

            const forms = formsetInfo.container.querySelectorAll('[data-formset-form]') ||
                         formsetInfo.container.querySelectorAll('.form-row') ||
                         formsetInfo.container.querySelectorAll(':scope > div');

            let visibleIndex = 0;
            forms.forEach((form, i) => {
                // Skip hidden/deleted forms
                if (form.style.display === 'none') return;

                // Update all name and id attributes
                form.querySelectorAll('[name], [id]').forEach(el => {
                    if (el.name) {
                        el.name = el.name.replace(new RegExp(`${prefix}-\\d+`), `${prefix}-${visibleIndex}`);
                    }
                    if (el.id) {
                        el.id = el.id.replace(new RegExp(`${prefix}-\\d+`), `${prefix}-${visibleIndex}`);
                    }
                });

                // Update for= attributes on labels
                form.querySelectorAll('label[for]').forEach(label => {
                    label.setAttribute('for',
                        label.getAttribute('for').replace(new RegExp(`${prefix}-\\d+`), `${prefix}-${visibleIndex}`)
                    );
                });

                // Update data-prefix attributes
                form.querySelectorAll('[data-prefix]').forEach(el => {
                    el.dataset.prefix = el.dataset.prefix.replace(new RegExp(`${prefix}-\\d+`), `${prefix}-${visibleIndex}`);
                });

                visibleIndex++;
            });

            // Update TOTAL_FORMS
            const totalFormsInput = document.getElementById(`id_${prefix}-TOTAL_FORMS`);
            if (totalFormsInput) {
                totalFormsInput.value = visibleIndex;
            }
        }

        /**
         * Re-initialize dependent widgets after adding a new form.
         */
        reinitializeWidgets(formEl) {
            // Re-initialize ChainedSelect if available
            if (window.ChainedSelect) {
                window.ChainedSelect.init();
            }

            // Re-initialize any other widgets that may be present
            // ConditionalFields, DatePicker, etc.
            if (window.ConditionalFields) {
                window.ConditionalFields.init();
            }

            // Trigger a custom event for any other widget initialization
            const event = new CustomEvent('formset:widgetsInit', {
                bubbles: true,
                detail: { form: formEl }
            });
            formEl.dispatchEvent(event);
        }

        /**
         * Get the current form count for a formset.
         */
        getFormCount(prefix) {
            const totalFormsInput = document.getElementById(`id_${prefix}-TOTAL_FORMS`);
            return totalFormsInput ? parseInt(totalFormsInput.value, 10) : 0;
        }

        /**
         * Programmatically add multiple forms.
         */
        addForms(prefix, count) {
            const forms = [];
            for (let i = 0; i < count; i++) {
                forms.push(this.addForm(prefix));
            }
            return forms;
        }
    }

    window.FormsetManager = new FormsetManagerClass();

    const init = () => window.FormsetManager.init();

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Re-init for htmx/Turbo
    document.addEventListener('htmx:afterSwap', init);
    document.addEventListener('turbo:render', init);
    document.addEventListener('turbo:frame-load', init);
})();
"""


def render_formset_manager_script():
    """
    Render the FormsetManager JavaScript.
    Call this once per page, typically at the end of your form.

    Returns:
        Safe HTML string containing the script tag.
    """
    return mark_safe(f'<script data-formset-manager-js>{FORMSET_MANAGER_JS}</script>')


# Track if JS has been rendered in this request
_js_rendered = False


def _reset_js_rendered(sender=None, **kwargs):
    """Reset the JS rendered flag between requests."""
    global _js_rendered
    _js_rendered = False


def render_formset_manager_script_once():
    """
    Render the FormsetManager JavaScript only once per request.
    Subsequent calls return empty string.

    Returns:
        Safe HTML string containing the script tag (or empty string).
    """
    global _js_rendered
    if not _js_rendered:
        _js_rendered = True
        return render_formset_manager_script()
    return mark_safe('')


# Reset flag between requests using Django's request_finished signal
try:
    from django.core.signals import request_finished
    request_finished.connect(_reset_js_rendered)
except ImportError:
    pass
