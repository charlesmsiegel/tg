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


class ParadoxRealm(HorizonRealm):
    """
    A Paradox Realm for Mage 20th Anniversary Edition.

    Paradox realms test mages who have accumulated significant paradox backlash.
    They strip the character of their magick and equipment, leaving only wits to
    overcome trials.
    """
    type = "paradox_realm"

    primary_sphere = models.CharField(
        max_length=20,
        choices=SphereChoices.choices,
        default=SphereChoices.CORRESPONDENCE,
        help_text="The sphere that created the greatest buildup of paradox"
    )

    paradigm = models.CharField(
        max_length=50,
        choices=ParadigmChoices.choices,
        default=ParadigmChoices.ANTIMAGICK,
        help_text="How the paradox realm interprets how reality 'should' be"
    )

    atmosphere_details = models.JSONField(
        default=list,
        blank=True,
        help_text="List of atmosphere attributes rolled for the realm"
    )

    obstacles = models.JSONField(
        default=list,
        blank=True,
        help_text="List of obstacles the character must overcome"
    )

    final_obstacle = models.JSONField(
        default=dict,
        blank=True,
        help_text="The final obstacle that allows escape from the realm"
    )

    class Meta:
        verbose_name = "Paradox Realm"
        verbose_name_plural = "Paradox Realms"

    def get_update_url(self):
        return reverse("locations:mage:update:paradox_realm", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("locations:mage:create:paradox_realm")

    def get_heading(self):
        return "mta_heading"

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
            # Two spheres combined
            sphere1 = cls.random_sphere()
            sphere2 = cls.random_sphere()
            while sphere2 == sphere1:
                sphere2 = cls.random_sphere()
            return f"{sphere1}+{sphere2}"
        else:
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
            # 14-16: Character's paradigm (not implemented in random)
            # 17-19: Antimagick
            # 20: Two paradigms
        }

        if roll in paradigm_map:
            return paradigm_map[roll]
        elif 14 <= roll <= 16:
            # Character's paradigm - default to a random one for now
            return random.choice([p for p in ParadigmChoices.values if p not in [ParadigmChoices.UNSTABLE]])
        elif 17 <= roll <= 19:
            return ParadigmChoices.ANTIMAGICK
        else:  # roll == 20
            # Two paradigms combined
            para1 = cls.random_paradigm()
            para2 = cls.random_paradigm()
            while para2 == para1:
                para2 = cls.random_paradigm()
            return f"{para1}+{para2}"

    @classmethod
    def random_obstacle_count(cls, primary_sphere):
        """
        Roll on Table B3 to determine number of obstacles.
        Returns a dict with 'primary_count' and 'random_count'
        """
        roll = cls.roll_d10()

        if roll == 1:
            return {"primary_count": 0, "random_count": 0}
        elif roll == 2:
            return {"primary_count": 1, "random_count": 0}
        elif roll == 3:
            return {"primary_count": 2, "random_count": 0}
        elif roll == 4:
            return {"primary_count": 3, "random_count": 0}
        elif roll == 5:
            return {"primary_count": cls.roll_d5(), "random_count": 0}
        elif roll == 6:
            return {"primary_count": cls.roll_d5(), "random_count": 1}
        elif roll == 7:
            return {"primary_count": 1, "random_count": 1}
        elif roll == 8:
            return {"primary_count": 1, "random_count": cls.roll_d5()}
        elif roll == 9:
            return {"primary_count": 0, "random_count": cls.roll_d5()}
        else:  # roll == 10
            primary = cls.roll_d5()
            random_count = cls.roll_d5()
            total = primary + random_count
            if total > 6:
                random_count = 6 - primary
            return {"primary_count": primary, "random_count": random_count}

    @classmethod
    def random_final_obstacle(cls):
        """Roll on Table B4 to determine the final obstacle"""
        roll = cls.roll_d10()

        final_obstacles = {
            1: {"type": "give_secret", "name": "Give a Secret"},
            2: {"type": "win_game", "name": "Win a Game"},
            3: {"type": "solve_riddle", "name": "Solve a Riddle"},
            4: {"type": "button", "name": "The Button"},
            5: {"type": "maze", "name": "Standard Maze"},
            6: {"type": "abnormal_maze", "name": "Abnormal Maze"},
            7: {"type": "silver_bullet", "name": "Silver Bullet for the Beast"},
            8: {"type": "guess_name", "name": "Guess My Name"},
            9: {"type": "any", "name": "Any Obstacle", "sphere": cls.random_sphere()},
        }

        if roll in final_obstacles:
            return final_obstacles[roll]
        else:  # roll == 10
            # Roll twice and combine
            obs1 = cls.random_final_obstacle()
            obs2 = cls.random_final_obstacle()
            return {
                "type": "combined",
                "name": "Combined Obstacles",
                "obstacles": [obs1, obs2]
            }

    @classmethod
    def random_atmosphere_detail(cls, paradigm):
        """
        Roll on the appropriate atmosphere table for the paradigm.
        Returns a dict describing the atmosphere element.
        """
        roll = cls.roll_d10()

        # This is a simplified version - you would expand these based on the tables
        # in the guide. For now, return basic structure.
        return {
            "roll": roll,
            "paradigm": paradigm,
            "description": f"Atmosphere detail {roll} for {paradigm}"
        }

    @classmethod
    def random_obstacle(cls, sphere):
        """
        Roll a random obstacle for the given sphere.
        Returns a dict describing the obstacle.
        """
        roll = cls.roll_d10()

        # This is a simplified version - you would expand these based on the obstacle
        # tables in the guide.
        return {
            "sphere": sphere,
            "roll": roll,
            "type": f"obstacle_{roll}",
            "name": f"{sphere.title()} Obstacle {roll}"
        }

    @classmethod
    def generate_random(cls, name="Random Paradox Realm", primary_sphere=None):
        """
        Generate a complete random paradox realm following the guide's procedures.

        Args:
            name: Name for the realm
            primary_sphere: Override the random sphere selection

        Returns:
            A new ParadoxRealm instance (unsaved)
        """
        # Step 1: Select sphere
        if primary_sphere is None:
            primary_sphere = cls.random_sphere()

        # Step 2: Select paradigm
        paradigm = cls.random_paradigm()

        # Step 3: Determine number of obstacles
        obstacle_counts = cls.random_obstacle_count(primary_sphere)

        # Step 4: Roll atmosphere details (2-3 times)
        num_atmosphere_rolls = random.randint(2, 3)
        atmosphere_details = []
        for _ in range(num_atmosphere_rolls):
            atmosphere_details.append(cls.random_atmosphere_detail(paradigm))

        # Step 5: Generate obstacles
        obstacles = []

        # Primary sphere obstacles
        for _ in range(obstacle_counts["primary_count"]):
            obstacles.append(cls.random_obstacle(primary_sphere))

        # Random sphere obstacles
        for _ in range(obstacle_counts["random_count"]):
            random_sphere = cls.random_sphere()
            obstacles.append(cls.random_obstacle(random_sphere))

        # Step 6: Generate final obstacle
        final_obstacle = cls.random_final_obstacle()

        # Create the realm
        realm = cls(
            name=name,
            primary_sphere=primary_sphere.split("+")[0] if "+" in primary_sphere else primary_sphere,
            paradigm=paradigm.split("+")[0] if "+" in paradigm else paradigm,
            atmosphere_details=atmosphere_details,
            obstacles=obstacles,
            final_obstacle=final_obstacle
        )

        return realm

    def __str__(self):
        return f"{self.name} ({self.get_primary_sphere_display()})"
