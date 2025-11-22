"""
Management command for bulk approval of pending items.

Allows STs to bulk approve:
- Characters (status change from Sub to App)
- Images (image_status change from sub to app)
- Freebies (freebies_approved flag)
- XP spend requests
- Weekly/Story XP requests
"""
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Bulk approve pending items for storytellers"

    def add_arguments(self, parser):
        parser.add_argument(
            "--type",
            type=str,
            choices=[
                "characters",
                "images",
                "freebies",
                "xp-spends",
                "xp-requests",
                "all",
            ],
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
            "--auto-approve-images",
            action="store_true",
            help="Automatically approve all submitted images",
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

    def handle(self, *args, **options):
        self.dry_run = options["dry_run"] or options["list_only"]
        self.list_only = options["list_only"]

        self.stdout.write(self.style.SUCCESS("\nPending Approvals\n"))

        if self.dry_run and not self.list_only:
            self.stdout.write(self.style.WARNING("[DRY RUN MODE]\n"))

        # Track approvals
        self.approved = {
            "characters": 0,
            "images": 0,
            "freebies": 0,
            "xp_spends": 0,
            "weekly_xp": 0,
            "story_xp": 0,
        }

        # Determine which types to process
        approval_type = options["type"]

        if approval_type in ["characters", "all"]:
            self.approve_characters(options)

        if approval_type in ["images", "all"] or options["auto_approve_images"]:
            self.approve_images(options)

        if approval_type in ["freebies", "all"]:
            self.approve_freebies(options)

        if approval_type in ["xp-spends", "all"]:
            self.approve_xp_spends(options)

        if approval_type in ["xp-requests", "all"]:
            self.approve_xp_requests(options)

        # Display summary
        self.display_summary()

    def approve_characters(self, options):
        """Approve submitted characters."""
        from characters.models.core.character import CharacterModel

        queryset = CharacterModel.objects.filter(status="Sub")

        if options["chronicle"]:
            queryset = queryset.filter(chronicle_id=options["chronicle"])

        if options["owner"]:
            try:
                user = User.objects.get(username=options["owner"])
                queryset = queryset.filter(owner=user)
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f"User {options['owner']} not found")
                )
                return

        count = queryset.count()

        if count > 0:
            self.stdout.write(self.style.WARNING(f"\nSubmitted Characters: {count}"))

            for char in queryset[:10]:
                owner_name = char.owner.username if char.owner else "No owner"
                chronicle_name = (
                    char.chronicle.name if char.chronicle else "No chronicle"
                )
                self.stdout.write(
                    f"  - {char.name} (ID: {char.id}, Owner: {owner_name}, Chronicle: {chronicle_name})"
                )

            if count > 10:
                self.stdout.write(f"  ... and {count - 10} more")

            if not self.list_only:
                if not self.dry_run:
                    queryset.update(status="App")
                    self.approved["characters"] = count
                    self.stdout.write(
                        self.style.SUCCESS(f"  ✓ Approved {count} character(s)")
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"  [DRY RUN] Would approve {count} character(s)"
                        )
                    )

    def approve_images(self, options):
        """Approve submitted images."""
        from characters.models.core.character import CharacterModel
        from items.models.core.item import ItemModel
        from locations.models.core.location import LocationModel

        # Combine all model types
        all_models = []

        for model_class in [CharacterModel, ItemModel, LocationModel]:
            queryset = model_class.objects.filter(image_status="sub").exclude(image="")

            if options["chronicle"]:
                queryset = queryset.filter(chronicle_id=options["chronicle"])

            if options["owner"]:
                try:
                    user = User.objects.get(username=options["owner"])
                    queryset = queryset.filter(owner=user)
                except User.DoesNotExist:
                    continue

            all_models.extend(list(queryset))

        count = len(all_models)

        if count > 0:
            self.stdout.write(self.style.WARNING(f"\nPending Images: {count}"))

            for obj in all_models[:10]:
                owner_name = obj.owner.username if obj.owner else "No owner"
                self.stdout.write(
                    f"  - {obj.name} (ID: {obj.id}, Type: {obj.type}, Owner: {owner_name})"
                )

            if count > 10:
                self.stdout.write(f"  ... and {count - 10} more")

            if not self.list_only:
                if not self.dry_run:
                    for obj in all_models:
                        obj.image_status = "app"
                        obj.save()
                    self.approved["images"] = count
                    self.stdout.write(
                        self.style.SUCCESS(f"  ✓ Approved {count} image(s)")
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"  [DRY RUN] Would approve {count} image(s)"
                        )
                    )

    def approve_freebies(self, options):
        """Approve freebie spends."""
        from characters.models.core.character import CharacterModel

        queryset = CharacterModel.objects.filter(freebies_approved=False, status="Sub")

        if options["chronicle"]:
            queryset = queryset.filter(chronicle_id=options["chronicle"])

        if options["owner"]:
            try:
                user = User.objects.get(username=options["owner"])
                queryset = queryset.filter(owner=user)
            except User.DoesNotExist:
                return

        count = queryset.count()

        if count > 0:
            self.stdout.write(
                self.style.WARNING(f"\nPending Freebie Approvals: {count}")
            )

            for char in queryset[:10]:
                owner_name = char.owner.username if char.owner else "No owner"
                self.stdout.write(
                    f"  - {char.name} (ID: {char.id}, Owner: {owner_name})"
                )

            if count > 10:
                self.stdout.write(f"  ... and {count - 10} more")

            if not self.list_only:
                if not self.dry_run:
                    queryset.update(freebies_approved=True)
                    self.approved["freebies"] = count
                    self.stdout.write(
                        self.style.SUCCESS(f"  ✓ Approved {count} freebie spend(s)")
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"  [DRY RUN] Would approve {count} freebie spend(s)"
                        )
                    )

    def approve_xp_spends(self, options):
        """Approve pending XP spends in character spent_xp fields."""
        from characters.models.core.character import CharacterModel

        queryset = CharacterModel.objects.all()

        if options["chronicle"]:
            queryset = queryset.filter(chronicle_id=options["chronicle"])

        if options["owner"]:
            try:
                user = User.objects.get(username=options["owner"])
                queryset = queryset.filter(owner=user)
            except User.DoesNotExist:
                return

        # Count total pending spends
        total_pending = 0
        characters_with_pending = []

        for char in queryset:
            if hasattr(char, "spent_xp"):
                pending_spends = [
                    spend
                    for spend in char.spent_xp
                    if spend.get("approved") == "Pending"
                ]
                if pending_spends:
                    total_pending += len(pending_spends)
                    characters_with_pending.append((char, pending_spends))

        if total_pending > 0:
            self.stdout.write(
                self.style.WARNING(
                    f"\nPending XP Spends: {total_pending} across {len(characters_with_pending)} character(s)"
                )
            )

            for char, spends in characters_with_pending[:5]:
                owner_name = char.owner.username if char.owner else "No owner"
                total_cost = sum(spend.get("cost", 0) for spend in spends)
                self.stdout.write(
                    f"  - {char.name} (ID: {char.id}): {len(spends)} spend(s), {total_cost} XP"
                )

            if len(characters_with_pending) > 5:
                self.stdout.write(
                    f"  ... and {len(characters_with_pending) - 5} more characters"
                )

            if not self.list_only:
                if not self.dry_run:
                    for char, spends in characters_with_pending:
                        for spend in char.spent_xp:
                            if spend.get("approved") == "Pending":
                                spend["approved"] = "Approved"
                        char.save()
                    self.approved["xp_spends"] = total_pending
                    self.stdout.write(
                        self.style.SUCCESS(f"  ✓ Approved {total_pending} XP spend(s)")
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"  [DRY RUN] Would approve {total_pending} XP spend(s)"
                        )
                    )

    def approve_xp_requests(self, options):
        """Approve weekly and story XP requests."""
        from characters.models.core.character import CharacterModel
        from game.models import StoryXPRequest, WeeklyXPRequest

        # Build character filter
        char_filter = {}
        if options["chronicle"]:
            char_filter["chronicle_id"] = options["chronicle"]

        if options["owner"]:
            try:
                user = User.objects.get(username=options["owner"])
                char_filter["owner"] = user
            except User.DoesNotExist:
                return

        # Get character IDs
        if char_filter:
            character_ids = CharacterModel.objects.filter(**char_filter).values_list(
                "id", flat=True
            )
            weekly_requests = WeeklyXPRequest.objects.filter(
                approved=False, character_id__in=character_ids
            )
            story_requests = StoryXPRequest.objects.filter(
                character_id__in=character_ids
            )
        else:
            weekly_requests = WeeklyXPRequest.objects.filter(approved=False)
            story_requests = StoryXPRequest.objects.all()[
                :0
            ]  # Story XP doesn't have approved field

        weekly_count = weekly_requests.count()

        if weekly_count > 0:
            self.stdout.write(
                self.style.WARNING(f"\nPending Weekly XP Requests: {weekly_count}")
            )

            for req in weekly_requests[:10]:
                char_name = req.character.name if req.character else "Unknown"
                week_str = str(req.week) if req.week else "Unknown week"
                self.stdout.write(f"  - {char_name}: {week_str} ({req.total_xp()} XP)")

            if weekly_count > 10:
                self.stdout.write(f"  ... and {weekly_count - 10} more")

            if not self.list_only:
                if not self.dry_run:
                    # Approve and award XP
                    for req in weekly_requests:
                        req.approved = True
                        req.save()
                        if req.character:
                            req.character.add_xp(req.total_xp())

                    self.approved["weekly_xp"] = weekly_count
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  ✓ Approved {weekly_count} weekly XP request(s)"
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"  [DRY RUN] Would approve {weekly_count} weekly XP request(s)"
                        )
                    )

    def display_summary(self):
        """Display approval summary."""
        self.stdout.write("\n" + "=" * 70)
        self.stdout.write(self.style.SUCCESS("APPROVAL SUMMARY"))
        self.stdout.write("=" * 70)

        total = sum(self.approved.values())

        if total == 0:
            if self.list_only:
                self.stdout.write("No pending items found")
            else:
                self.stdout.write(self.style.SUCCESS("Nothing to approve!"))
        else:
            for category, count in self.approved.items():
                if count > 0:
                    self.stdout.write(f"{category.replace('_', ' ').title()}: {count}")

            self.stdout.write("=" * 70)
            self.stdout.write(self.style.SUCCESS(f"Total approved: {total} item(s)"))

        self.stdout.write("=" * 70 + "\n")

        if self.dry_run and not self.list_only:
            self.stdout.write(
                self.style.WARNING("[DRY RUN] No items were actually approved")
            )
