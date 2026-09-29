from typing import Any

from django.views.generic import DetailView

from items.registry import registry

# Order of the filled cells in the contents strip (C14).
CONTENTS_ORDER = ("Primer", "Practices", "Spheres", "Abilities", "Rotes")


def grimoire_contents(rank, is_primer, practices, spheres, abilities, rotes):
    """The slots of ``Grimoire.has_rotes``: rotes + practices + spheres + abilities,
    plus one for a primer, must equal rank + 3.

    Takes the counts and returns the header numbers, the state ("complete", "under"
    or "over") and one cell per slot in CONTENTS_ORDER. Cells past rank + 3 are
    marked ``over``; slots nothing fills are empty cells.
    """
    counts = dict(
        zip(
            CONTENTS_ORDER,
            (1 if is_primer else 0, practices, spheres, abilities, rotes),
            strict=True,
        )
    )
    total = (rank or 0) + 3
    filled = sum(counts.values())
    cells = [
        {"label": label, "filled": True, "over": False}
        for label in CONTENTS_ORDER
        for _ in range(counts[label])
    ]
    for cell in cells[total:]:
        cell["over"] = True
    cells += [{"label": "", "filled": False, "over": False} for _ in range(total - filled)]
    if filled == total:
        state = "complete"
    elif filled > total:
        state = "over"
    else:
        state = "under"
    return {"rank": rank or 0, "total": total, "filled": filled, "state": state, "cells": cells}


def faction_chain(faction):
    """The faction and its parents, outermost first (Order of Hermes › House Quaesitor)."""
    chain, seen = [], set()
    while faction is not None and faction.pk not in seen:
        seen.add(faction.pk)
        chain.append(faction)
        faction = faction.parent
    return chain[::-1]


class _GrimoireDetailView(DetailView):

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        grimoire = self.object
        practices = list(grimoire.practices.all())
        instruments = list(grimoire.instruments.all())
        abilities = list(grimoire.abilities.all())
        spheres = list(grimoire.spheres.all())
        rotes = list(grimoire.rotes.select_related("practice", "effect", "attribute", "ability"))
        faction = grimoire.faction
        context.update(
            {
                "paradigms": list(faction.get_all_paradigms()) if faction else [],
                "practices": practices,
                "instruments": instruments,
                "abilities": abilities,
                "spheres": spheres,
                "rotes": rotes,
                "faction_chain": faction_chain(faction),
                "year": abs(grimoire.date_written),
                "contents": grimoire_contents(
                    grimoire.rank,
                    grimoire.is_primer,
                    len(practices),
                    len(spheres),
                    len(abilities),
                    len(rotes),
                ),
            }
        )
        return context


GrimoireDetailView = registry.view("items.Grimoire", "detail")


GrimoireListView = registry.view("items.Grimoire", "list")
GrimoireCreateView = registry.view("items.Grimoire", "create")
GrimoireUpdateView = registry.view("items.Grimoire", "update")
