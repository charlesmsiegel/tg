"""The scene's roll strip (Spread C4): a post's stored roll data, ready to render.

``Post.roll`` holds what ``game.models.roll_record`` wrote when the dice command
was parsed. ``roll_strip`` turns it into the rows ``_post.html`` draws, or
returns ``None`` for posts without it (older rolls, plain posts, damaged data),
which then show their message text as before.
"""

KINDS = {"roll", "stat", "rolls", "extended"}


def plural(count, word, plural_word=None):
    return f"{count} {word if count == 1 else plural_word or word + 's'}"


def outcome(successes, botch):
    if botch:
        return "Botch"
    if successes > 0:
        return plural(successes, "success", "successes")
    return "Failure"


def die_faces(values, difficulty):
    """One tile per die: it meets the difficulty (filled), or it is a 1 (rubric)."""
    faces = []
    for value in values:
        value = int(value)
        if not 1 <= value <= 10:
            raise ValueError(f"not a d10 face: {value}")
        faces.append({"value": value, "hit": value >= difficulty, "one": value == 1})
    return faces


def roll_strip(data):
    """Rows, labels and the result for a post's roll strip, or ``None``."""
    if not isinstance(data, dict) or data.get("kind") not in KINDS:
        return None
    try:
        return _strip(data)
    except (KeyError, TypeError, ValueError):
        return None


def _strip(data):
    kind = data["kind"]
    difficulty = int(data["difficulty"])
    pool = int(data["pool"])
    results = data["rolls"]
    if not isinstance(results, list) or not results:
        raise ValueError("no rolls")

    rows = []
    total = 0
    for number, result in enumerate(results, 1):
        successes = int(result["successes"])
        botch = bool(result["botch"])
        row_difficulty = int(result.get("difficulty", difficulty))
        total += successes
        rows.append(
            {
                "number": number,
                "difficulty": row_difficulty,
                "raised": row_difficulty != difficulty,
                "dice": die_faces(result["dice"], row_difficulty),
                "successes": successes,
                "botch": botch,
                "result": outcome(successes, botch),
                "total": total,
            }
        )

    botch = any(row["botch"] for row in rows)
    tags = [f"Diff {difficulty}"]
    if kind == "extended":
        label = "Extended roll"
        tags.append(f"Target {int(data['target'])}")
    elif kind == "rolls":
        label = plural(int(data.get("requested_rolls", len(rows))), "roll")
    else:
        label = "Roll"
    if data.get("specialty"):
        tags.append("Specialty")
    if data.get("willpower"):
        tags.append("Willpower")

    if kind == "extended":
        target = int(data["target"])
        if botch:
            result = "Botch"
        elif data.get("complete") or total >= target:
            result = f"Success · {plural(len(rows), 'roll')}"
        else:
            result = f"Incomplete · {total} / {target}"
    elif kind == "rolls":
        result = "Botch" if botch else ""
    else:
        result = rows[0]["result"]

    return {
        "kind": kind,
        "label": " · ".join([label, *tags]),
        "pool": str(data.get("pool_label") or "") or plural(pool, "die", "dice"),
        "text": str(data.get("text") or ""),
        "spent": str(data.get("spent") or ""),
        "multi": kind in ("rolls", "extended"),
        "rows": rows,
        "result": result,
        "botch": botch,
    }
