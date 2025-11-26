"""
Mummy item population script for Seattle Test Chronicle.

Creates MummyRelics (ancient artifacts), Vessels (Ba storage), and Ushabtis
(animated servants) for the Amenti community.
"""

from accounts.models import Profile
from game.models import Chronicle
from items.models.mummy import MummyRelic, Ushabti, Vessel


def populate_mummy_items():
    """Create all Mummy items for the test chronicle."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")
    st_user = Profile.objects.get(user__username="DarkMaster99").user

    # =========================================================================
    # MUMMY RELICS - LEADERSHIP ARTIFACTS
    # =========================================================================

    # Meritaten's Ankh
    meritaten_ankh, created = MummyRelic.objects.get_or_create(
        name="Ankh of Eternal Life",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """The golden ankh that Meritaten carried in her first life
and has accompanied her through each resurrection. The artifact is one of the
oldest mummy relics in Seattle, dating to the New Kingdom of Egypt.

The ankh amplifies healing Hekau and serves as a focus for resurrection
rituals. Its presence alone provides comfort to Amenti who feel their
connection to the living world weakening.

The artifact has never been lost, passing from Meritaten's hands only during
her periods of death-sleep, always to return upon her awakening.""",
            "rank": 5,
            "relic_type": "jewelry",
            "era": "new_kingdom",
            "original_owner": "Meritaten, Princess of Egypt",
            "powers": """Amplifies healing Hekau by two dice
Serves as focus for resurrection rituals
Provides Sekhem regeneration in sunlight
Comforts Amenti against Shadow influence""",
            "ba_cost": 2,
            "associated_hekau": "Celestial",
            "requires_sekhem": 3,
            "requires_ritual": False,
            "is_cursed": False,
            "is_unique": True,
            "is_sentient": False,
            "material": "Gold with lapis lazuli inlay",
            "hieroglyphic_inscription": "Life eternal, life renewed, the sun rises ever again",
            "history": """Created during the reign of Akhenaten, this ankh was
blessed by priests of the Aten. It has served Meritaten through countless
resurrections, its power growing with each cycle of death and renewal.""",
        },
    )
    if created:
        print(f"  Created Mummy Relic: {meritaten_ankh.name}")

    # Sethnakht's Staff
    sethnakht_staff, created = MummyRelic.objects.get_or_create(
        name="Staff of Thoth",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A gilded staff topped with an ibis head, the symbol of
Thoth. Sethnakht recovered this staff during his first resurrection and has
used it to unlock countless secrets of ancient knowledge.

The staff enhances scholarly Hekau and allows its bearer to read hieroglyphic
texts regardless of dialect or era. It also serves as a conduit for communion
with Thoth himself during proper rituals.

The House of Scrolls considers this staff their most sacred artifact, central
to their mission of preserving and uncovering ancient wisdom.""",
            "rank": 4,
            "relic_type": "tool",
            "era": "ptolemaic",
            "original_owner": "A priest of Thoth in Alexandria",
            "powers": """Enhances knowledge-based Hekau
Allows reading of any Egyptian text
Communion with Thoth during rituals
Perfect recall of witnessed writings""",
            "ba_cost": 1,
            "associated_hekau": "Nomenclature",
            "requires_sekhem": 2,
            "requires_ritual": False,
            "is_cursed": False,
            "is_unique": True,
            "is_sentient": False,
            "material": "Gilded cedar with ivory ibis head",
            "hieroglyphic_inscription": "Wisdom flows from the words of Thoth",
            "history": """Originally created for the Library of Alexandria, the
staff was spirited away before the library's destruction. It has served
scholars and seekers of knowledge ever since.""",
        },
    )
    if created:
        print(f"  Created Mummy Relic: {sethnakht_staff.name}")

    # Khonsu-mes's Scales
    scales_of_maat, created = MummyRelic.objects.get_or_create(
        name="Scales of Ma'at",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A set of golden scales used to weigh hearts against the
feather of Ma'at. While symbolic scales of justice are common, these scales
actually function - they can determine the guilt or innocence of those
brought before them.

Khonsu-mes uses the scales during the Keepers of Ma'at's most serious
judgments. The scales cannot be deceived by lies or illusions; they reveal
the truth of a person's heart with absolute clarity.

The judgment of the scales is considered final by all Amenti. Those found
wanting face consequences determined by the severity of their crimes.""",
            "rank": 5,
            "relic_type": "tool",
            "era": "old_kingdom",
            "original_owner": "Temple of Ma'at at Karnak",
            "powers": """Determine guilt or innocence absolutely
Cannot be deceived by supernatural means
Reveal hidden truths about the judged
Enforce oaths sworn upon them""",
            "ba_cost": 3,
            "associated_hekau": "Celestial",
            "requires_sekhem": 4,
            "requires_ritual": True,
            "is_cursed": False,
            "is_unique": True,
            "is_sentient": False,
            "material": "Gold with a genuine ostrich feather",
            "hieroglyphic_inscription": "Let Ma'at judge as she has judged since the first dawn",
            "history": """These scales served the Temple of Ma'at for millennia
before being entrusted to the Amenti. Their use is reserved for only the
most serious matters of justice.""",
        },
    )
    if created:
        print(f"  Created Mummy Relic: {scales_of_maat.name}")

    # =========================================================================
    # MUMMY RELICS - CULT ARTIFACTS
    # =========================================================================

    # Lions of Sekhmet Sword
    sekhmet_sword, created = MummyRelic.objects.get_or_create(
        name="Khopesh of Sekhmet's Wrath",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A curved Egyptian sword, the traditional weapon of ancient
warriors, blessed by Sekhmet herself according to cult tradition. The blade
has been used in countless battles against the enemies of Ma'at.

Sekhmet-Hathor carries this weapon into battle, its edge burning with divine
fire against those who have earned the war goddess's displeasure. The blade
inflicts wounds that resist supernatural healing.

The Lions of Sekhmet consider the khopesh a sacred trust, passed to their
worthiest warrior. Its bearer is expected to embody Sekhmet's role as both
destroyer and protector.""",
            "rank": 4,
            "relic_type": "weapon",
            "era": "middle_kingdom",
            "original_owner": "Champion of Sekhmet during the Hyksos wars",
            "powers": """Inflicts aggravated damage to supernatural creatures
Wounds resist supernatural healing
Burns with divine fire when activated
Inspires terror in enemies of Ma'at""",
            "ba_cost": 2,
            "associated_hekau": "Celestial",
            "requires_sekhem": 3,
            "requires_ritual": False,
            "is_cursed": False,
            "is_unique": True,
            "is_sentient": False,
            "material": "Bronze with gold and electrum inlay",
            "hieroglyphic_inscription": "The flame of Sekhmet consumes the enemies of Ra",
            "history": """Forged during the wars against the Hyksos invaders, this
blade has protected Egypt's faithful for over three thousand years.""",
        },
    )
    if created:
        print(f"  Created Mummy Relic: {sekhmet_sword.name}")

    # Healer's Scroll
    healers_scroll, created = MummyRelic.objects.get_or_create(
        name="Scroll of Isis's Compassion",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A papyrus scroll containing healing spells attributed to
Isis herself. The scroll has been carefully preserved across millennia, its
contents providing the foundation for Amenti healing traditions.

The scroll can be read to enhance healing Hekau or consulted for treatment
of injuries that defy conventional understanding. Its wisdom encompasses both
physical and spiritual healing.

The House of Scrolls maintains custody of this artifact, making it available
to healers who serve the Amenti community.""",
            "rank": 3,
            "relic_type": "scroll",
            "era": "ptolemaic",
            "original_owner": "Temple of Isis at Philae",
            "powers": """Enhances healing Hekau
Provides guidance for treating supernatural injuries
Can cure some forms of spiritual corruption
Protects reader from harm during treatment""",
            "ba_cost": 1,
            "associated_hekau": "Alchemy",
            "requires_sekhem": 2,
            "requires_ritual": False,
            "is_cursed": False,
            "is_unique": True,
            "is_sentient": False,
            "material": "Papyrus with red and black ink",
            "hieroglyphic_inscription": "The tears of Isis heal all wounds",
            "history": """Copied from temple records at Philae before the
Christian suppression of Egyptian religion. The scroll preserves knowledge
that would otherwise have been lost.""",
        },
    )
    if created:
        print(f"  Created Mummy Relic: {healers_scroll.name}")

    # =========================================================================
    # MUMMY RELICS - PERSONAL ARTIFACTS
    # =========================================================================

    # Scarab Amulet
    heart_scarab, created = MummyRelic.objects.get_or_create(
        name="Heart Scarab of Protection",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A carved scarab beetle of lapis lazuli, the traditional
amulet placed over a mummy's heart to ensure safe passage to the afterlife.
This particular scarab has been through multiple resurrections with its
owner and carries accumulated power.

The scarab provides protection against attempts to manipulate or control
the wearer's heart or emotions. It also helps resist the Shadow's attempts
to corrupt the Amenti's purpose.

Several such scarabs exist among Seattle's Amenti, each carrying the history
of its owner's deaths and rebirths.""",
            "rank": 3,
            "relic_type": "jewelry",
            "era": "late_period",
            "original_owner": "Various - personal amulets",
            "powers": """Protection against emotional manipulation
Resistance to Shadow corruption
Ensures safe transition during death
Anchors the Ba during resurrection""",
            "ba_cost": 1,
            "associated_hekau": "Celestial",
            "requires_sekhem": 1,
            "requires_ritual": False,
            "is_cursed": False,
            "is_unique": False,
            "is_sentient": False,
            "material": "Lapis lazuli with gold setting",
            "hieroglyphic_inscription": "Let not my heart be separated from me",
            "history": """Heart scarabs were common burial items, but those that
accompany Amenti through multiple cycles gain power from the experience.""",
        },
    )
    if created:
        print(f"  Created Mummy Relic: {heart_scarab.name}")

    # Eye of Horus
    eye_of_horus, created = MummyRelic.objects.get_or_create(
        name="Wadjet Eye of Seeing",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """An amulet shaped like the Eye of Horus, the sacred symbol
of protection and royal power. This particular eye has been enchanted to
grant true sight, piercing illusions and revealing hidden truths.

The eye is traditionally worn by Amenti who deal with the supernatural
community, where deception is common. Its presence ensures that lies
and illusions do not go undetected.

The artifact requires Ba to activate, making its use a conscious choice
rather than a passive protection.""",
            "rank": 3,
            "relic_type": "jewelry",
            "era": "new_kingdom",
            "original_owner": "Temple of Horus at Edfu",
            "powers": """Pierce illusions and disguises
Detect supernatural concealment
Reveal hidden spiritual presences
Protect against visual-based attacks""",
            "ba_cost": 2,
            "associated_hekau": "Celestial",
            "requires_sekhem": 2,
            "requires_ritual": False,
            "is_cursed": False,
            "is_unique": False,
            "is_sentient": False,
            "material": "Faience with gold and lapis accents",
            "hieroglyphic_inscription": "The eye of Horus sees all truth",
            "history": """Created for the Temple of Horus, this eye has served
those who seek truth for over two thousand years.""",
        },
    )
    if created:
        print(f"  Created Mummy Relic: {eye_of_horus.name}")

    # =========================================================================
    # MUMMY RELICS - CORRUPTED ARTIFACTS
    # =========================================================================

    # Apophis-Touched Item
    serpent_ring, created = MummyRelic.objects.get_or_create(
        name="Ring of the Serpent",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A gold ring bearing the image of a coiled serpent, recovered
from a destroyed Apophis cultist. The ring radiates corruption and whispers
promises of power to those who hold it.

The Amenti keep this ring secured, studying it to understand the Apophis
cult's methods while preventing its use. The ring appears to be a focus
for corrupting Hekau, twisting the user's magic toward destructive ends.

Those who have handled the ring report nightmares of serpents and darkness.
Long exposure may lead to corruption of the handler's purpose.""",
            "rank": 4,
            "relic_type": "jewelry",
            "era": "unknown",
            "original_owner": "Apophis cultist - destroyed",
            "powers": """Enhances destructive Hekau
Provides connection to Apophis's power
Corrupts user's purpose over time
Grants dark visions and knowledge""",
            "ba_cost": 0,
            "associated_hekau": "Unknown - corrupted",
            "requires_sekhem": 0,
            "requires_ritual": False,
            "is_cursed": True,
            "is_unique": True,
            "is_sentient": True,
            "material": "Gold with obsidian serpent eyes",
            "hieroglyphic_inscription": "Chaos is the only truth",
            "history": """Origin unknown - recovered from Apophis cultist in
Seattle, 2019. Secured for study and containment.""",
        },
    )
    if created:
        print(f"  Created Mummy Relic: {serpent_ring.name}")

    # =========================================================================
    # VESSELS - BA STORAGE
    # =========================================================================

    # Large Ceremonial Vessel
    large_vessel, created = Vessel.objects.get_or_create(
        name="Great Urn of the Phoenix",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A large alabaster urn used for storing Ba during major
ceremonies and as an emergency reserve for the Amenti community. The urn
can hold far more Ba than personal vessels, making it invaluable for group
rituals and resurrection preparations.

The urn is kept at the museum wing, disguised as part of the collection.
Only the most trusted Amenti know its true nature and location.

The Phoenix imagery represents the Amenti's cycle of death and rebirth,
making this vessel particularly appropriate for resurrection rituals.""",
            "rank": 5,
            "vessel_type": "urn",
            "max_ba": 50,
            "current_ba": 35,
            "transfer_rate": 5,
            "efficiency": 90,
            "is_portable": False,
            "requires_ritual": True,
            "is_attuned": False,
            "material": "Alabaster with gold inlay",
            "inscriptions": "From death comes life, eternal cycle of Ra",
        },
    )
    if created:
        print(f"  Created Vessel: {large_vessel.name}")

    # Personal Canopic Jar
    personal_canopic, created = Vessel.objects.get_or_create(
        name="Canopic Jar of Imset",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A canopic jar topped with a human head representing Imset,
one of the four sons of Horus. This personal vessel allows an Amenti to
store Ba for later use, maintaining a reserve for emergencies.

Personal canopic jars are common among Amenti who engage in dangerous
activities. The stored Ba can mean the difference between survival and
entering death-sleep at an inopportune moment.

This particular jar has served multiple owners, each adding to its
accumulated history and power.""",
            "rank": 3,
            "vessel_type": "canopic",
            "max_ba": 30,
            "current_ba": 20,
            "transfer_rate": 3,
            "efficiency": 85,
            "is_portable": True,
            "requires_ritual": False,
            "is_attuned": False,
            "material": "Limestone with painted features",
            "inscriptions": "Imset guards the liver, vessel of life",
        },
    )
    if created:
        print(f"  Created Vessel: {personal_canopic.name}")

    # Scarab Vessel
    scarab_vessel, created = Vessel.objects.get_or_create(
        name="Scarab of Khepri",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A large carved scarab beetle that serves as a portable
Ba vessel. The scarab can be carried easily and accessed quickly, making
it ideal for Amenti who travel frequently.

The scarab's connection to Khepri, the sun god of rebirth, makes it
particularly effective at storing Ba for resurrection purposes. Energy
stored in this vessel is especially potent for renewal rituals.

Several such scarabs exist among Seattle's Amenti, each crafted by those
skilled in Effigy magic.""",
            "rank": 2,
            "vessel_type": "scarab",
            "max_ba": 20,
            "current_ba": 15,
            "transfer_rate": 2,
            "efficiency": 80,
            "is_portable": True,
            "requires_ritual": False,
            "is_attuned": False,
            "material": "Black basalt with gold inlay",
            "inscriptions": "Khepri rises, bringing new life",
        },
    )
    if created:
        print(f"  Created Vessel: {scarab_vessel.name}")

    # Crystal Vessel
    crystal_vessel, created = Vessel.objects.get_or_create(
        name="Crystal of the Morning Sun",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A quartz crystal vessel that recharges slowly when exposed
to morning sunlight. The vessel was created by an Amenti who specialized in
solar magic and wanted a self-sustaining Ba reserve.

The crystal must be exposed to dawn light to recharge, gaining Ba proportional
to the clarity of the sunrise. Cloudy mornings produce less energy, while
clear dawns fill the crystal rapidly.

The vessel is kept at the House of Scrolls library, where it can be placed
in a window each morning.""",
            "rank": 3,
            "vessel_type": "crystal",
            "max_ba": 25,
            "current_ba": 18,
            "transfer_rate": 3,
            "efficiency": 95,
            "is_portable": True,
            "requires_ritual": False,
            "is_attuned": False,
            "material": "Clear quartz with rose gold mount",
            "inscriptions": "Ra's light fills all vessels",
        },
    )
    if created:
        print(f"  Created Vessel: {crystal_vessel.name}")

    # =========================================================================
    # USHABTIS - ANIMATED SERVANTS
    # =========================================================================

    # Guardian Ushabti
    guardian_ushabti, created = Ushabti.objects.get_or_create(
        name="Ushabti of the Vigilant Hawk",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A stone ushabti carved in the form of a Horus-headed warrior.
When animated, the ushabti serves as a guardian, protecting its master's
resting place or accompanying them on dangerous missions.

The ushabti stands about two feet tall when dormant but can animate into
a larger, more imposing form. Its combat capabilities are significant,
though it requires substantial Ba to maintain for extended periods.

The museum keeps this ushabti on display as a historical artifact, never
suspecting its true nature.""",
            "rank": 4,
            "is_currently_animated": False,
            "ba_to_animate": 4,
            "ba_per_day": 4,
            "animation_duration_hours": 24,
            "purpose": "guardian",
            "physical_rating": 4,
            "mental_rating": 2,
            "special_abilities": "Enhanced combat capabilities, supernatural senses, tireless vigilance",
            "material": "stone",
            "size_description": "Two feet tall, humanoid form",
            "appearance": "Horus-headed warrior in ancient Egyptian armor",
            "command_word": "Protect in the name of Horus",
            "obeys_only_creator": False,
        },
    )
    if created:
        print(f"  Created Ushabti: {guardian_ushabti.name}")

    # Servant Ushabti
    servant_ushabti, created = Ushabti.objects.get_or_create(
        name="Ushabti of the Faithful Servant",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A wooden ushabti carved in the form of a servant carrying
tools. When animated, it can perform household tasks, maintain living spaces,
and assist with daily needs.

The servant ushabti is common among Amenti who maintain mortal covers -
the ushabti can handle mundane tasks while its master focuses on more
important matters. Its work is careful and thorough.

Multiple servant ushabtis exist among Seattle's Amenti, each created to
specifications matching their master's needs.""",
            "rank": 2,
            "is_currently_animated": False,
            "ba_to_animate": 2,
            "ba_per_day": 2,
            "animation_duration_hours": 12,
            "purpose": "servant",
            "physical_rating": 2,
            "mental_rating": 2,
            "special_abilities": "Household maintenance, cooking, cleaning, organizing",
            "material": "wood",
            "size_description": "Eighteen inches tall, humanoid form",
            "appearance": "Traditional Egyptian servant with carrying basket",
            "command_word": "Serve as in life",
            "obeys_only_creator": False,
        },
    )
    if created:
        print(f"  Created Ushabti: {servant_ushabti.name}")

    # Scribe Ushabti
    scribe_ushabti, created = Ushabti.objects.get_or_create(
        name="Ushabti of the Eternal Scribe",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A clay ushabti holding a scroll and stylus. When animated,
the scribe can transcribe texts, take notes, and maintain records with
perfect accuracy.

The House of Scrolls maintains several scribe ushabtis for copying rare
texts and documenting their research. The ushabtis can work continuously
as long as they have Ba, producing identical copies of any written work.

The scribes can write in any language their master knows, making them
invaluable for translation work.""",
            "rank": 3,
            "is_currently_animated": False,
            "ba_to_animate": 3,
            "ba_per_day": 3,
            "animation_duration_hours": 16,
            "purpose": "scribe",
            "physical_rating": 1,
            "mental_rating": 4,
            "special_abilities": "Perfect transcription, multilingual writing, tireless recording",
            "material": "clay",
            "size_description": "Twenty inches tall, seated scribe pose",
            "appearance": "Traditional Egyptian scribe with writing implements",
            "command_word": "Record as Thoth commands",
            "obeys_only_creator": False,
        },
    )
    if created:
        print(f"  Created Ushabti: {scribe_ushabti.name}")

    # Messenger Ushabti
    messenger_ushabti, created = Ushabti.objects.get_or_create(
        name="Ushabti of the Swift Wing",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A small ushabti shaped like a falcon, capable of flight
when animated. The messenger can carry small objects or verbal messages
across the city, moving unseen through the night.

The falcon ushabti is invaluable for secure communication between Amenti.
It cannot be intercepted by conventional means and will deliver its message
or cargo only to the intended recipient.

The ushabti's flight is silent and its form blends with Seattle's urban
wildlife, making it effectively invisible to casual observation.""",
            "rank": 2,
            "is_currently_animated": False,
            "ba_to_animate": 2,
            "ba_per_day": 2,
            "animation_duration_hours": 8,
            "purpose": "messenger",
            "physical_rating": 2,
            "mental_rating": 3,
            "special_abilities": "Flight, message memorization, target finding, stealth",
            "material": "gold",
            "size_description": "Six inches tall, falcon form",
            "appearance": "Golden falcon with lapis eyes",
            "command_word": "Fly swift as Horus",
            "obeys_only_creator": False,
        },
    )
    if created:
        print(f"  Created Ushabti: {messenger_ushabti.name}")

    print("Mummy items populated successfully.")

    return {
        "leadership_relics": [meritaten_ankh, sethnakht_staff, scales_of_maat],
        "cult_relics": [sekhmet_sword, healers_scroll],
        "personal_relics": [heart_scarab, eye_of_horus],
        "corrupted_relics": [serpent_ring],
        "vessels": [large_vessel, personal_canopic, scarab_vessel, crystal_vessel],
        "ushabtis": [guardian_ushabti, servant_ushabti, scribe_ushabti, messenger_ushabti],
    }


if __name__ == "__main__":
    populate_mummy_items()
