"""
Background Links Script

Links NPCs, Items, and Locations to the character backgrounds that spawned them.
Uses the BackgroundRating.url field to create hyperlinks in the UI.
"""

from characters.models.core import CharacterModel
from characters.models.core.background_block import BackgroundRating
from items.models.core import ItemModel
from locations.models.core import LocationModel


def populate_background_links():
    """Link backgrounds to their associated NPCs, items, and locations."""
    print("Linking backgrounds to NPCs, items, and locations...")

    # =========================================================================
    # VAMPIRE BACKGROUND LINKS
    # =========================================================================
    link_vampire_backgrounds()

    # =========================================================================
    # WEREWOLF BACKGROUND LINKS
    # =========================================================================
    link_werewolf_backgrounds()

    # =========================================================================
    # MAGE BACKGROUND LINKS
    # =========================================================================
    link_mage_backgrounds()

    # =========================================================================
    # WRAITH BACKGROUND LINKS
    # =========================================================================
    link_wraith_backgrounds()

    # =========================================================================
    # CHANGELING BACKGROUND LINKS
    # =========================================================================
    link_changeling_backgrounds()

    # =========================================================================
    # DEMON BACKGROUND LINKS
    # =========================================================================
    link_demon_backgrounds()

    # =========================================================================
    # HUNTER BACKGROUND LINKS
    # =========================================================================
    link_hunter_backgrounds()

    # =========================================================================
    # MUMMY BACKGROUND LINKS
    # =========================================================================
    link_mummy_backgrounds()

    print("Background linking complete!")


def link_background_to_object(character_name, background_note, obj):
    """Helper to link a background to an object (NPC, item, or location)."""
    try:
        char = CharacterModel.objects.get(name=character_name)
        bg_rating = BackgroundRating.objects.filter(
            char=char,
            note__icontains=background_note
        ).first()

        if bg_rating and obj:
            bg_rating.url = obj.get_absolute_url()
            bg_rating.save()
            print(f"  Linked {char.name}'s {bg_rating.bg.name} ({background_note}) -> {obj.name}")
            return True
    except CharacterModel.DoesNotExist:
        pass
    except Exception as e:
        print(f"  Warning: Could not link {character_name}'s {background_note}: {e}")
    return False


def link_vampire_backgrounds():
    """Link vampire character backgrounds to NPCs, items, and locations."""
    print("\nVampire Background Links:")

    # Retainers -> Ghouls
    ghoul_links = [
        ("Marcus 'Shadow' Webb", "Danny Chen", "Danny Chen"),
        ("Isabella Santos", "Bethany Moore", "Bethany Moore"),
        ("Roland Cross", "Jennifer Walsh", "Jennifer Walsh"),
    ]

    for char_name, note, npc_name in ghoul_links:
        try:
            npc = CharacterModel.objects.get(name=npc_name)
            link_background_to_object(char_name, note, npc)
        except CharacterModel.DoesNotExist:
            print(f"  Warning: NPC '{npc_name}' not found")

    # Haven -> Locations
    haven_links = [
        ("Marcus 'Shadow' Webb", "Underground", "The Underground Seattle"),
        ("Victoria Chen", "Penthouse", "Seattle Art Museum Elysium"),
    ]

    for char_name, note, loc_name in haven_links:
        try:
            loc = LocationModel.objects.get(name=loc_name)
            link_background_to_object(char_name, note, loc)
        except LocationModel.DoesNotExist:
            print(f"  Warning: Location '{loc_name}' not found")


def link_werewolf_backgrounds():
    """Link werewolf character backgrounds to NPCs, items, and locations."""
    print("\nWerewolf Background Links:")

    # Kinfolk -> Kinfolk characters
    kinfolk_links = [
        ("Runs-Through-Shadows", "Kinfolk", "Maria Vasquez"),
        ("Storm's Fury", "Kinfolk", "Daniel Strongbow"),
    ]

    for char_name, note, npc_name in kinfolk_links:
        try:
            npc = CharacterModel.objects.get(name=npc_name)
            link_background_to_object(char_name, note, npc)
        except CharacterModel.DoesNotExist:
            print(f"  Warning: Kinfolk '{npc_name}' not found")

    # Caern -> Caern locations
    caern_links = [
        ("Runs-Through-Shadows", "Caern", "Cascadian Wilderness Caern"),
        ("Storm's Fury", "Caern", "Cascadian Wilderness Caern"),
    ]

    for char_name, note, loc_name in caern_links:
        try:
            loc = LocationModel.objects.get(name=loc_name)
            link_background_to_object(char_name, note, loc)
        except LocationModel.DoesNotExist:
            print(f"  Warning: Location '{loc_name}' not found")


def link_mage_backgrounds():
    """Link mage character backgrounds to NPCs, items, and locations."""
    print("\nMage Background Links:")

    # Chantry -> Chantry locations
    chantry_links = [
        ("Elena Vasquez", "Chantry", "The Cross House"),
        ("James Chen", "Chantry", "Digital Sanctum"),
    ]

    for char_name, note, loc_name in chantry_links:
        try:
            loc = LocationModel.objects.get(name=loc_name)
            link_background_to_object(char_name, note, loc)
        except LocationModel.DoesNotExist:
            print(f"  Warning: Location '{loc_name}' not found")

    # Node -> Node locations
    node_links = [
        ("Elena Vasquez", "Node", "Fremont Troll Node"),
        ("James Chen", "Node", "Gas Works Node"),
    ]

    for char_name, note, loc_name in node_links:
        try:
            loc = LocationModel.objects.get(name=loc_name)
            link_background_to_object(char_name, note, loc)
        except LocationModel.DoesNotExist:
            print(f"  Warning: Location '{loc_name}' not found")


def link_wraith_backgrounds():
    """Link wraith character backgrounds to NPCs, items, and locations."""
    print("\nWraith Background Links:")

    # Haunt -> Haunt locations
    haunt_links = [
        ('Margaret "Peggy" Sullivan', "Hospital", "Harborview Medical Center"),
        ("Thomas Ashworth", "Estate", "The Ashworth Estate"),
    ]

    for char_name, note, loc_name in haunt_links:
        try:
            loc = LocationModel.objects.get(name=loc_name)
            link_background_to_object(char_name, note, loc)
        except LocationModel.DoesNotExist:
            print(f"  Warning: Location '{loc_name}' not found")


def link_changeling_backgrounds():
    """Link changeling character backgrounds to NPCs, items, and locations."""
    print("\nChangeling Background Links:")

    # Freehold -> Freehold locations
    freehold_links = [
        ("Rowan Brightwater", "Freehold", "The Gilded Pumpkin"),
        ('Jack "Patches" McGee', "Freehold", "The Gilded Pumpkin"),
    ]

    for char_name, note, loc_name in freehold_links:
        try:
            loc = LocationModel.objects.get(name=loc_name)
            link_background_to_object(char_name, note, loc)
        except LocationModel.DoesNotExist:
            print(f"  Warning: Location '{loc_name}' not found")


def link_demon_backgrounds():
    """Link demon character backgrounds to NPCs, items, and locations."""
    print("\nDemon Background Links:")

    # Followers -> Thrall characters
    thrall_links = [
        ("Zephyrus", "Thrall", "Michael Torres"),
        ("Marcus Wells", "Thrall", "Sarah Kane"),
    ]

    for char_name, note, npc_name in thrall_links:
        try:
            npc = CharacterModel.objects.get(name=npc_name)
            link_background_to_object(char_name, note, npc)
        except CharacterModel.DoesNotExist:
            print(f"  Warning: Thrall '{npc_name}' not found")


def link_hunter_backgrounds():
    """Link hunter character backgrounds to NPCs, items, and locations."""
    print("\nHunter Background Links:")

    # Safehouse -> Location
    safehouse_links = [
        ("Sarah Mitchell", "Safehouse", "Hunter Safehouse Alpha"),
        ("David Okonkwo", "Safehouse", "The Network Hub"),
    ]

    for char_name, note, loc_name in safehouse_links:
        try:
            loc = LocationModel.objects.get(name=loc_name)
            link_background_to_object(char_name, note, loc)
        except LocationModel.DoesNotExist:
            print(f"  Warning: Location '{loc_name}' not found")


def link_mummy_backgrounds():
    """Link mummy character backgrounds to NPCs, items, and locations."""
    print("\nMummy Background Links:")

    # Cult -> Cult locations
    cult_links = [
        ("Amenhotep IV", "Cult", "Temple of the Eternal Sun"),
        ("Dr. Constance Grey", "Cult", "House of Scrolls"),
    ]

    for char_name, note, loc_name in cult_links:
        try:
            loc = LocationModel.objects.get(name=loc_name)
            link_background_to_object(char_name, note, loc)
        except LocationModel.DoesNotExist:
            print(f"  Warning: Location '{loc_name}' not found")


if __name__ == "__main__":
    populate_background_links()
