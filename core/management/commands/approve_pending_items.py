"""
Management command for bulk approval of pending items.

Approves, through the same services and model methods as the storyteller pages:
- Characters (``ApprovalService.approve_object``: status Sub to App)
- Images (``ApprovalService.approve_image``: image_status sub to app)
- Freebies (``Human.award_backstory_freebies(0)``: freebies_approved)
- Weekly XP requests (``WeeklyXPRequest.approve``: approved, XP awarded)

Every write names a scope (--chronicle, --owner or --all) and an --approver who
must hold the approve permission on each object; objects the approver may not
approve are skipped and reported. It asks for confirmation unless --noinput.
XP spends are not handled: each needs a storyteller decision on the trait.
"""

from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.management.base import BaseCommand, CommandError

from core.constants import CharacterStatus, ImageStatus
from core.permissions import Permission, PermissionManager


class Command(BaseCommand):
    help = (
        "Bulk approve pending characters, images, freebies and weekly XP requests "
        "through the approval services. Writes need --chronicle, --owner or --all "
        "and --approver."
    )

    TYPES = ["characters", "images", "freebies", "xp-requests"]

    def add_arguments(self, parser):
        parser.add_argument(
            "--type",
            type=str,
            choices=[*self.TYPES, "all"],
            default="all",
            help="Type of items to approve (default: all)",
        )
        parser.add_argument(
            "--chronicle",
            type=int,
            help="Only approve items in specific chronicle (by ID)",
        )
        parser.add_argument(
            "--owner",
            type=str,
            help="Only approve items from specific user (username)",
        )
        parser.add_argument(
            "--all",
            action="store_true",
            help="Approve across every chronicle and owner (required without a scope)",
        )
        parser.add_argument(
            "--approver",
            type=str,
            help="Username approving the items; must be allowed to approve each one",
        )
        parser.add_argument(
            "--auto-approve-images",
            action="store_true",
            help="Also process images whatever --type says",
        )
        parser.add_argument(
            "--list-only",
            action="store_true",
            help="Only list pending items without approving",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be approved without actually approving",
        )
        parser.add_argument(
            "--noinput",
            "--no-input",
            action="store_false",
            dest="interactive",
            help="Do not ask for confirmation",
        )

    def handle(self, *args, **options):
        self.list_only = options["list_only"]
        self.dry_run = options["dry_run"] or self.list_only
        self.options = options

        self.owner = None
        if options["owner"]:
            self.owner = self.get_user(options["owner"], "--owner")

        approver = None
        if not self.dry_run:
            if not (options["chronicle"] or options["owner"] or options["all"]):
                raise CommandError(
                    "Approving needs a scope: pass --chronicle ID, --owner USERNAME or --all "
                    "(or use --list-only / --dry-run)"
                )
            if not options["approver"]:
                raise CommandError("Approving needs --approver USERNAME")
        if options["approver"]:
            approver = self.get_user(options["approver"], "--approver")

        self.stdout.write(self.style.SUCCESS("\nPending Approvals\n"))
        if self.dry_run and not self.list_only:
            self.stdout.write(self.style.WARNING("[DRY RUN MODE]\n"))

        types = self.TYPES if options["type"] == "all" else [options["type"]]
        if options["auto_approve_images"] and "images" not in types:
            types = [*types, "images"]

        sections = [
            (label, items, approve)
            for label, items, approve in (self.collect(item_type) for item_type in types)
            if items
        ]
        for label, items, _approve in sections:
            self.list_items(label, items)
        total = sum(len(items) for _label, items, _approve in sections)

        self.approved = {}
        self.skipped = []
        if total and not self.dry_run:
            if options["interactive"] and not self.confirm(total, approver):
                self.stdout.write(self.style.WARNING("Operation cancelled."))
                return
            for label, items, approve in sections:
                self.approve_all(label, items, approve, approver)

        self.display_summary(total)

    def get_user(self, username, option):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f"{option}: user {username} not found") from None

    def confirm(self, total, approver):
        answer = input(f"Approve {total} item(s) as {approver.username}? [y/N]: ")
        return answer.strip().lower() in {"y", "yes"}

    def scoped(self, queryset):
        if self.options["chronicle"]:
            queryset = queryset.filter(chronicle_id=self.options["chronicle"])
        if self.owner:
            queryset = queryset.filter(owner=self.owner)
        return queryset

    def collect(self, item_type):
        """Return (label, items, approve callable) for one --type."""
        return {
            "characters": self.collect_characters,
            "images": self.collect_images,
            "freebies": self.collect_freebies,
            "xp-requests": self.collect_xp_requests,
        }[item_type]()

    def collect_characters(self):
        from characters.models.core.character import Character
        from core.services.approval import ApprovalService

        characters = self.scoped(
            Character.objects.filter(status=CharacterStatus.SUBMITTED).select_related(
                "owner", "chronicle"
            )
        )

        def approve(character, approver):
            ApprovalService.approve_object("character", character.pk, approver)

        return "Submitted Characters", list(characters), approve

    def collect_images(self):
        from core.services.approval import ApprovalService

        objects = []
        for model_type, model in ApprovalService.IMAGE_MODEL_MAP.items():
            queryset = model.objects.filter(image_status=ImageStatus.SUBMITTED).exclude(image="")
            objects.extend(
                (model_type, obj) for obj in self.scoped(queryset.select_related("owner"))
            )

        def approve(entry, approver):
            model_type, obj = entry
            self.check_permission(approver, obj)
            ApprovalService.approve_image(model_type, obj.pk)

        return "Pending Images", objects, approve

    def collect_freebies(self):
        from characters.models.core.human import Human

        humans = self.scoped(
            Human.objects.filter(
                status=CharacterStatus.SUBMITTED, freebies_approved=False
            ).select_related("owner")
        )

        def approve(human, approver):
            self.check_permission(approver, human)
            # The storyteller page awards backstory freebies; bulk approval awards none.
            human.award_backstory_freebies(0)

        return "Pending Freebie Approvals", list(humans), approve

    def collect_xp_requests(self):
        from characters.models.core.character import CharacterModel
        from game.models import WeeklyXPRequest

        requests = WeeklyXPRequest.objects.filter(approved=False).select_related(
            "character", "week"
        )
        if self.options["chronicle"] or self.owner:
            requests = requests.filter(character__in=self.scoped(CharacterModel.objects.all()))

        def approve(request, approver):
            if request.character is None:
                raise ValidationError("request has no character")
            self.check_permission(approver, request.character)
            request.approve()

        return "Pending Weekly XP Requests", list(requests), approve

    @staticmethod
    def check_permission(approver, obj):
        if not PermissionManager.user_has_permission(approver, obj, Permission.APPROVE):
            raise PermissionDenied(f"{approver.username} may not approve this")

    @staticmethod
    def describe(item):
        if isinstance(item, tuple):
            model_type, obj = item
            owner = obj.owner.username if obj.owner else "No owner"
            return f"{obj.name} (ID: {obj.id}, Type: {model_type}, Owner: {owner})"
        if hasattr(item, "week_id"):
            character = item.character.name if item.character else "Unknown"
            week = str(item.week) if item.week else "Unknown week"
            return f"{character}: {week} ({item.total_xp()} XP)"
        owner = item.owner.username if item.owner else "No owner"
        return f"{item.name} (ID: {item.id}, Owner: {owner})"

    def list_items(self, label, items):
        self.stdout.write(self.style.WARNING(f"\n{label}: {len(items)}"))
        for item in items[:10]:
            self.stdout.write(f"  - {self.describe(item)}")
        if len(items) > 10:
            self.stdout.write(f"  ... and {len(items) - 10} more")
        if self.dry_run and not self.list_only:
            self.stdout.write(self.style.WARNING(f"  [DRY RUN] Would approve {len(items)}"))

    def approve_all(self, label, items, approve, approver):
        count = 0
        for item in items:
            try:
                approve(item, approver)
            except (PermissionDenied, ValidationError, ValueError) as exc:
                self.skipped.append(f"{self.describe(item)}: {exc}")
            else:
                count += 1
        self.approved[label] = count
        self.stdout.write(self.style.SUCCESS(f"  ✓ {label}: approved {count}"))

    def display_summary(self, total):
        """Display approval summary."""
        self.stdout.write("\n" + "=" * 70)
        self.stdout.write(self.style.SUCCESS("APPROVAL SUMMARY"))
        self.stdout.write("=" * 70)

        if total == 0:
            self.stdout.write("No pending items found")
        elif self.dry_run:
            self.stdout.write(f"Pending: {total} item(s)")
        else:
            for label, count in self.approved.items():
                self.stdout.write(f"{label}: {count}")
            self.stdout.write(self.style.SUCCESS(f"Total approved: {sum(self.approved.values())}"))
            if self.skipped:
                self.stdout.write(self.style.WARNING(f"Skipped: {len(self.skipped)}"))
                for reason in self.skipped:
                    self.stdout.write(f"  - {reason}")

        self.stdout.write("=" * 70 + "\n")

        if self.dry_run and not self.list_only:
            self.stdout.write(self.style.WARNING("[DRY RUN] No items were actually approved"))
