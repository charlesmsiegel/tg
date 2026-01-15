# Output Templates

## Main Chantry Document

```markdown
# [Chantry Name]

**Rank:** [X] | **Faction:** [Name] | **Season:** [Season] | **Founded:** [Year]

[Read the full history](history.md)

## Concept

[2-3 paragraphs describing the chantry's current atmosphere, purpose, and character. Keep historical details brief—full history is in history.md]

## Statistics

### Backgrounds

| Background | Rating | Cost | Notes |
|------------|--------|------|-------|
| Node | [X] | [X pts] | [Link to node file] |
| Library | [X] | [X pts] | [Link to library file] |
| Sanctum | [X] | [X pts] | [Link to sanctum file] |
| Horizon Realm | [X] | [X pts] | [Link to realm file] |
| Retainers | [X] | [X pts] | [X sorcerers, X consors] |
| Resources | [X] | [X pts] | [Description] |
| ... | | | |
| **Total** | | **[X pts]** | |

### Leadership

**Type:** [Leadership Type]

| Position | Member | Arete |
|----------|--------|-------|
| [Title] | [Link to member] | [X] |

### Membership

| Category | Count | File |
|----------|-------|------|
| Leadership | [X] | [Link](members/leadership.md) |
| [Role Group] | [X] | [Link](members/[group].md) |
| Apprentices | [X] | [Link](members/apprentices.md) |
| Retainers | [X] | [Link](members/retainers.md) |
| **Total** | **[X]** | |

## Physical Location

[Description of location. Urban/rural, mundane cover, general layout.]

### Key Areas

| Location | Purpose | Link |
|----------|---------|------|
| [Name] | [Brief purpose] | [Link](locations/[name].md) |

## Magical Features

### Wards and Protections

[Description of magical security. Link to relevant rotes and items.]

- [Ward Name](rotes/[ward].md) — [Brief effect]
- [Item Name](items/common/[item].md) — [Brief purpose]

### Integrated Effects

[Any permanent magical features. Link to Enhancement background details if applicable.]

## Common Property

Items belonging to the chantry as a whole:

| Item | Type | Location | Link |
|------|------|----------|------|
| [Name] | [Charm/Talisman/etc.] | [Where stored] | [Link](items/common/[item].md) |

## Political Position

[1-2 paragraphs describing the chantry's role in faction politics, alliances, rivalries, reputation.]

## Story Hooks

- [Hook 1: Mystery or threat]
- [Hook 2: Opportunity or resource]
- [Hook 3: Internal conflict or challenge]
- [Hook 4: External relationship]
- [Hook 5: Historical secret or unfinished business]
```

## History Document

```markdown
# History of [Chantry Name]

**Founded:** [Year] | **Current Era:** [Season/phase]

## Founding

[2-3 paragraphs: who founded it, why, under what circumstances, original location, founding members, initial purpose, early challenges.]

## Early Years

[2-3 paragraphs: establishment period (first decade), struggles, achievements, faction relationships, identity formation.]

## Growth and Development

[2-3 paragraphs: evolution over time, expansion, membership changes, resource acquisition, signature practices, conflicts resolved, alliances formed.]

## Modern Era

[2-3 paragraphs: recent history, current leadership, present challenges/opportunities, ongoing projects, current faction role. Reference current members.]

## Major Events Timeline

| Year | Event |
|------|-------|
| [Year] | [Founding description] |
| [Year] | [Resource acquisition — link to Node/Library/etc.] |
| [Year] | [Major conflict or alliance] |
| [Year] | [Important discovery or creation — link to grimoire/rote] |
| [Year] | [Leadership change — link to member] |
| [Year] | [Recent significant event] |

## Notable Historical Figures

### [Historical Figure Name]

[2-3 sentences: role, contributions, legacy. Link to items, locations, or practices they established.]

## Legacy and Influence

[1-2 paragraphs: lasting impact on faction, reputation, unique contributions, what makes it distinctive.]
```

## Location File

```markdown
# [Location Name]

**Type:** [Room/Building/Area] | **Access:** [Open/Restricted/Leadership Only]

## Description

[2-3 paragraphs: physical description, atmosphere, sensory details.]

## Purpose

[What activities happen here, who uses it, when.]

## Notable Features

- [Feature 1 with links to relevant items/rotes]
- [Feature 2]

## Associated Members

- [Member](../members/[file].md#anchor) — [their connection]

## Story Hooks

- [Hook specific to this location]
```

## Point Validation Block

Include in main document after Background table:

```
VALIDATION:
Budget: [X] pts
Spent: [X] pts
Remaining: [X] pts
Rank: [X] (requires [X-X] pts) ✓
```

## Cross-Link Examples

```markdown
# From main document:
[Read the full history](history.md)
[The Athenaeum](libraries/athenaeum.md)
[Magister Cross](members/leadership.md#magister-scholae-octavian-cross)
[House Wards](items/common/house_wards.md)

# From member file:
[Covenant of the Silver Key](../covenant_of_the_silver_key.md)
[The Wellspring](../nodes/wellspring.md)
[Octavian's Mirror](../items/personal/octavians_mirror.md)

# From history:
[Current Deacon Helena](members/leadership.md#magistra-helena-valcourt)
[The Athenaeum](libraries/athenaeum.md) was established in 1891
```

Anchor format: lowercase with hyphens (`#magister-scholae-helena-valcourt`)
