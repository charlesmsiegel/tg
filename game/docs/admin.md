# game admin

This page describes how the `game` models appear in the Django admin
(`/admin/`, configured in [`game/admin.py`](../admin.py)). Read it before changing an
admin class, or when you need to edit data that has no page in the site, such as a
chronicle's game storytellers, setting elements or allowed object types.

Every model in [`game/models.py`](../models.py) is registered. The admin writes through
the models, so the `ValidatedSaveMixin` validation described in [models](models.md)
applies to admin saves too. Admin access is Django's own (`is_staff` plus model
permissions); the project's route policies do not cover `/admin/`.

## Registrations

| Model | Admin class | List columns | Filters and search | Other |
|-------|-------------|--------------|--------------------|-------|
| `Chronicle` | `ChronicleAdmin` | name, head ST, `storyteller_list`, headings, year, `total_scenes` | Filter: headings, year. Search: name, theme, mood | Fieldsets: Basic Information (name, headings, year), Narrative (theme, mood, common knowledge), Storytellers (head ST, game storytellers), Game Configuration (allowed objects). Horizontal pickers for the three many-to-many fields. |
| `Scene` | `SceneAdmin` | name, chronicle, location, finished, XP given, waiting for ST, `num_pcs`, `total_posts` | Filter: chronicle, finished, XP given, waiting for ST | `num_pcs` counts non-NPC characters |
| `Post` | `PostAdmin` | character, display name, scene, message | Filter: scene, character, display name | |
| `SettingElement` | `SettingElementAdmin` | name, gameline, description | Filter: gameline. Search: name, description | |
| `ObjectType` | `ObjectTypeAdmin` | name, type, gameline | Filter: type, gameline. Search: name | |
| `Gameline` | `GamelineAdmin` | name | Search: name | |
| `STRelationship` | `STRelationshipAdmin` | user, chronicle, gameline | | The only place in the site to grant or remove per-gameline storytellers |
| `Story` | `StoryAdmin` | name, chronicle, XP given | Filter: chronicle, XP given. Search: name | Joins the chronicle for the list |
| `Week` | `WeekAdmin` | `start_date`, end date, `num_characters`, `num_scenes` | Filter: end date | Horizontal picker for characters; `num_scenes` is `finished_scenes().count()` |
| `WeeklyXPRequest` | `WeeklyXPRequestAdmin` | character, week, `total_xp`, the five criteria, approved | Filter: approved, week. Search: character name | Fieldsets pair each criterion with its scene. Setting `approved` here does not award XP; only `WeeklyXPRequest.approve()` does. |
| `StoryXPRequest` | `StoryXPRequestAdmin` | character, story, the four categories, duration, `total_xp` | Filter: story and the four categories. Search: character and story names | `total_xp` is the four booleans plus `duration` |
| `UserSceneReadStatus` | `UserSceneReadStatusAdmin` | user, scene, read, last read post | Filter: read, scene. Search: username, scene name | `last_read_post` is a raw id field |
| `Journal` | `JournalAdmin` | character, `num_entries` | Search: character name | |
| `JournalEntry` | `JournalEntryAdmin` | journal, date, created, has message, has ST message | Filter: journal, date. Search: character name, message, ST message | `datetime_created` is read-only |
| `XPSpendingRequest` | `XPSpendingRequestAdmin` | character, trait name, type, value, cost, approved, created, approved by | Filter: approved, trait type, created. Search: character and trait names | `created_at` and `approved_at` read-only. Changing `approved` here neither applies the trait nor refunds XP. |
| `FreebieSpendingRecord` | `FreebieSpendingRecordAdmin` | character, trait name, type, value, cost, created | Filter: trait type, created. Search: character and trait names | `created_at` read-only |

Several list columns (`num_pcs`, `total_posts`, `num_characters`, `num_scenes`,
`num_entries`, `storyteller_list`, `total_scenes`) run a query per row; filter large
lists before opening them.

## See also

- [game models](models.md)
- [XP](xp.md)
- [Authorization](../../docs/architecture/authorization.md)
- [accounts models](../../accounts/docs/models.md#admin)
