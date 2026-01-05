import random

from django.db import models
from django.urls import reverse
from locations.models.mage.realm import HorizonRealm


class SphereChoices(models.TextChoices):
    CORRESPONDENCE = "correspondence", "Correspondence"
    ENTROPY = "entropy", "Entropy"
    FORCES = "forces", "Forces"
    LIFE = "life", "Life"
    MATTER = "matter", "Matter"
    MIND = "mind", "Mind"
    PRIME = "prime", "Prime"
    SPIRIT = "spirit", "Spirit"
    TIME = "time", "Time"


class ParadigmChoices(models.TextChoices):
    MECHANISTIC_COSMOS = "mechanistic_cosmos", "A Mechanistic Cosmos"
    GODS_AND_MONSTERS = "gods_and_monsters", "A World of Gods and Monsters"
    GOLDEN_AGE = "golden_age", "Bring Back the Golden Age!"
    DIVINE_AND_ALIVE = "divine_and_alive", "Creation is Innately Divine and Alive"
    DIVINE_ORDER = "divine_order", "Divine Order and Earthly Chaos"
    CHAOS = "chaos", "Everything is Chaos"
    DATA = "data", "Everything is Data"
    ILLUSION = "illusion", "Everything's an Illusion, Prison, or Mistake"
    FAITH = "faith", "It's All Good – Have Faith!"
    MIGHT_IS_RIGHT = "might_is_right", "Might is Right"
    OBLIVION = "oblivion", "One-Way Trip to Oblivion"
    TECH = "tech", "Tech Holds All Answers"
    ANTIMAGICK = "antimagick", "Antimagick (Sleeper Realm)"
    UNSTABLE = "unstable", "Unstable Realm (Different paradigm per obstacle)"


class FinalObstacleTypeChoices(models.TextChoices):
    GIVE_SECRET = "give_secret", "Give a Secret"
    WIN_GAME = "win_game", "Win a Game"
    SOLVE_RIDDLE = "solve_riddle", "Solve a Riddle"
    BUTTON = "button", "The Button"
    MAZE = "maze", "Standard Maze"
    ABNORMAL_MAZE = "abnormal_maze", "Abnormal Maze"
    SILVER_BULLET = "silver_bullet", "Silver Bullet for the Beast"
    GUESS_NAME = "guess_name", "Guess My Name"
    RANDOM_SPHERE = "random_sphere", "Any Sphere Obstacle"
    COMBINED = "combined", "Combined Obstacles"


class ParadoxRealm(HorizonRealm):
    """
    A Paradox Realm for Mage 20th Anniversary Edition.

    Paradox realms test mages who have accumulated significant paradox backlash.
    They strip the character of their magick and equipment, leaving only wits to
    overcome trials.
    """

    type = "paradox_realm"
    gameline = "mta"

    primary_sphere = models.CharField(
        max_length=20,
        choices=SphereChoices.choices,
        default=SphereChoices.CORRESPONDENCE,
        help_text="The sphere that created the greatest buildup of paradox",
    )

    secondary_sphere = models.CharField(
        max_length=20,
        choices=SphereChoices.choices,
        blank=True,
        null=True,
        help_text="Optional second sphere for combined-sphere realms",
    )

    paradigm = models.CharField(
        max_length=50,
        choices=ParadigmChoices.choices,
        default=ParadigmChoices.ANTIMAGICK,
        help_text="How the paradox realm interprets how reality 'should' be",
    )

    secondary_paradigm = models.CharField(
        max_length=50,
        choices=ParadigmChoices.choices,
        blank=True,
        null=True,
        help_text="Optional second paradigm for combined-paradigm realms",
    )

    atmosphere_details = models.JSONField(
        default=list,
        blank=True,
        help_text="List of atmosphere attributes rolled for the realm",
    )

    num_primary_obstacles = models.IntegerField(
        default=0, help_text="Number of obstacles from the primary sphere"
    )

    num_random_obstacles = models.IntegerField(
        default=0, help_text="Number of obstacles from random spheres"
    )

    final_obstacle_type = models.CharField(
        max_length=20,
        choices=FinalObstacleTypeChoices.choices,
        default=FinalObstacleTypeChoices.MAZE,
        help_text="Type of final obstacle to overcome",
    )

    final_obstacle_details = models.JSONField(
        default=dict, blank=True, help_text="Details of the final obstacle"
    )

    class Meta:
        verbose_name = "Paradox Realm"
        verbose_name_plural = "Paradox Realms"

    def get_update_url(self):
        return reverse("locations:mage:update:paradox_realm", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("locations:mage:create:paradox_realm")

    def get_obstacles(self):
        """Get all obstacles for this realm"""
        return ParadoxObstacle.objects.filter(realm=self).order_by("order")

    def get_atmosphere_elements(self):
        """Get all atmosphere elements for this realm"""
        return ParadoxAtmosphere.objects.filter(realm=self)

    # ===== RANDOM GENERATION METHODS =====

    @staticmethod
    def roll_d10():
        """Roll a single 10-sided die"""
        return random.randint(1, 10)

    @staticmethod
    def roll_d5():
        """Roll a 5-sided die (d10 divided by 2, rounded up)"""
        return (random.randint(1, 10) + 1) // 2

    @staticmethod
    def roll_2d10():
        """Roll two 10-sided dice and add them"""
        return random.randint(1, 10) + random.randint(1, 10)

    @staticmethod
    def roll_d100():
        """Roll percentile dice (1-100)"""
        return random.randint(1, 100)

    @classmethod
    def random_sphere(cls):
        """Roll on Table B1 to determine a random sphere"""
        roll = cls.roll_d10()
        if roll == 10:
            return None  # Indicates two spheres - handle separately
        spheres = list(SphereChoices.values)
        return spheres[roll - 1]

    @classmethod
    def random_paradigm(cls):
        """Roll on Table B2 to determine a random paradigm"""
        roll = cls.roll_2d10()

        # Map rolls to paradigms
        paradigm_map = {
            1: ParadigmChoices.UNSTABLE,
            2: ParadigmChoices.MECHANISTIC_COSMOS,
            3: ParadigmChoices.GODS_AND_MONSTERS,
            4: ParadigmChoices.GOLDEN_AGE,
            5: ParadigmChoices.DIVINE_AND_ALIVE,
            6: ParadigmChoices.DIVINE_ORDER,
            7: ParadigmChoices.CHAOS,
            8: ParadigmChoices.DATA,
            9: ParadigmChoices.ILLUSION,
            10: ParadigmChoices.FAITH,
            11: ParadigmChoices.MIGHT_IS_RIGHT,
            12: ParadigmChoices.OBLIVION,
            13: ParadigmChoices.TECH,
        }

        if roll in paradigm_map:
            return paradigm_map[roll], None
        elif 14 <= roll <= 16:
            # Character's paradigm - use a random one for base generation
            options = [p for p in ParadigmChoices.values if p not in [ParadigmChoices.UNSTABLE]]
            return random.choice(options), None
        elif 17 <= roll <= 19:
            return ParadigmChoices.ANTIMAGICK, None
        else:  # roll == 20
            return None, None  # Two paradigms - handle separately

    @classmethod
    def random_obstacle_count(cls):
        """
        Roll on Table B3 to determine number of obstacles.
        Returns a tuple: (primary_count, random_count)
        """
        roll = cls.roll_d10()

        if roll == 1:
            return 0, 0
        elif roll == 2:
            return 1, 0
        elif roll == 3:
            return 2, 0
        elif roll == 4:
            return 3, 0
        elif roll == 5:
            return cls.roll_d5(), 0
        elif roll == 6:
            return cls.roll_d5(), 1
        elif roll == 7:
            return 1, 1
        elif roll == 8:
            return 1, cls.roll_d5()
        elif roll == 9:
            return 0, cls.roll_d5()
        else:  # roll == 10
            primary = cls.roll_d5()
            random_count = cls.roll_d5()
            total = primary + random_count
            if total > 6:
                random_count = 6 - primary
            return primary, random_count

    @classmethod
    def random_final_obstacle(cls):
        """Roll on Table B4 to determine the final obstacle"""
        roll = cls.roll_d10()

        obstacle_map = {
            1: FinalObstacleTypeChoices.GIVE_SECRET,
            2: FinalObstacleTypeChoices.WIN_GAME,
            3: FinalObstacleTypeChoices.SOLVE_RIDDLE,
            4: FinalObstacleTypeChoices.BUTTON,
            5: FinalObstacleTypeChoices.MAZE,
            6: FinalObstacleTypeChoices.ABNORMAL_MAZE,
            7: FinalObstacleTypeChoices.SILVER_BULLET,
            8: FinalObstacleTypeChoices.GUESS_NAME,
            9: FinalObstacleTypeChoices.RANDOM_SPHERE,
        }

        if roll in obstacle_map:
            return obstacle_map[roll], {}
        else:  # roll == 10
            return FinalObstacleTypeChoices.COMBINED, {}

    @classmethod
    def random(cls, name="Random Paradox Realm", save=False):
        """
        Generate a complete random paradox realm following the guide's procedures.

        Args:
            name: Name for the realm
            save: Whether to save the realm and related objects to database

        Returns:
            A new ParadoxRealm instance
        """
        # Step 1: Select sphere
        primary = cls.random_sphere()
        secondary = None
        if primary is None:
            # Two spheres
            primary = cls.random_sphere()
            while primary is None:
                primary = cls.random_sphere()
            secondary = cls.random_sphere()
            while secondary == primary or secondary is None:
                secondary = cls.random_sphere()

        # Step 2: Select paradigm
        para1, para2 = cls.random_paradigm()
        if para1 is None:
            # Two paradigms
            para1, _ = cls.random_paradigm()
            para2, _ = cls.random_paradigm()
            while para2 == para1 or para2 is None:
                para2, _ = cls.random_paradigm()

        # Step 3: Determine number of obstacles
        num_primary, num_random = cls.random_obstacle_count()

        # Step 4: Generate final obstacle
        final_type, final_details = cls.random_final_obstacle()

        # Create the realm
        realm = cls(
            name=name,
            primary_sphere=primary,
            secondary_sphere=secondary,
            paradigm=para1,
            secondary_paradigm=para2,
            num_primary_obstacles=num_primary,
            num_random_obstacles=num_random,
            final_obstacle_type=final_type,
            final_obstacle_details=final_details,
        )

        if save:
            realm.save()

            # Generate atmosphere details (2-3 rolls)
            num_atmosphere_rolls = random.randint(2, 3)
            for i in range(num_atmosphere_rolls):
                ParadoxAtmosphere.random(realm=realm, paradigm=para1, save=True)

            # Generate primary sphere obstacles
            for i in range(num_primary):
                ParadoxObstacle.random(realm=realm, sphere=primary, order=i, save=True)

            # Generate random sphere obstacles
            for i in range(num_random):
                random_sphere = cls.random_sphere()
                while random_sphere is None:
                    random_sphere = cls.random_sphere()
                ParadoxObstacle.random(
                    realm=realm, sphere=random_sphere, order=num_primary + i, save=True
                )

        return realm

    def __str__(self):
        spheres = self.get_primary_sphere_display()
        if self.secondary_sphere:
            spheres += f" + {self.get_secondary_sphere_display()}"
        return f"{self.name} ({spheres})"


class ParadoxObstacle(models.Model):
    """An obstacle within a paradox realm"""

    realm = models.ForeignKey(
        ParadoxRealm, on_delete=models.CASCADE, related_name="realm_obstacles"
    )

    sphere = models.CharField(
        max_length=20,
        choices=SphereChoices.choices,
    )

    obstacle_number = models.IntegerField(
        help_text="The specific obstacle from the sphere's table (1-10)"
    )

    order = models.IntegerField(default=0, help_text="Order in which this obstacle appears")

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Paradox Obstacle"
        verbose_name_plural = "Paradox Obstacles"

    @classmethod
    def random(cls, realm, sphere, order=0, save=False):
        """Generate a random obstacle for the given sphere"""
        roll = ParadoxRealm.roll_d10()

        # Get obstacle name from the mapping
        obstacle_name = cls.get_obstacle_name(sphere, roll)

        obstacle = cls(
            realm=realm,
            sphere=sphere,
            obstacle_number=roll,
            order=order,
            name=obstacle_name,
            description=f"Obstacle #{roll} from {sphere} table",
        )

        if save:
            obstacle.save()

        return obstacle

    @staticmethod
    def get_obstacle_name(sphere, roll):
        """Get the name of an obstacle based on sphere and roll"""
        # Simplified mapping - full implementation would include all obstacle names
        obstacle_names = {
            SphereChoices.CORRESPONDENCE: {
                1: "Leaning Walls",
                2: "Chalk",
                3: "Mirrors",
                4: "Time Bomb",
                5: "One Step Forward...",
                6: "Compress",
                7: "Outside",
                8: "Salt",
                9: "Abnormal Maze",
                10: "Free Space",
            },
            SphereChoices.ENTROPY: {
                1: "Shell Game",
                2: "Avatar",
                3: "Heart",
                4: "Domino",
                5: "Crack",
                6: "Dust",
                7: "Bone Field",
                8: "The Shadow",
                9: "Regress",
                10: "Unravel",
            },
            SphereChoices.FORCES: {
                1: "Machine",
                2: "Spin",
                3: "Gap",
                4: "Fire",
                5: "Storm",
                6: "Geiger",
                7: "Hole",
                8: "Quake",
                9: "Chill",
                10: "Illusion",
            },
            SphereChoices.LIFE: {
                1: "Mouse",
                2: "Tree",
                3: "Elephant",
                4: "Child",
                5: "All as One",
                6: "Brood",
                7: "Skeleton Hedge",
                8: "Mortal",
                9: "This Thing Called ENT",
                10: "Boil",
            },
            SphereChoices.MATTER: {
                1: "Heavy",
                2: "Pipes",
                3: "Midas",
                4: "Just Right",
                5: "Vase",
                6: "Rocks Fall",
                7: "Sliding Tower",
                8: "Deep",
                9: "Slush",
                10: "Disappearing Floor",
            },
            SphereChoices.MIND: {
                1: "Two Guards",
                2: "Ten Chambers",
                3: "A Better You",
                4: "Trials",
                5: "Instructions",
                6: "Rage",
                7: "Mirrors",
                8: "Babble",
                9: "Speak Friend",
                10: "Vigenère",
            },
            SphereChoices.PRIME: {
                1: "Kiss the Chef",
                2: "Desert",
                3: "Drone",
                4: "Sinking Ship",
                5: "Zap",
                6: "Tapestry",
                7: "Dust",
                8: "Hedge Door",
                9: "Tall",
                10: "Pythagorean Cup",
            },
            SphereChoices.SPIRIT: {
                1: "The Dance",
                2: "Utopia",
                3: "Sleep",
                4: "Snow Globe",
                5: "Below",
                6: "Bell, Book, and Candle",
                7: "Starchild",
                8: "Card King",
                9: "Noir",
                10: "The Bottle Plant",
            },
            SphereChoices.TIME: {
                1: "Save a Life",
                2: "Trade",
                3: "Search",
                4: "Safe",
                5: "Hallway",
                6: "Good Guess",
                7: "Trigger",
                8: "Quantum Gravity",
                9: "Double Cat",
                10: "Big Maze",
            },
        }

        return obstacle_names.get(sphere, {}).get(roll, f"{sphere} Obstacle {roll}")

    def __str__(self):
        return f"{self.name} ({self.get_sphere_display()})"


class ParadoxAtmosphere(models.Model):
    """An atmosphere element for a paradox realm"""

    realm = models.ForeignKey(
        ParadoxRealm, on_delete=models.CASCADE, related_name="realm_atmospheres"
    )

    paradigm = models.CharField(
        max_length=50,
        choices=ParadigmChoices.choices,
    )

    atmosphere_number = models.IntegerField(
        help_text="The specific atmosphere from the paradigm's table (1-10)"
    )

    description = models.TextField()

    class Meta:
        verbose_name = "Paradox Atmosphere"
        verbose_name_plural = "Paradox Atmospheres"

    @classmethod
    def random(cls, realm, paradigm, save=False):
        """Generate a random atmosphere element for the given paradigm"""
        roll = ParadoxRealm.roll_d10()

        # Get description from the mapping
        description = cls.get_atmosphere_description(paradigm, roll)

        atmosphere = cls(
            realm=realm,
            paradigm=paradigm,
            atmosphere_number=roll,
            description=description,
        )

        if save:
            atmosphere.save()

        return atmosphere

    @staticmethod
    def get_atmosphere_description(paradigm, roll):
        """Get atmosphere description based on paradigm and roll"""
        # This is a simplified version with just the core descriptors
        # Full implementation would include complete text from the guide

        atmospheres = {
            ParadigmChoices.ANTIMAGICK: {
                1: "Moving chains slink along the ground, attempting to pin down anyone who touches them",
                2: "Burning wood smell intensifies, reaching burning flesh by final obstacle with distant screams",
                3: "Endless field of grass that starts vibrant but dies and rots as obstacles are completed",
                4: "Character grows fur and slowly transforms into a chimpanzee (reverts upon exit)",
                5: "Different rooms from character's childhood home, showing timeline where they never existed",
                6: "Steep mountain path with thinning air, becoming nearly breathless by final obstacle",
                7: "Blood-red sky - the character knows it's their own blood",
                8: "Burned libraries and destroyed golden age buildings that crumble as obstacles complete",
                9: "Faint buzzing/ringing that becomes louder with each obstacle completed",
                10: "Roll again and combine with another atmosphere table",
            },
            ParadigmChoices.MECHANISTIC_COSMOS: {
                1: "Ground is a giant spinning cog, path leads toward distant red light at center",
                2: "Copy-paste suburban homes with mechanical people on wheeled tracks, repeating routines",
                3: "Sky peels away revealing golden cogs stained with blood; blood pours by final obstacle",
                4: "Perfect piano scales echo through the realm with flawless rhythm",
                5: "Main street from childhood, frozen in time with red cords connecting people to places",
                6: "Character's skin becomes cold, stiff, and metal-like (reverts upon exit)",
                7: "Giant unblinking eye observes; character must step through it to leave",
                8: "Impossibly tall skyscrapers hide secrets of Paradox Personalities inside",
                9: "All structures are decrepit and ruined, withered by time",
                10: "Roll again and combine with another atmosphere table",
            },
            ParadigmChoices.GODS_AND_MONSTERS: {
                1: "Medieval hamlet with shuttered doors and windows, panicked breathing audible inside",
                2: "Thick vegetation grasps at character, pulling away possessions",
                3: "Thick fog limits vision to 20 feet even with supernatural senses",
                4: "Character's steps leave no impression; objects are heavier to manipulate",
                5: "It's raining",
                6: "Large wolf stalks the character through the realm",
                7: "Dark tunnel leading downward; torches become sparse until final obstacle in empty cave",
                8: "Aftermath of flood with knee-high water and floating driftwood/corpses",
                9: "Thriving vegetation withers to white dust; sky darkens; Earth visible by final obstacle",
                10: "Roll again and combine with another atmosphere table",
            },
            ParadigmChoices.GOLDEN_AGE: {
                1: "Hive-mind people praise character's magick at first, become fearful, then flee screaming",
                2: "Shining ivory castle in distance, getting closer; exit via crossing the drawbridge",
                3: "Island(s) that shrink as obstacles complete, bedroom-sized by final obstacle",
                4: "You cannot go back - places the character has been fade and disappear",
                5: "The realm is tinted rose",
                6: "Medieval villagers use magick freely; character is the only one who cannot",
                7: "Ruins of once-great kingdoms still have functioning mystical ancient civilization parts",
                8: "Character 'wakes' in hospital room, pursued by doctors before returning to realm",
                9: "Forests and prairies in orderly geometric patterns corresponding to sphere symbols",
                10: "Roll again and combine with another atmosphere table",
            },
            ParadigmChoices.DIVINE_AND_ALIVE: {
                1: "All objects move about like living things; even the realm itself is moving somewhere fast",
                2: "Heartbeat in the realm starts quiet, becomes deafening by final obstacle",
                3: "Everything is green: sky, ground, character, everything",
                4: "Vines and branches grasp at character, wrapping and slowing movement",
                5: "Realm begins to bleed red (or black oil); character bleeds too at final obstacle",
                6: "Realm is corpse of mile-tall god skeleton with vines/trees; wakes at completion",
                7: "River flows through realm on raft/canoe; leads to ocean and shipwreck island",
                8: "Pleasant room temperature, but not the character's preferred temperature",
                9: "Rapid rain cycle: 5-minute showers every 15 minutes, dries quickly between",
                10: "Roll again and combine with another atmosphere table",
            },
            ParadigmChoices.DIVINE_ORDER: {
                1: "Thick wild rosebushes hurt but leave no mark; roses bloom as obstacles complete",
                2: "Bright hot sun beats down, becoming more distracting until nearly blinding at end",
                3: "Haze makes everything out of focus and too vibrant, like missing a sense",
                4: "Pale formless figure stalks character; touch causes freezing frostbite",
                5: "Large stone faces dot landscape, overgrown and screaming",
                6: "Fruit trees with succulent-looking fruits containing only ash",
                7: "Glass stairway going upward toward sun; final obstacle is lecherous house",
                8: "Giant mechanical hand descends, grabs character, throws them to final obstacle",
                9: "Character has moment of complete universal clarity that fades upon return",
                10: "Roll again and combine with another atmosphere table",
            },
            ParadigmChoices.CHAOS: {
                1: "Realm pulsates through different colors including the character",
                2: "No air; atmosphere is thick breathable liquid requiring swimming",
                3: "Character shrunk to microscopic level, growing larger with each obstacle",
                4: "Lava flows quickly; ground constantly rumbling and crashing against plates",
                5: "Small island drifting on vast ocean; falls off edge into void at final obstacle",
                6: "Everything blends: character's feet fade into ground, sky and sea merge",
                7: "Sky changes with each step: colors, patterns, faces changing every second",
                8: "World is paint; style changes each obstacle: watercolor, oil, cartoon, etc.",
                9: "Ripple effect overextended: any motion has far greater kinetic impact",
                10: "Roll again and combine with another atmosphere table",
            },
            ParadigmChoices.DATA: {
                1: "Stone obelisks with runes label each obstacle by title",
                2: "Bioluminescent plants resembling large ferns/fungi, 2-5 meters tall",
                3: "Everything stretched thin and 2D, third dimension missing (feels squished)",
                4: "Art deco buildings with neon lights and glowing wire grids",
                5: "Wireframe world: only outlines visible in bright blue/green/white on black",
                6: "Events glitch out and repeat in bursts of neon zero-and-one sparks",
                7: "Worms, viruses, bugs move around like indifferent wildlife",
                8: "Police with CRT-TV heads showing old TV shows pursue the character",
                9: "No sound; all sounds display visually as breath/bubbles or comic effects",
                10: "Roll again and combine with another atmosphere table",
            },
            ParadigmChoices.ILLUSION: {
                1: "Ground only exists where character stands; materializes ahead, dematerializes behind",
                2: "Character phases through everything except blue-glowing obstacles; becomes solid again at end",
                3: "Character traverses via grimoires in library; each book contains an obstacle",
                4: "Paradox manifestation acts as prison warden, blocking character until complete",
                5: "World flickers like old film reel with clicking projector; melts away at completion",
                6: "Backstage movie set with character as star; each obstacle is a scene to act",
                7: "Island prison; character escapes cell and creeps through to board ship to reality",
                8: "None of the denizens have faces except the character",
                9: "Denizens are Mage 20th developers having meta conversations about game rules",
                10: "Roll again and combine with another atmosphere table",
            },
            ParadigmChoices.FAITH: {
                1: "Happy smiling townsfolk turn on character if they show upset or stress",
                2: "Gorgeous sunrise/sunset sky with vibrant colors stretching across heaven",
                3: "Rapid day/night cycle; happy frolicking day, monstrous hunting night",
                4: "Character finds childhood bicycle/transport that still fits perfectly",
                5: "Nothing lives; mannequins with painted smiles move around",
                6: "Character prone to lightheadedness/absentmindedness, waking elsewhere disoriented",
                7: "Much lower gravity giving bouncy effect; reverses upward at completion",
                8: "Friendly childhood pet follows and aids the character",
                9: "Character finds bar with old friend who buys them a drink",
                10: "Roll again and combine with another atmosphere table",
            },
            ParadigmChoices.MIGHT_IS_RIGHT: {
                1: "Crows/hawks/ravens/pterodactyls in sky become bloody and violent as obstacles complete",
                2: "Mechanical beast moves through barren land scraping up life; obstacles within it",
                3: "Realm at war; character must navigate battlegrounds carefully",
                4: "Shopkeeper offers escape for exorbitant fee; odd jobs are the obstacles",
                5: "Dark Lord villain sends obstacles to stop the Chosen One (the character)",
                6: "Powerful enemies from character's past chase them through the realm",
                7: "Warship crewed by pirates battles across ocean islands; sinks before final obstacle",
                8: "Obstacles within vast fortress (castle, military base, fortified location)",
                9: "Teachers and bullies from childhood harass character through obstacles",
                10: "Roll again and combine with another atmosphere table",
            },
            ParadigmChoices.OBLIVION: {
                1: "Protective suit slows movement; removing it causes unbearable pain",
                2: "Empty buildings missing walls like ant farms visible from outside",
                3: "Crumbling moon splinters and falls; turns red and explodes at completion",
                4: "Giant hourglass; character in top as sand falls; exits through bottom",
                5: "Dinosaurs roam; red star grows until entire sky is red by final obstacle",
                6: "Giant worm destroys everything; eats character after final obstacle to return them",
                7: "Realm slowly melts into infinite tar puddle; nothing left but tar by final obstacle",
                8: "Perpetual night with no sun",
                9: "No life; any denizens mentioned are animated corpses",
                10: "Roll again and combine with another atmosphere table",
            },
            ParadigmChoices.TECH: {
                1: "Thick smog chokes the atmosphere",
                2: "Artificial sun structured like lightbulb; flickers and dims the realm",
                3: "Starship moves between planet obstacles; boarded before final obstacle",
                4: "Barren of vegetation/life but soil is fertile and water flows",
                5: "Looks like nature preserve but metal/plastic/circuits half-inch beneath",
                6: "All mechanisms operated by voice commands to the letter",
                7: "Character in room with computer and cassette tapes; each tape contains obstacle",
                8: "Hollowed-out globe; vast underground civilization on inside",
                9: "Streams of text/numbers/images scroll on all flat surfaces at high speed",
                10: "Roll again and combine with another atmosphere table",
            },
            ParadigmChoices.UNSTABLE: {
                1: "Each obstacle governed by different paradigm atmosphere",
                2: "Paradigm shifts randomly throughout the realm",
                3: "Atmosphere contradicts itself in impossible ways",
                4: "Reality constantly glitches between multiple paradigms",
                5: "Character experiences multiple paradigm atmospheres simultaneously",
                6: "Paradigm changes based on character's beliefs or actions",
                7: "Different areas of realm follow different paradigms",
                8: "Paradigm randomizes with each obstacle completion",
                9: "All paradigms blend together in chaotic mixture",
                10: "Roll again and combine with another atmosphere table",
            },
        }

        return atmospheres.get(paradigm, {}).get(roll, f"Atmosphere element {roll} for {paradigm}")

    def __str__(self):
        return f"{self.get_paradigm_display()} Atmosphere #{self.atmosphere_number}"
