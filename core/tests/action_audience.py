"""The audience every action endpoint is tested against (Step 5).

owner, another player, an ST of this chronicle and gameline, an ST of this
chronicle but another gameline, an ST of another chronicle, staff, anonymous.
"""

from django.conf import settings
from django.contrib.auth import get_user_model

from game.models import Chronicle, Gameline, STRelationship

AUDIENCE = ("owner", "player", "st", "other_line_st", "other_chronicle_st", "staff", "anonymous")


class ActionAudienceMixin:
    """Creates the audience in ``setUp``; subclasses set ``gameline_code``."""

    gameline_code = "wod"

    def setUp(self):
        super().setUp()
        users = get_user_model()
        self.chronicle = Chronicle.objects.create(name="Action chronicle")
        self.other_chronicle = Chronicle.objects.create(name="Other chronicle")
        line = Gameline.objects.create(name=settings.GAMELINES[self.gameline_code]["name"])
        other_code = "vtm" if self.gameline_code != "vtm" else "wta"
        other_line = Gameline.objects.create(name=settings.GAMELINES[other_code]["name"])
        self.users = {
            "owner": users.objects.create_user("action_owner"),
            "player": users.objects.create_user("action_player"),
            "st": users.objects.create_user("action_st"),
            "other_line_st": users.objects.create_user("action_other_line_st"),
            "other_chronicle_st": users.objects.create_user("action_other_chronicle_st"),
            "staff": users.objects.create_user("action_staff", is_staff=True),
            "anonymous": None,
        }
        STRelationship.objects.create(
            user=self.users["st"], chronicle=self.chronicle, gameline=line
        )
        STRelationship.objects.create(
            user=self.users["other_line_st"], chronicle=self.chronicle, gameline=other_line
        )
        STRelationship.objects.create(
            user=self.users["other_chronicle_st"], chronicle=self.other_chronicle, gameline=line
        )

    def login_as(self, who):
        self.client.logout()
        if self.users[who] is not None:
            self.client.force_login(self.users[who])
