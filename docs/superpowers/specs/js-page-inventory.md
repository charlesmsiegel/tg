# Page JavaScript inventory

Inspected 2026-09-26 before implementation. Paths in the source column are relative
to `<app>/templates/<app>/`; destinations are relative to
`<app>/static/<app>/js/`. There are 23 executable inline blocks in 22 templates
in this scope, plus the existing external jQuery include. The excluded scene
script belongs to Step 11. No inline event attributes or `javascript:` URLs were
found in these scoped template trees.

| App | Template | Destination | Configuration / load condition | Step 10 candidate |
| --- | --- | --- | --- | --- |
| accounts | detail.html | detail.js | None; collapse event listeners registered on DOMContentLoaded | No |
| characters | changeling/ctdhuman/template_select.html | ctdhuman-template-select.js | None; gameline-specific colors remain literal | No |
| characters | demon/dtfhuman/template_select.html | dtfhuman-template-select.js | None; gameline-specific colors remain literal | No |
| characters | mage/mtahuman/template_select.html | mtahuman-template-select.js | None; gameline-specific colors remain literal | No |
| characters | vampire/vtmhuman/template_select.html | vtmhuman-template-select.js | None; gameline-specific colors remain literal | No |
| characters | werewolf/wtahuman/template_select.html | wtahuman-template-select.js | None; gameline-specific colors remain literal | No |
| characters | wraith/wtohuman/template_select.html | wtohuman-template-select.js | None; gameline-specific colors remain literal | No |
| characters | core/attribute_block/form.html | attribute-validation.js | `primary`, `secondary`, `tertiary` scalar data attributes | Yes: preserve validator |
| characters | core/ability_block/validation.html | ability-validation.js | Same targets; rendered only when all three are truthy; depends on TG.validation | Yes: preserve validator |
| characters | core/background_block/form.html | background-validation.js | `object.background_points`; `background_multipliers_json` serialized integer map; budget truthy guard; depends on TG.validation | Yes: preserve validator |
| characters | mage/mage/mage_enhancements_form.html | mage-enhancements.js | None | Possible conditional rewrite |
| characters | mage/mage/mage_xp_form.html block 1 | mage-xp.js | `object.is_group_member` boolean | Possible conditional rewrite |
| characters | mage/mage/mage_xp_form.html block 2 | mage-xp-rote.js | None | Possible conditional rewrite |
| characters | mage/sorcerer/sorcerer_freebies_form.html | sorcerer-freebies.js | `object.sorcerer_type` string | Possible conditional rewrite |
| characters | vampire/vampire/chargen.html | vampire-virtues.js | `object.creation_status == 5` guard; depends on TG.validation | Possible validator rewrite |
| characters | werewolf/gift/list.html | gift-list.js | Existing DOM filter inputs and row attributes | No |
| characters | wraith/thorn/list.html | thorn-list.js | Existing DOM filter inputs and row attributes | No |
| items | mage/wonder/form_include.html | wonder-form.js | Existing effect row prefixes; listens for dynamically added formset rows | No |
| locations | changeling/freehold/form.html | freehold-form.js | None | Possible conditional rewrite |
| locations | changeling/freehold/chargen/features.html | freehold-features.js | None | Possible conditional rewrite |
| locations | changeling/freehold/chargen/powers.html | freehold-powers.js | None | Possible conditional rewrite |
| locations | mage/chantry/effects_form.html | chantry-effects.js | None; existing preceding external jQuery 3.5.1 include retained | No |
| game | week/detail.html | week-detail.js | Rendered only for `is_st` with `pending_requests` | No |

All destinations will use ordinary synchronous script references at each original
script position, preserving registration and initialization order. Scalar
configuration belongs in escaped HTML data attributes. The background multiplier
value is already a JSON string, so Django `json_script` safely serializes that
string and the consumer parses both the JSON transport and the original JSON map;
this avoids modifying the view contract. Django-only comments are removed from
extracted JS. Algorithm bodies, current event hooks, and template conditions stay
unchanged. The six template selection scripts retain their distinct colors rather
than introducing shared behavior during relocation.

There are also 14 `form.conditional_js` outputs in these trees (freebie pages plus
core/npc/create.html). These now output only inert JSON rules; the conditional
form mixin declares the external behavior through its Media property.

A final scan of every app template found the account profile collapse listener
above; it is included in these corrected counts. Only the excluded scene page
retains executable inline JavaScript. Existing CSP blockers include inline
handlers in core/character_template/detail.html, core/character_template/list.html
and core/errors/500.html; these are unchanged.
