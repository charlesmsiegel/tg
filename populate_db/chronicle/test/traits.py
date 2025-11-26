"""
Seattle Test Chronicle - Gameline-Specific Trait Assignments

Assigns gameline-specific traits that weren't set during character creation:
- Werewolf Gifts (ManyToMany)
- Additional discipline/sphere/etc. details as needed

Run with: python manage.py shell < populate_db/chronicle/test/traits.py

Prerequisites:
- Run character scripts first (creates characters)
- Game data must be loaded (gifts, disciplines, etc.)
"""

from characters.models.werewolf.garou import Werewolf
from characters.models.werewolf.gift import Gift


def assign_werewolf_gifts():
    """Assign appropriate Gifts to Werewolf characters based on their tribe/auspice."""
    print("Assigning Werewolf Gifts...")

    # Gift assignments by character name
    # Format: {character_name: [list of gift names]}
    gift_assignments = {
        # Runs-Through-Fire (Glass Walker Ahroun)
        "Runs-Through-Fire": [
            "Razor Claws",          # Ahroun basic
            "The Falling Touch",    # Ahroun
            "Control Simple Machine",  # Glass Walker
            "Diagnostics",          # Glass Walker
        ],
        # Whispers-to-Stars (Uktena Theurge)
        "Whispers-to-Stars": [
            "Spirit Speech",        # Theurge basic
            "Sense Wyrm",           # All Garou
            "Shroud",               # Uktena
            "Spirit of the Lizard", # Uktena
        ],
        # Breaks-the-Chain (Bone Gnawer Ragabash)
        "Breaks-the-Chain": [
            "Blur of the Milky Eye",  # Ragabash basic
            "Scent of Sweet Honey",   # Ragabash
            "Cooking",                # Bone Gnawer
            "Resist Toxin",           # Bone Gnawer
        ],
        # Storm-Singer (Wendigo Galliard)
        "Storm-Singer": [
            "Call of the Wyld",       # Galliard basic
            "Mindspeak",              # Galliard
            "Call the Breeze",        # Wendigo
            "Camouflage",             # Wendigo
        ],
        # Judges-the-Fallen (Shadow Lord Philodox)
        "Judges-the-Fallen": [
            "Truth of Gaia",          # Philodox basic
            "Scent of the True Form", # Philodox
            "Aura of Confidence",     # Shadow Lord
            "Fatal Flaw",             # Shadow Lord
        ],
    }

    for char_name, gift_names in gift_assignments.items():
        try:
            garou = Werewolf.objects.get(name=char_name)
            for gift_name in gift_names:
                try:
                    gift = Gift.objects.get(name=gift_name)
                    garou.gifts.add(gift)
                    print(f"  Added '{gift_name}' to {char_name}")
                except Gift.DoesNotExist:
                    print(f"  Warning: Gift '{gift_name}' not found, skipping")
            garou.save()
        except Werewolf.DoesNotExist:
            print(f"  Warning: Werewolf '{char_name}' not found, skipping")

    print("Werewolf Gift assignment complete.")


def verify_vampire_disciplines():
    """Verify that vampire discipline dots are set correctly."""
    from characters.models.vampire.vampire import Vampire

    print("\nVerifying Vampire Disciplines...")
    vampires = Vampire.objects.filter(chronicle__name="Seattle Test Chronicle")

    for vamp in vampires:
        disciplines = []
        if vamp.obfuscate > 0:
            disciplines.append(f"Obfuscate {vamp.obfuscate}")
        if vamp.potence > 0:
            disciplines.append(f"Potence {vamp.potence}")
        if vamp.auspex > 0:
            disciplines.append(f"Auspex {vamp.auspex}")
        if vamp.dominate > 0:
            disciplines.append(f"Dominate {vamp.dominate}")
        if vamp.presence > 0:
            disciplines.append(f"Presence {vamp.presence}")
        if vamp.celerity > 0:
            disciplines.append(f"Celerity {vamp.celerity}")
        if vamp.fortitude > 0:
            disciplines.append(f"Fortitude {vamp.fortitude}")
        if vamp.thaumaturgy > 0:
            disciplines.append(f"Thaumaturgy {vamp.thaumaturgy}")
        if vamp.dementation > 0:
            disciplines.append(f"Dementation {vamp.dementation}")
        if vamp.animalism > 0:
            disciplines.append(f"Animalism {vamp.animalism}")

        if disciplines:
            print(f"  {vamp.name}: {', '.join(disciplines)}")
        else:
            print(f"  {vamp.name}: No disciplines set")


def verify_mage_spheres():
    """Verify that mage sphere dots are set correctly."""
    from characters.models.mage.mage import Mage

    print("\nVerifying Mage Spheres...")
    mages = Mage.objects.filter(chronicle__name="Seattle Test Chronicle")

    for mage in mages:
        spheres = []
        if mage.correspondence > 0:
            spheres.append(f"Correspondence {mage.correspondence}")
        if mage.entropy > 0:
            spheres.append(f"Entropy {mage.entropy}")
        if mage.forces > 0:
            spheres.append(f"Forces {mage.forces}")
        if mage.life > 0:
            spheres.append(f"Life {mage.life}")
        if mage.matter > 0:
            spheres.append(f"Matter {mage.matter}")
        if mage.mind > 0:
            spheres.append(f"Mind {mage.mind}")
        if mage.prime > 0:
            spheres.append(f"Prime {mage.prime}")
        if mage.spirit > 0:
            spheres.append(f"Spirit {mage.spirit}")
        if mage.time > 0:
            spheres.append(f"Time {mage.time}")

        if spheres:
            print(f"  {mage.name}: Arete {mage.arete}, {', '.join(spheres)}")
        else:
            print(f"  {mage.name}: Arete {mage.arete}, No spheres set")


def verify_wraith_arcanoi():
    """Verify that wraith arcanoi are set correctly."""
    from characters.models.wraith.wraith import Wraith

    print("\nVerifying Wraith Arcanoi...")
    wraiths = Wraith.objects.filter(chronicle__name="Seattle Test Chronicle")

    for wraith in wraiths:
        arcanoi = []
        if wraith.argos > 0:
            arcanoi.append(f"Argos {wraith.argos}")
        if wraith.castigate > 0:
            arcanoi.append(f"Castigate {wraith.castigate}")
        if wraith.embody > 0:
            arcanoi.append(f"Embody {wraith.embody}")
        if wraith.fatalism > 0:
            arcanoi.append(f"Fatalism {wraith.fatalism}")
        if wraith.flux > 0:
            arcanoi.append(f"Flux {wraith.flux}")
        if wraith.inhabit > 0:
            arcanoi.append(f"Inhabit {wraith.inhabit}")
        if wraith.keening > 0:
            arcanoi.append(f"Keening {wraith.keening}")
        if wraith.lifeweb > 0:
            arcanoi.append(f"Lifeweb {wraith.lifeweb}")
        if wraith.moliate > 0:
            arcanoi.append(f"Moliate {wraith.moliate}")
        if wraith.outrage > 0:
            arcanoi.append(f"Outrage {wraith.outrage}")
        if wraith.pandemonium > 0:
            arcanoi.append(f"Pandemonium {wraith.pandemonium}")
        if wraith.phantasm > 0:
            arcanoi.append(f"Phantasm {wraith.phantasm}")
        if wraith.usury > 0:
            arcanoi.append(f"Usury {wraith.usury}")

        if arcanoi:
            print(f"  {wraith.name}: {', '.join(arcanoi)}")
        else:
            print(f"  {wraith.name}: No arcanoi set")


def verify_changeling_arts():
    """Verify that changeling arts and realms are set correctly."""
    from characters.models.changeling.changeling import Changeling

    print("\nVerifying Changeling Arts and Realms...")
    changelings = Changeling.objects.filter(chronicle__name="Seattle Test Chronicle")

    for ctd in changelings:
        arts = []
        realms = []

        # Check Arts
        if ctd.chicanery > 0:
            arts.append(f"Chicanery {ctd.chicanery}")
        if ctd.legerdemain > 0:
            arts.append(f"Legerdemain {ctd.legerdemain}")
        if ctd.primal > 0:
            arts.append(f"Primal {ctd.primal}")
        if ctd.soothsay > 0:
            arts.append(f"Soothsay {ctd.soothsay}")
        if ctd.sovereign > 0:
            arts.append(f"Sovereign {ctd.sovereign}")
        if ctd.wayfare > 0:
            arts.append(f"Wayfare {ctd.wayfare}")

        # Check Realms
        if ctd.actor > 0:
            realms.append(f"Actor {ctd.actor}")
        if ctd.fae > 0:
            realms.append(f"Fae {ctd.fae}")
        if ctd.nature_realm > 0:
            realms.append(f"Nature {ctd.nature_realm}")
        if ctd.prop > 0:
            realms.append(f"Prop {ctd.prop}")
        if ctd.scene > 0:
            realms.append(f"Scene {ctd.scene}")

        if arts or realms:
            print(f"  {ctd.name}: Arts: {', '.join(arts) if arts else 'None'}; Realms: {', '.join(realms) if realms else 'None'}")
        else:
            print(f"  {ctd.name}: No arts or realms set")


def verify_demon_lores():
    """Verify that demon lores are set correctly."""
    from characters.models.demon.demon import Demon

    print("\nVerifying Demon Lores...")
    demons = Demon.objects.filter(chronicle__name="Seattle Test Chronicle")

    for demon in demons:
        lores = []
        if demon.lore_of_awakening > 0:
            lores.append(f"Awakening {demon.lore_of_awakening}")
        if demon.lore_of_the_beast > 0:
            lores.append(f"Beast {demon.lore_of_the_beast}")
        if demon.lore_of_the_celestials > 0:
            lores.append(f"Celestials {demon.lore_of_the_celestials}")
        if demon.lore_of_flame > 0:
            lores.append(f"Flame {demon.lore_of_flame}")
        if demon.lore_of_the_flesh > 0:
            lores.append(f"Flesh {demon.lore_of_the_flesh}")
        if demon.lore_of_the_forge > 0:
            lores.append(f"Forge {demon.lore_of_the_forge}")
        if demon.lore_of_the_fundament > 0:
            lores.append(f"Fundament {demon.lore_of_the_fundament}")
        if demon.lore_of_humanity > 0:
            lores.append(f"Humanity {demon.lore_of_humanity}")
        if demon.lore_of_light > 0:
            lores.append(f"Light {demon.lore_of_light}")
        if demon.lore_of_longing > 0:
            lores.append(f"Longing {demon.lore_of_longing}")
        if demon.lore_of_patterns > 0:
            lores.append(f"Patterns {demon.lore_of_patterns}")
        if demon.lore_of_radiance > 0:
            lores.append(f"Radiance {demon.lore_of_radiance}")
        if demon.lore_of_the_realms > 0:
            lores.append(f"Realms {demon.lore_of_the_realms}")
        if demon.lore_of_the_spirit > 0:
            lores.append(f"Spirit {demon.lore_of_the_spirit}")
        if demon.lore_of_storms > 0:
            lores.append(f"Storms {demon.lore_of_storms}")
        if demon.lore_of_transfiguration > 0:
            lores.append(f"Transfiguration {demon.lore_of_transfiguration}")
        if demon.lore_of_the_wild > 0:
            lores.append(f"Wild {demon.lore_of_the_wild}")
        if demon.lore_of_the_winds > 0:
            lores.append(f"Winds {demon.lore_of_the_winds}")

        if lores:
            print(f"  {demon.name}: {', '.join(lores)}")
        else:
            print(f"  {demon.name}: No lores set")


def verify_hunter_edges():
    """Verify that hunter edges are set correctly."""
    from characters.models.hunter.hunter import Hunter

    print("\nVerifying Hunter Edges...")
    hunters = Hunter.objects.filter(chronicle__name="Seattle Test Chronicle")

    for hunter in hunters:
        edges = []
        # Conviction Edges
        if hunter.discern > 0:
            edges.append(f"Discern {hunter.discern}")
        if hunter.burden > 0:
            edges.append(f"Burden {hunter.burden}")
        if hunter.expose > 0:
            edges.append(f"Expose {hunter.expose}")
        if hunter.witness > 0:
            edges.append(f"Witness {hunter.witness}")
        # Vision Edges
        if hunter.illuminate > 0:
            edges.append(f"Illuminate {hunter.illuminate}")
        if hunter.ward > 0:
            edges.append(f"Ward {hunter.ward}")
        if hunter.cleave > 0:
            edges.append(f"Cleave {hunter.cleave}")
        if hunter.hide > 0:
            edges.append(f"Hide {hunter.hide}")
        # Zeal Edges
        if hunter.demand > 0:
            edges.append(f"Demand {hunter.demand}")
        if hunter.confront > 0:
            edges.append(f"Confront {hunter.confront}")
        if hunter.becalm > 0:
            edges.append(f"Becalm {hunter.becalm}")

        if edges:
            print(f"  {hunter.name}: {', '.join(edges)}")
        else:
            print(f"  {hunter.name}: No edges set")


def populate_traits():
    """Main function to populate and verify all gameline traits."""
    print("=" * 60)
    print("POPULATING GAMELINE-SPECIFIC TRAITS")
    print("=" * 60)

    # Assign traits that need M2M adds
    assign_werewolf_gifts()

    # Verify all traits are set properly
    verify_vampire_disciplines()
    verify_mage_spheres()
    verify_wraith_arcanoi()
    verify_changeling_arts()
    verify_demon_lores()
    verify_hunter_edges()

    print("\n" + "=" * 60)
    print("TRAIT POPULATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    populate_traits()

populate_traits()
