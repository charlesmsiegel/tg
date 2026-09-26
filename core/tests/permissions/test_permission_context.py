"""Permission snapshots, request isolation, SQL parity and bounded row costs."""

from types import SimpleNamespace

from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase

from characters.models.core import Character
from characters.models.core.human import Human
from core.models import Observer
from core.permissions import Permission, PermissionManager
from game.models import Chronicle, Gameline, STRelationship
from items.models.core import ItemModel
from locations.models.core import LocationModel


class PermissionContextTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user("context_owner")
        cls.reader = User.objects.create_user("context_reader")
        cls.editor = User.objects.create_user("context_editor")
        cls.stranger = User.objects.create_user("context_stranger")
        cls.chronicle = Chronicle.objects.create(name="Context")
        cls.wod = Gameline.objects.create(name="World of Darkness")
        cls.vtm = Gameline.objects.create(name="Vampire: the Masquerade")
        for user, gameline in ((cls.editor, cls.wod), (cls.reader, cls.vtm)):
            STRelationship.objects.create(user=user, gameline=gameline, chronicle=cls.chronicle)
        cls.character = Human.objects.create(
            name="Subject", owner=cls.owner, chronicle=cls.chronicle
        )

    def request(self, user=None):
        request = RequestFactory().get("/")
        request.user = user or self.owner
        return request

    def test_repeated_permissions_have_no_queries(self):
        request = self.request()
        PermissionManager.user_has_permission(
            self.owner, self.character, Permission.VIEW_FULL, request=request
        )
        with self.assertNumQueries(0):
            for permission in Permission:
                PermissionManager.user_has_permission(
                    self.owner, self.character, permission, request=request
                )

    def test_live_owner_and_status_changes_do_not_retain_grants(self):
        request = self.request()
        self.assertTrue(
            PermissionManager.user_has_permission(
                self.owner, self.character, Permission.EDIT_FULL, request=request
            )
        )
        self.character.status = "App"
        self.assertFalse(
            PermissionManager.user_has_permission(
                self.owner, self.character, Permission.EDIT_FULL, request=request
            )
        )
        self.character.owner = self.stranger
        self.assertFalse(
            PermissionManager.user_has_permission(
                self.owner, self.character, Permission.VIEW_FULL, request=request
            )
        )

    def test_revocation_and_request_isolation(self):
        request = self.request(self.editor)
        self.assertTrue(
            PermissionManager.user_has_permission(
                self.editor, self.character, Permission.APPROVE, request=request
            )
        )
        STRelationship.objects.filter(user=self.editor).delete()
        PermissionManager.invalidate_request_cache(request)
        self.assertFalse(
            PermissionManager.user_has_permission(
                self.editor, self.character, Permission.APPROVE, request=request
            )
        )
        self.assertFalse(
            PermissionManager.user_has_permission(
                self.editor, self.character, Permission.APPROVE, request=self.request(self.editor)
            )
        )
        self.assertFalse(
            PermissionManager.user_has_permission(
                self.stranger, self.character, Permission.VIEW_FULL, request=request
            )
        )

    def test_snapshot_and_page_query_budget(self):
        from core.permission_context import get_object_permissions, prepare_permission_objects

        objects = [
            Human.objects.create(name=f"Row {i}", owner=self.owner, chronicle=self.chronicle)
            for i in range(20)
        ]
        for size in (1, 20):
            request = self.request(self.reader)
            with self.assertNumQueries(5):
                prepare_permission_objects(request, objects[:size])
            with self.assertNumQueries(0):
                for obj in objects[:size]:
                    perms = get_object_permissions(request, obj)
                    self.assertTrue(perms.can_view_full)
                    self.assertFalse(perms.can_approve)
                    self.assertFalse(perms.can_edit)
                    self.assertTrue(perms.is_chronicle_st)

    def test_snapshot_status_and_unsaved_identity(self):
        from core.permission_context import get_object_permissions

        request = self.request()
        self.assertTrue(get_object_permissions(request, self.character).can_chargen)
        self.character.status = "App"
        self.assertFalse(get_object_permissions(request, self.character).can_chargen)
        self.assertTrue(get_object_permissions(request, self.character).can_spend_xp)
        a, b = Human(owner=self.owner), Human(owner=self.stranger)
        self.assertTrue(get_object_permissions(request, a).can_edit)
        self.assertFalse(get_object_permissions(request, b).can_edit)

    def test_polymorphic_observer_filter_matches_object(self):
        Observer.objects.create(
            content_object=self.character, user=self.stranger, granted_by=self.owner
        )
        self.assertTrue(
            PermissionManager.user_has_permission(
                self.stranger, self.character, Permission.VIEW_PARTIAL
            )
        )
        visible = PermissionManager.filter_queryset_for_user(self.stranger, Character.objects.all())
        self.assertIn(self.character.pk, visible.values_list("pk", flat=True))

    def test_no_roles_filter_is_empty(self):
        self.assertFalse(
            PermissionManager.filter_queryset_for_user(
                self.stranger, Chronicle.objects.all()
            ).exists()
        )

    def test_role_status_visibility_matrix(self):
        staff = User.objects.create_user("context_staff", is_staff=True)
        head = User.objects.create_user("context_head")
        game_st = User.objects.create_user("context_game")
        self.chronicle.head_st = head
        self.chronicle.save()
        self.chronicle.game_storytellers.add(game_st)
        for model in (Human, ItemModel, LocationModel):
            objects = [
                model.objects.create(
                    name=f"Matrix {status} {visibility}",
                    status=status,
                    visibility=visibility,
                    owner=self.owner,
                    chronicle=self.chronicle,
                )
                for status in ("Un", "Rev", "Sub", "App", "Ret", "Dec")
                for visibility in ("PUB", "PRI", "CHR", "CUS")
            ]
            objects.append(model.objects.create(name="Shared", owner=None))
            Observer.objects.create(
                content_object=objects[0], user=self.stranger, granted_by=self.owner
            )
            for user in (
                self.owner,
                self.reader,
                self.editor,
                self.stranger,
                staff,
                head,
                game_st,
                AnonymousUser(),
            ):
                request = self.request(user)
                expected = {
                    obj.pk
                    for obj in objects
                    if PermissionManager.user_has_permission(
                        user, obj, Permission.VIEW_FULL, request=request
                    )
                    or PermissionManager.user_has_permission(
                        user, obj, Permission.VIEW_PARTIAL, request=request
                    )
                }
                queryset = model.objects.filter(pk__in=[obj.pk for obj in objects])
                actual = set(
                    PermissionManager.filter_queryset_for_user(user, queryset).values_list(
                        "pk", flat=True
                    )
                )
                with self.subTest(model=model.__name__, user=str(user)):
                    self.assertEqual(actual, expected)

    def test_middleware_adds_snapshot_without_shadowing_django_perms(self):
        from django.template.response import TemplateResponse

        from core.middleware.authorization import AuthorizationMiddleware

        request = self.request()
        django_perms = object()
        response = TemplateResponse(
            request, "unused.html", {"object": self.character, "perms": django_perms}
        )
        AuthorizationMiddleware(lambda r: response).process_template_response(request, response)
        self.assertTrue(response.context_data["object_perms"].can_chargen)
        self.assertIs(response.context_data["perms"], django_perms)
        public_response = TemplateResponse(
            request, "unused.html", {"public_object": {"name": "Public"}}
        )
        AuthorizationMiddleware(lambda r: public_response).process_template_response(
            request, public_response
        )
        self.assertNotIn("object_perms", public_response.context_data)

    def test_shared_chargen_template_gates_fields_and_submit_by_capability(self):
        from pathlib import Path

        from django.template import Context, Engine

        from core.permission_context import get_object_permissions

        source = Path("characters/templates/characters/core/chargen.html").read_text(
            encoding="utf-8"
        )
        engine = Engine(
            loaders=[
                (
                    "django.template.loaders.locmem.Loader",
                    {
                        "core/form.html": (
                            "{% block contents %}{% endblock %}"
                            "{% block buttons %}SUBMIT_BUTTON{% endblock %}"
                        ),
                        "step.html": "STEP_FIELDS",
                        "characters/core/character/not_owner.html": "ACCESS_DENIED",
                    },
                )
            ]
        )
        template = engine.from_string(source)
        for user, allowed in ((self.owner, True), (self.editor, True), (self.reader, False)):
            for key, approved in (("attributes", False), ("freebies", False), ("freebies", True)):
                with self.subTest(user=user.username, step=key, approved=approved):
                    self.character.freebies_approved = approved
                    html = template.render(
                        Context(
                            {
                                "object": self.character,
                                "object_perms": get_object_permissions(
                                    self.request(user), self.character
                                ),
                                "step": SimpleNamespace(key=key, template="step.html"),
                            }
                        )
                    )
                    self.assertEqual("STEP_FIELDS" in html, allowed)
                    self.assertEqual("ACCESS_DENIED" in html, not allowed)
                    self.assertEqual(
                        "SUBMIT_BUTTON" in html, allowed and (key != "freebies" or approved)
                    )

    def test_templates_retire_ambiguous_flag(self):
        from pathlib import Path

        from django.conf import settings

        for app in ("core", "characters", "items", "locations", "game"):
            for path in (Path(settings.BASE_DIR) / app / "templates").rglob("*.html"):
                self.assertNotIn("is_approved_user", path.read_text(encoding="utf-8"), str(path))

    def test_approval_template_uses_scoped_capability(self):
        # Render the actual approval template with a minimal base; unrelated
        # navigation and database-driven context processors are outside this test.
        from pathlib import Path

        from django.template import Context, Engine

        from core.permission_context import get_object_permissions

        source = Path("game/templates/game/xp_spending_request/detail.html").read_text(
            encoding="utf-8"
        )
        engine = Engine(
            loaders=[
                (
                    "django.template.loaders.locmem.Loader",
                    {"core/base.html": "{% block content %}{% endblock %}", "detail.html": source},
                )
            ]
        )
        record = SimpleNamespace(pk=1, character=self.character, approved="Pending")
        for user, expected in ((self.owner, False), (self.reader, False), (self.editor, True)):
            request = self.request(user)
            output = engine.get_template("detail.html").render(
                Context(
                    {
                        "object": record,
                        "user": user,
                        "object_perms": get_object_permissions(request, self.character),
                        "approval_form": SimpleNamespace(approved="APPROVAL_FORM"),
                    }
                )
            )
            self.assertEqual("APPROVAL_FORM" in output, expected)

    def test_base_subject_status_changes_stay_live(self):
        from characters.models.core import CharacterModel
        from core.permission_context import get_object_permissions

        base = CharacterModel.objects.non_polymorphic().get(pk=self.character.pk)
        request = self.request()
        self.assertTrue(get_object_permissions(request, base).can_chargen)
        base.status = "Sub"
        self.assertFalse(get_object_permissions(request, base).can_chargen)
        base.owner_id = self.stranger.pk
        self.assertFalse(get_object_permissions(request, base).can_view_full)

    def test_batched_linked_base_characters_do_not_add_queries_per_row(self):
        from django.contrib.contenttypes.models import ContentType

        from characters.models.core import CharacterModel
        from core.permission_context import get_object_permissions, prepare_permission_objects

        ids = [
            Human.objects.create(name=f"Linked {i}", owner=self.owner, chronicle=self.chronicle).pk
            for i in range(20)
        ]
        bases = list(CharacterModel.objects.non_polymorphic().filter(pk__in=ids))
        ContentType.objects.get_for_models(CharacterModel, Human)
        for count in (1, 20):
            rows = [SimpleNamespace(character=obj) for obj in bases[:count]]
            request = self.request(self.editor)
            with self.assertNumQueries(6):  # one hydration query, five membership queries
                prepare_permission_objects(request, rows)
            with self.assertNumQueries(0):
                for row in rows:
                    self.assertTrue(get_object_permissions(request, row.character).can_approve)

    def test_observer_identity_does_not_cross_model_trees(self):
        item = ItemModel.objects.create(name="Other tree", pk=self.character.pk, owner=self.owner)
        Observer.objects.create(
            content_object=self.character, user=self.stranger, granted_by=self.owner
        )
        self.assertFalse(
            PermissionManager.filter_queryset_for_user(
                self.stranger, ItemModel.objects.filter(pk=item.pk)
            ).exists()
        )
        self.assertFalse(
            PermissionManager.user_can_view(
                self.stranger, item, request=self.request(self.stranger)
            )
        )

    def test_snapshot_permission_fields_match_manager(self):
        from core.permission_context import get_object_permissions

        fields = {
            "can_view_full": Permission.VIEW_FULL,
            "can_view_partial": Permission.VIEW_PARTIAL,
            "can_edit": Permission.EDIT_FULL,
            "can_edit_limited": Permission.EDIT_LIMITED,
            "can_spend_xp": Permission.SPEND_XP,
            "can_spend_freebies": Permission.SPEND_FREEBIES,
            "can_approve": Permission.APPROVE,
            "can_delete": Permission.DELETE,
            "can_manage_observers": Permission.MANAGE_OBSERVERS,
        }
        for user in (self.owner, self.editor, self.reader, self.stranger, AnonymousUser()):
            request = self.request(user)
            for status in ("Un", "Rev", "Sub", "App", "Ret", "Dec"):
                self.character.status = status
                snapshot = get_object_permissions(request, self.character)
                for field, permission in fields.items():
                    with self.subTest(user=str(user), status=status, field=field):
                        self.assertEqual(
                            getattr(snapshot, field),
                            PermissionManager.user_has_permission(user, self.character, permission),
                        )

    def test_spending_controls_hide_self_approval_and_follow_npc_changes(self):
        from core.permission_context import get_object_permissions

        self.character.owner = self.editor
        request = self.request(self.editor)
        self.assertTrue(get_object_permissions(request, self.character).can_approve)
        self.assertFalse(get_object_permissions(request, self.character).can_approve_spending)
        self.character.npc = True
        self.assertTrue(get_object_permissions(request, self.character).can_approve_spending)
        self.editor.is_staff = True
        STRelationship.objects.filter(user=self.editor).delete()
        PermissionManager.invalidate_request_cache(request)
        self.assertFalse(get_object_permissions(request, self.character).can_approve_spending)

    def test_character_template_list_compiles(self):
        from django.template.loader import get_template

        get_template("core/character_template/list.html")

    def test_unpaginated_lists_do_not_prepare_unused_row_permissions(self):
        from django.views.generic import ListView

        from core.mixins import VisibilityFilterMixin

        class CharacterList(VisibilityFilterMixin, ListView):
            model = Human

        view = CharacterList()
        view.setup(self.request())
        view.object_list = Human.objects.all()
        with self.assertNumQueries(0):
            view.get_context_data()
