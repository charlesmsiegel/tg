from django.db.models import Count, F, Max, Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.views.generic import ListView

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


# vary_on_cookie must sit inside cache_page: SessionMiddleware only adds
# "Vary: Cookie" after the view returns, too late for the cache key, so without
# it one visitor's page (nav, scene tiles) would be served to everyone.
@method_decorator(cache_page(60 * 5), name="dispatch")  # Cache for 5 minutes
@method_decorator(vary_on_cookie, name="dispatch")
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
