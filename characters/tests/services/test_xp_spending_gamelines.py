"""The XP spending service works for every gameline whose model overrides ``spend_xp``."""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.models.changeling.changeling import Changeling
from characters.models.core.attribute_block import Attribute
from characters.models.demon.demon import Demon
from characters.models.demon.thrall import Thrall
from characters.models.hunter.hunter import Hunter
from characters.models.vampire.vampire import Vampire
from characters.models.werewolf.garou import Werewolf
from characters.models.wraith.wraith import Wraith
from characters.services.xp_spending import XPSpendingServiceFactory


class GamelineAttributeXPSpendTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="player")
        self.strength, _ = Attribute.objects.get_or_create(
            name="Strength", property_name="strength"
        )

    def spend_attribute(self, model):
        character = model.objects.create(name=f"Test {model.__name__}", owner=self.user, xp=50)
        service = XPSpendingServiceFactory.get_service(character)
        return service.spend("Attribute", self.strength)

    def test_attribute_spend_for_each_gameline(self):
        for model in (Vampire, Werewolf, Wraith, Changeling, Demon, Thrall, Hunter):
            with self.subTest(model=model.__name__):
                result = self.spend_attribute(model)
                self.assertTrue(result.success, result.error)
