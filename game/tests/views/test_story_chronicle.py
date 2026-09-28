"""Stories belong to chronicles (Spread M1): scoping, creation, legacy unassigned stories."""

from django.contrib.auth.models import User
from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.urls import reverse

from characters.models.core.human import Human
from game.forms import StoryEditForm
from game.models import Chronicle, Gameline, STRelationship, Story


class StoryChronicleTestBase(TestCase):
    def setUp(self):
        self.head = User.objects.create_user("story_head", password="pw")
        self.line_st = User.objects.create_user("story_line_st", password="pw")
        self.player = User.objects.create_user("story_player", password="pw")
        self.outsider = User.objects.create_user("story_outsider", password="pw")
        self.staff = User.objects.create_user("story_staff", password="pw", is_staff=True)
        self.chronicle = Chronicle.objects.create(name="Ashes", head_st=self.head)
        self.elsewhere = Chronicle.objects.create(name="Elsewhere")
        STRelationship.objects.create(
            user=self.line_st,
            chronicle=self.chronicle,
            gameline=Gameline.objects.create(name="Mage: the Ascension"),
        )
        Human.objects.create(name="Played", owner=self.player, chronicle=self.chronicle)
        self.ours = Story.objects.create(name="The Moving Streets", chronicle=self.chronicle)
        self.theirs = Story.objects.create(name="Distant Schism", chronicle=self.elsewhere)
        self.legacy = Story.objects.create(name="First Survey")
        self.url = self.chronicle.get_absolute_url()

    def get(self, user, url):
        self.client.force_login(user)
        return self.client.get(url)


class ChronicleStoryScopingTests(StoryChronicleTestBase):
    def test_stories_tab_and_overview_list_only_this_chronicles_stories(self):
        for query in ("?tab=stories", ""):
            with self.subTest(query=query or "overview"):
                response = self.get(self.player, self.url + query)
                self.assertEqual(list(response.context["stories"]), [self.ours])
                self.assertContains(response, "The Moving Streets")
                self.assertNotContains(response, "Distant Schism")

    def test_unassigned_stories_are_for_the_chronicles_managers(self):
        for user in (self.player, self.line_st):
            with self.subTest(user=user.username):
                response = self.get(user, self.url + "?tab=stories")
                self.assertNotContains(response, 'id="unassigned-stories"')
                self.assertNotContains(response, "First Survey")
        self.assertEqual(self.get(self.outsider, self.url + "?tab=stories").status_code, 404)
        response = self.get(self.head, self.url + "?tab=stories")
        self.assertContains(response, 'id="unassigned-stories"')
        self.assertContains(response, "First Survey")
        # Only staff can edit a story, so only staff get the way to assign it.
        update = reverse("game:story:update", kwargs={"pk": self.legacy.pk})
        self.assertNotContains(response, update)
        response = self.get(self.staff, self.url + "?tab=stories")
        self.assertContains(response, f'href="{update}"')
        self.assertNotContains(response, "Distant Schism")

    def test_unassigned_stories_stay_off_the_overview(self):
        response = self.get(self.head, self.url)
        self.assertNotContains(response, "First Survey")

    def test_stories_tab_query_count_does_not_grow(self):
        def count():
            self.client.force_login(self.staff)
            with CaptureQueriesContext(connection) as queries:
                self.assertEqual(self.client.get(self.url + "?tab=stories").status_code, 200)
            return len(queries)

        count()  # warm per-process caches
        few = count()
        for index in range(5):
            Story.objects.create(name=f"Act {index}", chronicle=self.chronicle)
            Story.objects.create(name=f"Old act {index}")
        self.assertEqual(count(), few)


class ChronicleStoryCreateTests(StoryChronicleTestBase):
    def test_new_story_from_the_chronicle_page_belongs_to_it(self):
        self.client.force_login(self.head)
        response = self.client.post(
            reverse("game:chronicle_create_story", kwargs={"pk": self.chronicle.pk}),
            {"name": "Act Two", "chronicle": self.elsewhere.pk},
        )
        self.assertEqual(response.status_code, 302)
        story = Story.objects.get(name="Act Two")
        # The page's chronicle wins; the form has no chronicle field to tamper with.
        self.assertEqual(story.chronicle, self.chronicle)
        response = self.get(self.head, self.url + "?tab=stories")
        self.assertContains(response, "Act Two")

    def test_who_may_create_is_unchanged(self):
        url = reverse("game:chronicle_create_story", kwargs={"pk": self.chronicle.pk})
        for user in (self.line_st, self.player):
            with self.subTest(user=user.username):
                self.client.force_login(user)
                self.assertEqual(self.client.post(url, {"name": "Nope"}).status_code, 403)
        self.assertFalse(Story.objects.filter(name="Nope").exists())


class StoryPagesTests(StoryChronicleTestBase):
    def test_detail_names_the_chronicle_only_to_its_readers(self):
        url = self.ours.get_absolute_url()
        response = self.get(self.player, url)
        self.assertEqual(response.context["story_chronicle"], self.chronicle)
        self.assertContains(response, f'href="{self.url}"')
        response = self.get(self.outsider, url)
        self.assertIsNone(response.context["story_chronicle"])
        self.assertNotContains(response, "Ashes")
        self.assertContains(response, "Another chronicle")
        response = self.get(self.outsider, self.legacy.get_absolute_url())
        self.assertContains(response, "Unassigned")

    def test_list_names_readable_chronicles(self):
        response = self.get(self.player, reverse("game:story:list"))
        rows = {story.name: story.visible_chronicle for story in response.context["object_list"]}
        self.assertEqual(
            rows,
            {"The Moving Streets": self.chronicle, "Distant Schism": None, "First Survey": None},
        )
        self.assertNotContains(response, "Elsewhere")

    def test_staff_assign_a_legacy_story(self):
        self.client.force_login(self.staff)
        url = reverse("game:story:update", kwargs={"pk": self.legacy.pk})
        response = self.client.get(url)
        self.assertContains(response, 'name="chronicle"')
        response = self.client.post(url, {"name": "First Survey", "chronicle": self.chronicle.pk})
        self.assertEqual(response.status_code, 302)
        self.legacy.refresh_from_db()
        self.assertEqual(self.legacy.chronicle, self.chronicle)

    def test_story_edit_permissions_are_unchanged(self):
        # The chronicle's head ST and its scoped STs still may not edit or create
        # stories outside the chronicle page, even with a gameline in the POST.
        update = reverse("game:story:update", kwargs={"pk": self.ours.pk})
        create = reverse("game:story:create")
        for user in (self.head, self.line_st, self.player):
            for url in (update, create):
                with self.subTest(user=user.username, url=url):
                    self.client.force_login(user)
                    self.assertEqual(self.client.get(url).status_code, 403)
                    response = self.client.post(
                        url, {"name": "Renamed", "chronicle": self.chronicle.pk, "gameline": "mta"}
                    )
                    self.assertEqual(response.status_code, 403)
        self.ours.refresh_from_db()
        self.assertEqual(self.ours.name, "The Moving Streets")

    def test_edit_form_offers_staffed_chronicles(self):
        form = StoryEditForm(user=self.staff)
        self.assertEqual(list(form.fields["chronicle"].queryset), [self.chronicle, self.elsewhere])
        form = StoryEditForm(user=self.head)
        self.assertEqual(list(form.fields["chronicle"].queryset), [self.chronicle])
