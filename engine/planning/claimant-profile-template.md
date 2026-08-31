# Claimant Profile Template

## Purpose

This file defines the compiled claimant-profile artifact for a specific work instance.

It is not new canon.
It is a structural artifact derived from:

- `engine/data/work-instance.yaml`
- the file named by `claimants.roster_source_path` in `engine/data/work-instance.yaml`, if present
- otherwise `engine/data/claimants.yaml`
- the work seed and balancing rules

Use this file to preserve dynamic claimant instantiation without allowing claimant identity to drift into new archetypes.

## Output Path

Write compiled claimant profiles to:

`schema-generation/claimant-profiles/WORK_ID-claimant-profiles.yaml`

## Top-Level Shape

```yaml
version: 0.1
work_id: WORK_ID_HERE
roster_source_path: CLAIMANT_ROSTER_PATH_HERE
generation:
  mode: mixed_authoring
  semantic_drift: mode_governed
  balancing_mode: hybrid
  variation_level: high
  seed: SEED_HERE
  active_claimants:
    - CLAIMANT_1
    - CLAIMANT_2
    - CLAIMANT_3
    - CLAIMANT_4
    - CLAIMANT_5
  hard_constraint_summary:
    passed: true
    notes:
      - NOTE_1
      - NOTE_2
  scoring_summary:
    winning_set_score: SCORE_HERE
    scoring_axes:
      - AXIS_1
      - AXIS_2
      - AXIS_3
profiles:
  - claimant_id: CLAIMANT_1
    definition_mode: locked | bounded_variation | slot_generated
    route_identity: ROUTE_ID_HERE
    source_summary:
      surface_persona: SURFACE_PERSONA_SUMMARY_HERE
      claimant_law_basis: WORK_SPECIFIC_ROSTER | GLOBAL_LIBRARY
    fixed_archetype_summary:
      genre_ontology: ONTOLOGY_HERE
      role_pressure: ROLE_PRESSURE_HERE
      primary_truth_style_family: TRUTH_STYLE_HERE
      primary_evidence_family: EVIDENCE_FAMILY_HERE
      voice_family: VOICE_FAMILY_HERE
    variation_policy_summary:
      selection_rule: SELECTION_RULE_HERE
      allowed_expression_fields:
        - FIELD_1
        - FIELD_2
    slot_spec_summary:
      used: true | false
      contrast_targets:
        - CLAIMANT_ID_HERE
      grounding_constraints:
        - CONSTRAINT_1
    selected_expression:
      primary_evidence_subtype: SUBTYPE_HERE
      secondary_evidence_affinities:
        - ITEM_1
        - ITEM_2
      speech_texture:
        - TEXTURE_1
        - TEXTURE_2
      contradiction_motif: MOTIF_HERE
      environmental_drift_signature:
        - DRIFT_1
        - DRIFT_2
      local_framing_tendency: TENDENCY_HERE
      artifact_pressure_profile: PROFILE_HERE
    selected_contamination_profile:
      diction_markers:
        - MARKER_1
        - MARKER_2
      cadence_markers:
        - MARKER_1
        - MARKER_2
      structure_markers:
        - MARKER_1
        - MARKER_2
      artifact_contamination_markers:
        - MARKER_1
        - MARKER_2
    focus_escalation_notes:
      ambient: NOTES_HERE
      passing_focus: NOTES_HERE
      primary_focus: NOTES_HERE
      dominant_focus: NOTES_HERE
    artifact_surface_behavior: HOW_FRAMING_AND_DOCUMENT_BODY_SHOULD_BEHAVE_HERE
    identity_integrity_pass:
      passed: true
      notes:
        - NOTE_1
    pairwise_contrast_summary:
      against_other_claimant:
        fixed_core: WHAT_STAYED_FIXED_HERE
        expressive_drift: WHAT_DRIFTED_HERE
        distinction: WHY_IT_IS_STILL_DISTINCT_HERE
```

## Rules

- Preserve canonical claimant identity according to the claimant's `definition_mode`.
- Locked claimants must reproduce authored source exactly.
- Bounded-variation claimants may drift only in fields explicitly allowed by their `variation_policy`.
- Slot-generated claimants must be derived deterministically from `slot_spec` plus seed and the other active claimants.
- Never change route identity or forbidden traits without explicit source-truth revision.
- Reject any active claimant set that violates hard no-cross constraints.
- Score only valid claimant sets.
- Prefer the highest-separated valid set, not the most novel set.
- If no valid set survives, write a validation or ambiguity report instead of weakening the rules silently.

## What This Artifact Must Make Clear

- what is fixed by archetype law
- which authoring mode governed each claimant
- what was selected as expressive drift
- what was generated from slot_spec, if applicable
- what text-surface contamination behavior was selected for this work instance
- why the set passed balancing
- how each claimant remains different from the others
- how the output can be reproduced from the same seed
