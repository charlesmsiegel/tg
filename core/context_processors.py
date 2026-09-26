from django.contrib.auth.models import AnonymousUser

from game.models import Scene
from game.security import filter_scenes, readable_chronicles


def all_chronicles(request):
    user = getattr(request, "user", AnonymousUser())
    chronicles = readable_chronicles(user)
    visible_scenes = filter_scenes(
        Scene.objects.filter(finished=False, chronicle__in=chronicles), user
    ).select_related("chronicle")
    by_chronicle = {chronicle.pk: [] for chronicle in chronicles}
    for scene in visible_scenes:
        by_chronicle[scene.chronicle_id].append(scene)
    return {
        "chronicles": chronicles,
        "navigation_chronicles": [
            {"chronicle": chronicle, "scenes": by_chronicle[chronicle.pk]}
            for chronicle in chronicles
        ],
    }
