# Template consolidation: analysis output

Output of `python scripts/template_similarity.py --threshold 0.9` at the base commit
(before any Step 8 change) and after the last Step 8 commit. Diffs are against each
group's first member. The remaining byte-identical groups are Step 2's one-line
`chargen.html` stubs and the five four-line gameline sheet templates (level 4 of the
extends policy); the remaining near-identical groups are listed as candidates for
later passes.

## Before

````text
Templates scanned: 890 (generated docs excluded)

## Byte-identical: 17 groups, 91 files

- x21 chargen.html
    characters/templates/characters/changeling/changeling/chargen.html
    characters/templates/characters/changeling/ctdhuman/chargen.html
    characters/templates/characters/core/human/chargen.html
    characters/templates/characters/demon/demon/chargen.html
    characters/templates/characters/demon/dtfhuman/chargen.html
    characters/templates/characters/demon/thrall/chargen.html
    characters/templates/characters/mage/companion/chargen.html
    characters/templates/characters/mage/mage/chargen.html
    characters/templates/characters/mage/mtahuman/chargen.html
    characters/templates/characters/mage/sorcerer/chargen.html
    characters/templates/characters/vampire/ghoul/chargen.html
    characters/templates/characters/vampire/vampire/chargen.html
    characters/templates/characters/vampire/vtmhuman/chargen.html
    characters/templates/characters/werewolf/drone/chargen.html
    characters/templates/characters/werewolf/fera/chargen.html
    characters/templates/characters/werewolf/fomor/chargen.html
    characters/templates/characters/werewolf/garou/chargen.html
    characters/templates/characters/werewolf/kinfolk/chargen.html
    characters/templates/characters/werewolf/wtahuman/chargen.html
    characters/templates/characters/wraith/wraith/chargen.html
    characters/templates/characters/wraith/wtohuman/chargen.html
- x8 history_block_form.html
    characters/templates/characters/changeling/ctdhuman/history_block_form.html
    characters/templates/characters/mage/companion/companion_history_block_form.html
    characters/templates/characters/mage/mtahuman/history_block_form.html
    characters/templates/characters/mage/sorcerer/sorcerer_history_block_form.html
    characters/templates/characters/vampire/vtmhuman/history_block_form.html
    characters/templates/characters/werewolf/fomor/history_block_form.html
    characters/templates/characters/werewolf/wtahuman/history_block_form.html
    characters/templates/characters/wraith/wtohuman/history_block_form.html
- x7 appearance_block_display.html
    characters/templates/characters/changeling/ctdhuman/appearance_block_display.html
    characters/templates/characters/mage/mtahuman/appearance_block_display.html
    characters/templates/characters/mage/sorcerer/sorcerer_appearance_block_display.html
    characters/templates/characters/vampire/vtmhuman/appearance_block_display.html
    characters/templates/characters/werewolf/fomor/appearance_block_display.html
    characters/templates/characters/werewolf/wtahuman/appearance_block_display.html
    characters/templates/characters/wraith/wtohuman/appearance_block_display.html
- x7 freebies_form.html
    characters/templates/characters/changeling/ctdhuman/freebies_form.html
    characters/templates/characters/mage/mtahuman/freebies_form.html
    characters/templates/characters/vampire/vtmhuman/freebies_form.html
    characters/templates/characters/werewolf/fomor/freebies_form.html
    characters/templates/characters/werewolf/kinfolk/freebies_form.html
    characters/templates/characters/werewolf/wtahuman/freebies_form.html
    characters/templates/characters/wraith/wtohuman/freebies_form.html
- x7 history_block_display.html
    characters/templates/characters/changeling/ctdhuman/history_block_display.html
    characters/templates/characters/mage/mtahuman/history_block_display.html
    characters/templates/characters/mage/sorcerer/sorcerer_history_block_display.html
    characters/templates/characters/vampire/vtmhuman/history_block_display.html
    characters/templates/characters/werewolf/fomor/history_block_display.html
    characters/templates/characters/werewolf/wtahuman/history_block_display.html
    characters/templates/characters/wraith/wtohuman/history_block_display.html
- x7 detail.html
    characters/templates/characters/core/archetype/detail.html
    characters/templates/characters/core/derangement/detail.html
    characters/templates/characters/mage/instrument/detail.html
    characters/templates/characters/werewolf/charm/detail.html
    characters/templates/characters/werewolf/fomoripower/detail.html
    core/templates/core/language/detail.html
    items/templates/items/core/material/detail.html
- x6 appearance_block_form.html
    characters/templates/characters/changeling/ctdhuman/appearance_block_form.html
    characters/templates/characters/mage/mtahuman/appearance_block_form.html
    characters/templates/characters/vampire/vtmhuman/appearance_block_form.html
    characters/templates/characters/werewolf/fomor/appearance_block_form.html
    characters/templates/characters/werewolf/wtahuman/appearance_block_form.html
    characters/templates/characters/wraith/wtohuman/appearance_block_form.html
- x6 basics_display_include.html
    characters/templates/characters/changeling/ctdhuman/basics_display_include.html
    characters/templates/characters/mage/mtahuman/basics_display_include.html
    characters/templates/characters/mummy/mtrhuman/basics_display_include.html
    characters/templates/characters/vampire/vtmhuman/basics_display_include.html
    characters/templates/characters/werewolf/wtahuman/basics_display_include.html
    characters/templates/characters/wraith/wtohuman/basics_display_include.html
- x5 specialties_block_form.html
    characters/templates/characters/changeling/ctdhuman/specialties_block_form.html
    characters/templates/characters/mage/mtahuman/specialties_block_form.html
    characters/templates/characters/vampire/vtmhuman/specialties_block_form.html
    characters/templates/characters/werewolf/wtahuman/specialties_block_form.html
    characters/templates/characters/wraith/wtohuman/specialties_block_form.html
- x3 detail.html
    characters/templates/characters/demon/conclave/detail.html
    characters/templates/characters/mage/cabal/detail.html
    characters/templates/characters/wraith/circle/detail.html
- x2 specialties_form.html
    characters/templates/characters/changeling/changeling/specialties_form.html
    characters/templates/characters/werewolf/fomor/specialties_block_form.html
- x2 title.html
    characters/templates/characters/changeling/house/display_includes/title.html
    characters/templates/characters/changeling/legacy/display_includes/title.html
- x2 companion_appearance_block_form.html
    characters/templates/characters/mage/companion/companion_appearance_block_form.html
    characters/templates/characters/mage/sorcerer/sorcerer_appearance_block_form.html
- x2 companion_xp_form.html
    characters/templates/characters/mage/companion/companion_xp_form.html
    characters/templates/characters/mage/sorcerer/sorcerer_xp_form.html
- x2 ghoul_advantage_display.html
    characters/templates/characters/vampire/ghoul/ghoul_advantage_display.html
    characters/templates/characters/vampire/revenant/revenant_advantage_display.html
- x2 ghoul_powers_block_display.html
    characters/templates/characters/vampire/ghoul/ghoul_powers_block_display.html
    characters/templates/characters/vampire/vampire/vampire_powers_block_display.html
- x2 detail.html
    items/templates/items/core/meleeweapon/detail.html
    items/templates/items/core/thrownweapon/detail.html

## Near-identical (>= 0.90): 31 groups, 126 files

### x32 list.html
    core/templates/core/book/list.html  (best sibling 0.900)
    game/templates/game/chronicle/list.html  (best sibling 0.900)
    game/templates/game/story/list.html  (best sibling 0.900)
    items/templates/items/changeling/treasure/list.html  (best sibling 0.900)
    items/templates/items/core/meleeweapon/list.html  (best sibling 0.900)
    items/templates/items/core/rangedweapon/list.html  (best sibling 0.900)
    items/templates/items/core/thrownweapon/list.html  (best sibling 0.900)
    items/templates/items/core/weapon/list.html  (best sibling 0.900)
    items/templates/items/demon/relic/list.html  (best sibling 0.900)
    items/templates/items/mage/artifact/list.html  (best sibling 0.900)
    items/templates/items/mage/charm/list.html  (best sibling 0.900)
    items/templates/items/mage/grimoire/list.html  (best sibling 0.900)
    items/templates/items/mage/periapt/list.html  (best sibling 0.900)
    items/templates/items/mage/sorcerer_artifact/list.html  (best sibling 0.900)
    items/templates/items/mage/talisman/list.html  (best sibling 0.900)
    items/templates/items/mage/wonder/list.html  (best sibling 0.900)
    items/templates/items/vampire/artifact/list.html  (best sibling 0.900)
    items/templates/items/vampire/bloodstone/list.html  (best sibling 0.900)
    items/templates/items/werewolf/fetish/list.html  (best sibling 0.900)
    items/templates/items/werewolf/talen/list.html  (best sibling 0.900)
    items/templates/items/wraith/artifact/list.html  (best sibling 0.900)
    items/templates/items/wraith/relic/list.html  (best sibling 0.900)
    locations/templates/locations/core/city/list.html  (best sibling 0.900)
    locations/templates/locations/demon/bastion/list.html  (best sibling 0.900)
    locations/templates/locations/demon/reliquary/list.html  (best sibling 0.900)
    locations/templates/locations/mage/demesne/list.html  (best sibling 0.900)
    locations/templates/locations/mage/library/list.html  (best sibling 0.900)
    locations/templates/locations/mage/node/list.html  (best sibling 0.900)
    locations/templates/locations/mage/realm/list.html  (best sibling 0.900)
    locations/templates/locations/mage/sanctum/list.html  (best sibling 0.900)
    locations/templates/locations/mage/sector/list.html  (best sibling 0.900)
    locations/templates/locations/werewolf/caern/list.html  (best sibling 0.900)
```diff
--- core/templates/core/book/list.html
+++ game/templates/game/chronicle/list.html
@@ -3 +3 @@
-    Books
+    Chronicles
@@ -9 +9 @@
-                <h3 class="tg-card-title wod_heading">Books</h3>
+                <h3 class="tg-card-title wod_heading">Chronicles</h3>
@@ -23 +23 @@
-                            <p class="text-muted">No books found.</p>
+                            <p class="text-muted">No chronicles found.</p>
--- core/templates/core/book/list.html
+++ game/templates/game/story/list.html
@@ -3 +3 @@
-    Books
+    Stories
@@ -9 +9 @@
-                <h3 class="tg-card-title wod_heading">Books</h3>
+                <h3 class="tg-card-title wod_heading">Stories</h3>
@@ -23 +23 @@
-                            <p class="text-muted">No books found.</p>
+                            <p class="text-muted">No stories found.</p>
--- core/templates/core/book/list.html
+++ items/templates/items/changeling/treasure/list.html
@@ -3 +3 @@
-    Books
+    Changeling Treasures
@@ -9 +9 @@
-                <h3 class="tg-card-title wod_heading">Books</h3>
+                <h3 class="tg-card-title ctd_heading">Changeling Treasures</h3>
@@ -23 +23 @@
-                            <p class="text-muted">No books found.</p>
+                            <p class="text-muted">No changeling treasures found.</p>
--- core/templates/core/book/list.html
+++ items/templates/items/core/meleeweapon/list.html
@@ -3 +3 @@
-    Books
+    Melee Weapons
@@ -9 +9 @@
-                <h3 class="tg-card-title wod_heading">Books</h3>
+                <h3 class="tg-card-title wod_heading">Melee Weapons</h3>
@@ -23 +23 @@
-                            <p class="text-muted">No books found.</p>
+                            <p class="text-muted">No melee weapons found.</p>
--- core/templates/core/book/list.html
+++ items/templates/items/core/rangedweapon/list.html
@@ -3 +3 @@
-    Books
+    Ranged Weapons
@@ -9 +9 @@
-                <h3 class="tg-card-title wod_heading">Books</h3>
+                <h3 class="tg-card-title wod_heading">Ranged Weapons</h3>
@@ -23 +23 @@
-                            <p class="text-muted">No books found.</p>
+                            <p class="text-muted">No ranged weapons found.</p>
--- core/templates/core/book/list.html
+++ items/templates/items/core/thrownweapon/list.html
@@ -3 +3 @@
-    Books
+    Thrown Weapons
@@ -9 +9 @@
-                <h3 class="tg-card-title wod_heading">Books</h3>
+                <h3 class="tg-card-title wod_heading">Thrown Weapons</h3>
@@ -23 +23 @@
-                            <p class="text-muted">No books found.</p>
+                            <p class="text-muted">No thrown weapons found.</p>
--- core/templates/core/book/list.html
+++ items/templates/items/core/weapon/list.html
@@ -3 +3 @@
-    Books
+    Weapons
@@ -9 +9 @@
-                <h3 class="tg-card-title wod_heading">Books</h3>
+                <h3 class="tg-card-title wod_heading">Weapons</h3>
@@ -23 +23 @@
-                            <p class="text-muted">No books found.</p>
+                            <p class="text-muted">No weapons found.</p>
--- core/templates/core/book/list.html
+++ items/templates/items/demon/relic/list.html
@@ -3 +3 @@
-    Books
+    Demon Relics
@@ -9 +9 @@
-                <h3 class="tg-card-title wod_heading">Books</h3>
+                <h3 class="tg-card-title dtf_heading">Demon Relics</h3>
@@ -23 +23 @@
-                            <p class="text-muted">No books found.</p>
+                            <p class="text-muted">No demon relics found.</p>
--- core/templates/core/book/list.html
+++ items/templates/items/mage/artifact/list.html
@@ -3 +3 @@
-    Books
+    Artifacts
@@ -9 +9 @@
-                <h3 class="tg-card-title wod_heading">Books</h3>
+                <h3 class="tg-card-title mta_heading">Artifacts</h3>
@@ -23 +23 @@
-                            <p class="text-muted">No books found.</p>
+                            <p class="text-muted">No artifacts found.</p>
--- core/templates/core/book/list.html
+++ items/templates/items/mage/charm/list.html
@@ -3 +3 @@
-    Books
+    Charms
@@ -9 +9 @@
-                <h3 class="tg-card-title wod_heading">Books</h3>
+                <h3 class="tg-card-title mta_heading">Charms</h3>
@@ -23 +23 @@
-                            <p class="text-muted">No books found.</p>
+                            <p class="text-muted">No charms found.</p>
--- core/templates/core/book/list.html
+++ items/templates/items/mage/grimoire/list.html
@@ -3 +3 @@
-    Books
+    Grimoires
@@ -9 +9 @@
-                <h3 class="tg-card-title wod_heading">Books</h3>
+                <h3 class="tg-card-title mta_heading">Grimoires</h3>
@@ -23 +23 @@
-                            <p class="text-muted">No books found.</p>
+                            <p class="text-muted">No grimoires found.</p>
--- core/templates/core/book/list.html
+++ items/templates/items/mage/periapt/list.html
@@ -3 +3 @@
-    Books
+    Periapts
@@ -9 +9 @@
-                <h3 class="tg-card-title wod_heading">Books</h3>
+                <h3 class="tg-card-title mta_heading">Periapts</h3>
@@ -23 +23 @@
-                            <p class="text-muted">No books found.</p>
+                            <p class="text-muted">No periapts found.</p>
--- core/templates/core/book/list.html
+++ items/templates/items/mage/sorcerer_artifact/list.html
@@ -3 +3 @@
-    Books
+    Sorcerer Artifacts
@@ -9 +9 @@
-                <h3 class="tg-card-title wod_heading">Books</h3>
+                <h3 class="tg-card-title mta_heading">Sorcerer Artifacts</h3>
@@ -23 +23 @@
-                            <p class="text-muted">No books found.</p>
+                            <p class="text-muted">No sorcerer artifacts found.</p>
--- core/templates/core/book/list.html
+++ items/templates/items/mage/talisman/list.html
@@ -3 +3 @@
-    Books
+    Talismans
@@ -9 +9 @@
-                <h3 class="tg-card-title wod_heading">Books</h3>
+                <h3 class="tg-card-title mta_heading">Talismans</h3>
@@ -23 +23 @@
-                            <p class="text-muted">No books found.</p>
+                            <p class="text-muted">No talismans found.</p>
--- core/templates/core/book/list.html
+++ items/templates/items/mage/wonder/list.html
@@ -3 +3 @@
-    Books
+    Wonders
@@ -9 +9 @@
-                <h3 class="tg-card-title wod_heading">Books</h3>
+                <h3 class="tg-card-title mta_heading">Wonders</h3>
@@ -23 +23 @@
-                            <p class="text-muted">No books found.</p>
+                            <p class="text-muted">No wonders found.</p>
--- core/templates/core/book/list.html
+++ items/templates/items/vampire/artifact/list.html
@@ -3 +3 @@
-    Books
+    Vampire Artifacts
@@ -9 +9 @@
-                <h3 class="tg-card-title wod_heading">Books</h3>
+                <h3 class="tg-card-title vtm_heading">Vampire Artifacts</h3>
@@ -23 +23 @@
-                            <p class="text-muted">No books found.</p>
+                            <p class="text-muted">No vampire artifacts found.</p>
--- core/templates/core/book/list.html
+++ items/templates/items/vampire/bloodstone/list.html
@@ -3 +3 @@
-    Books
+    Bloodstones
@@ -9 +9 @@
-                <h3 class="tg-card-title wod_heading">Books</h3>
+                <h3 class="tg-card-title vtm_heading">Bloodstones</h3>
@@ -23 +23 @@
-                            <p class="text-muted">No books found.</p>
+                            <p class="text-muted">No bloodstones found.</p>
--- core/templates/core/book/list.html
+++ items/templates/items/werewolf/fetish/list.html
@@ -3 +3 @@
-    Books
+    Fetishes
@@ -9 +9 @@
-                <h3 class="tg-card-title wod_heading">Books</h3>
+                <h3 class="tg-card-title wta_heading">Fetishes</h3>
@@ -23 +23 @@
-                            <p class="text-muted">No books found.</p>
+                            <p class="text-muted">No fetishes found.</p>
--- core/templates/core/book/list.html
+++ items/templates/items/werewolf/talen/list.html
@@ -3 +3 @@
-    Books
+    Talens
@@ -9 +9 @@
-                <h3 class="tg-card-title wod_heading">Books</h3>
+                <h3 class="tg-card-title wta_heading">Talens</h3>
@@ -23 +23 @@
-                            <p class="text-muted">No books found.</p>
+                            <p class="text-muted">No talens found.</p>
--- core/templates/core/book/list.html
+++ items/templates/items/wraith/artifact/list.html
@@ -3 +3 @@
-    Books
+    Wraith Artifacts
@@ -9 +9 @@
-                <h3 class="tg-card-title wod_heading">Books</h3>
+                <h3 class="tg-card-title wto_heading">Wraith Artifacts</h3>
@@ -23 +23 @@
-                            <p class="text-muted">No books found.</p>
+                            <p class="text-muted">No wraith artifacts found.</p>
--- core/templates/core/book/list.html
+++ items/templates/items/wraith/relic/list.html
@@ -3 +3 @@
-    Books
+    Wraith Relics
@@ -9 +9 @@
-                <h3 class="tg-card-title wod_heading">Books</h3>
+                <h3 class="tg-card-title wto_heading">Wraith Relics</h3>
@@ -23 +23 @@
-                            <p class="text-muted">No books found.</p>
+                            <p class="text-muted">No wraith relics found.</p>
--- core/templates/core/book/list.html
+++ locations/templates/locations/core/city/list.html
@@ -3 +3 @@
-    Books
+    Cities
@@ -9 +9 @@
-                <h3 class="tg-card-title wod_heading">Books</h3>
+                <h3 class="tg-card-title wod_heading">Cities</h3>
@@ -23 +23 @@
-                            <p class="text-muted">No books found.</p>
+                            <p class="text-muted">No cities found.</p>
--- core/templates/core/book/list.html
+++ locations/templates/locations/demon/bastion/list.html
@@ -3 +3 @@
-    Books
+    Bastions
@@ -9 +9 @@
-                <h3 class="tg-card-title wod_heading">Books</h3>
+                <h3 class="tg-card-title dtf_heading">Bastions</h3>
@@ -23 +23 @@
-                            <p class="text-muted">No books found.</p>
+                            <p class="text-muted">No bastions found.</p>
--- core/templates/core/book/list.html
+++ locations/templates/locations/demon/reliquary/list.html
@@ -3 +3 @@
-    Books
+    Reliquaries
@@ -9 +9 @@
-                <h3 class="tg-card-title wod_heading">Books</h3>
+                <h3 class="tg-card-title dtf_heading">Reliquaries</h3>
@@ -23 +23 @@
-                            <p class="text-muted">No books found.</p>
+                            <p class="text-muted">No reliquaries found.</p>
--- core/templates/core/book/list.html
+++ locations/templates/locations/mage/demesne/list.html
@@ -3 +3 @@
-    Books
+    Demesnes
@@ -9 +9 @@
-                <h3 class="tg-card-title wod_heading">Books</h3>
+                <h3 class="tg-card-title mta_heading">Demesnes</h3>
@@ -23 +23 @@
-                            <p class="text-muted">No books found.</p>
+                            <p class="text-muted">No demesnes found.</p>
--- core/templates/core/book/list.html
+++ locations/templates/locations/mage/library/list.html
@@ -3 +3 @@
-    Books
+    Libraries
@@ -9 +9 @@
-                <h3 class="tg-card-title wod_heading">Books</h3>
+                <h3 class="tg-card-title mta_heading">Libraries</h3>
@@ -23 +23 @@
-                            <p class="text-muted">No books found.</p>
+                            <p class="text-muted">No libraries found.</p>
--- core/templates/core/book/list.html
+++ locations/templates/locations/mage/node/list.html
@@ -3 +3 @@
-    Books
+    Nodes
@@ -9 +9 @@
-                <h3 class="tg-card-title wod_heading">Books</h3>
+                <h3 class="tg-card-title mta_heading">Nodes</h3>
@@ -23 +23 @@
-                            <p class="text-muted">No books found.</p>
+                            <p class="text-muted">No nodes found.</p>
--- core/templates/core/book/list.html
+++ locations/templates/locations/mage/realm/list.html
@@ -3 +3 @@
-    Books
+    Horizon Realms
@@ -9 +9 @@
-                <h3 class="tg-card-title wod_heading">Books</h3>
+                <h3 class="tg-card-title mta_heading">Horizon Realms</h3>
@@ -23 +23 @@
-                            <p class="text-muted">No books found.</p>
+                            <p class="text-muted">No horizon realms found.</p>
--- core/templates/core/book/list.html
+++ locations/templates/locations/mage/sanctum/list.html
@@ -3 +3 @@
-    Books
+    Sanctums
@@ -9 +9 @@
-                <h3 class="tg-card-title wod_heading">Books</h3>
+                <h3 class="tg-card-title mta_heading">Sanctums</h3>
@@ -23 +23 @@
-                            <p class="text-muted">No books found.</p>
+                            <p class="text-muted">No sanctums found.</p>
--- core/templates/core/book/list.html
+++ locations/templates/locations/mage/sector/list.html
@@ -3 +3 @@
-    Books
+    Sectors
@@ -9 +9 @@
-                <h3 class="tg-card-title wod_heading">Books</h3>
+                <h3 class="tg-card-title mta_heading">Sectors</h3>
@@ -23 +23 @@
-                            <p class="text-muted">No books found.</p>
+                            <p class="text-muted">No sectors found.</p>
--- core/templates/core/book/list.html
+++ locations/templates/locations/werewolf/caern/list.html
@@ -3 +3 @@
-    Books
+    Caerns
@@ -9 +9 @@
-                <h3 class="tg-card-title wod_heading">Books</h3>
+                <h3 class="tg-card-title wta_heading">Caerns</h3>
@@ -23 +23 @@
-                            <p class="text-muted">No books found.</p>
+                            <p class="text-muted">No caerns found.</p>
```

### x8 basics.html
    characters/templates/characters/changeling/ctdhuman/basics.html  (best sibling 0.965)
    characters/templates/characters/mage/mtahuman/basics.html  (best sibling 0.965)
    characters/templates/characters/vampire/vtmhuman/basics.html  (best sibling 0.965)
    characters/templates/characters/werewolf/fomor/basics.html  (best sibling 0.965)
    characters/templates/characters/werewolf/kinfolk/basics.html  (best sibling 0.902)
    characters/templates/characters/werewolf/wtahuman/basics.html  (best sibling 0.965)
    characters/templates/characters/wraith/wraith/basics.html  (best sibling 0.931)
    characters/templates/characters/wraith/wtohuman/basics.html  (best sibling 0.965)
```diff
--- characters/templates/characters/changeling/ctdhuman/basics.html
+++ characters/templates/characters/mage/mtahuman/basics.html
@@ -3 +3 @@
-    Create Human (Changeling)
+    Create Human (Mage)
@@ -7 +7 @@
-    id="ctdhumanForm"
+    id="mageHumanForm"
--- characters/templates/characters/changeling/ctdhuman/basics.html
+++ characters/templates/characters/vampire/vtmhuman/basics.html
@@ -3 +3 @@
-    Create Human (Changeling)
+    Create Human (Vampire)
@@ -7 +7 @@
-    id="ctdhumanForm"
+    id="vtmhumanForm"
--- characters/templates/characters/changeling/ctdhuman/basics.html
+++ characters/templates/characters/werewolf/fomor/basics.html
@@ -3 +3 @@
-    Create Human (Changeling)
+    Create Fomor
@@ -7 +7 @@
-    id="ctdhumanForm"
+    id="mageForm"
--- characters/templates/characters/changeling/ctdhuman/basics.html
+++ characters/templates/characters/werewolf/kinfolk/basics.html
@@ -3 +3 @@
-    Create Human (Changeling)
+    Create Kinfolk
@@ -7 +7 @@
-    id="ctdhumanForm"
+    id="mageForm"
@@ -15 +15 @@
-        <div class="col-sm">Decide identity and motivation; choose concept and Archetypes.</div>
+        <div class="col-sm">Decide identity and motivation; choose concept, Tribe, Breed, Relation and Archetypes.</div>
@@ -28,0 +29,2 @@
+            <div class="col-sm-2">Tribe</div>
+            <div class="col-sm-2">{{ form.tribe }}</div>
@@ -34,0 +37,2 @@
+            <div class="col-sm-2">Breed</div>
+            <div class="col-sm-2">{{ form.breed }}</div>
@@ -36,0 +41,2 @@
+            <div class="col-sm-2"></div>
+            <div class="col-sm-2"></div>
@@ -38,0 +45,2 @@
+            <div class="col-sm-2">Relation</div>
+            <div class="col-sm-2">{{ form.relation }}</div>
--- characters/templates/characters/changeling/ctdhuman/basics.html
+++ characters/templates/characters/werewolf/wtahuman/basics.html
@@ -3 +3 @@
-    Create Human (Changeling)
+    Create Human (Werewolf)
@@ -7 +7 @@
-    id="ctdhumanForm"
+    id="wtahumanForm"
--- characters/templates/characters/changeling/ctdhuman/basics.html
+++ characters/templates/characters/wraith/wraith/basics.html
@@ -3 +3 @@
-    Create Human (Changeling)
+    Create Wraith
@@ -7 +7 @@
-    id="ctdhumanForm"
+    id="wraithForm"
@@ -15 +15 @@
-        <div class="col-sm">Decide identity and motivation; choose concept and Archetypes.</div>
+        <div class="col-sm">Decide identity, motivation, and Guild; choose concept and Archetypes.</div>
@@ -38,0 +39,2 @@
+            <div class="col-sm-2">Guild</div>
+            <div class="col-sm-2">{{ form.guild }}</div>
--- characters/templates/characters/changeling/ctdhuman/basics.html
+++ characters/templates/characters/wraith/wtohuman/basics.html
@@ -3 +3 @@
-    Create Human (Changeling)
+    Create Human (Wraith)
@@ -7 +7 @@
-    id="ctdhumanForm"
+    id="wtoHumanForm"
```

### x6 template_select.html
    characters/templates/characters/changeling/ctdhuman/template_select.html  (best sibling 0.969)
    characters/templates/characters/demon/dtfhuman/template_select.html  (best sibling 0.969)
    characters/templates/characters/mage/mtahuman/template_select.html  (best sibling 0.969)
    characters/templates/characters/vampire/vtmhuman/template_select.html  (best sibling 0.969)
    characters/templates/characters/werewolf/wtahuman/template_select.html  (best sibling 0.969)
    characters/templates/characters/wraith/wtohuman/template_select.html  (best sibling 0.969)
```diff
--- characters/templates/characters/changeling/ctdhuman/template_select.html
+++ characters/templates/characters/demon/dtfhuman/template_select.html
@@ -8 +8 @@
-<div class="tg-card mb-4" data-gameline="ctd">
+<div class="tg-card mb-4" data-gameline="dtf">
@@ -10 +10 @@
-        <h4 class="tg-card-title ctd_heading">Choose a Starting Template (Optional)</h4>
+        <h4 class="tg-card-title dtf_heading">Choose a Starting Template (Optional)</h4>
@@ -52 +52 @@
-                                <h6 class="tg-card-title ctd_heading" style="margin-bottom: 4px; font-weight: 700;">
+                                <h6 class="tg-card-title dtf_heading" style="margin-bottom: 4px; font-weight: 700;">
@@ -126 +126 @@
-<script src="{% static 'characters/js/ctdhuman-template-select.js' %}"></script>
+<script src="{% static 'characters/js/dtfhuman-template-select.js' %}"></script>
--- characters/templates/characters/changeling/ctdhuman/template_select.html
+++ characters/templates/characters/mage/mtahuman/template_select.html
@@ -8 +8 @@
-<div class="tg-card mb-4" data-gameline="ctd">
+<div class="tg-card mb-4" data-gameline="mta">
@@ -10 +10 @@
-        <h4 class="tg-card-title ctd_heading">Choose a Starting Template (Optional)</h4>
+        <h4 class="tg-card-title mta_heading">Choose a Starting Template (Optional)</h4>
@@ -52 +52 @@
-                                <h6 class="tg-card-title ctd_heading" style="margin-bottom: 4px; font-weight: 700;">
+                                <h6 class="tg-card-title mta_heading" style="margin-bottom: 4px; font-weight: 700;">
@@ -126 +126 @@
-<script src="{% static 'characters/js/ctdhuman-template-select.js' %}"></script>
+<script src="{% static 'characters/js/mtahuman-template-select.js' %}"></script>
--- characters/templates/characters/changeling/ctdhuman/template_select.html
+++ characters/templates/characters/vampire/vtmhuman/template_select.html
@@ -8 +8 @@
-<div class="tg-card mb-4" data-gameline="ctd">
+<div class="tg-card mb-4" data-gameline="vtm">
@@ -10 +10 @@
-        <h4 class="tg-card-title ctd_heading">Choose a Starting Template (Optional)</h4>
+        <h4 class="tg-card-title vtm_heading">Choose a Starting Template (Optional)</h4>
@@ -52 +52 @@
-                                <h6 class="tg-card-title ctd_heading" style="margin-bottom: 4px; font-weight: 700;">
+                                <h6 class="tg-card-title vtm_heading" style="margin-bottom: 4px; font-weight: 700;">
@@ -126 +126 @@
-<script src="{% static 'characters/js/ctdhuman-template-select.js' %}"></script>
+<script src="{% static 'characters/js/vtmhuman-template-select.js' %}"></script>
--- characters/templates/characters/changeling/ctdhuman/template_select.html
+++ characters/templates/characters/werewolf/wtahuman/template_select.html
@@ -8 +8 @@
-<div class="tg-card mb-4" data-gameline="ctd">
+<div class="tg-card mb-4" data-gameline="wta">
@@ -10 +10 @@
-        <h4 class="tg-card-title ctd_heading">Choose a Starting Template (Optional)</h4>
+        <h4 class="tg-card-title wta_heading">Choose a Starting Template (Optional)</h4>
@@ -52 +52 @@
-                                <h6 class="tg-card-title ctd_heading" style="margin-bottom: 4px; font-weight: 700;">
+                                <h6 class="tg-card-title wta_heading" style="margin-bottom: 4px; font-weight: 700;">
@@ -126 +126 @@
-<script src="{% static 'characters/js/ctdhuman-template-select.js' %}"></script>
+<script src="{% static 'characters/js/wtahuman-template-select.js' %}"></script>
--- characters/templates/characters/changeling/ctdhuman/template_select.html
+++ characters/templates/characters/wraith/wtohuman/template_select.html
@@ -8 +8 @@
-<div class="tg-card mb-4" data-gameline="ctd">
+<div class="tg-card mb-4" data-gameline="wto">
@@ -10 +10 @@
-        <h4 class="tg-card-title ctd_heading">Choose a Starting Template (Optional)</h4>
+        <h4 class="tg-card-title wto_heading">Choose a Starting Template (Optional)</h4>
@@ -52 +52 @@
-                                <h6 class="tg-card-title ctd_heading" style="margin-bottom: 4px; font-weight: 700;">
+                                <h6 class="tg-card-title wto_heading" style="margin-bottom: 4px; font-weight: 700;">
@@ -126 +126 @@
-<script src="{% static 'characters/js/ctdhuman-template-select.js' %}"></script>
+<script src="{% static 'characters/js/wtohuman-template-select.js' %}"></script>
```

### x6 detail.html
    locations/templates/locations/vampire/barrens/detail.html  (best sibling 0.960)
    locations/templates/locations/vampire/chantry/detail.html  (best sibling 0.960)
    locations/templates/locations/vampire/domain/detail.html  (best sibling 0.960)
    locations/templates/locations/vampire/elysium/detail.html  (best sibling 0.960)
    locations/templates/locations/vampire/haven/detail.html  (best sibling 0.941)
    locations/templates/locations/vampire/rack/detail.html  (best sibling 0.960)
```diff
--- locations/templates/locations/vampire/barrens/detail.html
+++ locations/templates/locations/vampire/chantry/detail.html
@@ -23 +23 @@
-        {% include "locations/vampire/barrens/display_includes/basics.html" %}
+        {% include "locations/vampire/chantry/display_includes/basics.html" %}
--- locations/templates/locations/vampire/barrens/detail.html
+++ locations/templates/locations/vampire/domain/detail.html
@@ -23 +23 @@
-        {% include "locations/vampire/barrens/display_includes/basics.html" %}
+        {% include "locations/vampire/domain/display_includes/basics.html" %}
--- locations/templates/locations/vampire/barrens/detail.html
+++ locations/templates/locations/vampire/elysium/detail.html
@@ -23 +23 @@
-        {% include "locations/vampire/barrens/display_includes/basics.html" %}
+        {% include "locations/vampire/elysium/display_includes/basics.html" %}
--- locations/templates/locations/vampire/barrens/detail.html
+++ locations/templates/locations/vampire/haven/detail.html
@@ -23 +23,2 @@
-        {% include "locations/vampire/barrens/display_includes/basics.html" %}
+        {% include "locations/vampire/haven/display_includes/basics.html" %}
+        {% include "characters/core/meritflaw/display_includes/meritflaw_block.html" %}
--- locations/templates/locations/vampire/barrens/detail.html
+++ locations/templates/locations/vampire/rack/detail.html
@@ -23 +23 @@
-        {% include "locations/vampire/barrens/display_includes/basics.html" %}
+        {% include "locations/vampire/rack/display_includes/basics.html" %}
```

### x5 list.html
    characters/templates/characters/changeling/motley/list.html  (best sibling 0.932)
    characters/templates/characters/demon/conclave/list.html  (best sibling 0.936)
    characters/templates/characters/mage/cabal/list.html  (best sibling 0.936)
    characters/templates/characters/vampire/coterie/list.html  (best sibling 0.932)
    characters/templates/characters/wraith/circle/list.html  (best sibling 0.936)
```diff
--- characters/templates/characters/changeling/motley/list.html
+++ characters/templates/characters/demon/conclave/list.html
@@ -3 +3 @@
-    Motleys
+    Conclaves
@@ -11 +11 @@
-                        <h3 class="tg-card-title ctd_heading">Motleys</h3>
+                        <h3 class="tg-card-title dtf_heading">Conclaves</h3>
@@ -23,0 +24,3 @@
+                                    <span style="font-size: 0.9rem; color: var(--theme-text-secondary);">
+                                        {{ obj.get_display_type }}
+                                    </span>
@@ -39 +42 @@
-                    <p class="text-center" style="color: var(--theme-text-secondary);">No motleys found.</p>
+                    <p class="text-center" style="color: var(--theme-text-secondary);">No conclaves found.</p>
--- characters/templates/characters/changeling/motley/list.html
+++ characters/templates/characters/mage/cabal/list.html
@@ -3 +3 @@
-    Motleys
+    Cabals
@@ -11 +11 @@
-                        <h3 class="tg-card-title ctd_heading">Motleys</h3>
+                        <h3 class="tg-card-title mta_heading">Cabals</h3>
@@ -23,0 +24,3 @@
+                                    <span style="font-size: 0.9rem; color: var(--theme-text-secondary);">
+                                        {{ obj.get_display_type }}
+                                    </span>
@@ -39 +42 @@
-                    <p class="text-center" style="color: var(--theme-text-secondary);">No motleys found.</p>
+                    <p class="text-center" style="color: var(--theme-text-secondary);">No cabals found.</p>
--- characters/templates/characters/changeling/motley/list.html
+++ characters/templates/characters/vampire/coterie/list.html
@@ -3 +3 @@
-    Motleys
+    Coteries
@@ -11 +11 @@
-                        <h3 class="tg-card-title ctd_heading">Motleys</h3>
+                        <h3 class="tg-card-title vtm_heading">Coteries</h3>
@@ -39 +39 @@
-                    <p class="text-center" style="color: var(--theme-text-secondary);">No motleys found.</p>
+                    <p class="text-center" style="color: var(--theme-text-secondary);">No coteries found.</p>
--- characters/templates/characters/changeling/motley/list.html
+++ characters/templates/characters/wraith/circle/list.html
@@ -3 +3 @@
-    Motleys
+    Circles
@@ -11 +11 @@
-                        <h3 class="tg-card-title ctd_heading">Motleys</h3>
+                        <h3 class="tg-card-title wto_heading">Circles</h3>
@@ -23,0 +24,3 @@
+                                    <span style="font-size: 0.9rem; color: var(--theme-text-secondary);">
+                                        {{ obj.get_display_type }}
+                                    </span>
@@ -39 +42 @@
-                    <p class="text-center" style="color: var(--theme-text-secondary);">No motleys found.</p>
+                    <p class="text-center" style="color: var(--theme-text-secondary);">No circles found.</p>
```

### x4 form.html
    characters/templates/characters/core/archetype/form.html  (best sibling 0.929)
    characters/templates/characters/core/derangement/form.html  (best sibling 0.929)
    characters/templates/characters/mage/instrument/form.html  (best sibling 0.929)
    characters/templates/characters/werewolf/fomoripower/form.html  (best sibling 0.929)
```diff
--- characters/templates/characters/core/archetype/form.html
+++ characters/templates/characters/core/derangement/form.html
@@ -3 +3 @@
-    Create Archetype
+    Create Derangement
--- characters/templates/characters/core/archetype/form.html
+++ characters/templates/characters/mage/instrument/form.html
@@ -3 +3 @@
-    Create Archetype
+    Create Instrument
--- characters/templates/characters/core/archetype/form.html
+++ characters/templates/characters/werewolf/fomoripower/form.html
@@ -3 +3 @@
-    Create Archetype
+    Create Fomori Power
```

### x4 ability_block_display.html
    characters/templates/characters/mage/mtahuman/ability_block_display.html  (best sibling 0.934)
    characters/templates/characters/vampire/vtmhuman/ability_block_display.html  (best sibling 0.966)
    characters/templates/characters/werewolf/wtahuman/ability_block_display.html  (best sibling 0.966)
    characters/templates/characters/wraith/wtohuman/ability_block_display.html  (best sibling 0.903)
```diff
--- characters/templates/characters/mage/mtahuman/ability_block_display.html
+++ characters/templates/characters/vampire/vtmhuman/ability_block_display.html
@@ -21,4 +20,0 @@
-                                <div class="col-6">Art {% if object|get_specialty:'art' %}({{ object|get_specialty:'art' }}){% endif %}</div>
-                                <div class="col-6 dots">{{ object.art|dots }}</div>
-                            </div>
-                            <div class="row mb-2">
@@ -69,0 +66,4 @@
+                                <div class="col-6">Animal Ken {% if object|get_specialty:'animal_ken' %}({{ object|get_specialty:'animal_ken' }}){% endif %}</div>
+                                <div class="col-6 dots">{{ object.animal_ken|dots }}</div>
+                            </div>
+                            <div class="row mb-2">
@@ -90,4 +89,0 @@
-                                <div class="col-6">Meditation {% if object|get_specialty:'meditation' %}({{ object|get_specialty:'meditation' }}){% endif %}</div>
-                                <div class="col-6 dots">{{ object.meditation|dots }}</div>
-                            </div>
-                            <div class="row mb-2">
@@ -98,2 +94,2 @@
-                                <div class="col-6">Research {% if object|get_specialty:'research' %}({{ object|get_specialty:'research' }}){% endif %}</div>
-                                <div class="col-6 dots">{{ object.research|dots }}</div>
+                                <div class="col-6">Performance {% if object|get_specialty:'performance' %}({{ object|get_specialty:'performance' }}){% endif %}</div>
+                                <div class="col-6 dots">{{ object.performance|dots }}</div>
@@ -108,4 +103,0 @@
-                            </div>
-                            <div class="row mb-2">
-                                <div class="col-6">Technology {% if object|get_specialty:'technology' %}({{ object|get_specialty:'technology' }}){% endif %}</div>
-                                <div class="col-6 dots">{{ object.technology|dots }}</div>
@@ -131,8 +122,0 @@
-                                <div class="col-6">Cosmology {% if object|get_specialty:'cosmology' %}({{ object|get_specialty:'cosmology' }}){% endif %}</div>
-                                <div class="col-6 dots">{{ object.cosmology|dots }}</div>
-                            </div>
-                            <div class="row mb-2">
-                                <div class="col-6">Enigmas {% if object|get_specialty:'enigmas' %}({{ object|get_specialty:'enigmas' }}){% endif %}</div>
-                                <div class="col-6 dots">{{ object.enigmas|dots }}</div>
-                            </div>
-                            <div class="row mb-2">
@@ -164,0 +149,4 @@
+                            </div>
+                            <div class="row mb-2">
+                                <div class="col-6">Technology {% if object|get_specialty:'technology' %}({{ object|get_specialty:'technology' }}){% endif %}</div>
+                                <div class="col-6 dots">{{ object.technology|dots }}</div>
--- characters/templates/characters/mage/mtahuman/ability_block_display.html
+++ characters/templates/characters/werewolf/wtahuman/ability_block_display.html
@@ -21,4 +20,0 @@
-                                <div class="col-6">Art {% if object|get_specialty:'art' %}({{ object|get_specialty:'art' }}){% endif %}</div>
-                                <div class="col-6 dots">{{ object.art|dots }}</div>
-                            </div>
-                            <div class="row mb-2">
@@ -29,4 +24,0 @@
-                                <div class="col-6">Awareness {% if object|get_specialty:'awareness' %}({{ object|get_specialty:'awareness' }}){% endif %}</div>
-                                <div class="col-6 dots">{{ object.awareness|dots }}</div>
-                            </div>
-                            <div class="row mb-2">
@@ -50,0 +43,4 @@
+                            </div>
+                            <div class="row mb-2">
+                                <div class="col-6">Primal-Urge {% if object|get_specialty:'primal_urge' %}({{ object|get_specialty:'primal_urge' }}){% endif %}</div>
+                                <div class="col-6 dots">{{ object.primal_urge|dots }}</div>
@@ -69,0 +66,4 @@
+                                <div class="col-6">Animal Ken {% if object|get_specialty:'animal_ken' %}({{ object|get_specialty:'animal_ken' }}){% endif %}</div>
+                                <div class="col-6 dots">{{ object.animal_ken|dots }}</div>
+                            </div>
+                            <div class="row mb-2">
@@ -90,4 +89,0 @@
-                                <div class="col-6">Meditation {% if object|get_specialty:'meditation' %}({{ object|get_specialty:'meditation' }}){% endif %}</div>
-                                <div class="col-6 dots">{{ object.meditation|dots }}</div>
-                            </div>
-                            <div class="row mb-2">
@@ -98,2 +94,2 @@
-                                <div class="col-6">Research {% if object|get_specialty:'research' %}({{ object|get_specialty:'research' }}){% endif %}</div>
-                                <div class="col-6 dots">{{ object.research|dots }}</div>
+                                <div class="col-6">Performance {% if object|get_specialty:'performance' %}({{ object|get_specialty:'performance' }}){% endif %}</div>
+                                <div class="col-6 dots">{{ object.performance|dots }}</div>
@@ -108,4 +103,0 @@
-                            </div>
-                            <div class="row mb-2">
-                                <div class="col-6">Technology {% if object|get_specialty:'technology' %}({{ object|get_specialty:'technology' }}){% endif %}</div>
-                                <div class="col-6 dots">{{ object.technology|dots }}</div>
@@ -131,4 +122,0 @@
-                                <div class="col-6">Cosmology {% if object|get_specialty:'cosmology' %}({{ object|get_specialty:'cosmology' }}){% endif %}</div>
-                                <div class="col-6 dots">{{ object.cosmology|dots }}</div>
-                            </div>
-                            <div class="row mb-2">
@@ -139,4 +126,0 @@
-                                <div class="col-6">Finance {% if object|get_specialty:'finance' %}({{ object|get_specialty:'finance' }}){% endif %}</div>
-                                <div class="col-6 dots">{{ object.finance|dots }}</div>
-                            </div>
-                            <div class="row mb-2">
@@ -159,2 +143,2 @@
-                                <div class="col-6">Politics {% if object|get_specialty:'politics' %}({{ object|get_specialty:'politics' }}){% endif %}</div>
-                                <div class="col-6 dots">{{ object.politics|dots }}</div>
+                                <div class="col-6">Rituals {% if object|get_specialty:'rituals' %}({{ object|get_specialty:'rituals' }}){% endif %}</div>
+                                <div class="col-6 dots">{{ object.rituals|dots }}</div>
@@ -164,0 +149,4 @@
+                            </div>
+                            <div class="row mb-2">
+                                <div class="col-6">Technology {% if object|get_specialty:'technology' %}({{ object|get_specialty:'technology' }}){% endif %}</div>
+                                <div class="col-6 dots">{{ object.technology|dots }}</div>
--- characters/templates/characters/mage/mtahuman/ability_block_display.html
+++ characters/templates/characters/wraith/wtohuman/ability_block_display.html
@@ -5 +5 @@
-        <h5 class="tg-card-title mb-0">Abilities</h5>
+        <h2 class="mb-0">Abilities</h2>
@@ -13 +13 @@
-                            <h6 class="tg-card-title mb-0">Talents</h6>
+                            <h3 class="mb-0">Talents</h3>
@@ -21,4 +20,0 @@
-                                <div class="col-6">Art {% if object|get_specialty:'art' %}({{ object|get_specialty:'art' }}){% endif %}</div>
-                                <div class="col-6 dots">{{ object.art|dots }}</div>
-                            </div>
-                            <div class="row mb-2">
@@ -49,2 +45,2 @@
-                                <div class="col-6">Leadership {% if object|get_specialty:'leadership' %}({{ object|get_specialty:'leadership' }}){% endif %}</div>
-                                <div class="col-6 dots">{{ object.leadership|dots }}</div>
+                                <div class="col-6">Persuasion {% if object|get_specialty:'persuasion' %}({{ object|get_specialty:'persuasion' }}){% endif %}</div>
+                                <div class="col-6 dots">{{ object.persuasion|dots }}</div>
@@ -66 +62 @@
-                            <h6 class="tg-card-title mb-0">Skills</h6>
+                            <h3 class="mb-0">Skills</h3>
@@ -89,0 +86,4 @@
+                                <div class="col-6">Leadership {% if object|get_specialty:'leadership' %}({{ object|get_specialty:'leadership' }}){% endif %}</div>
+                                <div class="col-6 dots">{{ object.leadership|dots }}</div>
+                            </div>
+                            <div class="row mb-2">
@@ -98,2 +98,2 @@
-                                <div class="col-6">Research {% if object|get_specialty:'research' %}({{ object|get_specialty:'research' }}){% endif %}</div>
-                                <div class="col-6 dots">{{ object.research|dots }}</div>
+                                <div class="col-6">Performance {% if object|get_specialty:'performance' %}({{ object|get_specialty:'performance' }}){% endif %}</div>
+                                <div class="col-6 dots">{{ object.performance|dots }}</div>
@@ -104,8 +103,0 @@
-                            </div>
-                            <div class="row mb-2">
-                                <div class="col-6">Survival {% if object|get_specialty:'survival' %}({{ object|get_specialty:'survival' }}){% endif %}</div>
-                                <div class="col-6 dots">{{ object.survival|dots }}</div>
-                            </div>
-                            <div class="row mb-2">
-                                <div class="col-6">Technology {% if object|get_specialty:'technology' %}({{ object|get_specialty:'technology' }}){% endif %}</div>
-                                <div class="col-6 dots">{{ object.technology|dots }}</div>
@@ -119 +111 @@
-                            <h6 class="tg-card-title mb-0">Knowledges</h6>
+                            <h3 class="mb-0">Knowledges</h3>
@@ -126,0 +119,4 @@
+                                <div class="col-6">Bureaucracy {% if object|get_specialty:'bureaucracy' %}({{ object|get_specialty:'bureaucracy' }}){% endif %}</div>
+                                <div class="col-6 dots">{{ object.bureaucracy|dots }}</div>
+                            </div>
+                            <div class="row mb-2">
@@ -131,4 +126,0 @@
-                                <div class="col-6">Cosmology {% if object|get_specialty:'cosmology' %}({{ object|get_specialty:'cosmology' }}){% endif %}</div>
-                                <div class="col-6 dots">{{ object.cosmology|dots }}</div>
-                            </div>
-                            <div class="row mb-2">
@@ -139,4 +130,0 @@
-                                <div class="col-6">Finance {% if object|get_specialty:'finance' %}({{ object|get_specialty:'finance' }}){% endif %}</div>
-                                <div class="col-6 dots">{{ object.finance|dots }}</div>
-                            </div>
-                            <div class="row mb-2">
@@ -147,4 +134,0 @@
-                                <div class="col-6">Law {% if object|get_specialty:'law' %}({{ object|get_specialty:'law' }}){% endif %}</div>
-                                <div class="col-6 dots">{{ object.law|dots }}</div>
-                            </div>
-                            <div class="row mb-2">
@@ -164,0 +149,4 @@
+                            </div>
+                            <div class="row mb-2">
+                                <div class="col-6">Technology {% if object|get_specialty:'technology' %}({{ object|get_specialty:'technology' }}){% endif %}</div>
+                                <div class="col-6 dots">{{ object.technology|dots }}</div>
@@ -175 +163 @@
-                                <h6 class="tg-card-title mb-0">Secondary Talents</h6>
+                                <h3 class="mb-0">Secondary Talents</h3>
@@ -199 +187 @@
-                                <h6 class="tg-card-title mb-0">Secondary Skills</h6>
+                                <h3 class="mb-0">Secondary Skills</h3>
@@ -223 +211 @@
-                                <h6 class="tg-card-title mb-0">Secondary Knowledges</h6>
+                                <h3 class="mb-0">Secondary Knowledges</h3>
```

### x4 breed_faction_form.html
    characters/templates/characters/werewolf/fera/breed_faction_form.html  (best sibling 0.921)
    characters/templates/characters/werewolf/fera/extras_form.html  (best sibling 0.975)
    characters/templates/characters/werewolf/fera/history_form.html  (best sibling 0.975)
    characters/templates/characters/werewolf/fera/specialties_form.html  (best sibling 0.921)
```diff
--- characters/templates/characters/werewolf/fera/breed_faction_form.html
+++ characters/templates/characters/werewolf/fera/extras_form.html
@@ -6 +6 @@
-                <h5 class="tg-card-title wta_heading">Breed and Faction Selection</h5>
+                <h5 class="tg-card-title wta_heading">Character Details</h5>
@@ -17,5 +16,0 @@
-
-                    <p class="mb-4">
-                        Choose your character's breed (birth form) and faction/aspect/tribe based on your Fera type.
-                        These choices will determine your starting Gnosis, Rage, and available Gifts.
-                    </p>
--- characters/templates/characters/werewolf/fera/breed_faction_form.html
+++ characters/templates/characters/werewolf/fera/history_form.html
@@ -6 +6 @@
-                <h5 class="tg-card-title wta_heading">Breed and Faction Selection</h5>
+                <h5 class="tg-card-title wta_heading">First Change</h5>
@@ -17,5 +16,0 @@
-
-                    <p class="mb-4">
-                        Choose your character's breed (birth form) and faction/aspect/tribe based on your Fera type.
-                        These choices will determine your starting Gnosis, Rage, and available Gifts.
-                    </p>
--- characters/templates/characters/werewolf/fera/breed_faction_form.html
+++ characters/templates/characters/werewolf/fera/specialties_form.html
@@ -6 +6 @@
-                <h5 class="tg-card-title wta_heading">Breed and Faction Selection</h5>
+                <h5 class="tg-card-title wta_heading">Specialties</h5>
@@ -19,2 +19 @@
-                        Choose your character's breed (birth form) and faction/aspect/tribe based on your Fera type.
-                        These choices will determine your starting Gnosis, Rage, and available Gifts.
+                        Select specialties for abilities rated at 4 or higher. This is the final step of character creation!
@@ -39 +38 @@
-                        <button type="submit" class="btn btn-primary btn-lg">Continue</button>
+                        <button type="submit" class="btn btn-success btn-lg">Complete Character Creation</button>
```

### x4 list.html
    items/templates/items/hunter/gear/list.html  (best sibling 0.900)
    items/templates/items/hunter/relic/list.html  (best sibling 0.900)
    locations/templates/locations/hunter/huntingground/list.html  (best sibling 0.900)
    locations/templates/locations/hunter/safehouse/list.html  (best sibling 0.900)
```diff
--- items/templates/items/hunter/gear/list.html
+++ items/templates/items/hunter/relic/list.html
@@ -3 +3 @@
-    Hunter Gear
+    Hunter Relics
@@ -12 +12 @@
-                            <h1 class="tg-card-title htr_heading">Hunter Gear</h1>
+                            <h1 class="tg-card-title htr_heading">Hunter Relics</h1>
@@ -27 +27 @@
-                                        {{ obj.get_gear_type_display }}
+                                        Power Level: {{ obj.power_level }}
@@ -32 +32 @@
-                                    <div class="col-sm">No gear found.</div>
+                                    <div class="col-sm">No relics found.</div>
@@ -43 +43 @@
-                            <a href="{% url 'items:hunter:create:gear' %}" class="tg-btn btn-primary">Create Gear</a>
+                            <a href="{% url 'items:hunter:create:relic' %}" class="tg-btn btn-primary">Create Relic</a>
--- items/templates/items/hunter/gear/list.html
+++ locations/templates/locations/hunter/huntingground/list.html
@@ -3 +3 @@
-    Hunter Gear
+    Hunting Grounds
@@ -12 +12 @@
-                            <h1 class="tg-card-title htr_heading">Hunter Gear</h1>
+                            <h1 class="tg-card-title htr_heading">Hunting Grounds</h1>
@@ -27 +27 @@
-                                        {{ obj.get_gear_type_display }}
+                                        {% if obj.primary_threat %}{{ obj.get_primary_threat_display }}{% else %}Unknown Threat{% endif %}
@@ -32 +32 @@
-                                    <div class="col-sm">No gear found.</div>
+                                    <div class="col-sm">No hunting grounds found.</div>
@@ -43 +43 @@
-                            <a href="{% url 'items:hunter:create:gear' %}" class="tg-btn btn-primary">Create Gear</a>
+                            <a href="{% url 'locations:hunter:create:hunting_ground' %}" class="tg-btn btn-primary">Create Hunting Ground</a>
--- items/templates/items/hunter/gear/list.html
+++ locations/templates/locations/hunter/safehouse/list.html
@@ -3 +3 @@
-    Hunter Gear
+    Safehouses
@@ -12 +12 @@
-                            <h1 class="tg-card-title htr_heading">Hunter Gear</h1>
+                            <h1 class="tg-card-title htr_heading">Safehouses</h1>
@@ -27 +27 @@
-                                        {{ obj.get_gear_type_display }}
+                                        Rating: {{ obj.total_rating }}
@@ -32 +32 @@
-                                    <div class="col-sm">No gear found.</div>
+                                    <div class="col-sm">No safehouses found.</div>
@@ -43 +43 @@
-                            <a href="{% url 'items:hunter:create:gear' %}" class="tg-btn btn-primary">Create Gear</a>
+                            <a href="{% url 'locations:hunter:create:safehouse' %}" class="tg-btn btn-primary">Create Safehouse</a>
```

### x4 detail.html
    locations/templates/locations/mage/node/detail.html  (best sibling 0.912)
    locations/templates/locations/mage/realm/detail.html  (best sibling 0.981)
    locations/templates/locations/mage/sanctum/detail.html  (best sibling 0.960)
    locations/templates/locations/mage/sector/detail.html  (best sibling 0.981)
```diff
--- locations/templates/locations/mage/node/detail.html
+++ locations/templates/locations/mage/realm/detail.html
@@ -23,5 +22,0 @@
-    <div class="row mb-4">
-        {% include "locations/mage/node/display_includes/basics.html" %}
-        {% include "characters/core/meritflaw/display_includes/meritflaw_block.html" %}
-    </div>
-    {% include "characters/mage/resonance/display_includes/resonance.html" %}
--- locations/templates/locations/mage/node/detail.html
+++ locations/templates/locations/mage/sanctum/detail.html
@@ -22,7 +21,0 @@
-{% block model_specific %}
-    <div class="row mb-4">
-        {% include "locations/mage/node/display_includes/basics.html" %}
-        {% include "characters/core/meritflaw/display_includes/meritflaw_block.html" %}
-    </div>
-    {% include "characters/mage/resonance/display_includes/resonance.html" %}
-{% endblock model_specific %}
--- locations/templates/locations/mage/node/detail.html
+++ locations/templates/locations/mage/sector/detail.html
@@ -23,5 +23 @@
-    <div class="row mb-4">
-        {% include "locations/mage/node/display_includes/basics.html" %}
-        {% include "characters/core/meritflaw/display_includes/meritflaw_block.html" %}
-    </div>
-    {% include "characters/mage/resonance/display_includes/resonance.html" %}
+    {% include "locations/mage/sector/display_includes/basics.html" %}
```

### x3 appearance_block_form.html
    characters/templates/characters/changeling/ctdhuman/appearance_block_form.html  (best sibling 1.000)
    characters/templates/characters/mage/companion/companion_appearance_block_form.html  (best sibling 1.000)
    characters/templates/characters/mage/mage/mage_appearance_block_form.html  (best sibling 0.957)
```diff
--- characters/templates/characters/changeling/ctdhuman/appearance_block_form.html
+++ characters/templates/characters/mage/companion/companion_appearance_block_form.html
@@ -9,0 +10 @@
+    <div class="col-sm"></div>
@@ -11,0 +13 @@
+    <div class="col-sm"></div>
--- characters/templates/characters/changeling/ctdhuman/appearance_block_form.html
+++ characters/templates/characters/mage/mage/mage_appearance_block_form.html
@@ -11,0 +12,2 @@
+    <div class="col-sm">Age of Awakening</div>
+    <div class="col-sm">{{ form.age_of_awakening }}</div>
```

### x3 basics_display_include.html
    characters/templates/characters/changeling/ctdhuman/basics_display_include.html  (best sibling 1.000)
    characters/templates/characters/mage/companion/basics_display_include.html  (best sibling 0.900)
    characters/templates/characters/werewolf/fomor/basics_display_include.html  (best sibling 0.944)
```diff
--- characters/templates/characters/changeling/ctdhuman/basics_display_include.html
+++ characters/templates/characters/mage/companion/basics_display_include.html
@@ -1 +1 @@
-<div class="row mb-2">
+<div class="row mb-3">
@@ -13,0 +14,4 @@
+                    <div class="px-3 py-2">
+                        <span style="font-weight: 600; font-size: 0.875rem; color: var(--theme-text-secondary); margin-right: 8px;">Companion Type:</span>
+                        {{ object.get_companion_type_display }}
+                    </div>
--- characters/templates/characters/changeling/ctdhuman/basics_display_include.html
+++ characters/templates/characters/werewolf/fomor/basics_display_include.html
@@ -1 +1 @@
-<div class="row mb-2">
+<div class="row mb-3">
```

### x3 basics.html
    characters/templates/characters/demon/demon/basics.html  (best sibling 0.912)
    characters/templates/characters/demon/dtfhuman/basics.html  (best sibling 0.947)
    characters/templates/characters/demon/thrall/basics.html  (best sibling 0.947)
```diff
--- characters/templates/characters/demon/demon/basics.html
+++ characters/templates/characters/demon/dtfhuman/basics.html
@@ -3 +3 @@
-    Create Demon
+    Create Demon: The Fallen Human
@@ -7 +7 @@
-    id="demonForm"
+    id="dtfhumanForm"
@@ -15 +15 @@
-        <div class="col-sm">Create a fallen angel character for Demon: The Fallen.</div>
+        <div class="col-sm">Create a mortal character for the Demon: The Fallen setting.</div>
@@ -37,2 +37,2 @@
-            <div class="col-sm-2">House</div>
-            <div class="col-sm-2">{{ form.house }}</div>
+            <div class="col-sm-2"></div>
+            <div class="col-sm-2"></div>
--- characters/templates/characters/demon/demon/basics.html
+++ characters/templates/characters/demon/thrall/basics.html
@@ -3 +3 @@
-    Create Demon
+    Create Thrall
@@ -7 +7 @@
-    id="demonForm"
+    id="thrallForm"
@@ -15 +15 @@
-        <div class="col-sm">Create a fallen angel character for Demon: The Fallen.</div>
+        <div class="col-sm">Create a thrall character - a mortal bound to serve a demon.</div>
@@ -37,2 +37,2 @@
-            <div class="col-sm-2">House</div>
-            <div class="col-sm-2">{{ form.house }}</div>
+            <div class="col-sm-2"></div>
+            <div class="col-sm-2"></div>
```

### x3 list.html
    characters/templates/characters/demon/faction/list.html  (best sibling 0.909)
    characters/templates/characters/demon/house/list.html  (best sibling 0.909)
    characters/templates/characters/demon/lore/list.html  (best sibling 0.909)
```diff
--- characters/templates/characters/demon/faction/list.html
+++ characters/templates/characters/demon/house/list.html
@@ -3 +3 @@
-    Demon Factions
+    Houses
@@ -12 +12 @@
-                            <h1 class="tg-card-title dtf_heading">Demon Factions</h1>
+                            <h1 class="tg-card-title dtf_heading">Houses of the Fallen</h1>
@@ -25,0 +26 @@
+                                    <div class="col-sm">{{ obj.celestial_name }}</div>
@@ -29 +30 @@
-                                    <div class="col-sm">No factions found.</div>
+                                    <div class="col-sm">No houses found.</div>
--- characters/templates/characters/demon/faction/list.html
+++ characters/templates/characters/demon/lore/list.html
@@ -3 +3 @@
-    Demon Factions
+    Lores
@@ -12 +12 @@
-                            <h1 class="tg-card-title dtf_heading">Demon Factions</h1>
+                            <h1 class="tg-card-title dtf_heading">Lores</h1>
@@ -25,0 +26 @@
+                                    <div class="col-sm">{{ obj.property_name }}</div>
@@ -29 +30 @@
-                                    <div class="col-sm">No factions found.</div>
+                                    <div class="col-sm">No lores found.</div>
```

### x3 list.html
    characters/templates/characters/mummy/title/list.html  (best sibling 0.904)
    characters/templates/characters/vampire/discipline/list.html  (best sibling 0.917)
    characters/templates/characters/vampire/sect/list.html  (best sibling 0.917)
```diff
--- characters/templates/characters/mummy/title/list.html
+++ characters/templates/characters/vampire/discipline/list.html
@@ -3 +3 @@
-    Mummy Titles
+    Disciplines
@@ -11 +11 @@
-                        <h3 class="tg-card-title mtr_heading">Mummy Titles</h3>
+                        <h3 class="tg-card-title vtm_heading">Disciplines</h3>
@@ -23 +22,0 @@
-                                <span class="tg-badge badge-pill badge-secondary">Rank {{ obj.rank_level }}</span>
@@ -32 +31 @@
-                    <p class="text-center" style="color: var(--theme-text-secondary);">No titles found.</p>
+                    <p class="text-center" style="color: var(--theme-text-secondary);">No disciplines found.</p>
--- characters/templates/characters/mummy/title/list.html
+++ characters/templates/characters/vampire/sect/list.html
@@ -3 +3 @@
-    Mummy Titles
+    Vampire Sects
@@ -11 +11 @@
-                        <h3 class="tg-card-title mtr_heading">Mummy Titles</h3>
+                        <h3 class="tg-card-title vtm_heading">Vampire Sects</h3>
@@ -23 +22,0 @@
-                                <span class="tg-badge badge-pill badge-secondary">Rank {{ obj.rank_level }}</span>
@@ -32 +31 @@
-                    <p class="text-center" style="color: var(--theme-text-secondary);">No titles found.</p>
+                    <p class="text-center" style="color: var(--theme-text-secondary);">No vampire sects found.</p>
```

### x3 detail.html
    characters/templates/characters/vampire/ghoul/detail.html  (best sibling 0.917)
    characters/templates/characters/vampire/revenant/detail.html  (best sibling 0.906)
    characters/templates/characters/vampire/vampire/detail.html  (best sibling 0.917)
```diff
--- characters/templates/characters/vampire/ghoul/detail.html
+++ characters/templates/characters/vampire/revenant/detail.html
@@ -5 +5 @@
-    Ghoul Character Sheet
+    Revenant Character Sheet
@@ -8 +8 @@
-    {% include "characters/vampire/ghoul/basics_display_include.html" %}
+    {% include "characters/vampire/revenant/basics_display_include.html" %}
@@ -11 +11 @@
-    {% include "characters/vampire/ghoul/ghoul_advantage_display.html" %}
+    {% include "characters/vampire/revenant/revenant_advantage_display.html" %}
@@ -17 +17 @@
-    {% include "characters/vampire/ghoul/ghoul_powers_block_display.html" %}
+    {% include "characters/vampire/revenant/revenant_powers_block_display.html" %}
@@ -29,3 +28,0 @@
-    {% if object.status == "Sub" %}
-        {% include "characters/vampire/ghoul/freebies_form.html" %}
-    {% endif %}
--- characters/templates/characters/vampire/ghoul/detail.html
+++ characters/templates/characters/vampire/vampire/detail.html
@@ -5 +5 @@
-    Ghoul Character Sheet
+    Vampire Character Sheet
@@ -8 +8 @@
-    {% include "characters/vampire/ghoul/basics_display_include.html" %}
+    {% include "characters/vampire/vampire/basics_display_include.html" %}
@@ -11 +11 @@
-    {% include "characters/vampire/ghoul/ghoul_advantage_display.html" %}
+    {% include "characters/vampire/vampire/vampire_advantage_display.html" %}
@@ -17 +17 @@
-    {% include "characters/vampire/ghoul/ghoul_powers_block_display.html" %}
+    {% include "characters/vampire/vampire/vampire_powers_block_display.html" %}
@@ -30 +30 @@
-        {% include "characters/vampire/ghoul/freebies_form.html" %}
+        {% include "characters/vampire/vampire/freebies_form.html" %}
```

### x3 form.html
    game/templates/game/chronicle/form.html  (best sibling 0.948)
    game/templates/game/setting_element/form.html  (best sibling 0.948)
    game/templates/game/week/form.html  (best sibling 0.914)
```diff
--- game/templates/game/chronicle/form.html
+++ game/templates/game/setting_element/form.html
@@ -6 +6 @@
-        Create Chronicle
+        Create Setting Element
@@ -17 +17 @@
-                        Create Chronicle
+                        Create Setting Element
@@ -50 +50 @@
-                                <a href="{% url 'game:chronicles' %}" class="btn btn-secondary">Cancel</a>
+                                <a href="{% url 'game:setting_element:list' %}" class="btn btn-secondary">Cancel</a>
--- game/templates/game/chronicle/form.html
+++ game/templates/game/week/form.html
@@ -4 +4 @@
-        Update {{ object.name }}
+        Update Week
@@ -6 +6 @@
-        Create Chronicle
+        Create Week
@@ -15 +15 @@
-                        Update {{ object.name }}
+                        Update Week
@@ -17 +17 @@
-                        Create Chronicle
+                        Create Week
@@ -50 +50 @@
-                                <a href="{% url 'game:chronicles' %}" class="btn btn-secondary">Cancel</a>
+                                <a href="{% url 'game:week:list' %}" class="btn btn-secondary">Cancel</a>
```

### x2 specialties_form.html
    characters/templates/characters/changeling/changeling/specialties_form.html  (best sibling 1.000)
    characters/templates/characters/changeling/ctdhuman/specialties_block_form.html  (best sibling 1.000)
```diff
--- characters/templates/characters/changeling/changeling/specialties_form.html
+++ characters/templates/characters/changeling/ctdhuman/specialties_block_form.html
@@ -2 +2 @@
-    <h2 class="col-sm {{ object.get_heading }}">Choose Specialties</h2>
+    <h2 class="col-sm mta_heading">Choose Specialties</h2>
```

### x2 appearance_block_display.html
    characters/templates/characters/changeling/ctdhuman/appearance_block_display.html  (best sibling 1.000)
    characters/templates/characters/mage/companion/companion_appearance_block_display.html  (best sibling 0.958)
```diff
--- characters/templates/characters/changeling/ctdhuman/appearance_block_display.html
+++ characters/templates/characters/mage/companion/companion_appearance_block_display.html
@@ -7 +7 @@
-        aria-controls="appearanceSection">Appearance</h5>
+        aria-controls="appearanceSection">Appearance</h2>
```

### x2 freebies_form.html
    characters/templates/characters/changeling/ctdhuman/freebies_form.html  (best sibling 1.000)
    characters/templates/characters/vampire/ghoul/freebies_form.html  (best sibling 0.957)
```diff
--- characters/templates/characters/changeling/ctdhuman/freebies_form.html
+++ characters/templates/characters/vampire/ghoul/freebies_form.html
@@ -47,0 +48,6 @@
+    <div class="row centertext">
+        <div class="col-sm-3"></div>
+        <div class="col-sm-3 border">Discipline</div>
+        <div class="col-sm-3 border">7</div>
+        <div class="col-sm-3"></div>
+    </div>
```

### x2 history_block_display.html
    characters/templates/characters/changeling/ctdhuman/history_block_display.html  (best sibling 1.000)
    characters/templates/characters/mage/companion/companion_history_block_display.html  (best sibling 0.962)
```diff
--- characters/templates/characters/changeling/ctdhuman/history_block_display.html
+++ characters/templates/characters/mage/companion/companion_history_block_display.html
@@ -7 +7 @@
-        aria-controls="historySection">History</h5>
+        aria-controls="historySection">History</h2>
```

### x2 advantages_display.html
    characters/templates/characters/core/human/advantages_display.html  (best sibling 0.936)
    characters/templates/characters/mage/sorcerer/sorcerer_advantage_display.html  (best sibling 0.936)
```diff
--- characters/templates/characters/core/human/advantages_display.html
+++ characters/templates/characters/mage/sorcerer/sorcerer_advantage_display.html
@@ -18,0 +19,3 @@
+                <div class="mt-3">
+                    {% include "characters/mage/sorcerer/quintessence_wheel.html" %}
+                </div>
```

### x2 list.html
    characters/templates/characters/demon/demon/list.html  (best sibling 0.922)
    characters/templates/characters/demon/earthbound/list.html  (best sibling 0.922)
```diff
--- characters/templates/characters/demon/demon/list.html
+++ characters/templates/characters/demon/earthbound/list.html
@@ -3 +3 @@
-    Demons
+    Earthbound
@@ -11 +11 @@
-                        <h3 class="tg-card-title dtf_heading">Demons</h3>
+                        <h3 class="tg-card-title dtf_heading">Earthbound</h3>
@@ -16 +16 @@
-        {% for obj in demons %}
+        {% for obj in earthbounds %}
@@ -46 +46 @@
-                    <p class="text-center" style="color: var(--theme-text-secondary);">No demons found.</p>
+                    <p class="text-center" style="color: var(--theme-text-secondary);">No earthbound found.</p>
```

### x2 list.html
    characters/templates/characters/demon/dtfhuman/list.html  (best sibling 0.902)
    characters/templates/characters/demon/thrall/list.html  (best sibling 0.902)
```diff
--- characters/templates/characters/demon/dtfhuman/list.html
+++ characters/templates/characters/demon/thrall/list.html
@@ -3 +3 @@
-    DtF Humans
+    Thralls
@@ -11 +11 @@
-                        <h3 class="tg-card-title dtf_heading">DtF Humans</h3>
+                        <h3 class="tg-card-title dtf_heading">Thralls</h3>
@@ -16 +16 @@
-        {% for obj in dtfhumans %}
+        {% for obj in thralls %}
@@ -36 +36 @@
-                    <p class="text-center" style="color: var(--theme-text-secondary);">No DtF humans found.</p>
+                    <p class="text-center" style="color: var(--theme-text-secondary);">No thralls found.</p>
```

### x2 sorcerer_path_block_form.html
    characters/templates/characters/mage/sorcerer/sorcerer_path_block_form.html  (best sibling 0.920)
    characters/templates/characters/mage/sorcerer/sorcerer_psychic_block_form.html  (best sibling 0.920)
```diff
--- characters/templates/characters/mage/sorcerer/sorcerer_path_block_form.html
+++ characters/templates/characters/mage/sorcerer/sorcerer_psychic_block_form.html
@@ -13,2 +12,0 @@
-            <div class="col-sm">{{ f.practice }}</div>
-            <div class="col-sm">{{ f.ability }}</div>
@@ -23,2 +20,0 @@
-        <div class="col-sm">{{ numina_form_context.empty_form.practice }}</div>
-        <div class="col-sm">{{ numina_form_context.empty_form.ability }}</div>
```

### x2 ghoul_powers_block_display.html
    characters/templates/characters/vampire/ghoul/ghoul_powers_block_display.html  (best sibling 1.000)
    characters/templates/characters/vampire/revenant/revenant_powers_block_display.html  (best sibling 0.962)
```diff
--- characters/templates/characters/vampire/ghoul/ghoul_powers_block_display.html
+++ characters/templates/characters/vampire/revenant/revenant_powers_block_display.html
@@ -10 +10 @@
-                    {% for discipline in object.get_disciplines.items %}
+                    {% for discipline in disciplines.items %}
```

### x2 disciplines.html
    characters/templates/characters/vampire/ghoul/steps/disciplines.html  (best sibling 0.933)
    characters/templates/characters/vampire/vampire/steps/disciplines.html  (best sibling 0.933)
```diff
--- characters/templates/characters/vampire/ghoul/steps/disciplines.html
+++ characters/templates/characters/vampire/vampire/steps/disciplines.html
@@ -7 +7 @@
-                                <p class="tg-card-subtitle">You have Potence 1 automatically. You may spend up to 2 dots on additional disciplines{% if has_domitor %} from your domitor's clan{% else %} (Physical disciplines only){% endif %}.</p>
+                                <p class="tg-card-subtitle">Spend 3 dots on Clan Disciplines</p>
```

### x2 form.html
    characters/templates/characters/vampire/vtmhuman/form.html  (best sibling 0.988)
    characters/templates/characters/wraith/wtohuman/form.html  (best sibling 0.988)
```diff
--- characters/templates/characters/vampire/vtmhuman/form.html
+++ characters/templates/characters/wraith/wtohuman/form.html
@@ -2,0 +3,3 @@
+{% block creation_title %}
+    Create Human (Wraith)
+{% endblock creation_title %}
@@ -4,3 +6,0 @@
-{% block creation_title %}
-    Create Human (Vampire)
-{% endblock creation_title %}
```

### x2 power.html
    items/templates/items/mage/artifact/display_includes/power.html  (best sibling 0.909)
    items/templates/items/mage/charm/display_includes/power.html  (best sibling 0.909)
```diff
--- items/templates/items/mage/artifact/display_includes/power.html
+++ items/templates/items/mage/charm/display_includes/power.html
@@ -2 +2 @@
-    <div class="tg-card-header">
+    <div class="tg-card-header d-flex justify-content-between align-items-center">
@@ -3,0 +4 @@
+        <span class="tg-badge badge-pill badge-light">Arete {{ object.arete }}</span>
```

### x2 form.html
    items/templates/items/werewolf/fetish/form.html  (best sibling 0.938)
    items/templates/items/werewolf/talen/form.html  (best sibling 0.938)
```diff
--- items/templates/items/werewolf/fetish/form.html
+++ items/templates/items/werewolf/talen/form.html
@@ -3 +3 @@
-    Create Fetish
+    Create Talen
```

### x2 detail.html
    locations/templates/locations/demon/bastion/detail.html  (best sibling 0.920)
    locations/templates/locations/demon/reliquary/detail.html  (best sibling 0.920)
```diff
--- locations/templates/locations/demon/bastion/detail.html
+++ locations/templates/locations/demon/reliquary/detail.html
@@ -23,3 +23 @@
-    <div class="row mb-4">
-        {% include "locations/demon/bastion/display_includes/basics.html" %}
-    </div>
+    {% include "locations/demon/reliquary/display_includes/basics.html" %}
```

````

## After

````text
Templates scanned: 755 (generated docs excluded)

## Byte-identical: 2 groups, 26 files

- x21 chargen.html
    characters/templates/characters/changeling/changeling/chargen.html
    characters/templates/characters/changeling/ctdhuman/chargen.html
    characters/templates/characters/core/human/chargen.html
    characters/templates/characters/demon/demon/chargen.html
    characters/templates/characters/demon/dtfhuman/chargen.html
    characters/templates/characters/demon/thrall/chargen.html
    characters/templates/characters/mage/companion/chargen.html
    characters/templates/characters/mage/mage/chargen.html
    characters/templates/characters/mage/mtahuman/chargen.html
    characters/templates/characters/mage/sorcerer/chargen.html
    characters/templates/characters/vampire/ghoul/chargen.html
    characters/templates/characters/vampire/vampire/chargen.html
    characters/templates/characters/vampire/vtmhuman/chargen.html
    characters/templates/characters/werewolf/drone/chargen.html
    characters/templates/characters/werewolf/fera/chargen.html
    characters/templates/characters/werewolf/fomor/chargen.html
    characters/templates/characters/werewolf/garou/chargen.html
    characters/templates/characters/werewolf/kinfolk/chargen.html
    characters/templates/characters/werewolf/wtahuman/chargen.html
    characters/templates/characters/wraith/wraith/chargen.html
    characters/templates/characters/wraith/wtohuman/chargen.html
- x5 detail.html
    characters/templates/characters/changeling/ctdhuman/detail.html
    characters/templates/characters/mummy/mtrhuman/detail.html
    characters/templates/characters/vampire/vtmhuman/detail.html
    characters/templates/characters/werewolf/wtahuman/detail.html
    characters/templates/characters/wraith/wtohuman/detail.html

## Near-identical (>= 0.90): 22 groups, 66 files

### x8 basics.html
    characters/templates/characters/changeling/ctdhuman/basics.html  (best sibling 0.965)
    characters/templates/characters/mage/mtahuman/basics.html  (best sibling 0.965)
    characters/templates/characters/vampire/vtmhuman/basics.html  (best sibling 0.965)
    characters/templates/characters/werewolf/fomor/basics.html  (best sibling 0.965)
    characters/templates/characters/werewolf/kinfolk/basics.html  (best sibling 0.902)
    characters/templates/characters/werewolf/wtahuman/basics.html  (best sibling 0.965)
    characters/templates/characters/wraith/wraith/basics.html  (best sibling 0.931)
    characters/templates/characters/wraith/wtohuman/basics.html  (best sibling 0.965)
```diff
--- characters/templates/characters/changeling/ctdhuman/basics.html
+++ characters/templates/characters/mage/mtahuman/basics.html
@@ -3 +3 @@
-    Create Human (Changeling)
+    Create Human (Mage)
@@ -7 +7 @@
-    id="ctdhumanForm"
+    id="mageHumanForm"
--- characters/templates/characters/changeling/ctdhuman/basics.html
+++ characters/templates/characters/vampire/vtmhuman/basics.html
@@ -3 +3 @@
-    Create Human (Changeling)
+    Create Human (Vampire)
@@ -7 +7 @@
-    id="ctdhumanForm"
+    id="vtmhumanForm"
--- characters/templates/characters/changeling/ctdhuman/basics.html
+++ characters/templates/characters/werewolf/fomor/basics.html
@@ -3 +3 @@
-    Create Human (Changeling)
+    Create Fomor
@@ -7 +7 @@
-    id="ctdhumanForm"
+    id="mageForm"
--- characters/templates/characters/changeling/ctdhuman/basics.html
+++ characters/templates/characters/werewolf/kinfolk/basics.html
@@ -3 +3 @@
-    Create Human (Changeling)
+    Create Kinfolk
@@ -7 +7 @@
-    id="ctdhumanForm"
+    id="mageForm"
@@ -15 +15 @@
-        <div class="col-sm">Decide identity and motivation; choose concept and Archetypes.</div>
+        <div class="col-sm">Decide identity and motivation; choose concept, Tribe, Breed, Relation and Archetypes.</div>
@@ -28,0 +29,2 @@
+            <div class="col-sm-2">Tribe</div>
+            <div class="col-sm-2">{{ form.tribe }}</div>
@@ -34,0 +37,2 @@
+            <div class="col-sm-2">Breed</div>
+            <div class="col-sm-2">{{ form.breed }}</div>
@@ -36,0 +41,2 @@
+            <div class="col-sm-2"></div>
+            <div class="col-sm-2"></div>
@@ -38,0 +45,2 @@
+            <div class="col-sm-2">Relation</div>
+            <div class="col-sm-2">{{ form.relation }}</div>
--- characters/templates/characters/changeling/ctdhuman/basics.html
+++ characters/templates/characters/werewolf/wtahuman/basics.html
@@ -3 +3 @@
-    Create Human (Changeling)
+    Create Human (Werewolf)
@@ -7 +7 @@
-    id="ctdhumanForm"
+    id="wtahumanForm"
--- characters/templates/characters/changeling/ctdhuman/basics.html
+++ characters/templates/characters/wraith/wraith/basics.html
@@ -3 +3 @@
-    Create Human (Changeling)
+    Create Wraith
@@ -7 +7 @@
-    id="ctdhumanForm"
+    id="wraithForm"
@@ -15 +15 @@
-        <div class="col-sm">Decide identity and motivation; choose concept and Archetypes.</div>
+        <div class="col-sm">Decide identity, motivation, and Guild; choose concept and Archetypes.</div>
@@ -38,0 +39,2 @@
+            <div class="col-sm-2">Guild</div>
+            <div class="col-sm-2">{{ form.guild }}</div>
--- characters/templates/characters/changeling/ctdhuman/basics.html
+++ characters/templates/characters/wraith/wtohuman/basics.html
@@ -3 +3 @@
-    Create Human (Changeling)
+    Create Human (Wraith)
@@ -7 +7 @@
-    id="ctdhumanForm"
+    id="wtoHumanForm"
```

### x6 detail.html
    locations/templates/locations/vampire/barrens/detail.html  (best sibling 0.960)
    locations/templates/locations/vampire/chantry/detail.html  (best sibling 0.960)
    locations/templates/locations/vampire/domain/detail.html  (best sibling 0.960)
    locations/templates/locations/vampire/elysium/detail.html  (best sibling 0.960)
    locations/templates/locations/vampire/haven/detail.html  (best sibling 0.941)
    locations/templates/locations/vampire/rack/detail.html  (best sibling 0.960)
```diff
--- locations/templates/locations/vampire/barrens/detail.html
+++ locations/templates/locations/vampire/chantry/detail.html
@@ -23 +23 @@
-        {% include "locations/vampire/barrens/display_includes/basics.html" %}
+        {% include "locations/vampire/chantry/display_includes/basics.html" %}
--- locations/templates/locations/vampire/barrens/detail.html
+++ locations/templates/locations/vampire/domain/detail.html
@@ -23 +23 @@
-        {% include "locations/vampire/barrens/display_includes/basics.html" %}
+        {% include "locations/vampire/domain/display_includes/basics.html" %}
--- locations/templates/locations/vampire/barrens/detail.html
+++ locations/templates/locations/vampire/elysium/detail.html
@@ -23 +23 @@
-        {% include "locations/vampire/barrens/display_includes/basics.html" %}
+        {% include "locations/vampire/elysium/display_includes/basics.html" %}
--- locations/templates/locations/vampire/barrens/detail.html
+++ locations/templates/locations/vampire/haven/detail.html
@@ -23 +23,2 @@
-        {% include "locations/vampire/barrens/display_includes/basics.html" %}
+        {% include "locations/vampire/haven/display_includes/basics.html" %}
+        {% include "characters/core/meritflaw/display_includes/meritflaw_block.html" %}
--- locations/templates/locations/vampire/barrens/detail.html
+++ locations/templates/locations/vampire/rack/detail.html
@@ -23 +23 @@
-        {% include "locations/vampire/barrens/display_includes/basics.html" %}
+        {% include "locations/vampire/rack/display_includes/basics.html" %}
```

### x4 list.html
    core/templates/core/book/list.html  (best sibling 0.900)
    core/templates/core/registry/list.html  (best sibling 0.900)
    game/templates/game/chronicle/list.html  (best sibling 0.900)
    game/templates/game/story/list.html  (best sibling 0.900)
```diff
--- core/templates/core/book/list.html
+++ core/templates/core/registry/list.html
@@ -3 +3 @@
-    Books
+    {{ list_title }}
@@ -9 +9 @@
-                <h3 class="tg-card-title wod_heading">Books</h3>
+                <h3 class="tg-card-title {{ list_heading }}">{{ list_title }}</h3>
@@ -23 +23 @@
-                            <p class="text-muted">No books found.</p>
+                            <p class="text-muted">No {{ list_title|lower }} found.</p>
--- core/templates/core/book/list.html
+++ game/templates/game/chronicle/list.html
@@ -3 +3 @@
-    Books
+    Chronicles
@@ -9 +9 @@
-                <h3 class="tg-card-title wod_heading">Books</h3>
+                <h3 class="tg-card-title wod_heading">Chronicles</h3>
@@ -23 +23 @@
-                            <p class="text-muted">No books found.</p>
+                            <p class="text-muted">No chronicles found.</p>
--- core/templates/core/book/list.html
+++ game/templates/game/story/list.html
@@ -3 +3 @@
-    Books
+    Stories
@@ -9 +9 @@
-                <h3 class="tg-card-title wod_heading">Books</h3>
+                <h3 class="tg-card-title wod_heading">Stories</h3>
@@ -23 +23 @@
-                            <p class="text-muted">No books found.</p>
+                            <p class="text-muted">No stories found.</p>
```

### x4 list.html
    items/templates/items/hunter/gear/list.html  (best sibling 0.900)
    items/templates/items/hunter/relic/list.html  (best sibling 0.900)
    locations/templates/locations/hunter/huntingground/list.html  (best sibling 0.900)
    locations/templates/locations/hunter/safehouse/list.html  (best sibling 0.900)
```diff
--- items/templates/items/hunter/gear/list.html
+++ items/templates/items/hunter/relic/list.html
@@ -3 +3 @@
-    Hunter Gear
+    Hunter Relics
@@ -12 +12 @@
-                            <h1 class="tg-card-title htr_heading">Hunter Gear</h1>
+                            <h1 class="tg-card-title htr_heading">Hunter Relics</h1>
@@ -27 +27 @@
-                                        {{ obj.get_gear_type_display }}
+                                        Power Level: {{ obj.power_level }}
@@ -32 +32 @@
-                                    <div class="col-sm">No gear found.</div>
+                                    <div class="col-sm">No relics found.</div>
@@ -43 +43 @@
-                            <a href="{% url 'items:hunter:create:gear' %}" class="tg-btn btn-primary">Create Gear</a>
+                            <a href="{% url 'items:hunter:create:relic' %}" class="tg-btn btn-primary">Create Relic</a>
--- items/templates/items/hunter/gear/list.html
+++ locations/templates/locations/hunter/huntingground/list.html
@@ -3 +3 @@
-    Hunter Gear
+    Hunting Grounds
@@ -12 +12 @@
-                            <h1 class="tg-card-title htr_heading">Hunter Gear</h1>
+                            <h1 class="tg-card-title htr_heading">Hunting Grounds</h1>
@@ -27 +27 @@
-                                        {{ obj.get_gear_type_display }}
+                                        {% if obj.primary_threat %}{{ obj.get_primary_threat_display }}{% else %}Unknown Threat{% endif %}
@@ -32 +32 @@
-                                    <div class="col-sm">No gear found.</div>
+                                    <div class="col-sm">No hunting grounds found.</div>
@@ -43 +43 @@
-                            <a href="{% url 'items:hunter:create:gear' %}" class="tg-btn btn-primary">Create Gear</a>
+                            <a href="{% url 'locations:hunter:create:hunting_ground' %}" class="tg-btn btn-primary">Create Hunting Ground</a>
--- items/templates/items/hunter/gear/list.html
+++ locations/templates/locations/hunter/safehouse/list.html
@@ -3 +3 @@
-    Hunter Gear
+    Safehouses
@@ -12 +12 @@
-                            <h1 class="tg-card-title htr_heading">Hunter Gear</h1>
+                            <h1 class="tg-card-title htr_heading">Safehouses</h1>
@@ -27 +27 @@
-                                        {{ obj.get_gear_type_display }}
+                                        Rating: {{ obj.total_rating }}
@@ -32 +32 @@
-                                    <div class="col-sm">No gear found.</div>
+                                    <div class="col-sm">No safehouses found.</div>
@@ -43 +43 @@
-                            <a href="{% url 'items:hunter:create:gear' %}" class="tg-btn btn-primary">Create Gear</a>
+                            <a href="{% url 'locations:hunter:create:safehouse' %}" class="tg-btn btn-primary">Create Safehouse</a>
```

### x4 detail.html
    locations/templates/locations/mage/node/detail.html  (best sibling 0.912)
    locations/templates/locations/mage/realm/detail.html  (best sibling 0.981)
    locations/templates/locations/mage/sanctum/detail.html  (best sibling 0.960)
    locations/templates/locations/mage/sector/detail.html  (best sibling 0.981)
```diff
--- locations/templates/locations/mage/node/detail.html
+++ locations/templates/locations/mage/realm/detail.html
@@ -23,5 +22,0 @@
-    <div class="row mb-4">
-        {% include "locations/mage/node/display_includes/basics.html" %}
-        {% include "characters/core/meritflaw/display_includes/meritflaw_block.html" %}
-    </div>
-    {% include "characters/mage/resonance/display_includes/resonance.html" %}
--- locations/templates/locations/mage/node/detail.html
+++ locations/templates/locations/mage/sanctum/detail.html
@@ -22,7 +21,0 @@
-{% block model_specific %}
-    <div class="row mb-4">
-        {% include "locations/mage/node/display_includes/basics.html" %}
-        {% include "characters/core/meritflaw/display_includes/meritflaw_block.html" %}
-    </div>
-    {% include "characters/mage/resonance/display_includes/resonance.html" %}
-{% endblock model_specific %}
--- locations/templates/locations/mage/node/detail.html
+++ locations/templates/locations/mage/sector/detail.html
@@ -23,5 +23 @@
-    <div class="row mb-4">
-        {% include "locations/mage/node/display_includes/basics.html" %}
-        {% include "characters/core/meritflaw/display_includes/meritflaw_block.html" %}
-    </div>
-    {% include "characters/mage/resonance/display_includes/resonance.html" %}
+    {% include "locations/mage/sector/display_includes/basics.html" %}
```

### x3 basics.html
    characters/templates/characters/demon/demon/basics.html  (best sibling 0.912)
    characters/templates/characters/demon/dtfhuman/basics.html  (best sibling 0.947)
    characters/templates/characters/demon/thrall/basics.html  (best sibling 0.947)
```diff
--- characters/templates/characters/demon/demon/basics.html
+++ characters/templates/characters/demon/dtfhuman/basics.html
@@ -3 +3 @@
-    Create Demon
+    Create Demon: The Fallen Human
@@ -7 +7 @@
-    id="demonForm"
+    id="dtfhumanForm"
@@ -15 +15 @@
-        <div class="col-sm">Create a fallen angel character for Demon: The Fallen.</div>
+        <div class="col-sm">Create a mortal character for the Demon: The Fallen setting.</div>
@@ -37,2 +37,2 @@
-            <div class="col-sm-2">House</div>
-            <div class="col-sm-2">{{ form.house }}</div>
+            <div class="col-sm-2"></div>
+            <div class="col-sm-2"></div>
--- characters/templates/characters/demon/demon/basics.html
+++ characters/templates/characters/demon/thrall/basics.html
@@ -3 +3 @@
-    Create Demon
+    Create Thrall
@@ -7 +7 @@
-    id="demonForm"
+    id="thrallForm"
@@ -15 +15 @@
-        <div class="col-sm">Create a fallen angel character for Demon: The Fallen.</div>
+        <div class="col-sm">Create a thrall character - a mortal bound to serve a demon.</div>
@@ -37,2 +37,2 @@
-            <div class="col-sm-2">House</div>
-            <div class="col-sm-2">{{ form.house }}</div>
+            <div class="col-sm-2"></div>
+            <div class="col-sm-2"></div>
```

### x3 list.html
    characters/templates/characters/demon/faction/list.html  (best sibling 0.909)
    characters/templates/characters/demon/house/list.html  (best sibling 0.909)
    characters/templates/characters/demon/lore/list.html  (best sibling 0.909)
```diff
--- characters/templates/characters/demon/faction/list.html
+++ characters/templates/characters/demon/house/list.html
@@ -3 +3 @@
-    Demon Factions
+    Houses
@@ -12 +12 @@
-                            <h1 class="tg-card-title dtf_heading">Demon Factions</h1>
+                            <h1 class="tg-card-title dtf_heading">Houses of the Fallen</h1>
@@ -25,0 +26 @@
+                                    <div class="col-sm">{{ obj.celestial_name }}</div>
@@ -29 +30 @@
-                                    <div class="col-sm">No factions found.</div>
+                                    <div class="col-sm">No houses found.</div>
--- characters/templates/characters/demon/faction/list.html
+++ characters/templates/characters/demon/lore/list.html
@@ -3 +3 @@
-    Demon Factions
+    Lores
@@ -12 +12 @@
-                            <h1 class="tg-card-title dtf_heading">Demon Factions</h1>
+                            <h1 class="tg-card-title dtf_heading">Lores</h1>
@@ -25,0 +26 @@
+                                    <div class="col-sm">{{ obj.property_name }}</div>
@@ -29 +30 @@
-                                    <div class="col-sm">No factions found.</div>
+                                    <div class="col-sm">No lores found.</div>
```

### x3 basics_display_include.html
    characters/templates/characters/mage/companion/basics_display_include.html  (best sibling 0.900)
    characters/templates/characters/shared/human/basics_display_include.html  (best sibling 0.944)
    characters/templates/characters/werewolf/fomor/basics_display_include.html  (best sibling 0.944)
```diff
--- characters/templates/characters/mage/companion/basics_display_include.html
+++ characters/templates/characters/shared/human/basics_display_include.html
@@ -1 +1 @@
-<div class="row mb-3">
+<div class="row mb-2">
@@ -14,4 +13,0 @@
-                    <div class="px-3 py-2">
-                        <span style="font-weight: 600; font-size: 0.875rem; color: var(--theme-text-secondary); margin-right: 8px;">Companion Type:</span>
-                        {{ object.get_companion_type_display }}
-                    </div>
--- characters/templates/characters/mage/companion/basics_display_include.html
+++ characters/templates/characters/werewolf/fomor/basics_display_include.html
@@ -14,4 +13,0 @@
-                    <div class="px-3 py-2">
-                        <span style="font-weight: 600; font-size: 0.875rem; color: var(--theme-text-secondary); margin-right: 8px;">Companion Type:</span>
-                        {{ object.get_companion_type_display }}
-                    </div>
```

### x3 list.html
    characters/templates/characters/mummy/title/list.html  (best sibling 0.904)
    characters/templates/characters/vampire/discipline/list.html  (best sibling 0.917)
    characters/templates/characters/vampire/sect/list.html  (best sibling 0.917)
```diff
--- characters/templates/characters/mummy/title/list.html
+++ characters/templates/characters/vampire/discipline/list.html
@@ -3 +3 @@
-    Mummy Titles
+    Disciplines
@@ -11 +11 @@
-                        <h3 class="tg-card-title mtr_heading">Mummy Titles</h3>
+                        <h3 class="tg-card-title vtm_heading">Disciplines</h3>
@@ -23 +22,0 @@
-                                <span class="tg-badge badge-pill badge-secondary">Rank {{ obj.rank_level }}</span>
@@ -32 +31 @@
-                    <p class="text-center" style="color: var(--theme-text-secondary);">No titles found.</p>
+                    <p class="text-center" style="color: var(--theme-text-secondary);">No disciplines found.</p>
--- characters/templates/characters/mummy/title/list.html
+++ characters/templates/characters/vampire/sect/list.html
@@ -3 +3 @@
-    Mummy Titles
+    Vampire Sects
@@ -11 +11 @@
-                        <h3 class="tg-card-title mtr_heading">Mummy Titles</h3>
+                        <h3 class="tg-card-title vtm_heading">Vampire Sects</h3>
@@ -23 +22,0 @@
-                                <span class="tg-badge badge-pill badge-secondary">Rank {{ obj.rank_level }}</span>
@@ -32 +31 @@
-                    <p class="text-center" style="color: var(--theme-text-secondary);">No titles found.</p>
+                    <p class="text-center" style="color: var(--theme-text-secondary);">No vampire sects found.</p>
```

### x3 detail.html
    characters/templates/characters/vampire/ghoul/detail.html  (best sibling 0.933)
    characters/templates/characters/vampire/revenant/detail.html  (best sibling 0.923)
    characters/templates/characters/vampire/vampire/detail.html  (best sibling 0.933)
```diff
--- characters/templates/characters/vampire/ghoul/detail.html
+++ characters/templates/characters/vampire/revenant/detail.html
@@ -5 +5 @@
-    Ghoul Character Sheet
+    Revenant Character Sheet
@@ -8 +8 @@
-    {% include "characters/vampire/ghoul/basics_display_include.html" %}
+    {% include "characters/vampire/revenant/basics_display_include.html" %}
@@ -17 +17 @@
-    {% include "characters/shared/vampire/powers_block_display.html" %}
+    {% include "characters/vampire/revenant/revenant_powers_block_display.html" %}
@@ -29,3 +28,0 @@
-    {% if object.status == "Sub" %}
-        {% include "characters/vampire/ghoul/freebies_form.html" %}
-    {% endif %}
--- characters/templates/characters/vampire/ghoul/detail.html
+++ characters/templates/characters/vampire/vampire/detail.html
@@ -5 +5 @@
-    Ghoul Character Sheet
+    Vampire Character Sheet
@@ -8 +8 @@
-    {% include "characters/vampire/ghoul/basics_display_include.html" %}
+    {% include "characters/vampire/vampire/basics_display_include.html" %}
@@ -11 +11 @@
-    {% include "characters/shared/vampire/ghoul_advantage_display.html" %}
+    {% include "characters/vampire/vampire/vampire_advantage_display.html" %}
@@ -30 +30 @@
-        {% include "characters/vampire/ghoul/freebies_form.html" %}
+        {% include "characters/vampire/vampire/freebies_form.html" %}
```

### x3 form.html
    game/templates/game/chronicle/form.html  (best sibling 0.948)
    game/templates/game/setting_element/form.html  (best sibling 0.948)
    game/templates/game/week/form.html  (best sibling 0.914)
```diff
--- game/templates/game/chronicle/form.html
+++ game/templates/game/setting_element/form.html
@@ -6 +6 @@
-        Create Chronicle
+        Create Setting Element
@@ -17 +17 @@
-                        Create Chronicle
+                        Create Setting Element
@@ -50 +50 @@
-                                <a href="{% url 'game:chronicles' %}" class="btn btn-secondary">Cancel</a>
+                                <a href="{% url 'game:setting_element:list' %}" class="btn btn-secondary">Cancel</a>
--- game/templates/game/chronicle/form.html
+++ game/templates/game/week/form.html
@@ -4 +4 @@
-        Update {{ object.name }}
+        Update Week
@@ -6 +6 @@
-        Create Chronicle
+        Create Week
@@ -15 +15 @@
-                        Update {{ object.name }}
+                        Update Week
@@ -17 +17 @@
-                        Create Chronicle
+                        Create Week
@@ -50 +50 @@
-                                <a href="{% url 'game:chronicles' %}" class="btn btn-secondary">Cancel</a>
+                                <a href="{% url 'game:week:list' %}" class="btn btn-secondary">Cancel</a>
```

### x2 advantages_display.html
    characters/templates/characters/core/human/advantages_display.html  (best sibling 0.936)
    characters/templates/characters/mage/sorcerer/sorcerer_advantage_display.html  (best sibling 0.936)
```diff
--- characters/templates/characters/core/human/advantages_display.html
+++ characters/templates/characters/mage/sorcerer/sorcerer_advantage_display.html
@@ -18,0 +19,3 @@
+                <div class="mt-3">
+                    {% include "characters/mage/sorcerer/quintessence_wheel.html" %}
+                </div>
```

### x2 list.html
    characters/templates/characters/demon/demon/list.html  (best sibling 0.922)
    characters/templates/characters/demon/earthbound/list.html  (best sibling 0.922)
```diff
--- characters/templates/characters/demon/demon/list.html
+++ characters/templates/characters/demon/earthbound/list.html
@@ -3 +3 @@
-    Demons
+    Earthbound
@@ -11 +11 @@
-                        <h3 class="tg-card-title dtf_heading">Demons</h3>
+                        <h3 class="tg-card-title dtf_heading">Earthbound</h3>
@@ -16 +16 @@
-        {% for obj in demons %}
+        {% for obj in earthbounds %}
@@ -46 +46 @@
-                    <p class="text-center" style="color: var(--theme-text-secondary);">No demons found.</p>
+                    <p class="text-center" style="color: var(--theme-text-secondary);">No earthbound found.</p>
```

### x2 list.html
    characters/templates/characters/demon/dtfhuman/list.html  (best sibling 0.902)
    characters/templates/characters/demon/thrall/list.html  (best sibling 0.902)
```diff
--- characters/templates/characters/demon/dtfhuman/list.html
+++ characters/templates/characters/demon/thrall/list.html
@@ -3 +3 @@
-    DtF Humans
+    Thralls
@@ -11 +11 @@
-                        <h3 class="tg-card-title dtf_heading">DtF Humans</h3>
+                        <h3 class="tg-card-title dtf_heading">Thralls</h3>
@@ -16 +16 @@
-        {% for obj in dtfhumans %}
+        {% for obj in thralls %}
@@ -36 +36 @@
-                    <p class="text-center" style="color: var(--theme-text-secondary);">No DtF humans found.</p>
+                    <p class="text-center" style="color: var(--theme-text-secondary);">No thralls found.</p>
```

### x2 sorcerer_path_block_form.html
    characters/templates/characters/mage/sorcerer/sorcerer_path_block_form.html  (best sibling 0.920)
    characters/templates/characters/mage/sorcerer/sorcerer_psychic_block_form.html  (best sibling 0.920)
```diff
--- characters/templates/characters/mage/sorcerer/sorcerer_path_block_form.html
+++ characters/templates/characters/mage/sorcerer/sorcerer_psychic_block_form.html
@@ -13,2 +12,0 @@
-            <div class="col-sm">{{ f.practice }}</div>
-            <div class="col-sm">{{ f.ability }}</div>
@@ -23,2 +20,0 @@
-        <div class="col-sm">{{ numina_form_context.empty_form.practice }}</div>
-        <div class="col-sm">{{ numina_form_context.empty_form.ability }}</div>
```

### x2 powers_block_display.html
    characters/templates/characters/shared/vampire/powers_block_display.html  (best sibling 0.962)
    characters/templates/characters/vampire/revenant/revenant_powers_block_display.html  (best sibling 0.962)
```diff
--- characters/templates/characters/shared/vampire/powers_block_display.html
+++ characters/templates/characters/vampire/revenant/revenant_powers_block_display.html
@@ -10 +10 @@
-                    {% for discipline in object.get_disciplines.items %}
+                    {% for discipline in disciplines.items %}
```

### x2 disciplines.html
    characters/templates/characters/vampire/ghoul/steps/disciplines.html  (best sibling 0.933)
    characters/templates/characters/vampire/vampire/steps/disciplines.html  (best sibling 0.933)
```diff
--- characters/templates/characters/vampire/ghoul/steps/disciplines.html
+++ characters/templates/characters/vampire/vampire/steps/disciplines.html
@@ -7 +7 @@
-                                <p class="tg-card-subtitle">You have Potence 1 automatically. You may spend up to 2 dots on additional disciplines{% if has_domitor %} from your domitor's clan{% else %} (Physical disciplines only){% endif %}.</p>
+                                <p class="tg-card-subtitle">Spend 3 dots on Clan Disciplines</p>
```

### x2 form.html
    characters/templates/characters/vampire/vtmhuman/form.html  (best sibling 0.988)
    characters/templates/characters/wraith/wtohuman/form.html  (best sibling 0.988)
```diff
--- characters/templates/characters/vampire/vtmhuman/form.html
+++ characters/templates/characters/wraith/wtohuman/form.html
@@ -2,0 +3,3 @@
+{% block creation_title %}
+    Create Human (Wraith)
+{% endblock creation_title %}
@@ -4,3 +6,0 @@
-{% block creation_title %}
-    Create Human (Vampire)
-{% endblock creation_title %}
```

### x2 breed_faction_form.html
    characters/templates/characters/werewolf/fera/breed_faction_form.html  (best sibling 0.918)
    characters/templates/characters/werewolf/fera/history_form.html  (best sibling 0.918)
```diff
--- characters/templates/characters/werewolf/fera/breed_faction_form.html
+++ characters/templates/characters/werewolf/fera/history_form.html
@@ -6 +6 @@
-                <h5 class="tg-card-title wta_heading">Breed and Faction Selection</h5>
+                <h5 class="tg-card-title wta_heading">First Change</h5>
@@ -17,5 +16,0 @@
-
-                    <p class="mb-4">
-                        Choose your character's breed (birth form) and faction/aspect/tribe based on your Fera type.
-                        These choices will determine your starting Gnosis, Rage, and available Gifts.
-                    </p>
```

### x2 power.html
    items/templates/items/mage/artifact/display_includes/power.html  (best sibling 0.909)
    items/templates/items/mage/charm/display_includes/power.html  (best sibling 0.909)
```diff
--- items/templates/items/mage/artifact/display_includes/power.html
+++ items/templates/items/mage/charm/display_includes/power.html
@@ -2 +2 @@
-    <div class="tg-card-header">
+    <div class="tg-card-header d-flex justify-content-between align-items-center">
@@ -3,0 +4 @@
+        <span class="tg-badge badge-pill badge-light">Arete {{ object.arete }}</span>
```

### x2 form.html
    items/templates/items/werewolf/fetish/form.html  (best sibling 0.938)
    items/templates/items/werewolf/talen/form.html  (best sibling 0.938)
```diff
--- items/templates/items/werewolf/fetish/form.html
+++ items/templates/items/werewolf/talen/form.html
@@ -3 +3 @@
-    Create Fetish
+    Create Talen
```

### x2 detail.html
    locations/templates/locations/demon/bastion/detail.html  (best sibling 0.920)
    locations/templates/locations/demon/reliquary/detail.html  (best sibling 0.920)
```diff
--- locations/templates/locations/demon/bastion/detail.html
+++ locations/templates/locations/demon/reliquary/detail.html
@@ -23,3 +23 @@
-    <div class="row mb-4">
-        {% include "locations/demon/bastion/display_includes/basics.html" %}
-    </div>
+    {% include "locations/demon/reliquary/display_includes/basics.html" %}
```

````
