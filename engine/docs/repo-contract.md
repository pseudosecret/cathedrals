# Repo Contract

## Purpose

This document resolves repository path drift and ownership drift.

It defines where truth lives, where compiled outputs go, and which directories are templates versus generated artifacts.

## Ownership Model

### `engine/docs/`

Owns:

- artistic doctrine
- reader-experience constraints
- operator-facing execution rules
- build and validation contracts
- execution milestone defaults and workflow guidance

These files are human-authored repo truth.

### `engine/canon/`

Owns:

- ontology
- arc law
- prose/style law
- acceptance law

These files are human-authored repo truth.

### `engine/data/`

Owns:

- state model
- claimant definitions
- claimant instantiation envelopes and balancing law
- threshold geomancy rules
- work-instance definition

These files are structured repo truth.

### `engine/planning/`

Owns:

- templates
- examples
- support material for later compilation

This directory is not a destination for compiled planning outputs.

### `schema-generation/`

Owns compiled structural outputs only:

- `work-briefs/`
- `claimant-profiles/`
- `arc-briefs/`
- `scene-specs/`
- `artifact-specs/`
- `validation-reports/`
- `decision-graph.json`

Anything written here must be derivable from higher-order repo truth.

### `prose/`

Owns generated reader-facing content only:

- `scenes/`
- `artifacts/`
- `endings/`
- `interstitials/`

All generated content here must remain human-readable and editable.

### `src/`

Owns presentation logic only:

- Astro pages
- layouts
- components
- utilities for reading content and rendering the static experience

Important story truth must not live only in `src/`.

### Linear

Linear mirrors execution state after repo files exist.
Linear never becomes the sole location of lore, structure, or accepted prose.

## Canonical Path Rules

- Always reference repo doctrine and canon using `engine/...` paths.
- Never use bare `docs/...`, `canon/...`, or `data/...` paths in contracts.
- Never write compiled planning outputs to `engine/planning/`.
- Never treat `schema-generation/decision-graph.json` as hand-authored canon.
- Never store generated prose inside `.astro` files when it belongs under `prose/`.

## Output Rules

Use these locations by default:

- work brief: `schema-generation/work-briefs/<work-id>-work-brief.md`
- claimant profiles: `schema-generation/claimant-profiles/<work-id>-claimant-profiles.yaml`
- arc brief: `schema-generation/arc-briefs/<arc-file>.md`
- scene spec: `schema-generation/scene-specs/<scene-file>.md`
- artifact spec: `schema-generation/artifact-specs/<artifact-file>.md`
- validation or ambiguity report: `schema-generation/validation-reports/<report-file>.md`
- generated scene: `prose/scenes/<scene-file>.mdx`
- generated artifact: `prose/artifacts/<artifact-file>.mdx`
- generated ending: `prose/endings/<ending-file>.mdx`

## Source-of-Truth Guidance

If two files conflict:

1. `engine/llm-instructions.md`
2. `engine/docs/artistic-constitution.md`
3. `engine/docs/specs.md`
4. this file
5. `engine/data/work-instance.yaml`
6. other operator-facing docs in `engine/docs/`
7. `engine/canon/*.md`
8. `engine/data/*.yaml`
9. compiled files in `schema-generation/`
10. generated files in `prose/`
11. Linear

This ordering exists to prevent process drift from overriding canon, while still making repository mechanics explicit.
