const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const script = fs.readFileSync(
    path.join(__dirname, '../../static/characters/js/mage-spheres.js'), 'utf8'
);
const names = ['correspondence', 'time', 'spirit', 'forces', 'matter', 'life', 'entropy', 'mind', 'prime'];

function page() {
    const controls = {};
    const elements = { arete: { value: '1' }, resonance: { value: 'Dynamic' } };
    const paints = [];
    for (const name of names) {
        const dots = Array.from({ length: 5 }, (_, index) => ({ dataset: { value: String(index + 1) }, hidden: false }));
        const control = {
            dataset: { min: '0' },
            querySelectorAll: () => dots,
        };
        controls[name] = { control, dots };
        elements[name] = {
            value: '0',
            min: '0',
            closest: () => control,
            dispatchEvent: () => {},
        };
    }
    elements.affinity_sphere = {
        dataset: { sphereMap: '{"7":"mind"}' },
        selectedOptions: [{ value: '', textContent: '' }],
    };
    const handlers = {};
    const form = {
        elements,
        addEventListener: (name, handler) => { handlers[name] = handler; },
        querySelector: () => ({ disabled: false }),
    };
    const count = { textContent: '' };
    const message = { textContent: '' };
    const budget = {
        dataset: { target: '6', npc: 'false' },
        closest: () => form,
        querySelector: (selector) => selector === '[data-sphere-count]' ? count : message,
    };
    vm.runInNewContext(script, {
        document: { querySelector: () => budget },
        window: { TGDots: { paint: (control) => paints.push(control) } },
        Event: class Event {},
    });
    return { elements, controls, handlers, paints, count };
}

test('Sphere dot buttons follow Arete and ratings shrink when Arete falls', () => {
    const { elements, controls, handlers } = page();
    assert.deepEqual(controls.forces.dots.map((dot) => dot.hidden), [false, true, true, true, true]);
    elements.arete.value = '3';
    handlers.change();
    assert.deepEqual(controls.forces.dots.map((dot) => dot.hidden), [false, false, false, true, true]);
    elements.forces.value = '3';
    elements.arete.value = '1';
    handlers.change();
    assert.equal(elements.forces.value, '1');
    assert.deepEqual(controls.forces.dots.map((dot) => dot.hidden), [false, true, true, true, true]);
});

test('Selecting an Affinity Sphere adds and protects its first dot', () => {
    const { elements, controls, handlers, paints, count } = page();
    elements.affinity_sphere.selectedOptions = [{ value: '7', textContent: 'Mind (preferred)' }];
    handlers.change();
    assert.equal(elements.mind.value, '1');
    assert.equal(controls.mind.control.dataset.min, '1');
    assert.equal(count.textContent, '1 / 6');
    assert.ok(paints.includes(controls.mind.control));
    elements.mind.value = '0';
    handlers.input();
    assert.equal(elements.mind.value, '1');
});
