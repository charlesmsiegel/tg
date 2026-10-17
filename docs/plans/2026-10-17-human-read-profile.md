# Exact Human read profile and native catalogs

Base01bcfd5; controller approved read-only first slice of character mapping design.
No writes, migrations, generic Store/archive claims, push or publication before review.

- GET `character-profiles/human-v1/`: authenticated static exposed field/bounds/reference
  manifest, decimal-string native identity rules, fixed redactions and read-only caps.
- GET `catalogs/human-v1/{kind}/`: paginated explicit public reference facts. Native
  public-list policy and default querysets remain authoritative; policy drift fails closed.
  Background is a public Statistic reference with no owner/visibility fields. No private
  inherited metadata, reverse known-by characters or arbitrary relation expansions.
- GET `characters/{pk}/human-profile/`: native full-view permission, exact concrete Human
  only. Safe scalars and six bounded relation collections preserve IDs/nulls/repeats.
  Always omit ST notes, image storage, untyped legacy JSON and separate audit/reverse/
  group data with explicit fixed redactions. No full Human/archive completeness claim.
- Two canonical projections inside a read transaction, with fresh actor/target and
  request-permission invalidation; differences in exposed scalars OR relations fail409.
  Hidden/missing remain404 before subtype diagnostics. Authorized other subtypes422.
- HMAC fingerprint binds exposed payload, principal and request origin/script prefix.
  Hidden fields cannot affect token; it is not auth, CAS, permission lease or global
  database revision. No mutations accept it in this increment.
- Collections cap500; oversize profile fails422, never truncates. Catalog pages50/max100.
  Bounds describe native storage, do not clamp or imply local module/rule equivalence.

Execute inline with TDD: observe missing routes fail; implement explicit projections,
source-native reference querysets/policies and strict query/ID validation; regress races,
privacy, relations, nulls, large native IDs, bounds, no GET effects and no extra methods.
Run API/native permission/route/action/import focused tests, Ruff/Black, full required
suite with authorized external browser exclusion; coordinate independent review, then
commit cleanly and report. Existing v1 and all parent branch heads remain unchanged.
