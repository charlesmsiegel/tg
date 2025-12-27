from characters.models.core.ability_block import Ability
from characters.models.mage.focus import (
    CorruptedPractice,
    Instrument,
    Paradigm,
    Practice,
    SpecializedPractice,
    Tenet,
)
from characters.models.mage.mage import Mage, PracticeRating
from django.contrib.auth.models import User
from django.test import TestCase


class TestPractice(TestCase):
    def test_abilities(self):
        practice = Practice.objects.create(name="Practice 1")
        practice.abilities.add(Ability.objects.create(name="Brawl", property_name="brawl"))
        practice.abilities.add(Ability.objects.create(name="Awareness", property_name="awareness"))
        self.assertEqual(practice.abilities.count(), 2)

    def test_str(self):
        practice = Practice.objects.create(name="Practice 1")
        practice.abilities.add(Ability.objects.order_by("?").first())
        self.assertEqual(str(practice), "Practice 1")


class TestInstrument(TestCase):
    def test_str(self):
        instrument = Instrument.objects.create(name="Instrument 1")
        self.assertEqual(str(instrument), "Instrument 1")


class TestParadigm(TestCase):
    def setUp(self) -> None:
        self.paradigm = Paradigm.objects.create(name="Paradigm 1")
        self.tenet_1 = Tenet.objects.create(name="Tenet 1", tenet_type="per")
        self.tenet_2 = Tenet.objects.create(name="Tenet 2", tenet_type="asc")
        self.tenet_3 = Tenet.objects.create(name="Tenet 3", tenet_type="met")
        self.tenet_4 = Tenet.objects.create(name="Tenet 4", tenet_type="oth")
        self.tenet_5 = Tenet.objects.create(name="Tenet 5", tenet_type="per")
        self.practice_1 = Practice.objects.create(name="Practice 1")
        self.practice_2 = Practice.objects.create(name="Practice 2")
        self.practice_3 = Practice.objects.create(name="Practice 3")
        self.practice_4 = Practice.objects.create(name="Practice 4")

        self.tenet_1.associated_practices.add(self.practice_1)
        self.tenet_1.limited_practices.add(self.practice_2)

        self.tenet_2.associated_practices.add(self.practice_2)
        self.tenet_2.limited_practices.add(self.practice_3)

        self.tenet_3.associated_practices.add(self.practice_3)
        self.tenet_3.limited_practices.add(self.practice_4)
        return super().setUp()

    def test_str(self):
        self.assertEqual(str(self.paradigm), "Paradigm 1")

    def test_get_associated_practices(self):
        self.paradigm.tenets.add(self.tenet_1, self.tenet_2, self.tenet_3)
        associated_practices = self.paradigm.get_associated_practices()

        self.assertQuerySetEqual(
            associated_practices.order_by("id"),
            Practice.objects.filter(id__in=[self.practice_1.id]).order_by("id"),
            transform=lambda x: x,
        )

    def test_get_limited_practices(self):
        self.paradigm.tenets.add(self.tenet_1, self.tenet_2, self.tenet_3)
        limited_practices = self.paradigm.get_limited_practices()

        self.assertQuerySetEqual(
            limited_practices.order_by("id"),
            Practice.objects.filter(id__in=[self.practice_4.id]).order_by("id"),
            transform=lambda x: x,
        )

    def test_get_intersection_practices(self):
        self.paradigm.tenets.add(self.tenet_1, self.tenet_2, self.tenet_3)
        intersection_practices = self.paradigm.get_intersection_practices()

        self.assertQuerySetEqual(
            intersection_practices.order_by("id"),
            Practice.objects.filter(id__in=[self.practice_2.id, self.practice_3.id]).order_by("id"),
            transform=lambda x: x,
        )

    def test_set_tenets(self):
        result = self.paradigm.set_tenets(self.tenet_1, self.tenet_2, self.tenet_3)
        self.assertTrue(result)
        self.assertTrue(
            self.paradigm.tenets.filter(
                id__in=[self.tenet_1.id, self.tenet_2.id, self.tenet_3.id]
            ).exists()
        )

        result_invalid = self.paradigm.set_tenets(self.tenet_1, self.tenet_4, self.tenet_5)
        self.assertFalse(result_invalid)
        self.assertFalse(
            self.paradigm.tenets.filter(id__in=[self.tenet_4.id, self.tenet_5.id]).exists()
        )

    def test_add_tenet(self):
        self.paradigm.add_tenet(self.tenet_1)
        self.assertIn(self.tenet_1, self.paradigm.tenets.all())

    def test_has_tenets(self):
        self.paradigm.tenets.add(self.tenet_1, self.tenet_2, self.tenet_3)
        self.assertTrue(self.paradigm.has_tenets())

        self.paradigm.tenets.clear()
        self.paradigm.tenets.add(self.tenet_1, self.tenet_4)
        self.assertFalse(self.paradigm.has_tenets())


class TestInstrumentDetailView(TestCase):
    def setUp(self) -> None:
        self.instrument = Instrument.objects.create(name="Test Instrument")
        self.url = self.instrument.get_absolute_url()

    def test_effect_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_effect_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/instrument/detail.html")


class TestInstrumentCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Test Instrument",
            "description": "Test",
        }
        self.url = Instrument.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/instrument/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Instrument.objects.count(), 1)
        self.assertEqual(Instrument.objects.first().name, "Test Instrument")


class TestInstrumentUpdateView(TestCase):
    def setUp(self):
        self.instrument = Instrument.objects.create(name="Test Instrument", description="Test")
        self.valid_data = {
            "name": "Test Instrument 2",
            "description": "Test",
        }
        self.url = self.instrument.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/instrument/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.instrument.refresh_from_db()
        self.assertEqual(self.instrument.name, "Test Instrument 2")


class TestPracticeDetailView(TestCase):
    def setUp(self) -> None:
        self.practice = Practice.objects.create(name="Test Practice")
        self.url = self.practice.get_absolute_url()

    def test_effect_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_effect_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/practice/detail.html")


class TestPracticeCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Test Practice",
            "description": "Test",
            "benefit": "Test Benny",
            "penalty": "Test Penny",
        }
        self.url = Practice.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/practice/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Practice.objects.count(), 1)
        self.assertEqual(Practice.objects.first().name, "Test Practice")


class TestPracticeUpdateView(TestCase):
    def setUp(self):
        self.practice = Practice.objects.create(name="Test Practice", description="Test")
        self.valid_data = {
            "name": "Test Practice 2",
            "description": "Test",
            "benefit": "Test Benny",
            "penalty": "Test Penny",
        }
        self.url = self.practice.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/practice/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.practice.refresh_from_db()
        self.assertEqual(self.practice.name, "Test Practice 2")


class TestSpecializedPracticeDetailView(TestCase):
    def setUp(self) -> None:
        self.practice = Practice.objects.create(name="Practice")
        self.specialized_practice = SpecializedPractice.objects.create(
            name="Test SpecializedPractice", parent_practice=self.practice
        )
        self.url = self.specialized_practice.get_absolute_url()

    def test_effect_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_effect_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/specialized_practice/detail.html")


class TestSpecializedPracticeCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Test Specialized Practice",
            "description": "Test",
            "benefit": "Test Benny",
            "penalty": "Test Penny",
            "extra_benefit": "Test Extra",
        }
        self.url = SpecializedPractice.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/specialized_practice/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(SpecializedPractice.objects.count(), 1)
        self.assertEqual(SpecializedPractice.objects.first().name, "Test Specialized Practice")


class TestSpecializedPracticeUpdateView(TestCase):
    def setUp(self):
        self.specialized_practice = SpecializedPractice.objects.create(
            name="Test SpecializedPractice", description="Test"
        )
        self.valid_data = {
            "name": "Test Specialized Practice 2",
            "description": "Test",
            "benefit": "Test Benny",
            "penalty": "Test Penny",
            "extra_benefit": "Test Extra",
        }
        self.url = self.specialized_practice.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/specialized_practice/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.specialized_practice.refresh_from_db()
        self.assertEqual(self.specialized_practice.name, "Test Specialized Practice 2")


class TestCorruptedPracticeDetailView(TestCase):
    def setUp(self) -> None:
        self.corrupted_practice = CorruptedPractice.objects.create(name="Test CorruptedPractice")
        self.url = self.corrupted_practice.get_absolute_url()

    def test_effect_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_effect_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/corrupted_practice/detail.html")


class TestCorruptedPracticeCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Test Corrupted Practice",
            "description": "Test",
            "benefit": "Test Benny",
            "penalty": "Test Penny",
            "extra_benefit": "Test Extra",
            "price": "Test Price",
        }
        self.url = CorruptedPractice.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/corrupted_practice/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CorruptedPractice.objects.count(), 1)
        self.assertEqual(CorruptedPractice.objects.first().name, "Test Corrupted Practice")


class TestCorruptedPracticeUpdateView(TestCase):
    def setUp(self):
        self.corrupted_practice = CorruptedPractice.objects.create(
            name="Test CorruptedPractice", description="Test"
        )
        self.valid_data = {
            "name": "Test Corrupted Practice 2",
            "description": "Test",
            "benefit": "Test Benny",
            "penalty": "Test Penny",
            "extra_benefit": "Test Extra",
            "price": "Test Price",
        }
        self.url = self.corrupted_practice.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/corrupted_practice/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.corrupted_practice.refresh_from_db()
        self.assertEqual(self.corrupted_practice.name, "Test Corrupted Practice 2")


class TestTenetDetailView(TestCase):
    def setUp(self) -> None:
        self.tenet = Tenet.objects.create(name="Test Tenet")
        self.url = self.tenet.get_absolute_url()

    def test_effect_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_effect_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/tenet/detail.html")


class TestTenetCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Test Tenet",
            "description": "Test Description",
            "tenet_type": "asc",
        }
        self.url = Tenet.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/tenet/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Tenet.objects.count(), 1)
        self.assertEqual(Tenet.objects.first().name, "Test Tenet")


class TestTenetUpdateView(TestCase):
    def setUp(self):
        self.tenet = Tenet.objects.create(name="Test Tenet", description="Test")
        self.valid_data = {
            "name": "Test Tenet 2",
            "description": "Test Description",
            "tenet_type": "asc",
        }
        self.url = self.tenet.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/tenet/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.tenet.refresh_from_db()
        self.assertEqual(self.tenet.name, "Test Tenet 2")


class TestParadigmDetailView(TestCase):
    def setUp(self) -> None:
        self.paradigm = Paradigm.objects.create(name="Test Paradigm")
        self.url = self.paradigm.get_absolute_url()

    def test_effect_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_effect_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/paradigm/detail.html")


class TestParadigmCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Test Paradigm",
            "description": "Test description",
        }
        self.url = Paradigm.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/paradigm/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Paradigm.objects.count(), 1)
        self.assertEqual(Paradigm.objects.first().name, "Test Paradigm")


class TestParadigmUpdateView(TestCase):
    def setUp(self):
        self.paradigm = Paradigm.objects.create(name="Test Paradigm", description="Test")
        self.valid_data = {
            "name": "Test Paradigm 2",
            "description": "Test description",
        }
        self.url = self.paradigm.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/paradigm/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.paradigm.refresh_from_db()
        self.assertEqual(self.paradigm.name, "Test Paradigm 2")


class TestGenericCharacterDetailViews(TestCase):
    def setUp(self) -> None:
        self.practice = Practice.objects.create(name="Practice")
        self.purl = self.practice.get_absolute_url()
        self.corruptpractice = CorruptedPractice.objects.create(
            name="CPractice", parent_practice=self.practice
        )
        self.curl = self.corruptpractice.get_absolute_url()
        self.specializedpractice = SpecializedPractice.objects.create(
            name="SPractice", parent_practice=self.practice
        )
        self.surl = self.specializedpractice.get_absolute_url()

    def test_character_detail_view_templates(self):
        response = self.client.get(self.purl)
        self.assertTemplateUsed(response, "characters/mage/practice/detail.html")
        response = self.client.get(self.curl)
        self.assertTemplateUsed(response, "characters/mage/corrupted_practice/detail.html")
        response = self.client.get(self.surl)
        self.assertTemplateUsed(response, "characters/mage/specialized_practice/detail.html")


class TestPracticeRatingTenetBonus(TestCase):
    def setUp(self):
        # Create a user and mage
        self.user = User.objects.create_user(username="testuser")
        self.mage = Mage.objects.create(name="Test Mage", owner=self.user)

        # Create tenets
        self.metaphysical_tenet = Tenet.objects.create(name="Metaphysical Tenet", tenet_type="met")
        self.personal_tenet = Tenet.objects.create(name="Personal Tenet", tenet_type="per")
        self.ascension_tenet = Tenet.objects.create(name="Ascension Tenet", tenet_type="asc")
        self.other_tenet = Tenet.objects.create(name="Other Tenet", tenet_type="oth")

        # Create practices
        self.practice_only_associated = Practice.objects.create(name="Practice Only Associated")
        self.practice_only_limited = Practice.objects.create(name="Practice Only Limited")
        self.practice_both = Practice.objects.create(name="Practice Both")
        self.practice_neither = Practice.objects.create(name="Practice Neither")

        # Set up tenet relationships
        self.metaphysical_tenet.associated_practices.add(self.practice_only_associated)
        self.personal_tenet.limited_practices.add(self.practice_only_limited)
        self.ascension_tenet.associated_practices.add(self.practice_both)
        self.ascension_tenet.limited_practices.add(self.practice_both)

        # Assign tenets to mage
        self.mage.metaphysical_tenet = self.metaphysical_tenet
        self.mage.personal_tenet = self.personal_tenet
        self.mage.ascension_tenet = self.ascension_tenet
        self.mage.save()

    def test_only_associated_practice_bonus(self):
        pr = PracticeRating.objects.create(
            mage=self.mage, practice=self.practice_only_associated, rating=1
        )
        self.assertEqual(pr.get_tenet_bonus(), 1)

    def test_only_limited_practice_penalty(self):
        pr = PracticeRating.objects.create(
            mage=self.mage, practice=self.practice_only_limited, rating=1
        )
        self.assertEqual(pr.get_tenet_bonus(), -1)

    def test_both_associated_and_limited_practice(self):
        pr = PracticeRating.objects.create(mage=self.mage, practice=self.practice_both, rating=1)
        self.assertEqual(pr.get_tenet_bonus(), 0)

    def test_neither_associated_nor_limited_practice(self):
        pr = PracticeRating.objects.create(mage=self.mage, practice=self.practice_neither, rating=1)
        self.assertEqual(pr.get_tenet_bonus(), 0)

    def test_multiple_tenets_same_practice_associated(self):
        # Add the practice to another tenet's associated practices
        self.other_tenet.associated_practices.add(self.practice_only_associated)
        self.mage.other_tenets.add(self.other_tenet)

        pr = PracticeRating.objects.create(
            mage=self.mage, practice=self.practice_only_associated, rating=1
        )
        # Should still be +1 (only associated)
        self.assertEqual(pr.get_tenet_bonus(), 1)

    def test_no_mage_returns_zero(self):
        pr = PracticeRating.objects.create(
            mage=None, practice=self.practice_only_associated, rating=1
        )
        self.assertEqual(pr.get_tenet_bonus(), 0)

    def test_no_practice_returns_zero(self):
        pr = PracticeRating.objects.create(mage=self.mage, practice=None, rating=1)
        self.assertEqual(pr.get_tenet_bonus(), 0)
