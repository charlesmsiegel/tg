"""
Management command to sync character status with organizational memberships.

Ensures that Retired/Deceased characters are properly removed from:
- Groups
- Chantries
- Leadership positions
- Active scenes
"""
from django.core.management.base import BaseCommand
from characters.models.core.character import CharacterModel


class Command(BaseCommand):
    help = "Sync character status and remove retired/deceased from organizations"

    def add_arguments(self, parser):
        parser.add_argument(
            "--chronicle",
            type=int,
            help="Only process characters in specific chronicle (by ID)",
        )
        parser.add_argument(
            "--fix-all",
            action="store_true",
            help="Fix all characters, not just Retired/Deceased",
        )
        parser.add_argument(
            "--remove-from-scenes",
            action="store_true",
            help="Also remove from active scenes",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be changed without actually changing it",
        )

    def handle(self, *args, **options):
        self.dry_run = options["dry_run"]
        self.remove_from_scenes = options["remove_from_scenes"]

        # Build queryset
        if options["fix_all"]:
            queryset = CharacterModel.objects.all()
        else:
            queryset = CharacterModel.objects.filter(status__in=["Ret", "Dec"])

        if options["chronicle"]:
            queryset = queryset.filter(chronicle_id=options["chronicle"])

        total = queryset.count()

        self.stdout.write(
            self.style.SUCCESS(f"\nSyncing status for {total} character(s)...\n")
        )
        if self.dry_run:
            self.stdout.write(self.style.WARNING("[DRY RUN MODE]\n"))

        # Track changes
        self.changes = {
            "groups_removed": 0,
            "leadership_cleared": 0,
            "chantry_memberships": 0,
            "chantry_leadership": 0,
            "other_positions": 0,
            "scenes_removed": 0,
        }

        characters_processed = 0
        characters_changed = 0

        for character in queryset:
            if self.process_character(character):
                characters_changed += 1
            characters_processed += 1

        # Display summary
        self.display_summary(characters_processed, characters_changed)

    def process_character(self, character):
        """Process a single character and return True if any changes were made."""
        changed = False

        self.stdout.write(f"\nProcessing: {character.name} (ID: {character.id}, {character.get_status_display()})")

        # Only process Retired/Deceased
        if character.status not in ["Ret", "Dec"]:
            return False

        # Remove from Groups
        changed |= self.remove_from_groups(character)

        # Clear Group leadership
        changed |= self.clear_group_leadership(character)

        # Handle Chantry relationships (if character is a Human)
        if hasattr(character, "member_of"):
            changed |= self.remove_from_chantries(character)

        # Remove from active scenes if requested
        if self.remove_from_scenes:
            changed |= self.remove_from_active_scenes(character)

        if not changed:
            self.stdout.write("  No changes needed")

        return changed

    def remove_from_groups(self, character):
        """Remove character from all Groups."""
        from characters.models.core.group import Group

        groups = Group.objects.filter(members=character)
        count = groups.count()

        if count > 0:
            for group in groups:
                self.stdout.write(f"  - Removing from group: {group.name}")
                if not self.dry_run:
                    group.members.remove(character)

            self.changes["groups_removed"] += count
            return True

        return False

    def clear_group_leadership(self, character):
        """Clear Group leadership positions."""
        from characters.models.core.group import Group

        led_groups = Group.objects.filter(leader=character)
        count = led_groups.count()

        if count > 0:
            for group in led_groups:
                self.stdout.write(f"  - Clearing leadership of: {group.name}")
                if not self.dry_run:
                    group.leader = None
                    group.save()

            self.changes["leadership_cleared"] += count
            return True

        return False

    def remove_from_chantries(self, character):
        """Remove character from Chantry memberships and positions."""
        changed = False

        # Chantry memberships
        if hasattr(character, "member_of"):
            chantries = character.member_of.all()
            if chantries.exists():
                for chantry in chantries:
                    self.stdout.write(f"  - Removing from chantry: {chantry.name}")
                    if not self.dry_run:
                        chantry.members.remove(character)
                self.changes["chantry_memberships"] += chantries.count()
                changed = True

        # Chantry leadership
        if hasattr(character, "chantry_leader_at"):
            led_chantries = character.chantry_leader_at.all()
            if led_chantries.exists():
                for chantry in led_chantries:
                    self.stdout.write(f"  - Clearing chantry leadership at: {chantry.name}")
                    if not self.dry_run:
                        chantry.leaders.remove(character)
                self.changes["chantry_leadership"] += led_chantries.count()
                changed = True

        # Ambassador positions
        if hasattr(character, "ambassador_from"):
            ambassador_chantries = character.ambassador_from.all()
            if ambassador_chantries.exists():
                for chantry in ambassador_chantries:
                    self.stdout.write(f"  - Clearing ambassador position at: {chantry.name}")
                    if not self.dry_run:
                        chantry.ambassador = None
                        chantry.save()
                self.changes["other_positions"] += ambassador_chantries.count()
                changed = True

        # Node tender positions
        if hasattr(character, "tends_node_at"):
            node_chantries = character.tends_node_at.all()
            if node_chantries.exists():
                for chantry in node_chantries:
                    self.stdout.write(f"  - Clearing node tender at: {chantry.name}")
                    if not self.dry_run:
                        chantry.node_tender = None
                        chantry.save()
                self.changes["other_positions"] += node_chantries.count()
                changed = True

        # Investigator roles
        if hasattr(character, "investigator_at"):
            investigator_chantries = character.investigator_at.all()
            if investigator_chantries.exists():
                for chantry in investigator_chantries:
                    self.stdout.write(f"  - Removing investigator role at: {chantry.name}")
                    if not self.dry_run:
                        chantry.investigator.remove(character)
                self.changes["other_positions"] += investigator_chantries.count()
                changed = True

        # Guardian roles
        if hasattr(character, "guardian_of"):
            guardian_chantries = character.guardian_of.all()
            if guardian_chantries.exists():
                for chantry in guardian_chantries:
                    self.stdout.write(f"  - Removing guardian role at: {chantry.name}")
                    if not self.dry_run:
                        chantry.guardian.remove(character)
                self.changes["other_positions"] += guardian_chantries.count()
                changed = True

        # Teacher roles
        if hasattr(character, "teacher_at"):
            teacher_chantries = character.teacher_at.all()
            if teacher_chantries.exists():
                for chantry in teacher_chantries:
                    self.stdout.write(f"  - Removing teacher role at: {chantry.name}")
                    if not self.dry_run:
                        chantry.teacher.remove(character)
                self.changes["other_positions"] += teacher_chantries.count()
                changed = True

        return changed

    def remove_from_active_scenes(self, character):
        """Remove character from active (unfinished) scenes."""
        active_scenes = character.scenes.filter(finished=False)
        count = active_scenes.count()

        if count > 0:
            for scene in active_scenes:
                self.stdout.write(f"  - Removing from active scene: {scene.name}")
                if not self.dry_run:
                    scene.characters.remove(character)

            self.changes["scenes_removed"] += count
            return True

        return False

    def display_summary(self, processed, changed):
        """Display sync summary."""
        self.stdout.write("\n" + "=" * 70)
        self.stdout.write(self.style.SUCCESS("SYNC SUMMARY"))
        self.stdout.write("=" * 70)
        self.stdout.write(f"Characters processed: {processed}")
        self.stdout.write(f"Characters with changes: {changed}")
        self.stdout.write("")

        if sum(self.changes.values()) > 0:
            self.stdout.write("Changes made:")
            for category, count in self.changes.items():
                if count > 0:
                    self.stdout.write(f"  {category.replace('_', ' ').title()}: {count}")
        else:
            self.stdout.write(self.style.SUCCESS("No changes needed - all characters in sync!"))

        self.stdout.write("=" * 70 + "\n")

        if self.dry_run:
            self.stdout.write(
                self.style.WARNING("[DRY RUN] No changes were actually made")
            )
