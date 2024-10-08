from accounts.forms import CustomUSerCreationForm, ProfileUpdateForm
from characters.models.core import Character
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from game.models import Chronicle, Scene
from items.models.core import ItemModel
from locations.models.core.location import LocationModel


class SignUp(CreateView):
    """View for the Sign Up Page"""

    form_class = CustomUSerCreationForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"


class ProfileView(View):
    """View for User Profiles"""

    def get(self, request):
        if request.user.is_authenticated:
            context = self.get_context(request.user)
            return render(
                request,
                "accounts/index.html",
                context,
            )
        return redirect("/accounts/login/")

    def post(self, request):
        context = self.get_context(request.user)
        if any(x.startswith("XP for") for x in request.POST.keys()):
            to_remove = [x for x in request.POST.keys() if x.startswith("XP for")][0]
            new_dict = {
                k: v
                for k, v in request.POST.items()
                if k not in [to_remove, "csrfmiddlewaretoken"]
            }
            scene_name = [x for x in request.POST.keys() if x.startswith("XP for")][
                0
            ].split("XP for ")[-1]
            scene = Scene.objects.get(name=scene_name)
            for char in scene.characters.all():
                if char.name in new_dict.keys():
                    char.xp += int(new_dict[char.name])
                    char.save()
            scene.xp_given = True
            scene.save()
        elif "preferred_heading" in request.POST.keys():
            request.user.profile.preferred_heading = request.POST["preferred_heading"]
            request.user.profile.theme = request.POST["theme"]
            request.user.profile.save()
        elif any(x.startswith("image") for x in request.POST.keys()):
            char = [
                x
                for x in context["to_approve_images"]
                if "image " + x.name in request.POST.keys()
            ][0]
            char.image_status = "app"
            char.save()
        else:
            char = [x for x in context["to_approve"] if x.name in request.POST.keys()][
                0
            ]
            char.status = "App"
            char.save()
        context = self.get_context(request.user)
        return render(
            request,
            "accounts/index.html",
            context,
        )

    def get_context(self, user):
        chronicles_sted = [
            x for x in Chronicle.objects.all() if user in x.storytellers.all()
        ]
        to_approve = (
            list(
                Character.objects.filter(
                    status__in=["Un", "Sub"], chronicle__in=chronicles_sted
                ).order_by("name")
            )
            + list(
                LocationModel.objects.filter(
                    status__in=["Un", "Sub"], chronicle__in=chronicles_sted
                ).order_by("name")
            )
            + list(
                ItemModel.objects.filter(
                    status__in=["Un", "Sub"], chronicle__in=chronicles_sted
                ).order_by("name")
            )
        )
        to_approve.sort(key=lambda x: x.name)
        to_approve_images = (
            list(
                Character.objects.filter(
                    chronicle__in=chronicles_sted, image_status="sub"
                ).exclude(image="")
            )
            + list(
                LocationModel.objects.filter(
                    chronicle__in=chronicles_sted, image_status="sub"
                ).exclude(image="")
            )
            + list(
                ItemModel.objects.filter(
                    chronicle__in=chronicles_sted, image_status="sub"
                ).exclude(image="")
            )
        )
        to_approve_images.sort(key=lambda x: x.name)
        return {
            "characters": Character.objects.filter(owner=user).order_by("name"),
            "items": ItemModel.objects.filter(owner=user).order_by("name"),
            "xp_requests": Scene.objects.filter(
                story__chronicle__in=chronicles_sted, finished=True, xp_given=False
            ),
            "locations": LocationModel.objects.filter(owner=user).order_by("name"),
            "to_approve": to_approve,
            "to_approve_images": to_approve_images,
            "update_form": ProfileUpdateForm(),
        }
