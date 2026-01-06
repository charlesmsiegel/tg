"""
Point Pool Widget for Django

A widget that manages point allocations across form fields with real-time
validation and constraint enforcement.

Supports two modes:
1. Simple Mode: Single budget constraint across fields (e.g., 7 points for backgrounds)
2. Distribution Mode: Multiple groups with target totals in any permutation
   (e.g., primary/secondary/tertiary patterns)
"""

import json

from django import forms
from django.utils.safestring import mark_safe

# The JavaScript code, embedded directly so no static files needed
POINT_POOL_JS = """
(function() {
    'use strict';

    // Prevent double-initialization
    if (window.PointPoolManager) return;

    class PointPoolManager {
        constructor() {
            this.pools = {};
            this.initialized = new WeakSet();
        }

        init() {
            this.loadPoolConfigs();
            document.querySelectorAll('[data-point-pool]').forEach(input => {
                if (!this.initialized.has(input)) {
                    this.registerInput(input);
                    this.initialized.add(input);
                }
            });
            // Initial update for all pools
            Object.keys(this.pools).forEach(poolName => {
                this.updateDisplay(poolName);
            });
        }

        loadPoolConfigs() {
            document.querySelectorAll('script[data-pool-config]').forEach(script => {
                const poolName = script.dataset.poolConfig;
                try {
                    const config = JSON.parse(script.textContent);
                    if (!this.pools[poolName]) {
                        this.pools[poolName] = {
                            config: config,
                            inputs: {},
                            groups: {}
                        };
                    } else {
                        this.pools[poolName].config = config;
                    }
                } catch (e) {
                    console.error(`PointPool: Failed to parse config for ${poolName}:`, e);
                }
            });
        }

        registerInput(input) {
            const poolName = input.dataset.poolName;
            const groupName = input.dataset.poolGroup;
            const fieldName = this.getFieldName(input);

            if (!poolName) return;

            if (!this.pools[poolName]) {
                this.pools[poolName] = {
                    config: {},
                    inputs: {},
                    groups: {}
                };
            }

            const pool = this.pools[poolName];
            pool.inputs[fieldName] = input;

            if (groupName) {
                if (!pool.groups[groupName]) {
                    pool.groups[groupName] = [];
                }
                if (!pool.groups[groupName].includes(fieldName)) {
                    pool.groups[groupName].push(fieldName);
                }
            }

            // Listen for changes
            input.addEventListener('change', () => this.handleChange(poolName, fieldName));
            input.addEventListener('input', () => this.handleChange(poolName, fieldName));
        }

        getFieldName(input) {
            const name = input.name || input.id;
            const parts = name.split('-');
            return parts[parts.length - 1].replace('id_', '');
        }

        handleChange(poolName, fieldName) {
            this.updateDisplay(poolName);
        }

        getInputValue(input) {
            if (input.tagName === 'SELECT') {
                return parseInt(input.value, 10) || 0;
            }
            return parseInt(input.value, 10) || 0;
        }

        getGroupTotal(poolName, groupName) {
            const pool = this.pools[poolName];
            if (!pool || !pool.groups[groupName]) return 0;

            const baseValue = pool.config.base_value || 0;
            return pool.groups[groupName].reduce((sum, fieldName) => {
                const input = pool.inputs[fieldName];
                return sum + (input ? this.getInputValue(input) : baseValue);
            }, 0);
        }

        getTotalPoints(poolName) {
            const pool = this.pools[poolName];
            if (!pool) return 0;

            return Object.values(pool.inputs).reduce((sum, input) => {
                return sum + this.getInputValue(input);
            }, 0);
        }

        getCurrentGroupTotals(poolName) {
            const pool = this.pools[poolName];
            if (!pool) return {};

            const totals = {};
            Object.keys(pool.groups).forEach(groupName => {
                totals[groupName] = this.getGroupTotal(poolName, groupName);
            });
            return totals;
        }

        // Check if a distribution can reach valid targets (distribution mode)
        isValidState(poolName, groupTotals) {
            const pool = this.pools[poolName];
            if (!pool || !pool.config.targets) return true;

            const targets = [...pool.config.targets].sort((a, b) => a - b);
            const currentTotals = Object.values(groupTotals).sort((a, b) => a - b);

            // Generate all permutations of targets and check if any works
            const permutations = this.getPermutations(targets);

            for (const targetPerm of permutations) {
                let valid = true;
                for (let i = 0; i < currentTotals.length; i++) {
                    if (currentTotals[i] > targetPerm[i]) {
                        valid = false;
                        break;
                    }
                }
                if (valid) return true;
            }
            return false;
        }

        getPermutations(arr) {
            if (arr.length <= 1) return [arr];
            const result = [];
            for (let i = 0; i < arr.length; i++) {
                const rest = [...arr.slice(0, i), ...arr.slice(i + 1)];
                const restPerms = this.getPermutations(rest);
                for (const perm of restPerms) {
                    result.push([arr[i], ...perm]);
                }
            }
            return result;
        }

        // Check if setting a field to a value maintains validity
        isFieldValueValid(poolName, fieldName, targetValue) {
            const pool = this.pools[poolName];
            if (!pool) return true;

            const config = pool.config;
            const minValue = config.min_value ?? 0;
            const maxValue = config.max_value ?? 10;

            // Check basic range constraints
            if (targetValue < minValue || targetValue > maxValue) {
                return false;
            }

            // Simple mode: check total budget
            if (config.mode === 'simple') {
                const currentValue = this.getInputValue(pool.inputs[fieldName]);
                const currentTotal = this.getTotalPoints(poolName);
                const newTotal = currentTotal - currentValue + targetValue;
                return newTotal <= config.total_budget;
            }

            // Distribution mode: check if distribution remains achievable
            if (config.mode === 'distribution' && config.targets) {
                const groupTotals = this.getCurrentGroupTotals(poolName);

                // Find which group this field belongs to
                let fieldGroup = null;
                for (const [groupName, fields] of Object.entries(pool.groups)) {
                    if (fields.includes(fieldName)) {
                        fieldGroup = groupName;
                        break;
                    }
                }

                if (fieldGroup) {
                    const currentValue = this.getInputValue(pool.inputs[fieldName]);
                    groupTotals[fieldGroup] = groupTotals[fieldGroup] - currentValue + targetValue;
                }

                return this.isValidState(poolName, groupTotals);
            }

            return true;
        }

        // Find the maximum value a group can reach while staying valid
        getMaxGroupValue(poolName, groupName) {
            const pool = this.pools[poolName];
            if (!pool || !pool.config.targets) return Infinity;

            const targets = pool.config.targets;
            const maxTarget = Math.max(...targets);
            const currentTotals = this.getCurrentGroupTotals(poolName);
            const currentValue = currentTotals[groupName] || 0;

            // Try increasing until invalid
            for (let testValue = currentValue + 1; testValue <= maxTarget; testValue++) {
                const testTotals = { ...currentTotals };
                testTotals[groupName] = testValue;
                if (!this.isValidState(poolName, testTotals)) {
                    return testValue - 1;
                }
            }
            return maxTarget;
        }

        updateDisplay(poolName) {
            const pool = this.pools[poolName];
            if (!pool) return;

            const config = pool.config;
            const totalPoints = this.getTotalPoints(poolName);

            // Update total status display
            this.updateTotalStatus(poolName, totalPoints);

            // Update group status displays (distribution mode)
            if (config.mode === 'distribution') {
                this.updateGroupStatuses(poolName);
            }

            // Update input constraints
            this.updateInputConstraints(poolName);
        }

        updateTotalStatus(poolName, totalPoints) {
            const pool = this.pools[poolName];
            const config = pool.config;
            const statusElement = document.querySelector(`[data-pool-total="${poolName}"]`);

            if (!statusElement) return;

            let totalBudget;
            let remaining;
            let isComplete = false;
            let isValid = true;

            if (config.mode === 'simple') {
                totalBudget = config.total_budget || 0;
                remaining = totalBudget - totalPoints;
            } else if (config.mode === 'distribution') {
                totalBudget = config.targets ? config.targets.reduce((a, b) => a + b, 0) : 0;
                remaining = totalBudget - totalPoints;

                const groupTotals = this.getCurrentGroupTotals(poolName);
                const sortedTotals = Object.values(groupTotals).sort((a, b) => a - b);
                const sortedTargets = [...config.targets].sort((a, b) => a - b);

                isValid = this.isValidState(poolName, groupTotals);
                isComplete = remaining === 0 &&
                    sortedTotals.length === sortedTargets.length &&
                    sortedTotals.every((val, idx) => val === sortedTargets[idx]);
            }

            // Update status text and color
            if (remaining > 0) {
                statusElement.textContent = `${remaining} point${remaining !== 1 ? 's' : ''} remaining to allocate`;
                statusElement.style.color = 'var(--theme-text-secondary, #6c757d)';
            } else if (remaining === 0) {
                if (isComplete) {
                    statusElement.textContent = 'Complete! Valid distribution achieved.';
                    statusElement.style.color = '#28a745';
                } else if (isValid) {
                    statusElement.textContent = 'All points allocated - verify distribution is correct';
                    statusElement.style.color = '#ffc107';
                } else {
                    statusElement.textContent = 'All points allocated - but distribution is invalid';
                    statusElement.style.color = '#dc3545';
                }
            } else {
                statusElement.textContent = `${Math.abs(remaining)} point${Math.abs(remaining) !== 1 ? 's' : ''} over limit!`;
                statusElement.style.color = '#dc3545';
            }
        }

        updateGroupStatuses(poolName) {
            const pool = this.pools[poolName];
            if (!pool || !pool.config.targets) return;

            const groupTotals = this.getCurrentGroupTotals(poolName);

            Object.entries(groupTotals).forEach(([groupName, currentTotal]) => {
                const element = document.querySelector(`[data-pool-group-status="${poolName}:${groupName}"]`);
                if (!element) return;

                const maxValue = this.getMaxGroupValue(poolName, groupName);
                const canAdd = maxValue - currentTotal;

                if (canAdd > 0) {
                    element.textContent = `Total: ${currentTotal} (can add ${canAdd} more)`;
                    element.style.color = 'var(--theme-text-secondary, #6c757d)';
                } else {
                    element.textContent = `Total: ${currentTotal} (at maximum for valid distribution)`;
                    element.style.color = '#17a2b8';
                }
            });
        }

        updateInputConstraints(poolName) {
            const pool = this.pools[poolName];
            if (!pool) return;

            const config = pool.config;
            const minValue = config.min_value ?? 0;
            const maxValue = config.max_value ?? 10;

            Object.entries(pool.inputs).forEach(([fieldName, input]) => {
                const currentValue = this.getInputValue(input);

                if (input.tagName === 'SELECT') {
                    // Handle select dropdowns - disable invalid options
                    Array.from(input.options).forEach(option => {
                        const optionValue = parseInt(option.value, 10);
                        if (isNaN(optionValue)) {
                            option.disabled = false;
                            return;
                        }
                        const isValid = this.isFieldValueValid(poolName, fieldName, optionValue);
                        option.disabled = !isValid;
                    });
                } else if (input.tagName === 'INPUT' && input.type === 'number') {
                    // Handle number inputs - set max dynamically
                    input.min = minValue;

                    // Find the maximum valid value for this field
                    let maxAllowed = currentValue;
                    for (let testValue = currentValue + 1; testValue <= maxValue; testValue++) {
                        if (this.isFieldValueValid(poolName, fieldName, testValue)) {
                            maxAllowed = testValue;
                        } else {
                            break;
                        }
                    }
                    input.max = maxAllowed;
                }
            });
        }

        // Public API for programmatic access
        getValues(poolName) {
            const pool = this.pools[poolName];
            if (!pool) return {};
            const values = {};
            Object.entries(pool.inputs).forEach(([fieldName, input]) => {
                values[fieldName] = this.getInputValue(input);
            });
            return values;
        }

        setValue(poolName, fieldName, value) {
            const pool = this.pools[poolName];
            if (!pool || !pool.inputs[fieldName]) return;
            const input = pool.inputs[fieldName];
            input.value = value;
            this.updateDisplay(poolName);
        }

        isValid(poolName) {
            const pool = this.pools[poolName];
            if (!pool) return true;

            const config = pool.config;
            const totalPoints = this.getTotalPoints(poolName);

            if (config.mode === 'simple') {
                return totalPoints <= config.total_budget;
            }

            if (config.mode === 'distribution' && config.targets) {
                const groupTotals = this.getCurrentGroupTotals(poolName);
                return this.isValidState(poolName, groupTotals);
            }

            return true;
        }

        isComplete(poolName) {
            const pool = this.pools[poolName];
            if (!pool) return false;

            const config = pool.config;
            const totalPoints = this.getTotalPoints(poolName);

            if (config.mode === 'simple') {
                return totalPoints === config.total_budget;
            }

            if (config.mode === 'distribution' && config.targets) {
                const totalBudget = config.targets.reduce((a, b) => a + b, 0);
                if (totalPoints !== totalBudget) return false;

                const groupTotals = this.getCurrentGroupTotals(poolName);
                const sortedTotals = Object.values(groupTotals).sort((a, b) => a - b);
                const sortedTargets = [...config.targets].sort((a, b) => a - b);

                return sortedTotals.every((val, idx) => val === sortedTargets[idx]);
            }

            return false;
        }
    }

    window.PointPoolManager = new PointPoolManager();

    const init = () => window.PointPoolManager.init();

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


class PointPoolInput(forms.NumberInput):
    """
    A number input widget for point pool fields.

    Self-contained: automatically injects JavaScript when rendered.
    Works with PointPoolMixin to provide constraint enforcement.
    """

    # Track if JS has been rendered in this request
    _js_rendered = False

    def __init__(
        self,
        pool_name=None,
        pool_group=None,
        pool_config=None,
        is_root=False,
        attrs=None,
    ):
        self.pool_name = pool_name
        self.pool_group = pool_group
        self.pool_config = pool_config
        self.is_root = is_root  # First widget renders config

        if attrs is None:
            attrs = {}
        super().__init__(attrs=attrs)

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)

        attrs["data-point-pool"] = "true"

        if self.pool_name:
            attrs["data-pool-name"] = self.pool_name

        if self.pool_group:
            attrs["data-pool-group"] = self.pool_group

        existing = attrs.get("class", "")
        attrs["class"] = f"{existing} point-pool-input".strip()

        return attrs

    def render(self, name, value, attrs=None, renderer=None):
        # Render the standard input
        input_html = super().render(name, value, attrs, renderer)

        parts = [input_html]

        # Inject JavaScript (only once per page)
        if not PointPoolInput._js_rendered:
            PointPoolInput._js_rendered = True
            parts.append(f"<script data-point-pool-js>{POINT_POOL_JS}</script>")

        # If this is the root widget and we have config, embed it
        if self.is_root and self.pool_config and self.pool_name:
            config_json = json.dumps(self.pool_config)
            parts.append(
                f'<script type="application/json" data-pool-config="{self.pool_name}">'
                f"{config_json}</script>"
            )

        # Add a micro-script to re-initialize (handles dynamic/AJAX-loaded forms)
        parts.append(
            "<script>" "if(window.PointPoolManager)window.PointPoolManager.init();" "</script>"
        )

        return mark_safe("".join(parts))

    @classmethod
    def reset_js_rendered(cls):
        """Reset the JS rendered flag. Called automatically between requests."""
        cls._js_rendered = False


class PointPoolSelect(forms.Select):
    """
    A select widget for point pool fields.

    Use this when fields have a finite set of valid values (e.g., 0-5).
    """

    # Track if JS has been rendered in this request
    _js_rendered = False

    def __init__(
        self,
        pool_name=None,
        pool_group=None,
        pool_config=None,
        is_root=False,
        attrs=None,
        choices=(),
    ):
        self.pool_name = pool_name
        self.pool_group = pool_group
        self.pool_config = pool_config
        self.is_root = is_root

        if attrs is None:
            attrs = {}
        super().__init__(attrs=attrs, choices=choices)

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)

        attrs["data-point-pool"] = "true"

        if self.pool_name:
            attrs["data-pool-name"] = self.pool_name

        if self.pool_group:
            attrs["data-pool-group"] = self.pool_group

        existing = attrs.get("class", "")
        attrs["class"] = f"{existing} point-pool-select".strip()

        return attrs

    def render(self, name, value, attrs=None, renderer=None):
        # Render the standard select
        select_html = super().render(name, value, attrs, renderer)

        parts = [select_html]

        # Inject JavaScript (only once per page)
        # Share the flag with PointPoolInput since they use the same JS
        if not PointPoolInput._js_rendered:
            PointPoolInput._js_rendered = True
            parts.append(f"<script data-point-pool-js>{POINT_POOL_JS}</script>")

        # If this is the root widget and we have config, embed it
        if self.is_root and self.pool_config and self.pool_name:
            config_json = json.dumps(self.pool_config)
            parts.append(
                f'<script type="application/json" data-pool-config="{self.pool_name}">'
                f"{config_json}</script>"
            )

        # Add a micro-script to re-initialize
        parts.append(
            "<script>" "if(window.PointPoolManager)window.PointPoolManager.init();" "</script>"
        )

        return mark_safe("".join(parts))

    @classmethod
    def reset_js_rendered(cls):
        """Reset the JS rendered flag."""
        # Share with PointPoolInput
        PointPoolInput._js_rendered = False


# Reset flag between requests using Django's request_finished signal
try:
    from django.core.signals import request_finished

    request_finished.connect(lambda sender, **kwargs: PointPoolInput.reset_js_rendered())
except ImportError:
    pass
