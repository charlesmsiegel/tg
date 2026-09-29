const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const scriptPath = path.join(__dirname, '../../static/characters/js/linked-npc-fields.js');
const script = fs.existsSync(scriptPath) ? fs.readFileSync(scriptPath, 'utf8') : '';

function page() {
    const select = { value: '', addEventListener: (name, handler) => { select.onChange = handler; } };
    function group(dataset) {
        const input = { disabled: false };
        return { dataset, hidden: false, input, querySelectorAll: () => [input] };
    }
    const archetypes = group({ npcExcept: 'werewolf changeling fera' });
    const vampire = group({ npcTypes: 'vampire' });
    const werewolf = group({ npcTypes: 'werewolf fera' });
    const groups = [archetypes, vampire, werewolf];
    const section = {
        dataset: {},
        querySelector: () => select,
        querySelectorAll: () => groups,
    };
    vm.runInNewContext(script, {
        document: {
            readyState: 'complete',
            addEventListener: () => {},
            querySelector: () => section,
        },
    });
    return { select, archetypes, vampire, werewolf };
}

test('Allies details follow the selected character type', () => {
    const { select, archetypes, vampire, werewolf } = page();
    assert.equal(vampire.hidden, true);
    assert.equal(archetypes.hidden, true);
    select.value = 'vampire';
    select.onChange();
    assert.equal(vampire.hidden, false);
    assert.equal(archetypes.hidden, false);
    assert.equal(werewolf.hidden, true);
    assert.equal(werewolf.input.disabled, true);
    select.value = 'werewolf';
    select.onChange();
    assert.equal(vampire.hidden, true);
    assert.equal(archetypes.hidden, true);
    assert.equal(werewolf.hidden, false);
    assert.equal(werewolf.input.disabled, false);
});
