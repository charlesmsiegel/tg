# Wraith: Shadow/Psyche Transition Mechanics

This document explains the mechanics for Wraiths becoming Spectres (Shadow dominant) and the reverse process of redemption.

## Catharsis Mechanics

**Catharsis** occurs when the Shadow temporarily takes control of the wraith's corpus.

### Triggering Catharsis
- **Trigger Condition**: Shadow's temporary Angst exceeds Psyche's permanent Willpower
- **Check Method**: `wraith.check_catharsis_trigger()`
- **Activate**: `wraith.trigger_catharsis()`

### During Catharsis
- `in_catharsis` flag is set to `True`
- `is_shadow_dominant` is set to `True`
- `catharsis_count` is incremented
- Shadow controls the wraith's actions for the scene

### Resolving Catharsis
```python
wraith.resolve_catharsis(shadow_won=False)  # Psyche regains control
wraith.resolve_catharsis(shadow_won=True)   # Shadow maintains dominance
```

## Harrowing Mechanics

**Harrowing** is when the Psyche enters the Labyrinth to face the Shadow in a spiritual battle.

### Harrowing Triggers
Checked via `wraith.check_harrowing_trigger()` which returns a list of active triggers:

1. **zero_willpower**: Willpower reduced to 0
2. **zero_corpus**: Corpus reduced to 0 or below
3. **no_fetters**: All Fetters lost
4. **max_angst**: Permanent Angst reaches 10 (Spectrehood threshold)

### Triggering Harrowing
```python
result = wraith.trigger_harrowing(trigger_type="zero_willpower")
# Returns info about the Harrowing event
```

### Resolving Harrowing
```python
wraith.resolve_harrowing(result="success")    # Psyche survives
wraith.resolve_harrowing(result="failure")    # Becomes Spectre
wraith.resolve_harrowing(result="catharsis")  # Extraordinary success, reduces Angst
```

**Results:**
- **Success**: Wraith survives, continues as normal
- **Catharsis**: Extraordinary success - reduces Permanent Angst by 1 and temporary Angst by 3
- **Failure**: Wraith becomes a Spectre (calls `become_spectre()`)

## Becoming a Spectre

When a Wraith loses a Harrowing or succumbs to their Shadow:

```python
wraith.become_spectre()
```

### Effects:
1. **Character Type**: Changes from "wraith" to "spectre"
2. **Shadow Dominance**: `is_shadow_dominant` set to `True`
3. **Spectrehood Date**: Timestamp recorded
4. **Passions**: All normal Passions converted to Dark Passions
5. **Fetters**: All Fetter ratings halved (representing weakened connection to living world)
6. **Eidolon**: Any Eidolon background points converted to Permanent Angst (Eidolon suppressed)

### Automatic Changes:
- Passions become twisted, shadow-driven versions
- Connection to living world weakens
- Shadow takes permanent control
- Character now serves Oblivion

## Redemption Mechanics

Spectres can potentially be redeemed back to Wraith status through a difficult process.

### Checking Redemption Eligibility
```python
result = wraith.attempt_redemption()
```

### Requirements:
1. **At least 1 Fetter** must remain (connection to living world)
2. **Permanent Angst < 10** (must be reduced through Castigate or other means)
3. **External Assistance** required (Pardoner, Darksider, or similar)

### Redemption Process

1. **Check Eligibility**:
```python
check = wraith.attempt_redemption()
if check["can_attempt"]:
    # Proceed with contested roll
```

2. **Contested Roll**:
- **Psyche Pool**: Willpower + Eidolon (if any)
- **Shadow Pool**: Permanent Angst
- **Difficulty**: 6 for both sides

3. **Complete Redemption**:
```python
result = wraith.complete_redemption(
    psyche_successes=3,  # Psyche rolled 3 successes
    shadow_successes=1   # Shadow rolled 1 success
)
```

### Success Effects:
- Character type changes back to "wraith"
- `is_shadow_dominant` set to `False`
- Dark Passions redeemed (number based on margin of success)
- Permanent Angst reduced by margin of success
- Temporary Angst reduced by 2× margin of success

### Failure Effects:
- Remains a Spectre
- Shadow grows stronger from failed attempt
- Can attempt again if requirements are met

## Utility Methods

### Get Current Status
```python
# Catharsis information
catharsis_info = wraith.get_catharsis_info()
# Returns: in_catharsis, catharsis_count, can_trigger, shadow_dominant, angst, willpower

# Harrowing information
harrowing_info = wraith.get_harrowing_info()
# Returns: harrowing_count, last_result, active_triggers, at_risk, angst_permanent, corpus, willpower
```

## Example Workflow

### Wraith Falls to Shadow
```python
# Wraith's Angst rises above Willpower
if wraith.check_catharsis_trigger():
    wraith.trigger_catharsis()
    # Shadow takes control for the scene

# Later, Catharsis resolves
wraith.resolve_catharsis(shadow_won=True)  # Shadow maintains control

# Eventually, a Harrowing is triggered
triggers = wraith.check_harrowing_trigger()
if "max_angst" in triggers:
    wraith.trigger_harrowing(trigger_type="max_angst")
    # Contested roll happens...
    wraith.resolve_harrowing(result="failure")
    # Wraith becomes Spectre
```

### Spectre Redemption
```python
# Check if redemption is possible
check = spectre.attempt_redemption()

if check["can_attempt"]:
    # Perform contested rolls
    psyche_roll = roll_dice(spectre.willpower + spectre.eidolon, difficulty=6)
    shadow_roll = roll_dice(spectre.angst_permanent, difficulty=6)

    # Complete redemption
    result = spectre.complete_redemption(
        psyche_successes=psyche_roll,
        shadow_successes=shadow_roll
    )

    if result["success"]:
        print(f"Redeemed! {result['passions_redeemed']} Passions restored.")
    else:
        print("Redemption failed. Shadow remains in control.")
```

## Fields Reference

### New Wraith Model Fields:

- `in_catharsis` (bool): Currently in Catharsis event
- `catharsis_count` (int): Total number of Catharsis events
- `harrowing_count` (int): Total number of Harrowings
- `last_harrowing_result` (str): Result of last Harrowing (none/success/failure/catharsis)
- `is_shadow_dominant` (bool): Whether Shadow currently controls the wraith
- `spectrehood_date` (datetime): When wraith became Spectre (if applicable)
- `redemption_attempts` (int): Number of redemption attempts made
