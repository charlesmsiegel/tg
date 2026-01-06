import json
import logging

from core.forms.character_template import (
    CharacterTemplateForm,
    CharacterTemplateImportForm,
)
from core.mixins import MessageMixin
from core.models import CharacterTemplate
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    UpdateView,
)

logger = logging.getLogger(__name__)


class STRequiredMixin(UserPassesTestMixin):
    """Mixin to restrict access to Storytellers only (or superusers/staff)"""

    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        # Allow superusers and staff
        if user.is_superuser or user.is_staff:
            return True
        return user.profile.is_st()

    def handle_no_permission(self):
        # If user is not authenticated, let LoginRequiredMixin handle it
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        # User is authenticated but not an ST
        messages.error(
            self.request,
            "You must be a Storyteller to access template management features.",
        )
        return redirect("core:home")


class CharacterTemplateListView(LoginRequiredMixin, STRequiredMixin, ListView):
    """List all templates (official + user-created)"""

    model = CharacterTemplate
    template_name = "core/character_template/list.html"
    context_object_name = "templates"
    paginate_by = 20

    def get_queryset(self):
        qs = CharacterTemplate.objects.all().select_related("owner", "chronicle")

        # Filter by gameline if specified
        gameline = self.request.GET.get("gameline")
        if gameline:
            qs = qs.filter(gameline=gameline)

        # Filter by character type if specified
        character_type = self.request.GET.get("character_type")
        if character_type:
            qs = qs.filter(character_type=character_type)

        # Filter by ownership
        filter_type = self.request.GET.get("filter", "all")
        if filter_type == "mine":
            qs = qs.filter(owner=self.request.user)
        elif filter_type == "official":
            qs = qs.filter(is_official=True)
        elif filter_type == "community":
            qs = qs.filter(is_official=False, is_public=True)

        return qs.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.request.GET.get("filter", "all")
        context["gameline"] = self.request.GET.get("gameline", "")
        context["character_type"] = self.request.GET.get("character_type", "")
        return context


class CharacterTemplateDetailView(LoginRequiredMixin, STRequiredMixin, DetailView):
    """View a template in detail"""

    model = CharacterTemplate
    template_name = "core/character_template/detail.html"
    context_object_name = "template"

    def get_queryset(self):
        return CharacterTemplate.objects.select_related("owner", "chronicle")


class CharacterTemplateCreateView(LoginRequiredMixin, STRequiredMixin, MessageMixin, CreateView):
    """Create a new user template (ST only)"""

    model = CharacterTemplate
    form_class = CharacterTemplateForm
    template_name = "core/character_template/form.html"
    success_message = "Template created successfully!"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse("core:character_template_detail", kwargs={"pk": self.object.pk})


class CharacterTemplateUpdateView(LoginRequiredMixin, STRequiredMixin, MessageMixin, UpdateView):
    """Edit a user template (ST only, owner or superuser)"""

    model = CharacterTemplate
    form_class = CharacterTemplateForm
    template_name = "core/character_template/form.html"
    success_message = "Template updated successfully!"

    def get_queryset(self):
        # Only allow editing own templates or if superuser
        if self.request.user.is_superuser:
            return CharacterTemplate.objects.all()
        return CharacterTemplate.objects.filter(owner=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse("core:character_template_detail", kwargs={"pk": self.object.pk})


class CharacterTemplateDeleteView(LoginRequiredMixin, STRequiredMixin, MessageMixin, DeleteView):
    """Delete a user template (ST only, owner or superuser)"""

    model = CharacterTemplate
    template_name = "core/character_template/delete.html"
    success_url = reverse_lazy("core:character_template_list")
    success_message = "Template deleted successfully!"

    def get_queryset(self):
        # Only allow deleting own templates (not official ones) or if superuser
        if self.request.user.is_superuser:
            return CharacterTemplate.objects.all()
        return CharacterTemplate.objects.filter(owner=self.request.user, is_official=False)


class CharacterTemplateExportView(LoginRequiredMixin, STRequiredMixin, DetailView):
    """Export a template as JSON"""

    model = CharacterTemplate

    def get(self, request, *args, **kwargs):
        template = self.get_object()

        # Build export data
        export_data = {
            "name": template.name,
            "gameline": template.gameline,
            "character_type": template.character_type,
            "faction": template.faction,
            "concept": template.concept,
            "description": template.description,
            "basic_info": template.basic_info,
            "attributes": template.attributes,
            "abilities": template.abilities,
            "backgrounds": template.backgrounds,
            "powers": template.powers,
            "merits_flaws": template.merits_flaws,
            "specialties": template.specialties,
            "languages": template.languages,
            "equipment": template.equipment,
            "suggested_freebie_spending": template.suggested_freebie_spending,
            # Metadata
            "exported_from": "World of Darkness Character Manager",
            "template_version": "1.0",
        }

        # Create JSON response
        response = HttpResponse(json.dumps(export_data, indent=2), content_type="application/json")
        filename = f"{template.name.replace(' ', '_').lower()}_template.json"
        response["Content-Disposition"] = f'attachment; filename="{filename}"'

        return response


class CharacterTemplateImportView(LoginRequiredMixin, STRequiredMixin, MessageMixin, FormView):
    """Import a template from JSON"""

    form_class = CharacterTemplateImportForm
    template_name = "core/character_template/import.html"
    success_url = reverse_lazy("core:character_template_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        try:
            # Read and parse JSON file
            json_file = form.cleaned_data["json_file"]
            json_data = json.loads(json_file.read().decode("utf-8"))

            # Validate required fields
            required_fields = ["name", "gameline", "character_type"]
            for field in required_fields:
                if field not in json_data:
                    messages.error(self.request, f"Missing required field in JSON: {field}")
                    return self.form_invalid(form)

            # Create template from JSON
            template = CharacterTemplate.objects.create(
                name=json_data.get("name"),
                gameline=json_data.get("gameline"),
                character_type=json_data.get("character_type"),
                faction=json_data.get("faction", ""),
                concept=json_data.get("concept", ""),
                description=json_data.get("description", ""),
                basic_info=json_data.get("basic_info", {}),
                attributes=json_data.get("attributes", {}),
                abilities=json_data.get("abilities", {}),
                backgrounds=json_data.get("backgrounds", []),
                powers=json_data.get("powers", {}),
                merits_flaws=json_data.get("merits_flaws", []),
                specialties=json_data.get("specialties", []),
                languages=json_data.get("languages", []),
                equipment=json_data.get("equipment", ""),
                suggested_freebie_spending=json_data.get("suggested_freebie_spending", {}),
                # Set ownership
                owner=self.request.user,
                is_official=False,
                is_public=form.cleaned_data.get("is_public", False),
                chronicle=form.cleaned_data.get("chronicle"),
                status="App",  # Auto-approve imported templates
            )

            messages.success(
                self.request,
                f"Successfully imported template '{template.name}'. You can now edit it or use it for character creation.",
            )

            return redirect("core:character_template_detail", pk=template.pk)

        except json.JSONDecodeError:
            messages.error(self.request, "Invalid JSON file. Please check the format.")
            return self.form_invalid(form)
        except Exception as e:
            logger.error(
                f"Error importing template for user {self.request.user.id}: {e}",
                exc_info=True,
            )
            messages.error(self.request, f"Error importing template: {str(e)}")
            return self.form_invalid(form)


class CharacterTemplateQuickNPCView(LoginRequiredMixin, STRequiredMixin, View):
    """Quick NPC creation from a template (ST only)"""

    def post(self, request, *args, **kwargs):
        template = get_object_or_404(CharacterTemplate, pk=kwargs["pk"])

        try:
            # Dynamically import the correct character model based on template
            character_model = self.get_character_model(template)

            if not character_model:
                messages.error(
                    request,
                    f"Character type '{template.character_type}' not supported for quick NPC creation.",
                )
                return redirect("core:character_template_detail", pk=template.pk)

            # Use atomic transaction for NPC creation and template application
            with transaction.atomic():
                # Create NPC character with basic info
                npc_name = f"{template.concept} (NPC)"
                character = character_model.objects.create(
                    name=npc_name,
                    owner=request.user,
                    chronicle=template.chronicle,
                    status="App",  # Auto-approve NPCs
                    npc=True,  # Mark as NPC
                )

                # Apply template to character
                template.apply_to_character(character)

                # Save character
                character.save()

            messages.success(
                request,
                f"NPC '{npc_name}' created successfully from template '{template.name}'!",
            )

            # Redirect to character detail page
            return redirect(character.get_absolute_url())

        except Exception as e:
            logger.error(
                f"Error creating NPC from template {template.pk} for user {request.user.id}: {e}",
                exc_info=True,
            )
            messages.error(request, f"Error creating NPC from template: {str(e)}")
            return redirect("core:character_template_detail", pk=template.pk)

    def get_character_model(self, template):
        """Get the appropriate character model based on template character_type"""
        # Map character types to their model classes
        character_type_map = {
            "mage": ("characters.models.mage.mtahuman", "MtAHuman"),
            "vampire": ("characters.models.vampire.vampire", "Vampire"),
            "werewolf": ("characters.models.werewolf.werewolf", "Werewolf"),
            "changeling": ("characters.models.changeling.changeling", "Changeling"),
            "wraith": ("characters.models.wraith.wraith", "Wraith"),
            "demon": ("characters.models.demon.demon", "Demon"),
        }

        if template.character_type not in character_type_map:
            return None

        module_path, class_name = character_type_map[template.character_type]

        try:
            from importlib import import_module

            module = import_module(module_path)
            return getattr(module, class_name)
        except (ImportError, AttributeError):
            return None
