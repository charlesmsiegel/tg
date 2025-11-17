import re
from datetime import datetime, timedelta

from core.utils import dice
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Max, OuterRef, Subquery
from django.urls import reverse
from django.utils.timezone import (  # ensure timezone-aware now if using TIME_ZONE settings
    now,
)


class ObjectType(models.Model):
    name = models.CharField(max_length=100, default="")
    type = models.CharField(
        default="",
        max_length=100,
        choices=[
            ("char", "Character"),
            ("loc", "Location"),
            ("obj", "Item"),
        ],
    )
    gameline = models.CharField(
        default="",
        max_length=100,
        choices=[
            ("wod", "World of Darkness"),
            ("vtm", "Vampire: the Masquerade"),
            ("wta", "Werewolf: the Apocalypse"),
            ("mta", "Mage: the Ascension"),
            ("wto", "Wraith: the Oblivion"),
            ("ctd", "Changeling: the Dreaming"),
            ("dtf", "Demon: the Fallen"),
        ],
    )

    class Meta:
        verbose_name = "Object Type"
        verbose_name_plural = "Object Types"
        ordering = ["type", "gameline", "name"]

    def __str__(self):
        return (
            self.get_gameline_display()
            + "/"
            + self.get_type_display()
            + "/"
            + self.name
        )


class SettingElement(models.Model):
    name = models.CharField(max_length=100, default="")
    description = models.TextField(default="")

    def __str__(self):
        return self.name


class Gameline(models.Model):
    name = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name


class Chronicle(models.Model):
    name = models.CharField(max_length=100, default="")
    storytellers = models.ManyToManyField(User, blank=True, through="STRelationship")
    theme = models.CharField(max_length=200, default="")
    mood = models.CharField(max_length=200, default="")
    common_knowledge_elements = models.ManyToManyField(SettingElement, blank=True)
    year = models.IntegerField(default=2022)

    headings = models.CharField(
        default="",
        max_length=100,
        choices=[
            ("vtm_heading", "Vampire: the Masquerade"),
            ("wta_heading", "Werewolf: the Apocalypse"),
            ("mta_heading", "Mage: the Ascension"),
            ("ctd_heading", "Changeling: the Dreaming"),
            ("wto_heading", "Wraith: the Oblivion"),
            ("dtf_heading", "Demon: the Fallen"),
            ("wod_heading", "World of Darkness"),
        ],
    )

    allowed_objects = models.ManyToManyField(ObjectType, blank=True)

    class Meta:
        verbose_name = "Chronicle"
        verbose_name_plural = "Chronicles"

    def __str__(self):
        return self.name

    def get_scenes(self):
        return Scene.objects.filter(chronicle=self)

    def get_active_scenes(self):
        return Scene.objects.filter(chronicle=self, finished=False)

    def get_absolute_url(self):
        return reverse("game:chronicle", kwargs={"pk": self.pk})

    def get_deceased_character_url(self):
        return reverse("game:deceased", kwargs={"pk": self.pk})

    def get_retired_character_url(self):
        return reverse("game:retired", kwargs={"pk": self.pk})

    def get_npc_url(self):
        return reverse("game:npc", kwargs={"pk": self.pk})

    def storyteller_list(self):
        return ", ".join([x.username for x in self.storytellers.all()])

    def get_scenes_url(self):
        return reverse("game:chronicle_scenes", kwargs={"pk": self.pk})

    def add_setting_element(self, name, description):
        se = SettingElement.objects.get_or_create(name=name, description=description)[0]
        self.common_knowledge_elements.add(se)

    def total_scenes(self):
        return Scene.objects.filter(chronicle=self).count()

    def add_scene(self, name, location, date_of_scene=None):
        if isinstance(location, str):
            from locations.models import LocationModel

            location = LocationModel.objects.get(name=location)
        if Scene.objects.filter(name=name, chronicle=self, location=location).exists():
            return Scene.objects.filter(
                name=name, chronicle=self, location=location
            ).first()
        s = Scene.objects.create(
            name=name,
            chronicle=self,
            location=location,
            date_of_scene=date_of_scene,
        )
        self.save()
        return s


class STRelationship(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    chronicle = models.ForeignKey(Chronicle, on_delete=models.SET_NULL, null=True)
    gameline = models.ForeignKey(Gameline, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ["gameline__id"]


class Story(models.Model):
    name = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("game:story:detail", kwargs={"pk": self.pk})


class Week(models.Model):
    end_date = models.DateField()
    characters = models.ManyToManyField("characters.CharacterModel", blank=True)

    class Meta:
        ordering = ["-end_date"]

    @property
    def start_date(self):
        return self.end_date - timedelta(days=7)

    def __str__(self):
        return f"{self.start_date } - { self.end_date }"

    def finished_scenes(self):
        # Subquery to get the most recent datetime_created for each Scene
        recent_post_subquery = (
            Post.objects.filter(scene=OuterRef("pk"))
            .values("scene")
            .annotate(latest_dt=Max("datetime_created"))
            .values("latest_dt")
        )

        # Annotate each Scene with latest_post_date (datetime)
        # and then filter by conditions:
        # 1) Scene is finished
        # 2) The date portion of latest_post_date is between start_date and end_date
        return Scene.objects.annotate(
            latest_post_date=Subquery(recent_post_subquery)
        ).filter(
            finished=True,
            latest_post_date__date__gte=self.start_date,
            latest_post_date__date__lte=self.end_date,
        )

    def weekly_characters(self):
        """Get all characters who participated in scenes this week.

        Optimized to avoid N+1 query issues.
        """
        from characters.models.core.human import Human

        scene_ids = self.finished_scenes().values_list("id", flat=True)
        return (
            Human.objects.filter(scenes__id__in=scene_ids, npc=False)
            .distinct()
            .order_by("name")
        )


class Scene(models.Model):
    name = models.CharField(max_length=100, default="")
    chronicle = models.ForeignKey(
        "game.Chronicle", on_delete=models.SET_NULL, null=True
    )
    date_played = models.DateField(auto_now_add=True)
    characters = models.ManyToManyField(
        "characters.CharacterModel", related_name="scenes", blank=True
    )
    location = models.ForeignKey(
        "locations.LocationModel", on_delete=models.SET_NULL, null=True
    )
    user_read_status = models.ManyToManyField(
        User, blank=True, through="UserSceneReadStatus"
    )
    finished = models.BooleanField(default=False)
    xp_given = models.BooleanField(default=False)
    waiting_for_st = models.BooleanField(default=False)
    st_message = models.CharField(max_length=300, default="")
    date_of_scene = models.DateField(default=now, null=True, blank=True)

    class Meta:
        verbose_name = "Scene"
        verbose_name_plural = "Scenes"
        ordering = ["-date_of_scene", "-date_played"]

    def __str__(self):
        if self.name not in ["", "''"]:
            return self.name
        return str(self.location) + " " + str(self.date)

    def get_absolute_url(self):
        return reverse("game:scene", kwargs={"pk": self.pk})

    def close(self):
        self.finished = True
        latest_post = (
            Post.objects.filter(scene=self).order_by("-datetime_created").first()
        )
        if latest_post is None:
            from_date = datetime.date.today()
        else:
            from_date = latest_post.datetime_created.date()

        sunday_date = get_next_sunday(from_date)

        week, created = Week.objects.get_or_create(end_date=sunday_date)
        week.characters.add(*self.characters.all())

        self.save()

    def total_characters(self):
        return self.characters.count()

    def add_character(self, character):
        if isinstance(character, str):
            from characters.models.core import CharacterModel

            character = CharacterModel.objects.get(name=character)
        self.characters.add(character)
        return character

    def total_posts(self):
        return Post.objects.filter(scene=self).count()

    def add_post(self, character, display, message):
        if character not in self.characters.all():
            self.add_character(character)
        if display == "":
            display = character.name
        if message.lower().startswith("@storyteller"):
            self.waiting_for_st = True
            self.st_message = message[len("@storyteller ") :]
            self.save()
            return None
        if self.waiting_for_st and character.owner.profile.is_st():
            self.waiting_for_st = False
            self.save()
        try:
            message = message_processing(character, message)
        except ValueError:
            return
        post = Post.objects.create(
            character=character, message=message, display_name=display, scene=self
        )
        for user in User.objects.filter(charactermodel__scenes=self).distinct():
            if user != character.owner:
                status = UserSceneReadStatus.objects.get_or_create(
                    user=user, scene=self
                )[0]
                status.read = False
                status.save()
            else:
                status = UserSceneReadStatus.objects.get_or_create(
                    user=user, scene=self
                )[0]
                status.read = True
                status.save()
        return post

    def most_recent_post(self):
        return Post.objects.filter(scene=self).order_by("-datetime_created").first()

    def award_xp(self, character_awards):
        """Award XP to characters based on dict of {character: bool}.

        Args:
            character_awards: Dict mapping Character objects to bool indicating
                             whether they should receive XP.
        """
        self.xp_given = True
        for char, should_award in character_awards.items():
            if should_award:
                char.add_xp(1)
        self.save()


class UserSceneReadStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    scene = models.ForeignKey(Scene, on_delete=models.SET_NULL, null=True)
    read = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user}-{self.scene}: {self.read}"


class Post(models.Model):
    character = models.ForeignKey(
        "characters.CharacterModel", on_delete=models.SET_NULL, null=True
    )
    display_name = models.CharField(max_length=100)
    scene = models.ForeignKey("game.Scene", on_delete=models.SET_NULL, null=True)
    message = models.TextField(default="")
    datetime_created = models.DateTimeField(default=now, db_index=True)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        indexes = [
            models.Index(fields=["-datetime_created"]),
            models.Index(fields=["scene", "-datetime_created"]),
        ]

    def __str__(self):
        if self.display_name:
            return self.display_name + ": " + self.message
        return self.character.name + ": " + self.message


class JournalEntry(models.Model):
    journal = models.ForeignKey("Journal", on_delete=models.SET_NULL, null=True)
    message = models.TextField(default="")
    st_message = models.TextField(default="")
    date = models.DateTimeField(db_index=True)
    datetime_created = models.DateTimeField(default=now, db_index=True)

    class Meta:
        ordering = ["-date", "datetime_created"]
        indexes = [
            models.Index(fields=["journal", "-date"]),
        ]


class Journal(models.Model):
    character = models.OneToOneField(
        "characters.CharacterModel", on_delete=models.CASCADE
    )

    def add_post(self, date, message):
        try:
            message = message_processing(self.character, message)
        except ValueError:
            return
        je = JournalEntry.objects.create(journal=self, message=message, date=date)
        return je

    def get_absolute_url(self):
        return reverse("game:journal", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.character.name}'s Journal"

    def all_entries(self):
        return JournalEntry.objects.filter(journal=self)


def message_processing(character, message):
    temporary_point_regex = re.compile(
        r"#WP(-?\d+)|#WP|#Q(-?\d+)|#P(-?\d+)|#(-?\d+)(B|L|A)"
    )
    wp_spend = False
    expenditures = []

    for match in temporary_point_regex.finditer(message):
        full_match = match.group(0)
        if match.group(1):
            wp_amount = int(match.group(1))
            character.temporary_willpower -= wp_amount
            expenditures.append(f"{wp_amount}WP")
            character.save()
        elif full_match == "#WP":
            character.temporary_willpower -= 1
            wp_spend = True
            expenditures.append("WP")
            character.save()
        elif match.group(2):
            if hasattr(character, "quintessence"):
                character.quintessence -= int(match.group(2))
                expenditures.append(f"{int(match.group(2))}Q")
                character.save()
        elif match.group(3):
            if hasattr(character, "paradox"):
                character.paradox += int(match.group(3))
                expenditures.append(f"{int(match.group(3))}P")
                character.save()
        elif match.group(4):
            damage_type = match.group(5)
            damage_amount = int(match.group(4))
            expenditures.append(f"{damage_amount}{damage_type}")
            if damage_type == "B":
                for _ in range(damage_amount):
                    character.add_bashing()
            if damage_type == "L":
                for _ in range(damage_amount):
                    character.add_lethal()
            if damage_type == "A":
                for _ in range(damage_amount):
                    character.add_aggravated()
            character.save()

    expenditures = ", ".join(["#" + x for x in expenditures])
    if "/rolls" in message:
        text, roll = message.split("/rolls")
        text = text.strip()
        roll = roll.strip()
        if match := re.match(
            r"^(?P<num_rolls>\d+)\s+rolls\s+@\s+(?P<num_dice>\d+)(?:\s+difficulty\s+(?P<difficulty>\d+))?(?:\s+(?P<specialty>\S+))?",
            roll,
            re.IGNORECASE,
        ):
            num_rolls = int(match.group("num_rolls"))
            num_dice = int(match.group("num_dice"))
            difficulty = (
                int(match.group("difficulty")) if match.group("difficulty") else 6
            )
            specialty_str = match.group("specialty")
            specialty = specialty_str.lower() == "true" if specialty_str else False
            r = rolls(
                num_rolls,
                num_dice,
                difficulty=difficulty,
                specialty=specialty,
            )
            roll_description = (
                f"{num_rolls} rolls of {num_dice} dice at difficulty {difficulty}"
            )
            if specialty:
                roll_description += " with relevant specialty"
            m = ""
            if text:
                m += text + ": "
            if expenditures:
                m += expenditures + ": "
            m += roll_description + ": " + r
            message = m
        else:
            raise ValueError("Command does not match the expected format.")
    elif "/roll" in message:
        text, roll = message.split("/roll")
        text = text.strip()
        roll = roll.strip()
        # Full Pattern
        if match := re.match(
            r"^(?P<num_dice>\d+)(?:\s+difficulty\s+(?P<difficulty>\d+))?(?:\s+(?P<specialty>\S+))?",
            roll,
            re.IGNORECASE,
        ):
            num_dice = int(match.group("num_dice"))
            difficulty = (
                int(match.group("difficulty")) if match.group("difficulty") else 6
            )
            specialty_str = match.group("specialty")
            specialty = specialty_str.lower() == "true" if specialty_str else False
            r = roll_once(
                num_dice,
                difficulty=difficulty,
                specialty=specialty,
                willpower=wp_spend,
            )
            roll_description = f"roll of {num_dice} dice at difficulty {difficulty}"
            if specialty:
                roll_description += " with relevant specialty"
            m = ""
            if text:
                m += text + ": "
            if expenditures:
                m += expenditures + ": "
            m += roll_description + ": " + r
            message = m
        else:
            raise ValueError("Command does not match the expected format.")
    return message


def roll_once(number_of_dice, difficulty=6, specialty=False, willpower=False):
    roll, success_count = dice(
        number_of_dice, difficulty=difficulty, specialty=specialty
    )
    if willpower:
        success_count += 1
        if success_count < 0:
            success_count = 0
    roll = ", ".join(map(str, roll))
    return f"{roll}: <b>{success_count}</b>"


def rolls(num_rolls, num_dice, difficulty, specialty):
    roll_list = []
    successes = []
    difficulties = []
    for _ in range(num_rolls):
        difficulties.append(difficulty)
        roll, success_count = dice(num_dice, difficulty=difficulty, specialty=specialty)
        roll = ", ".join(map(str, roll))
        roll_list.append(roll)
        successes.append(success_count)
        if success_count == 0:
            difficulty += 1
        if success_count < 0:
            break
    join_list = []
    for roll, suxx, diff in zip(roll_list, successes, difficulties):
        join_list.append(f"{roll}: <b>{suxx}</b>")
        if suxx == 0:
            join_list[-1] = join_list[-1] + f": difficulty increased to {diff + 1}"
    return "Rolls:<br>" + f"<br>".join(join_list)


class WeeklyXPRequest(models.Model):
    week = models.ForeignKey(Week, on_delete=models.SET_NULL, null=True)
    character = models.ForeignKey(
        "characters.CharacterModel", on_delete=models.SET_NULL, null=True
    )
    finishing = models.BooleanField(default=True)
    learning = models.BooleanField(default=False)
    rp = models.BooleanField(default=False)
    focus = models.BooleanField(default=False)
    standingout = models.BooleanField(default=False)
    learning_scene = models.ForeignKey(
        Scene, on_delete=models.SET_NULL, null=True, related_name="learning_requests"
    )
    rp_scene = models.ForeignKey(
        Scene, on_delete=models.SET_NULL, null=True, related_name="rp_requests"
    )
    focus_scene = models.ForeignKey(
        Scene, on_delete=models.SET_NULL, null=True, related_name="focus_requests"
    )
    standingout_scene = models.ForeignKey(
        Scene, on_delete=models.SET_NULL, null=True, related_name="standingout_requests"
    )
    approved = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=["character", "week"]),
            models.Index(fields=["approved"]),
        ]

    def __str__(self):
        return f"{self.character.name} request for {self.week}"

    def clean(self):
        """Validate that scenes are provided when XP is claimed for those categories."""
        super().clean()
        errors = {}
        if self.learning and not self.learning_scene:
            errors[
                "learning_scene"
            ] = "Learning scene required when learning XP is claimed"
        if self.rp and not self.rp_scene:
            errors["rp_scene"] = "RP scene required when RP XP is claimed"
        if self.focus and not self.focus_scene:
            errors["focus_scene"] = "Focus scene required when focus XP is claimed"
        if self.standingout and not self.standingout_scene:
            errors[
                "standingout_scene"
            ] = "Standing out scene required when standing out XP is claimed"
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """Ensure validation runs on save."""
        self.full_clean()
        super().save(*args, **kwargs)

    def total_xp(self):
        """Calculate total XP for this request."""
        return sum(
            [self.finishing, self.learning, self.rp, self.focus, self.standingout]
        )


class StoryXPRequest(models.Model):
    story = models.ForeignKey(Story, on_delete=models.SET_NULL, null=True)
    character = models.ForeignKey(
        "characters.CharacterModel", on_delete=models.SET_NULL, null=True
    )
    success = models.BooleanField(default=False)
    danger = models.BooleanField(default=False)
    growth = models.BooleanField(default=False)
    drama = models.BooleanField(default=False)
    duration = models.IntegerField(default=0)


def get_next_sunday(from_date):
    """
    Given a date, returns a date object representing the upcoming Sunday
    (including the given date if it's already a Sunday).
    """
    # weekday(): Monday=0, Sunday=6
    offset = (6 - from_date.weekday()) % 7
    return from_date + timedelta(days=offset)
