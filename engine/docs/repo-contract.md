# Repo Contract

## Authority Order

When active files conflict, use:

1. root `README.md`
2. `engine/llm-instructions.md`
3. `engine/docs/artistic-constitution.md`
4. `engine/canon/`
5. `engine/data/work-instance.yaml`
6. other active `engine/docs/`, prompts, and templates
7. an accepted generation bundle on its generation branch
8. deterministic projections in `schema-generation/` and `prose/`
9. tracker state

Historical records never override active engine truth.

## Engine Canon

Human-authored engine canon exists before generation:

- `engine/docs/`: doctrine, workflow, schema, validation, and build contracts
- `engine/canon/`: ontology, grammar, style, and acceptance law
- `engine/data/`: state, claimant-set law, geomancy, scope, and bundle schema
- `engine/prompts/`: deterministic preparation and the sole creative instruction
- `engine/planning/`: shapes for records generated inside the one transaction

Engine canon may constrain relationships and structure. It may not prewrite the
particular characters, incident, routes, artifacts, revelations, or endings.

## Generated Work Canon

Generated work canon begins only when one complete creative bundle is returned. On a
generation branch it owns exact fictional facts, claimant profiles, characters, arcs,
scenes, artifacts, choices, endings, poetry, and prose.

Generated work canon is immutable and local to its generation ID. It never becomes
engine canon merely because it was accepted once.

## Downstream Directories

- `generated-work/` preserves the raw bundle, manifest, hashes, and verdicts.
- `schema-generation/` contains deterministic structured projections.
- `prose/` contains deterministic readable MDX projections.
- `src/` contains Astro presentation logic only.

No downstream directory is authoritative during `engine_revision`. Important story
truth must never live only in `src/`.

## Main Branch

`main` contains the machine, not a canonical generated story. Generated bundles and
their projections belong on generation branches, build branches, or releases. Empty
downstream directories may remain on `main` as destination scaffolding.

## Immutability

Generated prose is readable, inspectable, renderable, diffable, and preservable—not
editable. Accepted hashes make literary mutation detectable. If a work fails, reject
the generation rather than modifying it.

## Path Rules

- Always cite engine truth with `engine/...` paths.
- Never write compiled output into `engine/planning/`.
- Never treat `schema-generation/decision-graph.json` as hand-authored canon.
- Never embed generated literary content in Astro components.
- Never use a missing path as canonical authority.
- Never mark a milestone complete while any declared output is absent.
