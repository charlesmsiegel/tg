"""Users, chronicles and form helpers shared by the chantry view tests."""

from html.parser import HTMLParser

from django.contrib.auth import get_user_model

from game.models import Chronicle, Gameline, STRelationship


def add_chantry_actors(testcase):
    """Attach player, st (Mage ST of chronicle), vampire_st, other_st, staff to testcase."""
    users = get_user_model()
    testcase.player = users.objects.create_user("chantry_player")
    testcase.st = users.objects.create_user("chantry_st")
    testcase.vampire_st = users.objects.create_user("chantry_vampire_st")
    testcase.other_st = users.objects.create_user("chantry_other_st")
    testcase.staff = users.objects.create_user("chantry_staff", is_staff=True)
    testcase.chronicle = Chronicle.objects.create(name="Chantry chronicle")
    testcase.other_chronicle = Chronicle.objects.create(name="Other chronicle")
    mage = Gameline.objects.get_or_create(name="Mage: the Ascension")[0]
    vampire = Gameline.objects.get_or_create(name="Vampire: the Masquerade")[0]
    STRelationship.objects.create(user=testcase.st, chronicle=testcase.chronicle, gameline=mage)
    STRelationship.objects.create(
        user=testcase.vampire_st, chronicle=testcase.chronicle, gameline=vampire
    )
    STRelationship.objects.create(
        user=testcase.other_st, chronicle=testcase.other_chronicle, gameline=mage
    )


class FormValues(HTMLParser):
    """Collect what a browser would submit for every control in a rendered page."""

    def __init__(self):
        super().__init__()
        self.data = {}
        self._select = None
        self._select_multiple = False
        self._first_option = None
        self._textarea = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        name = attrs.get("name")
        if tag == "input" and name and name != "csrfmiddlewaretoken":
            kind = attrs.get("type", "text")
            if kind in {"submit", "button", "reset"}:
                return
            if kind in {"checkbox", "radio"} and "checked" not in attrs:
                return
            self.data.setdefault(name, []).append(attrs.get("value", "on"))
        elif tag == "select" and name:
            self._select = name
            self._select_multiple = "multiple" in attrs
            self._first_option = None
            self.data.setdefault(name, [])
        elif tag == "option" and self._select:
            value = attrs.get("value", "")
            if self._first_option is None:
                self._first_option = value
            if "selected" in attrs:
                self.data[self._select].append(value)
        elif tag == "textarea" and name:
            self._textarea = name
            self.data[name] = [""]

    def handle_endtag(self, tag):
        if tag == "select" and self._select:
            chosen = self.data[self._select]
            if not chosen and not self._select_multiple and self._first_option is not None:
                chosen.append(self._first_option)
            self._select = None
        elif tag == "textarea":
            self._textarea = None

    def handle_data(self, data):
        if self._textarea:
            self.data[self._textarea][0] += data


def submitted_values(response):
    parser = FormValues()
    parser.feed(response.content.decode())
    return parser.data
