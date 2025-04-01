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
