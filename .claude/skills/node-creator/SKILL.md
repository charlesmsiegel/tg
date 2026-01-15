---
name: node-creator
description: "Create Nodes (places of power where Quintessence gathers) for Mage: The Ascension 20th Anniversary Edition. Handles Rank, Size, Ratio, Resonance, merits/flaws, Reality Zones, and output calculations. Requires mage-rules-reference for Resonance/Practice lookups. Triggers: create a node, design a place of power, M20 node, stat up a node, quintessence wellspring."
---

# Node Creator

Design mechanically valid Nodes for M20. Source: *Sources of Magick* by Charles Siegel.

## What is a Node?

A Node is a location where Quintessence naturally gathers, providing:
- **Quintessence**: Free-flowing energy absorbed directly
- **Tass**: Solidified Quintessence in physical form
- **Reality Zone**: Area where certain Practices work better/worse

## Core Statistics

### Rank (0-10)

| Rank | Description | Base Points |
|------|-------------|-------------|
| 1 | Minor trickle | 3 |
| 2 | Small wellspring | 6 |
| 3 | Moderate source | 9 |
| 4 | Significant power | 12 |
| 5 | Major Node | 15 |
| 6+ | Legendary | 18+ |

**Base Points = 3 × Rank**

### Size

| Rating | Size | Point Modifier |
|--------|------|----------------|
| -2 | Household Object | Grants +2 |
| -1 | Small Room | Grants +1 |
| 0 | Average Room | No modifier |
| +1 | Small Building | Costs 1 |
| +2 | Large Building | Costs 2 |

### Ratio (Quintessence : Tass)

| Rating | Ratio | Description | Point Modifier |
|--------|-------|-------------|----------------|
| -2 | 0.0 | All Tass | Grants +2 |
| -1 | 0.25 | Mostly Tass | Grants +1 |
| 0 | 0.5 | Equal split | No modifier |
| +1 | 0.75 | Mostly Quint | Costs 1 |
| +2 | 1.0 | All Quint | Costs 2 |

## Point Calculation

```
Points Remaining = Base Points - Resonance Cost - Merit/Flaw Cost - Size - Ratio

Quintessence/Week = floor(Points Remaining × Ratio)
Tass/Week = Points Remaining - Quintessence/Week
```

**Validation**: Points Remaining must be > 0

## Resonance

Total Resonance must equal or exceed **Minimum Required**:
```
Minimum Required = Rank + Resonance from Merits/Flaws
```

- **Sphere Attuned** grants 1 free Resonance (Sphere-appropriate)
- **Corrupted** adds "Corrupted 2" automatically

Only Resonance beyond Minimum Required costs points (1 per extra dot).

Query traits via mage-rules-reference:
```bash
python lookup.py references/resonance-traits.json "Forces"
```

## Merits & Flaws

Maximum 7 points each. See [references/node-merits-flaws.md](references/node-merits-flaws.md) for full details.

**Common Merits**: Cyclic Node [1-2], Famous Node [1-5], Focus Locked [1-3], Functioning Caern/Freehold/Haunt [2], Genius Locus [3,5], Manifestation [1-5], Shallowing [2], Sphere Attuned [2], Spirit Guardian [1-5]

**Common Flaws**: Corrupted [-4], Dangerous Energies [-3], Enemy [-1 to -5], Former Caern/Freehold/Haunt [-2], Infamous Node [-1 to -5], Isolated Node [-2], Shallowing [-2]

## Reality Zone

Every Node has a Reality Zone equal to its Rank.

**Rules:**
1. Total Practice ratings must equal exactly 0
2. Sum of positive ratings must equal Rank
3. Use only base Practices (query `practices.json`)

```bash
# List valid practices
python lookup.py references/practices.json --keys

# Check excluded practices
python lookup.py references/reality-zones.json "excluded_practices"
```

**Design**: Match Practices to Node concept. Library → +High Ritual Magick, -Gutter Magick.

## Creation Workflow

1. **Concept**: Location, why Quintessence gathers, atmosphere
2. **Set Rank**: 1-3 for starting cabals, 4-5 major, 6+ legendary
3. **Choose Size/Ratio**: Physical extent and energy manifestation
4. **Select Resonance**: Traits totaling ≥ Minimum Required
5. **Add Merits/Flaws**: Story complications and benefits
6. **Design Reality Zone**: Practices summing to 0, positives = Rank
7. **Describe Output**: Quintessence feel, Tass physical form
8. **Validate**: All checks must pass

## Validation Checklist

- [ ] Rank 0-10
- [ ] Points Remaining > 0
- [ ] Total Resonance ≥ Minimum Required
- [ ] Reality Zone sums to 0
- [ ] Reality Zone positive total = Rank
- [ ] Merit/Flaw limits ≤ 7 each
- [ ] Functioning Freehold has Sphere Attuned (Mind)
- [ ] Functioning Caern (if Sphere Attuned) is Spirit
- [ ] Quint/week + Tass/week = Points Remaining

## Point Validation Block

Include in output:
```
Base Points:           [3 × Rank] = X
- Resonance beyond min:         - X
- Net Merit/Flaw Cost:          - X
- Size Cost:                    - X
- Ratio Cost:                   - X
= Points Remaining:             = X

Output: X Quint/week + X Tass/week = X (matches Points Remaining)
Resonance: X total (min required: X) ✓
Reality Zone: +X positive, sum = 0 ✓
```

## Output Format

See [references/output-template.md](references/output-template.md) for complete format.
