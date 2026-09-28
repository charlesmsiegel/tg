"""Template tags for the Tellurium "Spread" design (core/templates/core/tl_base.html).

    {% load tl %}
    {% dots 3 %}                      filled/empty circles, ink or gameline accent
    {% boxes 4 10 %}                  squares (current Willpower, pools)
    {% trait "Strength" 3 "Wiry" %}   label + specialty + dots on one row
    {% track "Willpower" perm=6 temp=4 %}   label + permanent dots over current boxes
    {% fact "Nature" object.nature %}       cover fact row, linked when the value has a URL
    {% qp_wheel 4 2 %}                Mage Quintessence / Paradox wheel
    {{ name|cover_title_class }}      size step for large cover titles
    {{ object|gameline_code }}        "mta", "vtm", ... or "wod"
    {% tl_object_actions %}           submit / approve actions, Spread-styled
"""

import math

from django import template
from django.conf import settings
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe

from core.templatetags.object_actions import object_actions

register = template.Library()


def _int(value):
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


@register.simple_tag
def dots(value, total=5, variant="ink", size=""):
    """<span class="tl-dots"> with ``total`` circles. variant: ink|acc, size: ''|lg."""
    value, total = _int(value), _int(total)
    cls = "tl-dots"
    if variant == "acc":
        cls += " tl-dots--acc"
    if size == "lg":
        cls += " tl-dots--lg"
    inner = format_html_join(
        "",
        '<span class="tl-dot{}"></span>',
        ((" is-on" if i < value else "",) for i in range(total)),
    )
    return format_html(
        '<span class="{}" role="img" aria-label="{} of {}">{}</span>', cls, value, total, inner
    )


@register.simple_tag
def boxes(value, total=10):
    value, total = _int(value), _int(total)
    inner = format_html_join(
        "",
        '<span class="tl-box{}"></span>',
        ((" is-on" if i < value else "",) for i in range(total)),
    )
    return format_html(
        '<span class="tl-boxes" role="img" aria-label="{} of {}">{}</span>', value, total, inner
    )


@register.inclusion_tag("core/tl/trait_row.html")
def trait(label, value, specialty="", total=5, variant="ink", url=""):
    return {
        "label": label,
        "value": value,
        "specialty": specialty,
        "total": total,
        "variant": variant,
        "url": url,
    }


@register.simple_tag
def track(label, perm=None, temp=None, total=10, variant="ink"):
    """Label on the left; permanent dots and/or temporary squares on the right."""
    rows = []
    if perm is not None:
        rows.append(dots(perm, total, variant))
    if temp is not None:
        rows.append(boxes(temp, total))
    return format_html(
        '<div class="tl-track"><span class="tl-track__label">{}</span>'
        '<div class="tl-track__rows">{}</div></div>',
        label,
        mark_safe("".join(rows)),
    )


@register.simple_tag
def fact(label, value, url=None):
    """One cover fact row (mono key, value on the right); nothing when value is empty.

    The value links to ``url``, or to its own ``get_absolute_url()`` when it has one.
    """
    if value is None or value == "":
        return ""
    if url is None and hasattr(value, "get_absolute_url"):
        try:
            url = value.get_absolute_url()
        except Exception:  # noqa: BLE001 - unrouted models simply render as text
            url = None
    inner = format_html('<a href="{}">{}</a>', url, value) if url else format_html("{}", value)
    return format_html(
        '<div class="tl-facts__row"><span class="tl-facts__k">{}</span>'
        '<span class="tl-facts__v">{}</span></div>',
        label,
        inner,
    )


@register.simple_tag
def qp_wheel(quintessence, paradox, label="Quintessence"):
    """20 boxes, index 0 at 189deg running clockwise over the top.

    Box i is Paradox when i >= 20 - paradox, else Quintessence when i < quintessence:
    Paradox wins where the two overlap, as in characters/mage/mage/qp_wheel.html.
    The positions come from trigonometry, so each box carries an inline left/top:
    the one deliberate inline style in the Spread templates.
    """
    q, p = _int(quintessence), _int(paradox)
    parts = []
    for i in range(20):
        a = math.radians(189 + 18 * i)
        left, top = 82 + 72 * math.cos(a) - 7.5, 82 + 72 * math.sin(a) - 7.5
        state = " is-p" if i >= 20 - p else (" is-q" if i < q else "")
        parts.append(
            format_html(
                '<span class="tl-qp__box{}" style="left:{}px;top:{}px"></span>',
                state,
                round(left, 1),
                round(top, 1),
            )
        )
    return format_html(
        '<div class="tl-qp" role="img" aria-label="{} {}, Paradox {}, of 20">{}'
        '<div class="tl-qp__center"><span class="tl-qp__q">{}</span><hr>'
        '<span class="tl-qp__p">{}</span></div></div>',
        label,
        q,
        p,
        mark_safe("".join(parts)),
        q,
        p,
    )


# Display fonts differ in width; a wider face reaches each size step sooner.
TITLE_FONT_FACTORS = {
    "mta": 1.1,
    "vtm": 1.0,
    "wta": 1.1,
    "ctd": 1.0,
    "wto": 0.75,
    "dtf": 1.05,
    "htr": 1.1,
    "mtr": 1.0,
    "wod": 0.8,
}


@register.filter
def cover_title_class(name, gameline="wod"):
    """Size-step class from the longest word, so most titles fit without a client refit.

    ``gameline`` is anything ``gameline_code`` accepts (tuned factor) or a number
    (explicit factor).
    """
    try:
        factor = float(gameline)
    except (TypeError, ValueError):
        factor = TITLE_FONT_FACTORS.get(gameline_code(gameline), 1.0)
    longest = max((len(w) for w in str(name).split()), default=0) * factor
    if longest <= 9:
        return ""
    if longest <= 12:
        return "tl-cover__name--l"
    if longest <= 16:
        return "tl-cover__name--m"
    return "tl-cover__name--s"


@register.filter
def gameline_code(value):
    """Gameline code for ``data-gameline``.

    Accepts a model with ``get_gameline()`` or ``gameline``, a Chronicle (its
    ``headings`` such as "mta_heading"), or a plain string ("mta", "mta_heading").
    Anything unknown falls back to "wod".
    """
    if value is None or value == "":
        return "wod"
    if not isinstance(value, str):
        if hasattr(value, "get_gameline"):
            value = value.get_gameline()
        elif getattr(value, "gameline", None):
            value = value.gameline
        elif hasattr(value, "headings"):
            value = value.headings
        else:
            return "wod"
    code = str(value or "").lower().removesuffix("_heading")
    return code if code in settings.GAMELINES else "wod"


@register.filter
def gameline_name(value):
    """Short gameline name for eyebrows: "Mage", "Vampire", ... ("" for the generic line)."""
    code = gameline_code(value)
    if code == "wod":
        return ""
    return settings.GAMELINES[code]["name"].split(":")[0]


@register.filter
def update_url(obj):
    """obj.get_update_url(), or "" when the model has no update route."""
    try:
        return obj.get_update_url()
    except Exception:  # noqa: BLE001 - NoReverseMatch, NotImplementedError, AttributeError
        return ""


@register.filter
def type_label(obj):
    """The object's display type: get_type() when it has one, else its verbose name."""
    get_type = getattr(obj, "get_type", None)
    if callable(get_type):
        try:
            return get_type()
        except Exception:  # noqa: BLE001
            pass
    meta = getattr(obj, "_meta", None)
    return str(meta.verbose_name).title() if meta else ""


@register.inclusion_tag("core/tl/object_actions.html", takes_context=True)
def tl_object_actions(context):
    """Same permission logic as {% object_actions %}, rendered in Spread markup."""
    return object_actions(context)
