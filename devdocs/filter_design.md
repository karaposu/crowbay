# filepath: devdocs/filter_design.md

# Task Filter Design

> **Provenance**: extracted from `depricated_src/api_spec.yaml` (`CreateTaskRequest.filters` and the `RegionFilter`/`CountryFilter`/`CityFilter` schemas) so the design survives the deletion of `depricated_src/`. Terminology updated to Launcher/Jumper. This file is now the living home of the filter design.

## Purpose

Filters are how a Launcher targets a task at exactly the Jumpers they want. They are the demand-side half of Crowdjump's core differentiator: filters run against **verified attributes** (extracted from proofs), never against self-declared profile data. A filter is only as good as the verification behind it.

## Design Principles

1. **Structured + raw, side by side.** Fuzzy filters carry the Launcher's original wording (`raw_statement`) alongside the parsed structure. The Telegram bot collects intent conversationally ("young people around my city"), an LLM parses it into the structured form, the Launcher confirms, and the raw statement is kept for audit, re-parsing, and dispute resolution.
2. **Everything optional.** Every field at every level is nullable. An empty filter object means "any verified Jumper."
3. **Inclusion with exceptions.** Location filtering is set arithmetic: name a scope, subtract exceptions. This is what makes statements like "EMEA but not Russia" or "Germany except Berlin" expressible.
4. **Binary matching (MVP).** A Jumper either qualifies or doesn't. No scoring, no partial matches, no ranking — plain SQL against verified attributes.
5. **Fast picking.** Location is prompted first in the task-creation flow and must be quick to specify — presets and shorthand ("Minsk and Istanbul", "EMEA", "not India") matter more than exhaustive forms.

## Schema

Two tiers: `basic_filters` (demographics from identity proofs) and `advanced_filters` (facts from social-account proofs).

```yaml
filters:
  basic_filters:
    location_filter:
      raw_statement: string          # original Launcher wording, kept verbatim
      regions:                       # named multi-country scopes (EMEA, LATAM, ...)
        - name: string
          exceptions:
            countries: [string]
            cities: [string]
      countries:
        - name: string
          exceptions:
            cities: [string]         # (country-level "exceptions.countries" existed in
                                     #  the original schema but is meaningless; dropped)
      cities:
        - name: string               # city entries take no meaningful exceptions
    age_range:
      min: integer
      max: integer
    gender: string
    language: string
    ethnicity:
      allowed: [string]
      not_allowed: [string]
      raw_statement: string

  advanced_filters:
    min_instagram_followers: integer
    min_tiktok_followers: integer
    min_linkedin_connections: integer
    min_github_repositories: integer
    telegram_account_age_days: integer   # minimum account age in days
    has_profile_picture: boolean
    account_verified: boolean
```

### Example

"Women 18–25 in EMEA but not Russia, plus Istanbul, with at least 1k Instagram followers":

```json
{
  "basic_filters": {
    "location_filter": {
      "raw_statement": "EMEA but not Russia, plus Istanbul",
      "regions": [{ "name": "EMEA", "exceptions": { "countries": ["Russia"] } }],
      "cities": [{ "name": "Istanbul" }]
    },
    "age_range": { "min": 18, "max": 25 },
    "gender": "female"
  },
  "advanced_filters": {
    "min_instagram_followers": 1000
  }
}
```

## Evaluation Semantics

The original spec defined only the shape; these are the intended rules for the matcher:

- **AND across fields.** Every specified filter field must pass.
- **OR within location lists.** A Jumper qualifies on location if they fall inside *any* listed region, country, or city — after that entry's exceptions are subtracted.
- **Exceptions subtract from their parent scope only.** `EMEA except Russia` removes Russia from EMEA; it says nothing about a separately listed country.
- **Unspecified means unconstrained.** Null field → no requirement.
- **Verified attributes only.** Matching reads the `verification_data` store (`field_name`/`field_value`, `is_current = true`, confidence above threshold). A Jumper without a verified attribute for a specified filter does not match — absence is failure, not a pass.
- **Region resolution.** Named regions resolve through a static region → country mapping table (EMEA, LATAM, APAC, ...) maintained as a config asset.

## MVP Subset

Per PROJECT.md, MVP matches on four demographics:

| Filter | In original schema | MVP source attribute |
|---|---|---|
| Location (country/city) | yes | ID document + declared city |
| Age range | yes | ID date of birth |
| Gender | yes | ID + selfie |
| **Education level** | **no — gap** | deferred proof type; MVP may use self-declaration flagged as unverified, or ship with three filters |

Noticed gap: the original schema never included `education_level` even though every requirements doc lists it as a core demographic. Add it to `basic_filters` when implementing.

Deferred beyond MVP: `language`, `ethnicity`, named regions (needs the mapping table), and all `advanced_filters` (each requires its own social-proof module in the attribute verification pipeline).

## Interaction with Differential Pay (Beyond MVP)

The planned per-group pay rates ("18–25 earn $10, 25–35 earn $7"; "female $15 / male $10") reuse these same filter primitives: a rate group is a filter expression plus a `you_earn` value. Design the matcher so a filter expression is a reusable, evaluable object rather than logic inlined into task matching — rate groups, task visibility, and audience-size estimation all want to evaluate the same expressions.

## Open Questions

1. **Ethnicity filtering** is legally and ethically exposed (discrimination law varies by jurisdiction; the demographic-framework doc already flags this). Decide jurisdictions and permitted use cases deliberately — or drop the filter — before implementing it.
2. **Gender values**: enumerate accepted values (the schema is a free string).
3. **Region taxonomy**: pick the canonical region list and its country mapping (who says what EMEA contains?).
4. **Raw-statement parsing**: which model parses Launcher wording into structure, and what the confirmation UX looks like when parse confidence is low.
5. **Audience preview**: Launchers should see the matching-Jumper count before funding ("your filters match 23 verified Jumpers") — needs the same evaluator plus a privacy floor (don't display counts small enough to identify individuals).
