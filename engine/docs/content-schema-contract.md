# Content Schema Contract

## Authority

`engine/data/generation-bundle.schema.json` is the machine-readable output contract
for the sole creative transaction. The accepted raw bundle is generated-work canon.
Everything under `schema-generation/` and `prose/` is a deterministic projection of
that bundle, not an input to another creative generation stage.

## Generation-Branch Layout

`main` keeps downstream directories empty. A generation branch or release may contain:

```text
generated-work/<generation-id>/
  bundle.json
  manifest.json
  mechanical-validation.json
  artistic-acceptance.json

schema-generation/
  work-canon/<work-id>.json
  claimant-profiles/<work-id>.json
  character-profiles/<work-id>.json
  arc-briefs/<arc-id>.json
  scene-specs/<scene-id>.json
  artifact-specs/<artifact-id>.json
  decision-graph.json

prose/
  scenes/<scene-id>.mdx
  artifacts/<artifact-id>.mdx
  endings/<ending-id>.mdx
```

No generated work becomes canonical content of `main`.

## Bundle Boundary

The creative response must be exactly one JSON document conforming to the schema. Do
not wrap it in prose or Markdown fences. A truncated or ambiguous response fails.

The bundle contains together:

- provenance
- exact generated work canon and chronology
- five generated claimant profiles and their relationships
- generated non-claimant characters
- arc purposes and structural roles
- scene specifications and complete scene prose
- artifact specifications and complete artifact text
- ending specifications and complete ending prose
- formal-composition placement metadata
- the complete decision graph and state effects

Stable IDs use lowercase letters, digits, and underscores. Examples such as
`claimant_a`, `generated_claimant_id`, `scene_01`, and `artifact_01` are synthetic and
carry no desired fictional meaning.

## Deterministic Projection

After the bundle passes schema and cross-reference validation, a deterministic tool
may:

1. preserve the raw response as `bundle.json`
2. copy each structured record to its declared output directory
3. add mechanical frontmatter derived only from that record
4. copy `prose_mdx` or `body_mdx` verbatim beneath the frontmatter
5. serialize `decision_graph` as `schema-generation/decision-graph.json`
6. calculate file hashes and write the manifest

Projection must not summarize, rephrase, reorder literary paragraphs, normalize
punctuation, repair dialogue, add transitions, or otherwise change creative content.

## MDX Projection

Scene frontmatter is derived mechanically:

```yaml
---
id: scene_01
work_id: hospice-annex-v01
arc_id: generated_arc_id
claimant_focus_ids:
  - claimant_a
artifact_ids:
  - artifact_01
choice_edge_ids:
  - edge_01
major_decision: false
generation_id: generation_example
---
```

Artifact and ending frontmatter follow the same rule: identifiers, relationships,
state metadata, and generation ID come from the bundle; the literary body is copied
verbatim. Generated MDX is restricted to plain Markdown plus an engine-approved
component allowlist. Imports, exports, scripts, and arbitrary JSX fail mechanical
validation.

## Cross-Reference Validation

JSON Schema cannot enforce graph-wide identity. Deterministic validation must also
confirm:

- all IDs are unique within and across relevant namespaces
- all technical claimant slots appear exactly once
- every referenced claimant, character, arc, scene, artifact, ending, node, and edge exists
- every arc's scene list agrees with scene records
- every graph node resolves to exactly one scene or ending
- every graph edge has existing endpoints
- the entry scene and opening decision group exist
- the opening group has exactly three playable options
- every other meaningful decision has two to five playable options
- opening branches split again
- reconvergent nodes preserve multiple inbound edges and consequential state
- every major decision exposes a consequential hesitation path
- redirective endings name valid new-beginning scenes
- formal-composition anchors resolve to generated content
- prose, artifact, and ending hard word limits are respected
- `creative_transaction_count` equals `1`

## Manifest and Immutability

`manifest.json` records the provenance required by `engine/data/work-instance.yaml`
and a SHA-256 hash for:

- `bundle.json`
- every projected scene, artifact, and ending file
- the projected decision graph
- mechanical and artistic validation results

Once accepted, any literary hash mismatch invalidates the generation. Humans may
inspect, diff, render, preserve, or reject generated prose; they may not edit it.

## Validation Results

Mechanical validation emits structured pass/fail details. Artistic evaluation emits:

```json
{
  "generation_id": "generation_example",
  "result": "PASS",
  "reasons": []
}
```

or:

```json
{
  "generation_id": "generation_example",
  "result": "FAIL GENERATION",
  "reasons": ["Concrete reasons only"]
}
```

Neither result may contain or trigger replacement prose. A failed generation is
preserved or discarded as a whole; a later attempt starts a new generation ID and a
new single creative transaction.
