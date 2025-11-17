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
    """
    context = {"notification_count": 0, "notification_breakdown": {}}

    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            breakdown = {}
            count = 0

            # Count unread scenes
            unread_scenes = profile.unread_scenes().count()
            if unread_scenes > 0:
                breakdown["Unread Scenes"] = unread_scenes
                count += unread_scenes

            # Count weekly XP requests (for players)
            weekly_xp = len(profile.get_unfulfilled_weekly_xp_requests())
            if weekly_xp > 0:
                breakdown["Weekly XP Requests"] = weekly_xp
                count += weekly_xp

            # Count XP requests (for STs)
            if profile.is_st():
                # XP requests from scenes
                xp_requests = profile.xp_requests().count()
                if xp_requests > 0:
                    breakdown["Scene XP Requests"] = xp_requests
                    count += xp_requests

                # Count items needing approval
                chars_to_approve = profile.characters_to_approve().count()
                if chars_to_approve > 0:
                    breakdown["Characters to Approve"] = chars_to_approve
                    count += chars_to_approve

                locs_to_approve = profile.locations_to_approve().count()
                if locs_to_approve > 0:
                    breakdown["Locations to Approve"] = locs_to_approve
                    count += locs_to_approve

                items_to_approve = profile.items_to_approve().count()
                if items_to_approve > 0:
                    breakdown["Items to Approve"] = items_to_approve
                    count += items_to_approve

                rotes_to_approve = len(profile.rotes_to_approve())
                if rotes_to_approve > 0:
                    breakdown["Rotes to Approve"] = rotes_to_approve
                    count += rotes_to_approve

                # Freebies to approve
                freebies = len(profile.freebies_to_approve())
                if freebies > 0:
                    breakdown["Freebies to Approve"] = freebies
                    count += freebies

                # XP spend requests
                xp_spend = len(profile.xp_spend_requests())
                if xp_spend > 0:
                    breakdown["XP Spend Requests"] = xp_spend
                    count += xp_spend

                # Count image approvals
                char_images = profile.character_images_to_approve().count()
                if char_images > 0:
                    breakdown["Character Images to Approve"] = char_images
                    count += char_images

                loc_images = profile.location_images_to_approve().count()
                if loc_images > 0:
                    breakdown["Location Images to Approve"] = loc_images
                    count += loc_images

                item_images = profile.item_images_to_approve().count()
                if item_images > 0:
                    breakdown["Item Images to Approve"] = item_images
                    count += item_images

                # Count scenes needing attention
                from game.models import Scene

                scenes_attention = Scene.objects.filter(waiting_for_st=True).count()
                if scenes_attention > 0:
                    breakdown["Scenes Needing Attention"] = scenes_attention
                    count += scenes_attention

                # Count updated journals
                journals = profile.get_updated_journals().count()
                if journals > 0:
                    breakdown["Updated Journals"] = journals
                    count += journals

                # Count weekly XP approvals (for STs)
                weekly_xp_approve = len(
                    profile.get_unfulfilled_weekly_xp_requests_to_approve()
                )
                if weekly_xp_approve > 0:
                    breakdown["Weekly XP to Approve"] = weekly_xp_approve
                    count += weekly_xp_approve

            context["notification_count"] = count
            context["notification_breakdown"] = breakdown
        except Exception:
            # If there's any error, just return 0 notifications
            context["notification_count"] = 0
            context["notification_breakdown"] = {}

    return context
