"""
Management command to find duplicate objects across all model types.

Finds potential duplicates based on:
- Same name
- Same owner
- Same chronicle
- Same type

Works with all objects that inherit from core.models.Model including:
- Characters
- Items
- Locations
- Effects
- And any other custom objects
"""

from collections import defaultdict

from django.core.management.base import BaseCommand
from django.db.models import Count, Q


class Command(BaseCommand):
    help = "Find duplicate objects (characters, items, locations, effects, etc.)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--type",
            type=str,
            choices=["character", "item", "location", "effect", "all"],
            default="all",
            help="Type of objects to check (default: all)",
        )
        parser.add_argument(
            "--chronicle",
            type=int,
            help="Only check objects in specific chronicle (by ID)",
        )
        parser.add_argument(
            "--owner",
            type=str,
            help="Only check objects owned by specific user (username)",
        )
        parser.add_argument(
            "--auto-merge",
            action="store_true",
            help="Automatically merge exact duplicates (USE WITH CAUTION)",
        )
        parser.add_argument(
            "--delete-empty",
            action="store_true",
            help="Delete empty unfinished duplicates (name only, no other data)",
        )
        parser.add_argument(
            "--export",
            type=str,
            help="Export duplicate list to CSV file (provide filename)",
        )

    def handle(self, *args, **options):
        self.auto_merge = options["auto_merge"]
        self.delete_empty = options["delete_empty"]

        self.stdout.write(self.style.SUCCESS("\nSearching for duplicate objects...\n"))

        # Determine which model types to check
        if options["type"] == "all":
            self.check_all_types(options)
        else:
            self.check_specific_type(options["type"], options)

    def check_all_types(self, options):
        """Check all object types for duplicates."""
        types_to_check = [
            ("characters", "characters.models.core.character", "CharacterModel"),
            ("items", "items.models.core.item", "ItemModel"),
            ("locations", "locations.models.core.location", "LocationModel"),
            ("effects", "characters.models.mage.effect", "Effect"),
        ]

        all_duplicates = []

        for type_name, module_path, class_name in types_to_check:
            try:
                # Dynamically import the model
                module_parts = module_path.rsplit(".", 1)
                module = __import__(module_parts[0], fromlist=[module_parts[1]])
                model_class = getattr(module, class_name)

                duplicates = self.find_duplicates(model_class, type_name, options)
                all_duplicates.extend(duplicates)

            except (ImportError, AttributeError) as e:
                self.stdout.write(self.style.WARNING(f"Could not check {type_name}: {e}"))

        # Display overall summary
        self.display_summary(all_duplicates)

        # Export if requested
        if options["export"]:
            self.export_duplicates(all_duplicates, options["export"])

    def check_specific_type(self, obj_type, options):
        """Check a specific object type for duplicates."""
        type_map = {
            "character": ("characters.models.core.character", "CharacterModel"),
            "item": ("items.models.core.item", "ItemModel"),
            "location": ("locations.models.core.location", "LocationModel"),
            "effect": ("characters.models.mage.effect", "Effect"),
        }

        if obj_type not in type_map:
            self.stdout.write(self.style.ERROR(f"Unknown type: {obj_type}"))
            return

        module_path, class_name = type_map[obj_type]

        try:
            module_parts = module_path.rsplit(".", 1)
            module = __import__(module_parts[0], fromlist=[module_parts[1]])
            model_class = getattr(module, class_name)

            duplicates = self.find_duplicates(model_class, obj_type, options)
            self.display_summary(duplicates)

            if options["export"]:
                self.export_duplicates(duplicates, options["export"])

        except (ImportError, AttributeError) as e:
            self.stdout.write(self.style.ERROR(f"Could not load {obj_type}: {e}"))

    def find_duplicates(self, model_class, type_name, options):
        """Find duplicates for a specific model class."""
        queryset = model_class.objects.all()

        # Apply filters
        if options["chronicle"]:
            queryset = queryset.filter(chronicle_id=options["chronicle"])

        if options["owner"]:
            from django.contrib.auth.models import User

            try:
                user = User.objects.get(username=options["owner"])
                queryset = queryset.filter(owner=user)
            except User.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"User {options['owner']} not found"))
                return []

        # Group by name, owner, and chronicle
        duplicates = []
        name_groups = defaultdict(list)

        for obj in queryset:
            key = (
                obj.name.lower().strip() if obj.name else "",
                obj.owner_id if hasattr(obj, "owner") else None,
                obj.chronicle_id if hasattr(obj, "chronicle") else None,
            )
            name_groups[key].append(obj)

        # Find groups with more than one object
        for key, objects in name_groups.items():
            if len(objects) > 1:
                name, owner_id, chronicle_id = key

                # Get owner and chronicle names
                owner_name = "None"
                if owner_id:
                    from django.contrib.auth.models import User

                    try:
                        owner_name = User.objects.get(id=owner_id).username
                    except User.DoesNotExist:
                        owner_name = f"Unknown (ID: {owner_id})"

                chronicle_name = "None"
                if chronicle_id:
                    from game.models import Chronicle

                    try:
                        chronicle_name = Chronicle.objects.get(id=chronicle_id).name
                    except Chronicle.DoesNotExist:
                        chronicle_name = f"Unknown (ID: {chronicle_id})"

                duplicate_group = {
                    "type": type_name,
                    "name": name or "(empty)",
                    "owner": owner_name,
                    "chronicle": chronicle_name,
                    "objects": objects,
                }

                duplicates.append(duplicate_group)

                # Handle auto-merge if enabled
                if self.auto_merge:
                    self.attempt_merge(duplicate_group)
                elif self.delete_empty:
                    self.delete_empty_duplicates(duplicate_group)

        return duplicates

    def attempt_merge(self, duplicate_group):
        """Attempt to automatically merge exact duplicates."""
        objects = duplicate_group["objects"]

        # Find the "best" object to keep (prefer Approved > Submitted > newest)
        def sort_key(obj):
            status_priority = {"App": 3, "Sub": 2, "Un": 1, "Ret": 0, "Dec": 0}
            return (
                status_priority.get(obj.status, 0),
                obj.id,  # Older ID = created first
            )

        objects_sorted = sorted(objects, key=sort_key, reverse=True)
        keeper = objects_sorted[0]
        to_delete = objects_sorted[1:]

        # Only merge if they're truly identical (same status, same basic fields)
        can_merge = all(
            obj.status == keeper.status and obj.description == keeper.description
            for obj in to_delete
        )

        if can_merge:
            for obj in to_delete:
                obj.delete()

            self.stdout.write(
                self.style.SUCCESS(
                    f"  ✓ Merged {len(to_delete)} duplicate(s) of "
                    f"{duplicate_group['name']} (kept ID: {keeper.id})"
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"  ⚠ Cannot auto-merge {duplicate_group['name']} - "
                    f"objects differ in content"
                )
            )

    def delete_empty_duplicates(self, duplicate_group):
        """Delete empty unfinished duplicates."""
        objects = duplicate_group["objects"]

        for obj in objects:
            # Only delete if Unfinished, no description, and no other significant data
            if obj.status == "Un" and (not obj.description or obj.description.strip() == ""):
                obj.delete()
                self.stdout.write(
                    self.style.SUCCESS(f"  ✓ Deleted empty duplicate: {obj.name} (ID: {obj.id})")
                )

    def display_summary(self, all_duplicates):
        """Display summary of found duplicates."""
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write(self.style.SUCCESS("DUPLICATE OBJECTS FOUND"))
        self.stdout.write("=" * 80 + "\n")

        if not all_duplicates:
            self.stdout.write(self.style.SUCCESS("No duplicates found!"))
            self.stdout.write("=" * 80 + "\n")
            return

        # Group by type
        by_type = defaultdict(list)
        for dup in all_duplicates:
            by_type[dup["type"]].append(dup)

        total_objects = 0

        for obj_type, duplicates in sorted(by_type.items()):
            self.stdout.write(
                self.style.WARNING(f"\n{obj_type.upper()} ({len(duplicates)} duplicate groups):")
            )

            for dup in duplicates[:10]:  # Show first 10 per type
                objects = dup["objects"]
                total_objects += len(objects)

                self.stdout.write(f"\n  Name: {dup['name']}")
                self.stdout.write(f"  Owner: {dup['owner']}")
                self.stdout.write(f"  Chronicle: {dup['chronicle']}")
                self.stdout.write(f"  Instances: {len(objects)}")

                for obj in objects:
                    self.stdout.write(f"    - ID: {obj.id}, Status: {obj.get_status_display()}")

            if len(duplicates) > 10:
                self.stdout.write(f"\n  ... and {len(duplicates) - 10} more groups")

        self.stdout.write("\n" + "=" * 80)
        self.stdout.write(f"Total duplicate groups: {len(all_duplicates)}")
        self.stdout.write(f"Total objects involved: {total_objects}")
        self.stdout.write("=" * 80 + "\n")

    def export_duplicates(self, duplicates, filename):
        """Export duplicates to CSV file."""
        import csv

        with open(filename, "w", newline="") as csvfile:
            fieldnames = [
                "type",
                "name",
                "owner",
                "chronicle",
                "instance_count",
                "object_ids",
                "statuses",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for dup in duplicates:
                objects = dup["objects"]
                writer.writerow(
                    {
                        "type": dup["type"],
                        "name": dup["name"],
                        "owner": dup["owner"],
                        "chronicle": dup["chronicle"],
                        "instance_count": len(objects),
                        "object_ids": ", ".join(str(obj.id) for obj in objects),
                        "statuses": ", ".join(obj.get_status_display() for obj in objects),
                    }
                )

        self.stdout.write(self.style.SUCCESS(f"Exported duplicates to {filename}"))
