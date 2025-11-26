"""
Group Membership Script

Assigns characters to their appropriate groups (Coteries, Packs, Cabals, etc.)
"""

from characters.models.core import CharacterModel

# Vampire groups
from characters.models.vampire.coterie import Coterie

# Werewolf groups
from characters.models.werewolf.pack import Pack

# Mage groups
from characters.models.mage.cabal import Cabal

# Wraith groups
from characters.models.wraith.circle import Circle

# Changeling groups
from characters.models.changeling.motley import Motley

# Demon groups
from characters.models.demon.court import DemonCourt

# Hunter groups
from characters.models.hunter.organization import HunterOrganization


def populate_group_membership():
    """Assign characters to their groups."""
    print("Assigning characters to groups...")

    # =========================================================================
    # VAMPIRE COTERIES
    # =========================================================================
    assign_vampire_coteries()

    # =========================================================================
    # WEREWOLF PACKS
    # =========================================================================
    assign_werewolf_packs()

    # =========================================================================
    # MAGE CABALS
    # =========================================================================
    assign_mage_cabals()

    # =========================================================================
    # WRAITH CIRCLES
    # =========================================================================
    assign_wraith_circles()

    # =========================================================================
    # CHANGELING MOTLEYS
    # =========================================================================
    assign_changeling_motleys()

    # =========================================================================
    # DEMON COURTS
    # =========================================================================
    assign_demon_courts()

    # =========================================================================
    # HUNTER ORGANIZATIONS
    # =========================================================================
    assign_hunter_organizations()

    print("Group membership assignment complete!")


def assign_vampire_coteries():
    """Assign vampires to their coteries."""
    coterie_assignments = {
        "The Inner Circle": [
            "Marcus 'Shadow' Webb",
            "Isabella Santos",
            "Roland Cross",
        ],
        "The Night Gallery": [
            "Victoria Chen",
            "Sebastian Marsh",
        ],
        "The Underground": [
            "Dmitri 'The Bear' Volkov",
            "Luna Reyes",
        ],
    }

    for coterie_name, character_names in coterie_assignments.items():
        try:
            coterie = Coterie.objects.get(name=coterie_name)
            for char_name in character_names:
                try:
                    char = CharacterModel.objects.get(name=char_name)
                    coterie.members.add(char)
                    print(f"  Added {char_name} to {coterie_name}")
                except CharacterModel.DoesNotExist:
                    print(f"  Warning: Character '{char_name}' not found")
        except Coterie.DoesNotExist:
            print(f"  Warning: Coterie '{coterie_name}' not found")


def assign_werewolf_packs():
    """Assign werewolves to their packs."""
    pack_assignments = {
        "Silicon Fangs": [
            "Runs-Through-Shadows",
            "Storm's Fury",
        ],
        "The Wardens": [
            "Gaia's Whisper",
        ],
        "The Forgotten": [
            "Cracks-the-Code",
        ],
    }

    for pack_name, character_names in pack_assignments.items():
        try:
            pack = Pack.objects.get(name=pack_name)
            for char_name in character_names:
                try:
                    char = CharacterModel.objects.get(name=char_name)
                    pack.members.add(char)
                    print(f"  Added {char_name} to {pack_name}")
                except CharacterModel.DoesNotExist:
                    print(f"  Warning: Character '{char_name}' not found")
        except Pack.DoesNotExist:
            print(f"  Warning: Pack '{pack_name}' not found")


def assign_mage_cabals():
    """Assign mages to their cabals."""
    cabal_assignments = {
        "The Invisible College": [
            "Elena Vasquez",
        ],
        "Digital Underground": [
            "James Chen",
        ],
        "The Fortunate Few": [
            "Dr. Helena Cross",
        ],
        "The Threshold": [
            "Samuel Wright",
        ],
    }

    for cabal_name, character_names in cabal_assignments.items():
        try:
            cabal = Cabal.objects.get(name=cabal_name)
            for char_name in character_names:
                try:
                    char = CharacterModel.objects.get(name=char_name)
                    cabal.members.add(char)
                    print(f"  Added {char_name} to {cabal_name}")
                except CharacterModel.DoesNotExist:
                    print(f"  Warning: Character '{char_name}' not found")
        except Cabal.DoesNotExist:
            print(f"  Warning: Cabal '{cabal_name}' not found")


def assign_wraith_circles():
    """Assign wraiths to their circles."""
    circle_assignments = {
        "The Unquiet": [
            'Margaret "Peggy" Sullivan',
            "Thomas Ashworth",
        ],
        "The Watch": [
            "Detective James Morrison",
        ],
        "The Lost Generation": [
            "Emma Thornton",
        ],
    }

    for circle_name, character_names in circle_assignments.items():
        try:
            circle = Circle.objects.get(name=circle_name)
            for char_name in character_names:
                try:
                    char = CharacterModel.objects.get(name=char_name)
                    circle.members.add(char)
                    print(f"  Added {char_name} to {circle_name}")
                except CharacterModel.DoesNotExist:
                    print(f"  Warning: Character '{char_name}' not found")
        except Circle.DoesNotExist:
            print(f"  Warning: Circle '{circle_name}' not found")


def assign_changeling_motleys():
    """Assign changelings to their motleys."""
    motley_assignments = {
        "The Toybox Rebellion": [
            "Rowan Brightwater",
            'Jack "Patches" McGee',
        ],
        "Court of Whispers": [
            "Lady Silvermist",
        ],
        "Storm's Eye": [
            "Thunder's Echo",
        ],
    }

    for motley_name, character_names in motley_assignments.items():
        try:
            motley = Motley.objects.get(name=motley_name)
            for char_name in character_names:
                try:
                    char = CharacterModel.objects.get(name=char_name)
                    motley.members.add(char)
                    print(f"  Added {char_name} to {motley_name}")
                except CharacterModel.DoesNotExist:
                    print(f"  Warning: Character '{char_name}' not found")
        except Motley.DoesNotExist:
            print(f"  Warning: Motley '{motley_name}' not found")


def assign_demon_courts():
    """Assign demons to their courts/conclaves."""
    court_assignments = {
        "The Architects": [
            "Zephyrus",
        ],
        "The Muses": [
            "Seraph",
        ],
        "The Reckoning": [
            "Marcus Wells",
        ],
    }

    for court_name, character_names in court_assignments.items():
        try:
            court = DemonCourt.objects.get(name=court_name)
            for char_name in character_names:
                try:
                    char = CharacterModel.objects.get(name=char_name)
                    court.members.add(char)
                    print(f"  Added {char_name} to {court_name}")
                except CharacterModel.DoesNotExist:
                    print(f"  Warning: Character '{char_name}' not found")
        except DemonCourt.DoesNotExist:
            print(f"  Warning: Court '{court_name}' not found")


def assign_hunter_organizations():
    """Assign hunters to their organizations."""
    org_assignments = {
        "The Vigil": [
            "Sarah Mitchell",
            "David Okonkwo",
        ],
        "The Network": [
            "Marcus Cole",
        ],
        "Support Group": [
            "Jennifer Hayes",
        ],
    }

    for org_name, character_names in org_assignments.items():
        try:
            org = HunterOrganization.objects.get(name=org_name)
            for char_name in character_names:
                try:
                    char = CharacterModel.objects.get(name=char_name)
                    org.members.add(char)
                    print(f"  Added {char_name} to {org_name}")
                except CharacterModel.DoesNotExist:
                    print(f"  Warning: Character '{char_name}' not found")
        except HunterOrganization.DoesNotExist:
            print(f"  Warning: Organization '{org_name}' not found")


if __name__ == "__main__":
    populate_group_membership()
