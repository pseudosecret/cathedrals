# Generation Workflow Contract

## Invariant

One generation instance has exactly one creative model transaction. "One command"
does not excuse multiple hidden calls. Creative planning and final prose are authored
together in the same response.

## 1. Deterministic Preparation

Preparation may read only engine canon and operator-supplied technical parameters. It
must produce a context package containing:

- generation and work seeds
- engine commit and configuration hashes
- model/provider parameters and documented maximum output
- a budget calculation using `engine/data/work-instance.yaml`
- an abstract scene/branch skeleton with stable technical slots
- required decision cardinalities, reconvergence positions, and state laws
- seeded threshold-geomancy figures, resultants, and transition pressure
- the generation-bundle JSON Schema
- the single-transaction prompt

Preparation may not name characters, select claimant archetypes, invent incident
facts, choose artifacts, decide scene events, write choices, or describe endings.

### Budget Gate

Calculate:

```text
ceil(hard_max_creative_words / words_per_token_assumption)
+ structured_metadata_token_allowance
+ json_serialization_token_allowance
```

Fail before generation unless the result is at or below:

```text
selected_model_max_output_tokens - safety_reserve_tokens
```

Never respond to budget failure by splitting creative authorship across calls. Reduce
engine scope in a separate engine revision or select a model with sufficient output.

## 2. Single Creative Transaction

Send the complete prepared context once. The model returns exactly one JSON document
conforming to `engine/data/generation-bundle.schema.json` and containing the whole
fictional instantiation.

The same transaction authors:

- generated work canon
- five claimant identities and relationships
- other characters
- exact incident and chronology
- arcs and scene purposes
- scenes, choices, artifacts, clues, contradictions, endings, poetry, and prose
- graph topology labels and state effects inside the deterministic skeleton

No generated output from this call may become a prompt for a later creative call.

## 3. Deterministic Post-Processing

After the response ends:

1. preserve the raw response
2. parse JSON
3. validate the schema and all references
4. split records into the standard repo paths
5. add mechanical frontmatter
6. hash the bundle and projected files
7. compile the static Astro site

Post-processing may repair only serialization defects while every literary string and
creative fact remains byte-for-byte unchanged. If repair would require judgment,
interpretation, completion, or wording, fail the generation.

## 4. Validation

### Mechanical

Mechanical checks are deterministic and may fail for malformed structure, duplicate
IDs, broken graph edges, bad state transitions, missing sections, invalid choice
cardinality, unsafe MDX, hard-budget overflow, or build failure.

### Artistic

Artistic evaluation reads the complete immutable work and returns `PASS` or
`FAIL GENERATION` with reasons. It may assess differentiation, prose quality, scene
function, concrete detail, route distinctness, artifact force, thematic coherence,
redundancy, generic AI habits, and ending strength.

Artistic evaluation must not supply edits, replacement text, or a repair prompt.

## 5. Acceptance and Rejection

- `PASS`: preserve hashes, publish from a generation branch or release, and keep the
  reader runtime static.
- `FAIL GENERATION`: do not build for publication and do not repair the universe.
- A later fresh attempt uses a new generation ID, repeats deterministic preparation,
  and makes one new creative transaction.

## Human Escalation

Ask the human only for engine-level doctrine, ontology, mechanics, scope, technical
constraints, safety/legal issues, or impossible README requirements. Fictional
underdetermination is generative space, not a blocker.

## Forbidden Pipeline

The following is noncompliant even if one operator command triggers it:

```text
generate claimant -> generate arc -> generate scene -> critique -> rewrite -> continue
```

The only compliant creative path is:

```text
deterministic preparation -> one creative response -> deterministic processing
```
