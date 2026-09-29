const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const scriptPath = path.join(__dirname, '../../static/characters/js/mage-rote-budget.js');
const script = fs.existsSync(scriptPath) ? fs.readFileSync(scriptPath, 'utf8') : '';
const spheres = ['correspondence', 'time', 'spirit', 'matter', 'life', 'forces', 'entropy', 'mind', 'prime'];

function page() {
    const elements = {
        select_or_create_rote: { checked: false },
        select_or_create_effect: { checked: false },
        rote_options: { value: '' },
        effect_options: { value: '' },
    };
    for (const name of spheres) elements[name] = { value: '0' };
    const handlers = {};
    const form = {
        elements,
        addEventListener: (name, handler) => { handlers[name] = handler; },
    };
    const preview = { hidden: false };
    const remaining = { textContent: '' };
    const budget = {
        dataset: { available: '5', roteCosts: '{"11":2}', effectCosts: '{"12":4}' },
        closest: () => form,
        querySelector: (selector) => selector === '[data-rote-preview]' ? preview : remaining,
    };
    vm.runInNewContext(script, { document: { querySelector: () => budget } });
    return { elements, handlers, preview, remaining };
}

test('Rote balance is projected for selected rotes and effects', () => {
    const { elements, handlers, preview, remaining } = page();
    assert.equal(preview.hidden, true);
    elements.rote_options.value = '11';
    handlers.change();
    assert.equal(preview.hidden, false);
    assert.equal(remaining.textContent, '3');
    elements.select_or_create_rote.checked = true;
    elements.effect_options.value = '12';
    handlers.change();
    assert.equal(remaining.textContent, '1');
});

test('New effect Sphere dots change the projected balance', () => {
    const { elements, handlers, preview, remaining } = page();
    elements.select_or_create_rote.checked = true;
    elements.select_or_create_effect.checked = true;
    handlers.change();
    assert.equal(preview.hidden, true);
    elements.forces.value = '2';
    elements.mind.value = '1';
    handlers.input();
    assert.equal(remaining.textContent, '2');
    elements.mind.value = '4';
    handlers.input();
    assert.equal(remaining.textContent, '-1');
});
