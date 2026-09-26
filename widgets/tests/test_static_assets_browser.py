"""Real Chromium characterization tests, with no database or driver download.

Run with ``python -m widgets.tests.test_static_assets_browser`` or Django's
test runner. Set TG_BROWSER_BINARY when Chrome/Chromium is not on PATH or in
its standard Windows location. Missing browsers skip; browser failures fail.
"""

import html
import json
import os
import re
import shutil
import subprocess
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from django import forms
from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.signals import request_finished
from django.template import Context, Template
from django.template.loader import render_to_string
from django.test import SimpleTestCase

from widgets.mixins.conditional import ConditionalFieldsMixin
from widgets.widgets.chained import ChainedSelect
from widgets.widgets.create_or_select import CreateOrSelectWidget
from widgets.widgets.filterable import render_filterable_list_script
from widgets.widgets.formset_manager import render_formset_manager_script
from widgets.widgets.metadata_select import OptionMetadataSelect
from widgets.widgets.point_pool import PointPoolInput

ROOT = Path(__file__).resolve().parents[2]
urlpatterns = []


class StaticAssetsBrowserTests(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        candidates = [
            os.environ.get("TG_BROWSER_BINARY"),
            shutil.which("chromium"),
            shutil.which("chromium-browser"),
            shutil.which("google-chrome"),
            "C:/Program Files/Google/Chrome/Application/chrome.exe",
            "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
        ]
        cls.browser = next((p for p in candidates if p and Path(p).is_file()), None)
        if not cls.browser:
            raise unittest.SkipTest("Set TG_BROWSER_BINARY to a local Chromium browser")

    def setUp(self):
        # The original inline implementation resets per-request emission flags.
        request_finished.send(sender=self.__class__)

    def run_browser(self, body, assertions, media=""):
        harness = """
        <script>
        window.addEventListener('load', async () => {
            const result = document.createElement('pre');
            result.id = 'browser-test-result';
            const check = (value, message) => { if (!value) throw Error(message); };
            const get = id => document.getElementById(id);
            const change = (id, value) => {
                get(id).value = value;
                get(id).dispatchEvent(new Event('change', {bubbles:true}));
                get(id).dispatchEvent(new Event('input', {bubbles:true}));
            };
            const visible = id => getComputedStyle(get(id)).display !== 'none';
            try {
                ASSERTIONS
                result.textContent = JSON.stringify({passed: true});
            } catch (error) {
                result.textContent = JSON.stringify({passed: false, error: error.stack});
            }
            document.body.appendChild(result);
        });
        </script>
        """.replace("ASSERTIONS", assertions)
        page = (
            '<!doctype html><html><head><meta charset="utf-8">'
            "<style>.d-none {display:none}</style>"
            + str(media)
            + "</head><body>"
            + str(body)
            + harness
            + "</body></html>"
        ).encode()
        missing = []

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path == "/":
                    content, mime = page, "text/html; charset=utf-8"
                elif self.path.startswith(settings.STATIC_URL):
                    asset = finders.find(self.path.removeprefix(settings.STATIC_URL))
                    if not asset:
                        missing.append(self.path)
                        self.send_error(404)
                        return
                    content, mime = Path(asset).read_bytes(), "text/javascript"
                else:
                    self.send_error(404)
                    return
                self.send_response(200)
                self.send_header("Content-Type", mime)
                self.end_headers()
                self.wfile.write(content)

            def log_message(self, *args):
                pass

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with tempfile.TemporaryDirectory(prefix="tg-browser-") as profile:
                completed = subprocess.run(
                    [
                        self.browser,
                        "--headless=new",
                        "--no-sandbox",
                        "--disable-gpu",
                        "--no-first-run",
                        "--disable-background-networking",
                        f"--user-data-dir={profile}",
                        "--dump-dom",
                        "--virtual-time-budget=1500",
                        f"http://127.0.0.1:{server.server_port}/",
                    ],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    timeout=30,
                )
        finally:
            server.shutdown()
            server.server_close()
            thread.join()
        self.assertFalse(missing, f"Missing static assets: {missing}")
        match = re.search(r'<pre id="browser-test-result">(.*?)</pre>', completed.stdout, re.S)
        self.assertIsNotNone(match, completed.stderr[-3000:] + completed.stdout[-3000:])
        result = json.loads(html.unescape(match.group(1)))
        self.assertTrue(result["passed"], result.get("error"))

    def test_point_pool_totals_and_limits(self):
        first = PointPoolInput(
            pool_name="points",
            is_root=True,
            pool_config={"mode": "simple", "total_budget": 5, "min_value": 0, "max_value": 5},
        )
        second = PointPoolInput(pool_name="points")
        self.run_browser(
            first.render("allies", 1, {"id": "allies"})
            + second.render("contacts", 1, {"id": "contacts"})
            + '<p id="total" data-pool-total="points"></p>',
            """
            check(get('total').textContent.includes('3 points remaining'), 'initial total');
            change('allies', '4');
            check(get('total').textContent.includes('All points allocated'), 'changed total');
            check(get('contacts').max === '1', 'remaining input constrained');
            change('allies', '5');
            check(get('total').textContent.includes('1 point over limit'), 'over budget');
            """,
            first.media + second.media,
        )

    def test_chained_select_populates_and_clears(self):
        root = ChainedSelect(
            chain_name="chain",
            choices=[("", "Choose"), ("a", "A"), ("b", "B")],
            choices_tree={
                "parent:a": [{"value": "one", "label": "One"}],
                "parent:b": [{"value": "two", "label": "Two"}],
            },
        )
        child = ChainedSelect(chain_name="chain", chain_position=1, parent_field="parent")
        self.run_browser(
            root.render("parent", "", {"id": "parent"})
            + child.render("child", "", {"id": "child"}),
            """
            change('parent', 'a');
            check(get('child').options.length === 2, 'populated child');
            check(get('child').options[1].text === 'One', 'first parent choices');
            change('child', 'one');
            change('parent', 'b');
            check(get('child').value === '', 'old selection cleared');
            check(get('child').options[1].value === 'two', 'second parent choices');
            change('parent', '');
            check(get('child').options.length === 1, 'empty parent clears children');
            """,
            root.media + child.media,
        )

    def test_conditional_fields_change_visibility(self):
        class ConditionalForm(ConditionalFieldsMixin, forms.Form):
            category = forms.ChoiceField(choices=[("other", "Other"), ("note", "Note")])
            note = forms.CharField(required=False)
            conditional_fields = {"note": {"visible_when": {"category": {"value_is": "note"}}}}

        form = ConditionalForm()
        self.run_browser(
            str(form["category"]) + form.wrap_field("note") + form.conditional_js(),
            """
            check(!visible('note_wrap'), 'initially hidden');
            change('id_category', 'note');
            check(visible('note_wrap'), 'shown after matching value');
            change('id_category', 'other');
            check(!visible('note_wrap'), 'hidden after nonmatching value');
            """,
            form.media,
        )

    def test_create_or_select_toggle(self):
        widget = CreateOrSelectWidget(group_name="item")
        self.run_browser(
            """
            <div id="existing" data-create-or-select-container="item" data-create-or-select-mode="select">Existing</div>
            <div id="new" data-create-or-select-container="item" data-create-or-select-mode="create">New</div>
            """ + widget.render("create", False, {"id": "create"}),
            """
            check(visible('existing') && !visible('new'), 'initial select mode');
            get('create').click();
            check(!visible('existing') && visible('new'), 'create mode');
            get('create').click();
            check(visible('existing') && !visible('new'), 'return to select');
            """,
            widget.media,
        )

    def test_option_metadata_change_event(self):
        widget = OptionMetadataSelect(
            choices=[("a", "A", {"cost": "2"}), ("b", "B", {"cost": "5"})]
        )
        self.run_browser(
            widget.render("choice", "a", {"id": "choice"}),
            """
            check(OptionMetadata.get('#choice').cost === '2', 'initial metadata');
            let detail;
            get('choice').addEventListener('metadata:change', event => detail = event.detail);
            change('choice', 'b');
            check(detail.value === 'b' && detail.metadata.cost === '5', 'metadata event');
            """,
            widget.media,
        )

    def test_formset_add_remove_and_delete(self):
        self.run_browser(
            """
            <input id="id_items-TOTAL_FORMS" value="1">
            <div data-formset-container data-formset-prefix="items" id="rows">
              <div data-formset-form id="existing"><input name="items-0-title">
                <input type="checkbox" name="items-0-DELETE" id="deleted">
                <button id="delete" data-formset-remove="items">Remove</button></div>
            </div>
            <template id="empty_items_form"><div data-formset-form>
              <input name="items-__prefix__-title" id="id_items-__prefix__-title">
              <button data-formset-remove="items">Remove</button></div></template>
            <button id="add" data-formset-add="items">Add</button>
            """ + render_formset_manager_script(),
            """
            get('add').click();
            get('add').click();
            check(get('id_items-TOTAL_FORMS').value === '3', 'two forms added');
            check(!!get('id_items-2-title'), 'prefix substituted');
            get('rows').children[2].querySelector('button').click();
            check(get('id_items-TOTAL_FORMS').value === '2', 'new form removed');
            check(!!get('id_items-1-title') && !get('id_items-2-title'), 'last row removed');
            get('delete').click();
            check(get('deleted').checked && !visible('existing'), 'existing row marked deleted');
            check(get('id_items-TOTAL_FORMS').value === '2', 'deleted row retained for submission');
            """,
        )

    def test_filterable_list_search_and_clear(self):
        self.run_browser(
            """
            <input id="search" data-filter-input="name"><button id="clear" data-filter-clear>Clear</button>
            <span id="count" data-filter-count></span><div id="empty" data-filter-no-results>No results</div>
            <div data-filterable-list="names"><div id="alpha" data-filterable-item data-name="Alpha">Alpha</div>
            <div id="beta" data-filterable-item data-name="Beta">Beta</div></div>
            """ + render_filterable_list_script(),
            """
            check(visible('alpha') && visible('beta'), 'initial items visible');
            change('search', 'ALP');
            check(visible('alpha') && !visible('beta'), 'case insensitive filtering');
            change('search', 'missing');
            check(!visible('alpha') && !visible('beta') && visible('empty'), 'empty state');
            get('clear').click();
            check(get('search').value === '' && visible('alpha') && visible('beta'), 'clear restores all');
            """,
        )

    def test_attribute_validator_allocation_and_constraints(self):
        names = (
            "strength",
            "dexterity",
            "stamina",
            "charisma",
            "manipulation",
            "appearance",
            "perception",
            "intelligence",
            "wits",
        )
        form = forms.Form()
        form.fields = {name: forms.IntegerField(initial=1) for name in names}
        body = render_to_string(
            "characters/core/attribute_block/form.html",
            {"form": form, "primary": 7, "secondary": 5, "tertiary": 3},
        )
        self.run_browser(
            body,
            """
            check(get('total-remaining').textContent.includes('15 points remaining'), 'initial budget');
            for (const [name, value] of Object.entries({strength:4, dexterity:3, stamina:3,
                charisma:3, manipulation:3, appearance:2, perception:2, intelligence:2, wits:2})) {
                change('id_' + name, String(value));
            }
            check(get('total-remaining').textContent.includes('Complete!'), 'valid 10/8/6 distribution');
            check(get('id_strength').max === '4', 'cannot exceed category limit');
            change('id_strength', '5');
            check(get('total-remaining').textContent.includes('1 point over limit'), 'over allocation');
            """,
            form.media,
        )

    def test_page_media_at_bottom_combines_chained_metadata_and_conditional_fields(self):
        class CombinedForm(ConditionalFieldsMixin, forms.Form):
            category = forms.ChoiceField(
                choices=[("", "Choose"), ("background", "Background")],
                widget=ChainedSelect(
                    chain_name="combined",
                    choices_tree={
                        "category:background": [
                            {
                                "value": "allies",
                                "label": "Allies",
                                "metadata": {"poolable": "true"},
                            },
                            {
                                "value": "contacts",
                                "label": "Contacts",
                                "metadata": {"poolable": "false"},
                            },
                        ]
                    },
                ),
            )
            example = forms.ChoiceField(
                choices=[],
                widget=ChainedSelect(
                    chain_name="combined",
                    chain_position=1,
                    parent_field="category",
                    attrs={"data-metadata-select": "true"},
                ),
            )
            # Load the metadata manager through another widget on the same form.
            rating = forms.ChoiceField(choices=[("1", "One")], widget=OptionMetadataSelect)
            pooled = forms.BooleanField(required=False)
            conditional_fields = {
                "pooled": {"visible_when": {"example": {"metadata_truthy": "poolable"}}}
            }

        page = Template("""
            {% load widget_media %}
            {{ form.category }}{{ form.example }}{{ form.rating }}
            <div id="pooled_wrap">{{ form.pooled }}</div>
            {{ form.conditional_js }}
            {% page_media %}
        """).render(Context({"form": CombinedForm()}))
        self.run_browser(
            page,
            """
            check(!visible('pooled_wrap'), 'conditional state initialized at bottom');
            change('id_category', 'background');
            check(get('id_example').options.length === 3, 'chained options populated');
            let metadataEvents = 0;
            get('id_example').addEventListener('metadata:change', () => metadataEvents++);
            change('id_example', 'allies');
            check(visible('pooled_wrap'), 'metadata enables conditional field');
            change('id_example', 'contacts');
            check(!visible('pooled_wrap'), 'metadata hides conditional field');
            check(metadataEvents === 2, 'one metadata event per selection');
            const sources = Array.from(document.scripts).filter(s => s.src).map(s => s.src);
            check(sources.length === 3 && new Set(sources).size === 3, 'combined media deduplicated');
        """,
        )

    def test_formset_tag_initializes_new_row_widgets_with_bottom_media(self):
        class RowForm(forms.Form):
            choice = forms.ChoiceField(
                choices=[("a", "A"), ("b", "B")],
                widget=OptionMetadataSelect,
            )
            create = forms.BooleanField(required=False, widget=CreateOrSelectWidget)
            points = forms.IntegerField(
                initial=0,
                widget=PointPoolInput(
                    pool_name="dynamic",
                    is_root=True,
                    pool_config={
                        "mode": "simple",
                        "total_budget": 5,
                        "min_value": 0,
                        "max_value": 5,
                    },
                ),
            )

        formset = forms.formset_factory(RowForm, extra=0)(prefix="rows")
        page = Template("""
            {% load formset_tags widget_media %}
            <p id="dynamic-total" data-pool-total="dynamic"></p>
            {% formset formset %}
                {{ subform.choice }}{{ subform.points }}{{ subform.create }}
                <div id="select-{{ subform.prefix }}"
                     data-create-or-select-container="{{ subform.create.html_name }}"
                     data-create-or-select-mode="select">Existing</div>
                <div id="create-{{ subform.prefix }}"
                     data-create-or-select-container="{{ subform.create.html_name }}"
                     data-create-or-select-mode="create">New</div>
            {% endformset %}
            {% page_media %}
        """).render(Context({"formset": formset}))
        self.run_browser(
            page,
            """
            document.querySelector('[data-formset-add]').click();
            check(get('id_rows-TOTAL_FORMS').value === '1', 'empty formset adds row');
            check(visible('select-rows-0') && !visible('create-rows-0'), 'new toggle initialized');
            get('id_rows-0-create').click();
            check(!visible('select-rows-0') && visible('create-rows-0'), 'new toggle responds');
            let changes = 0;
            get('id_rows-0-choice').addEventListener('metadata:change', () => changes++);
            change('id_rows-0-choice', 'b');
            check(changes === 1, 'new metadata widget has one listener');
            change('id_rows-0-points', '3');
            check(get('dynamic-total').textContent.includes('2 points remaining'), 'new point pool responds');
        """,
        )

    def test_chained_ajax_request_protocol_and_response_metadata(self):
        root = ChainedSelect(
            chain_name="remote",
            form_path="allowed.Form",
            choices=[("", "Choose"), ("a & b", "A & B")],
        )
        child = ChainedSelect(
            chain_name="remote",
            chain_position=1,
            parent_field="parent",
            ajax_url="/__chained_select__/",
        )
        self.run_browser(
            root.render("parent", "", {"id": "parent"})
            + child.render("child", "", {"id": "child"})
            + str(root.media + child.media),
            """
            let requested, headers;
            window.fetch = async (url, options) => {
                requested = new URL(url);
                headers = options.headers;
                return {ok: true, json: async () => ({choices: [
                    {value: 'one', label: 'Remote choice', metadata: {poolable: 'true'}}
                ]})};
            };
            change('parent', 'a & b');
            check(get('child').disabled, 'child disabled during request');
            await new Promise(resolve => setTimeout(resolve, 20));
            check(requested.pathname === '/__chained_select__/', 'endpoint unchanged');
            check(requested.searchParams.get('field') === 'child', 'child field sent');
            check(requested.searchParams.get('parent_value') === 'a & b', 'parent value encoded');
            check(requested.searchParams.get('form') === 'allowed.Form', 'form allowlist identifier sent');
            check(headers['X-Requested-With'] === 'XMLHttpRequest', 'AJAX header sent');
            check(!get('child').disabled && get('child').options.length === 2, 'response populated child');
            check(get('child').options[1].dataset.poolable === 'true', 'response metadata preserved');
            change('parent', '');
            check(!get('child').disabled && get('child').options.length === 1, 'empty parent resets child');
        """,
        )


if __name__ == "__main__":
    import django

    settings.configure(
        SECRET_KEY="browser-fixtures",
        STATIC_URL="/static/",
        ROOT_URLCONF=__name__,
        INSTALLED_APPS=["django.contrib.staticfiles", "widgets"],
        STATICFILES_DIRS=[
            ROOT / "source_static",
            ROOT / "characters" / "static",
            ROOT / "core" / "static",
        ],
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [ROOT / "characters" / "templates"],
                "APP_DIRS": True,
                "OPTIONS": {"libraries": {"dots": "core.templatetags.dots"}},
            }
        ],
    )
    django.setup()
    unittest.main(verbosity=2)
