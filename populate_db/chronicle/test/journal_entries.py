"""
Journal Entries Script

Creates sample journal entries for characters to simulate downtime activity.
"""

from datetime import date, timedelta

from characters.models.core import CharacterModel
from game.models import Chronicle, Journal, JournalEntry


def populate_journal_entries():
    """Create journal entries for test chronicle characters."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")

    print("Creating journal entries...")

    # Get PC characters
    characters = CharacterModel.objects.filter(
        chronicle=chronicle,
        npc=False,
    )

    entries_created = 0

    for char in characters:
        # Create or get journal for character
        journal, _ = Journal.objects.get_or_create(
            character=char,
            defaults={"chronicle": chronicle}
        )

        # Create sample entries based on character type
        entries = get_entries_for_character(char)

        for entry_data in entries:
            entry, created = JournalEntry.objects.get_or_create(
                journal=journal,
                title=entry_data["title"],
                defaults={
                    "entry": entry_data["entry"],
                    "date": entry_data["date"],
                    "st_message": entry_data.get("st_message", ""),
                }
            )
            if created:
                entries_created += 1

    print(f"Created {entries_created} journal entries")


def get_entries_for_character(char):
    """Get appropriate journal entries based on character type."""
    entries = []

    # Base date for entries (2022, when scenes take place)
    base_date = date(2022, 3, 1)

    # Generic downtime entry
    entries.append({
        "title": "Settling In",
        "entry": f"""Spent the week getting familiar with Seattle. Met some of the
local {get_faction_name(char)} and started establishing my presence.

Need to focus on:
- Building contacts
- Learning the local power structure
- Finding reliable feeding/resource sources

The city has its own rhythm. I'll need to adapt.""",
        "date": base_date,
        "st_message": "Good start! +1 XP for establishing your character."
    })

    # Character-type specific entries
    if "vampire" in str(type(char)).lower() or hasattr(char, 'clan'):
        entries.extend(get_vampire_entries(char, base_date))
    elif "garou" in str(type(char)).lower() or hasattr(char, 'tribe'):
        entries.extend(get_werewolf_entries(char, base_date))
    elif "mage" in str(type(char)).lower() or hasattr(char, 'tradition'):
        entries.extend(get_mage_entries(char, base_date))
    elif "wraith" in str(type(char)).lower():
        entries.extend(get_wraith_entries(char, base_date))
    elif "changeling" in str(type(char)).lower() or hasattr(char, 'kith'):
        entries.extend(get_changeling_entries(char, base_date))
    elif "demon" in str(type(char)).lower() or hasattr(char, 'house'):
        entries.extend(get_demon_entries(char, base_date))
    elif "hunter" in str(type(char)).lower():
        entries.extend(get_hunter_entries(char, base_date))
    elif "mummy" in str(type(char)).lower():
        entries.extend(get_mummy_entries(char, base_date))

    return entries


def get_faction_name(char):
    """Get the faction name for a character."""
    char_type = str(type(char)).lower()
    if "vampire" in char_type:
        return "Kindred"
    elif "garou" in char_type or "werewolf" in char_type:
        return "Garou"
    elif "mage" in char_type:
        return "Awakened"
    elif "wraith" in char_type:
        return "Restless Dead"
    elif "changeling" in char_type:
        return "Kithain"
    elif "demon" in char_type:
        return "Fallen"
    elif "hunter" in char_type:
        return "hunters"
    elif "mummy" in char_type:
        return "Amenti"
    return "others like me"


def get_vampire_entries(char, base_date):
    """Get vampire-specific journal entries."""
    return [
        {
            "title": "Hunting Grounds",
            "entry": """Spent three nights mapping out the local hunting grounds.
The Rack near Pioneer Square is decent but crowded. Found a quieter
spot near Capitol Hill - college students, always willing to party.

Need to be careful about the Sheriff's territory. Don't want to step
on any toes this early.""",
            "date": base_date + timedelta(days=14),
            "st_message": ""
        },
        {
            "title": "Court Observations",
            "entry": """Attended Elysium last night. Interesting dynamics:
- The Prince seems secure but bored
- The Primogen are playing their usual games
- The Anarchs are more organized than I expected

Made a few connections. The Nosferatu information broker seems useful.
Will follow up.""",
            "date": base_date + timedelta(days=30),
            "st_message": "Good political awareness! Note: the Primogen situation may become relevant soon."
        }
    ]


def get_werewolf_entries(char, base_date):
    """Get werewolf-specific journal entries."""
    return [
        {
            "title": "Running the Bawn",
            "entry": """Spent the week running patrol with the pack. The Cascades
are beautiful but I can feel the Wyrm's touch even here. Industrial
runoff from the city. Spirit unease.

The caern is holding but we need to be vigilant. The Theurge says
the spirits are restless.""",
            "date": base_date + timedelta(days=14),
            "st_message": ""
        },
        {
            "title": "Umbral Scouting",
            "entry": """Crossed into the Umbra near the waterfront. The reflection
of Seattle is... troubling. Weaver-spirits everywhere, binding the
city in patterns. But there are cracks where the Wyrm seeps through.

Found signs of Bane activity near the industrial district. Reported
to the sept. We'll need to investigate.""",
            "date": base_date + timedelta(days=30),
            "st_message": "The Bane activity you found will be relevant in the upcoming story."
        }
    ]


def get_mage_entries(char, base_date):
    """Get mage-specific journal entries."""
    return [
        {
            "title": "Studying the Local Resonance",
            "entry": """Seattle's Tapestry is fascinating. The tech industry has
created strong patterns of Virtual Web influence, but there are
older currents underneath. Native American spirit traditions,
maritime superstitions, the dreams of generations of settlers.

The nodes here are contested. Need to be careful about stepping
on Tradition territory.""",
            "date": base_date + timedelta(days=14),
            "st_message": ""
        },
        {
            "title": "Technocratic Activity",
            "entry": """Noticed increased Technocratic surveillance in the downtown
corridor. They're watching the tech companies - probably looking
for Reality Deviants among the programmers.

Staying low profile for now. Working on my coincidental magic to
avoid drawing attention.""",
            "date": base_date + timedelta(days=30),
            "st_message": "Good instincts. The Technocracy is more active than usual right now."
        }
    ]


def get_wraith_entries(char, base_date):
    """Get wraith-specific journal entries."""
    return [
        {
            "title": "Checking on My Fetters",
            "entry": """Visited my Fetters this week. [Sarah still visits my grave.
I wish I could tell her I'm okay. That I'm still here.]

The hospital has changed so much since I died. New wing, new staff.
But the Shadowlands version remembers everything. The fire. The
screams.

*The Shadow whispers that I should let go. I won't.*""",
            "date": base_date + timedelta(days=14),
            "st_message": ""
        },
        {
            "title": "Tempest Warnings",
            "entry": """The Tempest is more active lately. Other wraiths are
nervous - talking about something stirring in the deeper reaches.

Keeping close to the Skinlands for now. My Fetters anchor me here.
Need to stay connected to the living world.

*The Shadow is louder today. I need to be careful.*""",
            "date": base_date + timedelta(days=30),
            "st_message": "Your instincts are correct. Something is coming."
        }
    ]


def get_changeling_entries(char, base_date):
    """Get changeling-specific journal entries."""
    return [
        {
            "title": "Glamour Gathering",
            "entry": """Found a wonderful source of Glamour! There's a children's
storytelling hour at the library every Saturday. Pure imagination,
unfiltered belief. It's like drinking starlight.

Also attended a poetry slam at a coffeehouse. The artist's passion
was intoxicating. Will definitely go back.""",
            "date": base_date + timedelta(days=14),
            "st_message": ""
        },
        {
            "title": "Freehold Politics",
            "entry": """Court was interesting tonight. The Duke is worried about
something - wouldn't say what, but the nobles were whispering about
Banality incursions.

Made friends with a Pooka. He tells the best lies. I mean stories.
The motley is coming together nicely.""",
            "date": base_date + timedelta(days=30),
            "st_message": "The Duke's concerns may become relevant to your story soon."
        }
    ]


def get_demon_entries(char, base_date):
    """Get demon-specific journal entries."""
    return [
        {
            "title": "Host Adjustment",
            "entry": """Still getting used to this body. The host's memories are
fragmentary - I see flashes of their life, feel echoes of their
emotions. It's strange to be mortal again after so long.

The hunger for Faith is constant. I need to be careful not to let
it consume me. I've seen what happens to Fallen who lose themselves.""",
            "date": base_date + timedelta(days=14),
            "st_message": ""
        },
        {
            "title": "Finding Purpose",
            "entry": """Met with other Fallen in the city. We're all searching for
something - redemption, revenge, understanding. The Earthbound stir
in their ancient prisons. The war never really ended.

But maybe we can be something different. Something better than what
we were. Maybe that's why we're here.""",
            "date": base_date + timedelta(days=30),
            "st_message": "Beautiful character development. This kind of introspection is what the chronicle needs."
        }
    ]


def get_hunter_entries(char, base_date):
    """Get hunter-specific journal entries."""
    return [
        {
            "title": "Research and Recon",
            "entry": """Spent the week mapping supernatural activity in the city.
There's more here than I expected. Vampires in the clubs, something
weird in the forest preserves, rumors of ghost sightings.

The network provided some useful intel. Other hunters have been here
before. Some of them didn't survive.""",
            "date": base_date + timedelta(days=14),
            "st_message": ""
        },
        {
            "title": "First Hunt",
            "entry": """Tracked down a vampire feeding ground near the university.
Didn't engage - not ready for that yet. But I documented everything.
Feeding patterns, probable haven location, security.

Information is a weapon. Right now it's the best weapon I have.
Soon, I'll have more.""",
            "date": base_date + timedelta(days=30),
            "st_message": "Smart approach. Remember - patience and preparation save lives."
        }
    ]


def get_mummy_entries(char, base_date):
    """Get mummy-specific journal entries."""
    return [
        {
            "title": "Awakening Adjustment",
            "entry": """Another resurrection. This time in Seattle, far from the
Lands of Faith. The modern world is... overwhelming. So much noise,
so many distractions.

But Ma'at endures. The balance must be maintained. I sense Apophis's
servants are active here. My purpose remains clear.""",
            "date": base_date + timedelta(days=14),
            "st_message": ""
        },
        {
            "title": "Establishing the Web",
            "entry": """Made contact with local cultists. They maintain the old ways,
even in this faithless age. Their devotion sustains me.

Also found signs of tomb robbers - artifacts from Egypt appearing
in private collections. Will investigate. Some things should remain
buried.""",
            "date": base_date + timedelta(days=30),
            "st_message": "The artifacts you've noticed may be connected to something larger."
        }
    ]


if __name__ == "__main__":
    populate_journal_entries()
