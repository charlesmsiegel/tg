#!/usr/bin/env python3
"""
Batch script to add Django messages framework to all character CRUD views.
This script updates Create, Update, and Basics views across all gamelines.
"""

import re
from pathlib import Path


def add_imports_if_missing(content):
    """Add message-related imports if not present."""
    imports_to_add = []

    # Check if MessageMixin import exists
    if "from core.views.message_mixin import MessageMixin" not in content:
        imports_to_add.append("from core.views.message_mixin import MessageMixin")

    # Check if messages import exists
    if "from django.contrib import messages" not in content:
        imports_to_add.append("from django.contrib import messages")

    if not imports_to_add:
        return content

    # Find the last django import line
    lines = content.split("\n")
    last_import_idx = 0
    for i, line in enumerate(lines):
        if line.startswith("from django") or line.startswith("import"):
            last_import_idx = i

    # Insert new imports after last import
    for imp in imports_to_add:
        lines.insert(last_import_idx + 1, imp)

    return "\n".join(lines)


def update_create_view(content, class_name, model_name):
    """Add MessageMixin to CreateView classes."""
    # Pattern: class NameCreateView(CreateView):
    pattern = rf"class {class_name}CreateView\(CreateView\):"
    replacement = f"class {class_name}CreateView(MessageMixin, CreateView):"

    updated = re.sub(pattern, replacement, content)

    # Add success/error messages if class was found and doesn't have them
    if f"class {class_name}CreateView(MessageMixin, CreateView):" in updated:
        # Check if messages already exist
        if (
            "success_message ="
            not in updated.split(f"class {class_name}CreateView")[1].split("\n\n")[0]
        ):
            # Add messages after template_name
            pattern = rf'(class {class_name}CreateView.*?template_name = "[^"]*")'
            replacement = rf'\1\n    success_message = "{model_name} \'{{name}}\' created successfully!"\n    error_message = "Failed to create {model_name.lower()}. Please correct the errors below."'
            updated = re.sub(pattern, replacement, updated, flags=re.DOTALL)

    return updated


def update_update_view(content, class_name, model_name):
    """Add MessageMixin to UpdateView classes."""
    # Pattern: class NameUpdateView(SpecialUserMixin, UpdateView):
    pattern = rf"class {class_name}UpdateView\((SpecialUserMixin, )?UpdateView\):"

    def replace_func(match):
        if "SpecialUserMixin" in match.group(0):
            return f"class {class_name}UpdateView(MessageMixin, SpecialUserMixin, UpdateView):"
        else:
            return f"class {class_name}UpdateView(MessageMixin, UpdateView):"

    updated = re.sub(pattern, replace_func, content)

    # Add success/error messages if needed
    if f"class {class_name}UpdateView" in updated and "MessageMixin" in updated:
        class_section = updated.split(f"class {class_name}UpdateView")[1].split("\n\n")[
            0
        ]
        if "success_message =" not in class_section:
            pattern = rf'(class {class_name}UpdateView.*?template_name = "[^"]*")'
            replacement = rf'\1\n    success_message = "{model_name} \'{{name}}\' updated successfully!"\n    error_message = "Failed to update {model_name.lower()}. Please correct the errors below."'
            updated = re.sub(pattern, replacement, updated, flags=re.DOTALL)

    return updated


def update_basics_view(content, class_name, model_name):
    """Add messages to Basics/Creation views."""
    # Find the BasicsView form_valid method
    pattern = rf"(class {class_name}BasicsView.*?def form_valid\(self, form\):.*?)(return super\(\)\.form_valid\(form\))"

    def replace_func(match):
        method_content = match.group(1)
        return_statement = match.group(2)

        # Check if messages already exist
        if "messages.success" in method_content:
            return match.group(0)

        # Add success message before return
        new_content = f"""{method_content}messages.success(
            self.request,
            f"{model_name} '{{self.object.name}}' created successfully! Continue with character creation."
        )
        {return_statement}"""
        return new_content

    updated = re.sub(pattern, replace_func, content, flags=re.DOTALL)

    # Also add form_invalid method if it doesn't exist
    if f"class {class_name}BasicsView" in updated:
        class_section_pattern = (
            rf"(class {class_name}BasicsView.*?)(    def get_success_url)"
        )

        def add_form_invalid(match):
            class_content = match.group(1)
            next_method = match.group(2)

            if "def form_invalid" in class_content:
                return match.group(0)

            form_invalid_method = f"""
    def form_invalid(self, form):
        messages.error(
            self.request,
            "Please correct the errors in the form below."
        )
        return super().form_invalid(form)

{next_method}"""
            return class_content + form_invalid_method

        updated = re.sub(
            class_section_pattern, add_form_invalid, updated, flags=re.DOTALL
        )

    return updated


def process_view_file(file_path, class_prefix, model_name):
    """Process a single view file."""
    print(f"\nProcessing: {file_path}")

    with open(file_path, "r") as f:
        content = f.read()

    original_content = content

    # Add imports
    content = add_imports_if_missing(content)

    # Update Create view
    content = update_create_view(content, class_prefix, model_name)

    # Update Update view
    content = update_update_view(content, class_prefix, model_name)

    # Update Basics view
    content = update_basics_view(content, class_prefix, model_name)

    if content != original_content:
        with open(file_path, "w") as f:
            f.write(content)
        print(f"  ✓ Updated {file_path}")
        return True
    else:
        print(f"  - No changes needed for {file_path}")
        return False


def main():
    """Main execution function."""
    updates = [
        ("/home/user/tg/characters/views/mage/mage.py", "Mage", "Mage"),
        ("/home/user/tg/characters/views/werewolf/garou.py", "Werewolf", "Werewolf"),
        (
            "/home/user/tg/characters/views/changeling/changeling.py",
            "Changeling",
            "Changeling",
        ),
        ("/home/user/tg/characters/views/demon/demon.py", "Demon", "Demon"),
    ]

    updated_count = 0
    for file_path, class_prefix, model_name in updates:
        if Path(file_path).exists():
            if process_view_file(file_path, class_prefix, model_name):
                updated_count += 1
        else:
            print(f"  ✗ File not found: {file_path}")

    print(f"\n{'='*60}")
    print(f"Updated {updated_count} out of {len(updates)} files")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
