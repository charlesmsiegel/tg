import logging

from django.core.cache import cache

from accounts.dashboard import ProfileDashboard

logger = logging.getLogger(__name__)


def theme_context(request):
    """
    Add theme-related context variables to all templates.
    """
    context = {}
    if request.user.is_authenticated:
        profile = request.user.profile
        context["user_theme"] = profile.theme
        context["user_highlight_text"] = profile.highlight_text

    return context


def notification_count(request):
    """
    Add notification count and breakdown to all templates for authenticated users.
    Results are cached for 60 seconds to reduce database queries.
    """
    context = {"notification_count": 0, "notification_breakdown": {}}

    if request.user.is_authenticated:
        cache_key = f"notification_count_{request.user.id}"
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

        try:
            profile = request.user.profile
            context = ProfileDashboard(profile).notification_context()

            # Cache for 60 seconds
            cache.set(cache_key, context, 60)

        except Exception as e:
            # Log the error for debugging, but return 0 notifications to avoid breaking the page
            logger.warning(
                f"Error calculating notification count for user {request.user.id}: {e}",
                exc_info=True,
            )
            context["notification_count"] = 0
            context["notification_breakdown"] = {}

    return context
