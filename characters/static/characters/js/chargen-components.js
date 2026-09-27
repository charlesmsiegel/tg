/* Alpine components (CSP build) for interactive character creation.
 *
 * Every limit and target comes from the server (data-* or json_script built
 * from characters.rules). Components give instant feedback only; they never
 * block input or submission. The server's validator and submit decide.
 */
document.addEventListener('alpine:init', function () {
    'use strict';

    /* tgDots: clickable dots over a number input (widgets.widgets.dots).
     * data-min/data-max: rating bounds from the step's allocation rule.
     * pick(n): set the rating to n, or one lower when n is the current top dot;
     * fires input+change so totals and validation update. sync(): typed value. */
    window.Alpine.data('tgDots', function () {
        return {
            value: 0,
            min: 0,
            max: 5,
            init: function () {
                this.min = Number(this.$el.dataset.min) || 0;
                this.max = Number(this.$el.dataset.max) || 5;
                this.$refs.input.hidden = true;
                this.sync();
            },
            sync: function () {
                var value = parseInt(this.$refs.input.value, 10);
                this.value = isNaN(value) ? 0 : value;
            },
            filled: function (dot) {
                return dot <= this.value;
            },
            pressed: function (dot) {
                return dot === this.value ? 'true' : 'false';
            },
            pick: function (dot) {
                var next = dot === this.value ? dot - 1 : dot;
                next = Math.max(this.min, Math.min(this.max, next));
                var input = this.$refs.input;
                input.value = String(next);
                this.value = next;
                input.dispatchEvent(new Event('input', { bubbles: true }));
                input.dispatchEvent(new Event('change', { bubbles: true }));
            }
        };
    });

    /* tgPool: running sums of the enclosing form's visible inputs against the
     * targets in the json_script named by data-rules (rule.client_data()).
     * summary: text such as "Physical 8 · Social 6 · Mental 5 (need 10/8/6)". */
    window.Alpine.data('tgPool', function () {
        return {
            summary: '',
            rules: [],
            form: null,
            init: function () {
                var source = document.getElementById(this.$el.dataset.rules);
                this.rules = source ? JSON.parse(source.textContent) : [];
                this.form = this.$el.closest('form');
                var update = this.update.bind(this);
                if (this.form) {
                    this.form.addEventListener('input', update);
                    this.form.addEventListener('change', update);
                }
                this.update();
            },
            rating: function (name) {
                var field = this.form ? this.form.elements.namedItem(name) : null;
                if (!field || field.type === 'hidden') return null;
                var value = parseInt(field.value, 10);
                return isNaN(value) ? 0 : value;
            },
            sum: function (names) {
                var self = this;
                return names.reduce(function (total, name) {
                    var value = self.rating(name);
                    return value === null ? total : total + value;
                }, 0);
            },
            describe: function (rule) {
                var self = this;
                if (rule.groups) {
                    var parts = rule.groups.map(function (group) {
                        return rule.group_labels[group[0]] + ' ' + self.sum(group[1]);
                    });
                    return parts.join(' · ') + ' (need ' + rule.targets.join('/') + ')';
                }
                var current = this.sum(rule.fields || []);
                var bound = rule.comparison === 'at_most' ? 'at most ' : '';
                return rule.label + ' ' + current + ' of ' + bound + rule.total;
            },
            update: function () {
                this.summary = this.rules.map(this.describe.bind(this)).join('; ');
            }
        };
    });

    /* tgConditional: shows the fields the server says are visible.
     * data-visibility: initial {field: bool}; apply(event) merges the
     * tg-visibility event the server sends (HX-Trigger) with option fragments. */
    window.Alpine.data('tgConditional', function () {
        return {
            shown: {},
            init: function () {
                this.shown = JSON.parse(this.$el.dataset.visibility || '{}');
            },
            apply: function (event) {
                var detail = event && event.detail ? event.detail : {};
                var next = Object.assign({}, this.shown);
                Object.keys(next).forEach(function (name) {
                    if (typeof detail[name] === 'boolean') next[name] = detail[name];
                });
                this.shown = next;
            }
        };
    });
});
