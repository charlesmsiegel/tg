const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const scriptPath = path.join(__dirname, '../../static/characters/js/linked-npc-fields.js');
const script = fs.existsSync(scriptPath) ? fs.readFileSync(scriptPath, 'utf8') : '';

function page() {
    const select = { value: '', addEventListener: (name, handler) => { select.onChange = handler; } };
    function choice(values) {
        const field = {
            value: '',
            options: values.map(value => ({ value, hidden: false, disabled: false })),
            addEventListener: (name, handler) => { field.onChange = handler; },
        };
        return field;
    }
    const feraType = choice(['', 'bastet', 'corax']);
    const feraBreed = choice(['', 'homid', 'feline', 'corvid']);
    const affiliation = choice(['', '1', '4']);
    const faction = choice(['', '2', '5']);
    const subfaction = choice(['', '3', '6']);
    const fields = { fera_type: feraType, fera_breed: feraBreed, affiliation, faction, subfaction };
    function group(dataset) {
        const input = { disabled: false };
        return { dataset, hidden: false, input, querySelectorAll: () => [input] };
    }
    const archetypes = group({ npcExcept: 'werewolf changeling fera' });
    const vampire = group({ npcTypes: 'vampire' });
    const werewolf = group({ npcTypes: 'werewolf fera' });
    const groups = [archetypes, vampire, werewolf];
    const details = { hidden: false };
    const section = {
        dataset: {
            feraBreeds: JSON.stringify({ bastet: ['homid', 'feline'], corax: ['homid', 'corvid'] }),
            factionParents: JSON.stringify({ 1: '', 2: '1', 3: '2', 4: '', 5: '4', 6: '5' }),
        },
        querySelector: (selector) => selector === '[data-linked-npc-details]' ? details :
            selector === '[name="npc_type"]' ? select : fields[selector.match(/\[name="(.+)"\]/)?.[1]],
        querySelectorAll: () => groups,
    };
    vm.runInNewContext(script, {
        document: {
            readyState: 'complete',
            addEventListener: () => {},
            querySelector: () => section,
        },
    });
    return { select, details, archetypes, vampire, werewolf, fields };
}

test('Allies details follow the selected character type', () => {
    const { select, details, archetypes, vampire, werewolf } = page();
    assert.equal(details.hidden, true);
    assert.equal(vampire.hidden, true);
    assert.equal(archetypes.hidden, true);
    select.value = 'vampire';
    select.onChange();
    assert.equal(details.hidden, false);
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

test('Fera breed and Mage faction choices follow their parent selectors', () => {
    const { fields } = page();
    fields.fera_type.value = 'bastet';
    fields.fera_type.onChange();
    assert.equal(fields.fera_breed.options.find(option => option.value === 'feline').hidden, false);
    assert.equal(fields.fera_breed.options.find(option => option.value === 'corvid').hidden, true);
    fields.fera_breed.value = 'feline';
    fields.fera_type.value = 'corax';
    fields.fera_type.onChange();
    assert.equal(fields.fera_breed.value, '');
    fields.affiliation.value = '1';
    fields.affiliation.onChange();
    assert.equal(fields.faction.options.find(option => option.value === '2').disabled, false);
    assert.equal(fields.faction.options.find(option => option.value === '5').disabled, true);
    fields.faction.value = '2';
    fields.faction.onChange();
    assert.equal(fields.subfaction.options.find(option => option.value === '3').hidden, false);
    assert.equal(fields.subfaction.options.find(option => option.value === '6').hidden, true);
});
