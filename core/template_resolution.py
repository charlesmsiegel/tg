"""Specific-then-shared template lookup.

A view keeps naming its gameline- or model-specific template (the override slot)
and adds a shared template after it. Django's ``select_template`` renders the first
name that exists, so a page uses the shared template until someone writes the
specific file, usually as ``{% extends "<shared>" %}`` plus the blocks it changes.

Shared fragments live under ``characters/templates/characters/shared/`` and
``core/templates/core/shared/``; the item/location registry's fallbacks live under
``core/templates/core/registry/``. The view mixins built on this are
``core.mixins.SharedTemplateMixin`` and ``core.mixins.ListHeadingMixin``. See
``docs/architecture/frontend.md``.
"""


def shared_template_names(names, *shared):
    """``names`` followed by each shared fallback, without duplicates, order kept."""
    result = []
    for name in (*names, *shared):
        if name and name not in result:
            result.append(name)
    return result
