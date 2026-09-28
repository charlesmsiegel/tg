(function() {
    'use strict';

    const PRIMARY = Number(document.currentScript.dataset.primary);
    const SECONDARY = Number(document.currentScript.dataset.secondary);
    const TERTIARY = Number(document.currentScript.dataset.tertiary);
    const BASE = 3; // Each category starts with 3 points (1 per attribute)
    const MAX_ATTRIBUTE = 5;
    const MIN_ATTRIBUTE = 1;
    const TOTAL_POINTS = BASE * 3 + PRIMARY + SECONDARY + TERTIARY;

    // Target totals for each category - order doesn't matter, any category can be any target
    // Sort to ensure we always have [smallest, middle, largest] for comparison
    const TARGETS = [BASE + TERTIARY, BASE + SECONDARY, BASE + PRIMARY].sort((a, b) => a - b);

    // Attribute groupings
    const CATEGORIES = {
        physical: ['strength', 'dexterity', 'stamina'],
        social: ['charisma', 'manipulation', 'appearance'],
        mental: ['perception', 'intelligence', 'wits']
    };

    // Get all attribute input fields
    const inputs = {};
    Object.values(CATEGORIES).flat().forEach(attr => {
        const input = document.querySelector(`#id_${attr}`);
        if (input) {
            inputs[attr] = input;
            // Listen for changes on all inputs
            input.addEventListener('change', updateDisplay);
            input.addEventListener('input', updateDisplay);
        }
    });

    function getCategoryTotal(categoryName) {
        return CATEGORIES[categoryName].reduce((sum, attr) => {
            const value = parseInt(inputs[attr]?.value) || MIN_ATTRIBUTE;
            return sum + value;
        }, 0);
    }

    function getCurrentTotals() {
        return {
            physical: getCategoryTotal('physical'),
            social: getCategoryTotal('social'),
            mental: getCategoryTotal('mental')
        };
    }

    function getTotalPoints() {
        const totals = getCurrentTotals();
        return totals.physical + totals.social + totals.mental;
    }

    // Check if a given distribution can still reach a valid [6,8,10] assignment
    function isValidState(physTotal, socTotal, menTotal) {
        // Try all 6 permutations of assigning TARGETS to the three categories
        const permutations = [
            [physTotal, socTotal, menTotal],
        ];

        // Check if the current totals can fit into any permutation of TARGETS
        // Each category total must be <= some target, and we must be able to assign targets 1-to-1
        const currentTotals = [physTotal, socTotal, menTotal];

        // Generate all permutations of TARGETS
        const targetPermutations = [
            [TARGETS[0], TARGETS[1], TARGETS[2]],
            [TARGETS[0], TARGETS[2], TARGETS[1]],
            [TARGETS[1], TARGETS[0], TARGETS[2]],
            [TARGETS[1], TARGETS[2], TARGETS[0]],
            [TARGETS[2], TARGETS[0], TARGETS[1]],
            [TARGETS[2], TARGETS[1], TARGETS[0]],
        ];

        // Check if any permutation works
        for (const targetPerm of targetPermutations) {
            if (currentTotals[0] <= targetPerm[0] &&
                currentTotals[1] <= targetPerm[1] &&
                currentTotals[2] <= targetPerm[2]) {
                // This permutation could work
                return true;
            }
        }

        return false;
    }

    function isAttributeValueValid(attrName, targetValue) {
        // Can't exceed maximum or go below minimum
        if (targetValue > MAX_ATTRIBUTE || targetValue < MIN_ATTRIBUTE) {
            return false;
        }

        // Calculate what the totals would be with this attribute at targetValue
        const totals = getCurrentTotals();

        // Find which category this attribute belongs to
        let category = null;
        for (const [cat, attrs] of Object.entries(CATEGORIES)) {
            if (attrs.includes(attrName)) {
                category = cat;
                break;
            }
        }

        if (!category) return false;

        // Get current value of this attribute
        const currentValue = parseInt(inputs[attrName]?.value) || MIN_ATTRIBUTE;

        // Adjust the category total to reflect the new value
        totals[category] = totals[category] - currentValue + targetValue;

        // Check if the new state is still valid
        return isValidState(totals.physical, totals.social, totals.mental);
    }

    function canIncreaseAttribute(attrName) {
        const currentValue = parseInt(inputs[attrName]?.value) || MIN_ATTRIBUTE;
        return isAttributeValueValid(attrName, currentValue + 1);
    }

    // The target each category is heading for: the categories ranked by their
    // current totals take primary, secondary and tertiary in that order (ties
    // keep Physical, Social, Mental order), which is the assignment that
    // overshoots least. Returns {category: target}.
    function getRankedTargets() {
        const totals = getCurrentTotals();
        const ranked = Object.keys(CATEGORIES).sort((a, b) => totals[b] - totals[a]);
        const descending = TARGETS.slice().reverse();
        const assigned = {};
        ranked.forEach((categoryName, index) => { assigned[categoryName] = descending[index]; });
        return assigned;
    }

    // State classes instead of colours: the stylesheet maps them to tokens.
    function setState(element, state) {
        element.classList.toggle('is-over', state === 'over');
        element.classList.toggle('is-ready', state === 'ready');
        element.classList.toggle('is-done', state === 'done');
    }

    function plural(count) {
        return count + ' point' + (count !== 1 ? 's' : '');
    }

    function updateDisplay() {
        const totals = getCurrentTotals();
        const totalPoints = getTotalPoints();
        const pointsRemaining = TOTAL_POINTS - totalPoints;

        // Check if we have a valid distribution
        const sortedTotals = [totals.physical, totals.social, totals.mental].sort((a,b) => a-b);
        const isValidDistribution = pointsRemaining === 0 &&
                                   sortedTotals.length === TARGETS.length &&
                                   sortedTotals.every((val, idx) => val === TARGETS[idx]);

        // Update total remaining points and the status tag beside it
        const totalElement = document.getElementById('total-remaining');
        const tagElement = document.querySelector('[data-allocation-tag]');
        let state = 'progress';
        if (totalElement) {
            if (pointsRemaining > 0) {
                totalElement.textContent = plural(pointsRemaining) + ' remaining to allocate';
            } else if (pointsRemaining === 0) {
                // Check if it's a valid distribution
                if (isValidState(totals.physical, totals.social, totals.mental)) {
                    if (isValidDistribution) {
                        totalElement.textContent = 'Complete! Valid distribution achieved.';
                        state = 'ready';
                    } else {
                        totalElement.textContent = 'All points allocated - verify distribution is correct';
                    }
                } else {
                    totalElement.textContent = 'All points allocated - but distribution is invalid';
                    state = 'over';
                }
            } else {
                totalElement.textContent = plural(Math.abs(pointsRemaining)) + ' over limit!';
                state = 'over';
            }
            setState(totalElement, state);
        }
        // A category above its ranked target is too many even while dots remain.
        const ranked = getRankedTargets();
        if (state === 'progress' && Object.keys(ranked).some(name => totals[name] > ranked[name])) {
            state = 'over';
        }
        if (tagElement) {
            tagElement.textContent = state === 'ready' ? 'Ready' : state === 'over' ? 'Too many' : 'In progress';
            setState(tagElement, state);
        }

        // Per-category count against its ranked target: "n left", "done" or "n over"
        for (const [categoryName, currentTotal] of Object.entries(totals)) {
            const element = document.getElementById(categoryName + '-status');
            if (element) {
                const difference = ranked[categoryName] - currentTotal;
                if (difference < 0) {
                    element.textContent = -difference + ' over';
                    setState(element, 'over');
                } else if (difference > 0) {
                    element.textContent = difference + ' left';
                    setState(element, 'progress');
                } else {
                    element.textContent = 'done';
                    setState(element, 'done');
                }
            }
        }

        // Validate each input and enforce constraints
        Object.entries(inputs).forEach(([attrName, input]) => {
            if (!input) return;

            const currentValue = parseInt(input.value) || MIN_ATTRIBUTE;

            if (input.tagName === 'SELECT') {
                // Handle select dropdowns
                Array.from(input.options).forEach(option => {
                    const optionValue = parseInt(option.value);
                    // Check if this specific value would be valid
                    const isValid = isAttributeValueValid(attrName, optionValue);
                    option.disabled = !isValid;
                });
            } else if (input.tagName === 'INPUT' && input.type === 'number') {
                // Handle number inputs - set max attribute dynamically
                input.min = MIN_ATTRIBUTE;

                // Find the maximum valid value for this attribute
                let maxAllowed = currentValue;
                for (let testValue = currentValue + 1; testValue <= MAX_ATTRIBUTE; testValue++) {
                    if (isAttributeValueValid(attrName, testValue)) {
                        maxAllowed = testValue;
                    } else {
                        break;
                    }
                }

                input.max = maxAllowed;
            }
        });
    }

    // Initial update on page load
    updateDisplay();
})();
