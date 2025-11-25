import random


def add_dot(character, trait, maximum):
    trait_value = getattr(character, trait, None)
    if trait_value is not None and trait_value < maximum:
        setattr(character, trait, trait_value + 1)
        character.save()
        return True
    return False


def check_floor_ceiling(x, floor, ceiling):
    if x < floor:
        return floor
    if x > ceiling:
        return ceiling
    return x


def weighted_choice(dictionary, floor=0, ceiling=5):
    d = {
        k: check_floor_ceiling(v, floor=floor, ceiling=ceiling)
        for k, v in dictionary.items()
    }
    l = []
    for key, value in d.items():
        for _ in range(value + 1):
            for __ in range(value + 1):
                l.append(key)
    return random.choice(l)


def dice(dicepool, difficulty=6, specialty=False):
    dice_list = [random.randint(1, 10) for _ in range(dicepool)]
    ones = len([x for x in dice_list if x == 1])
    tens = len([x for x in dice_list if x == 10])
    successes = len([x for x in dice_list if x >= difficulty])
    total = successes - ones
    if successes == 0:
        return dice_list, total
    if specialty:
        total += tens
    return dice_list, max([total, 0])


def compute_level(x, level=0):
    if x.parent is None:
        return level
    return compute_level(x.parent, level=level + 1)


def level_name(x):
    return (compute_level(x) * "&emsp;&emsp;") + x.name


def tree_sort(x, l=None):
    if l is None:
        l = []
    l.append(x)
    for y in x.children.order_by("name"):
        tree_sort(y, l=l)
    return l


def filepath(instance, filename):
    s = str(instance.__class__).split(" ")[-1][:-1][1:-1]
    s = "/".join([x for x in s.split(".") if x != "models"])
    s += "/" + instance.name
    s += "." + filename.split(".")[-1]
    s = s.lower().replace(" ", "_")
    return s


def get_gameline_name(s):
    """
    Get the full name of a gameline from its code.

    Args:
        s: Gameline code (e.g., 'vtm', 'wta')

    Returns:
        Full gameline name (e.g., 'Vampire: the Masquerade')
    """
    from django.conf import settings

    return settings.GAMELINES.get(s, {}).get("name", s)


def get_short_gameline_name(s):
    """
    Get the short app name of a gameline from its code.

    Args:
        s: Gameline code (e.g., 'vtm', 'wta')

    Returns:
        App name (e.g., 'vampire', 'werewolf')
    """
    from django.conf import settings

    return settings.GAMELINES.get(s, {}).get("app_name", "")


def fast_selector(cls):
    max_value = cls.objects.last().id
    index = random.randint(1, max_value)
    while not cls.objects.filter(pk=index).exists():
        index = random.randint(1, max_value)
    return cls.objects.get(pk=index)


def display_queryset(prop):
    return "<br>".join([f'<a href="{x.get_absolute_url()}">{x}</a>' for x in prop])


class CharacterOrganizationRegistry:
    """
    Registry for managing character organizational cleanup handlers.

    Each model with organizational relationships to characters can register
    a cleanup handler that will be called when a character is retired or deceased.
    This decouples the Character model from knowing about all organizational structures.
    """

    _handlers = []

    @classmethod
    def register(cls, handler):
        """
        Register a cleanup handler function.

        Args:
            handler: A callable that takes a character instance and removes
                    it from organizational structures. Should handle its own
                    exceptions gracefully.
        """
        if handler not in cls._handlers:
            cls._handlers.append(handler)

    @classmethod
    def cleanup_character(cls, character):
        """
        Execute all registered cleanup handlers for a character.

        Args:
            character: The Character instance being retired or deceased
        """
        for handler in cls._handlers:
            try:
                handler(character)
            except Exception as e:
                # Log but don't fail if one handler has an issue
                import logging
                logger = logging.getLogger(__name__)
                logger.error(
                    f"Error in organization cleanup handler {handler.__name__} "
                    f"for character {character.id}: {e}"
                )
