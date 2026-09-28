from django.db.models import Count, F, Max, Q
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from core.cache import cache_page_per_visitor
from core.models import NewsItem
from game.models import Scene
from game.security import filter_scenes, staffed_chronicles

CONTINUE_SCENE_LIMIT = 6


def continue_scenes(user):
    """Unfinished scenes the user plays in or runs, most recently active first."""
    if not user.is_authenticated:
        return Scene.objects.none()
    mine = Scene.objects.filter(finished=False).filter(
        Q(characters__owner=user) | Q(chronicle__in=staffed_chronicles(user))
    )
    visible = filter_scenes(mine, user).values("pk")
    return (
        Scene.objects.filter(pk__in=visible)
        .select_related("chronicle", "location")
        .annotate(post_count=Count("post"), last_post=Max("post__datetime_created"))
        .order_by(F("last_post").desc(nulls_last=True), "-date_played")[:CONTINUE_SCENE_LIMIT]
    )


@method_decorator(cache_page_per_visitor(60 * 5), name="dispatch")  # Cache for 5 minutes
class HomeListView(ListView):
    model = NewsItem
    template_name = "core/index.html"
    context_object_name = "news"
    ordering = ["-date"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["continue_scenes"] = continue_scenes(self.request.user)
        return context
