# Repo Contract

## Authority Order

When active files conflict, use:

1. root `README.md`
2. `engine/llm-instructions.md`
3. `engine/docs/artistic-constitution.md`
4. `engine/canon/`
5. `engine/data/work-instance.yaml`
6. other active `engine/docs/`, prompts, and templates
7. immutable committed generation records in their run directory
8. deterministic projections in `schema-generation/` and `prose/`
9. tracker state

Historical records never override active engine truth.

## Engine Canon

Human-authored engine canon exists before generation:

- `engine/docs/`: doctrine, workflow, schema, validation, and build contracts
- `engine/canon/`: ontology, grammar, style, and acceptance law
- `engine/data/`: state, claimant-set law, geomancy, scope, and generation protocol
- `engine/prompts/`: deterministic preparation and phase-specific run instructions
- `engine/planning/`: documentation shapes for generated records

Engine canon may constrain relationships and structure. It may not prewrite the
particular characters, incident, routes, artifacts, revelations, or endings.

## Generated Work Canon

Generated work canon begins with the Genesis foundation and becomes complete when its
constraint record commits; it grows only through immutable, causally forward
Architecture and packet commits. Within its run it owns
exact fictional facts, claimant profiles, characters, arcs, scenes, artifacts,
choices, endings, poetry, and prose.

Generated work canon is immutable and local to its generation ID. It never becomes
engine canon merely because it was accepted once.

## Downstream Directories

- `generated-work/<generation-id>/provenance/` preserves the frozen manifest, raw
  responses, committed records, append-only ledger/constraints/planning history, hashes, and verdicts.
- `generated-work/<generation-id>/web/` is the normal static Astro project and keeps
  its deterministic work JSON plus verbatim literary source files.
- `.cathedrals/runs/<generation-id>/` is ignored operational state used for atomic
  commits, resume, constraint retrieval, prospective planning, validation,
  pre-publication builds, and rejected-work diagnostic builds.
- `.cathedrals/runs/<generation-id>/engine-snapshot/` is the run-local copy of the
  launcher and engine used after the run starts.
- root `schema-generation/`, `prose/`, and `src/` remain legacy projection scaffolds;
  the executable does not mutate them during an engine revision.

No downstream directory is authoritative during `engine_revision`. Important story
truth must never live only in an Astro route.

## Source and Generated Work

The current local launcher and engine are legitimate inputs, whether modified or
unmodified. Each new run copies them into its own run directory and never consults the
installation again. Successful publication copies only the new generated-work tree.
Failed runs remain under `.cathedrals/` and do not publish by default.

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
