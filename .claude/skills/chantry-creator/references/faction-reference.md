# Faction Reference

All faction-specific data is in **mage-rules-reference**. Query via lookup script.

## Chantry Names

```bash
# Get chantry term for a faction
python lookup.py references/faction-chantry-names.json "Order of Hermes"
# Output: "Covenant"

python lookup.py references/faction-chantry-names.json "Verbena"
# Output: "Grove"

# List all faction chantry names
python lookup.py references/faction-chantry-names.json --all
```

## Title Systems

```bash
# Get title structure for a faction
python lookup.py references/faction-titles.json "Order of Hermes"
# Output: by_arete, gendered forms, houses

python lookup.py references/faction-titles.json "Celestial Chorus"
# Output: by_role (leader, senior, member, apprentice), sub_factions
```

**Title format varies by faction:**
- **Order of Hermes**: Titles by Arete level (Initiate → Magister Mundi)
- **Most Traditions**: Titles by role (leader, senior, member, apprentice)
- **Technocracy**: Professional titles by role

## Practices

```bash
# Get practices for a faction
python lookup.py references/faction-practices.json "Order of Hermes"
# Output: High Ritual Magick, Alchemy, Dominion, etc.

# Get abilities for a practice
python lookup.py references/practice-abilities.json "High Ritual Magick"
```

## Languages

```bash
# Get common languages for a faction
python lookup.py references/faction-languages.json "Order of Hermes"
# Output: Latin, Enochian, etc.
```

## Workflow

1. **Get chantry name**: Query `faction-chantry-names.json`
2. **Get title system**: Query `faction-titles.json`
3. **Get practices**: Query `faction-practices.json`
4. **Apply titles**: Use by_arete or by_role based on faction structure
5. **Name members**: Follow faction naming conventions (see below)

## Naming Conventions

**Order of Hermes**: Latin names, classical references, titles of achievement
- Examples: Octavian Cross, Helena Valcourt, Marcus Aurelius Drake

**Celestial Chorus**: Religious names, saint references, faith titles
- Examples: Brother Thomas, Sister Miriam, Father Xavier

**Akashayana**: Sanskrit/Asian names, dharma names
- Examples: Sifu Chen Wei, Master Ananda, Disciple Sanjay

**Verbena**: Celtic/pagan names, nature references, craft names
- Examples: Rowan Thornwood, Brighid Moonwater, Elder Ashwhisper

**Virtual Adepts**: Handles, codenames, tech references
- Examples: Crash_Override, NeonSamurai, ByteWitch

**Euthanatos**: Sanskrit terms, death-related epithets
- Examples: Kali's Hand, Chandra Vikram, Yama's Witness

**Society of Ether**: Academic titles, inventor names
- Examples: Dr. Reginald Sterling, Professor Ada Thornton

**Technocracy**: Professional names, operational codenames
- Examples: Agent Morrison, Dr. Sarah Chen, Director Williams

**Dreamspeakers**: Traditional names from various indigenous cultures
- Examples: Grandfather Crow, Dancing Elk, Spirit Walker

**Cult of Ecstasy**: Evocative names, sensation references
- Examples: Bliss, Raven Moonsong, DJ Euphoria
