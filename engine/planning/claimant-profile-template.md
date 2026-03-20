# Claimant Profile Template

## Purpose

This file defines the compiled claimant-profile artifact for a specific work instance.

It is not new canon.
It is a structural artifact derived from:

- `engine/data/claimants.yaml`
- `engine/data/work-instance.yaml`
- the work seed and balancing rules

Use this file to preserve dynamic claimant instantiation without allowing claimant identity to drift into new archetypes.

## Output Path

Write compiled claimant profiles to:

`schema-generation/claimant-profiles/WORK_ID-claimant-profiles.yaml`

## Top-Level Shape

```yaml
version: 0.1
work_id: WORK_ID_HERE
generation:
  mode: instantiation_only
  semantic_drift: expression_only
  balancing_mode: hybrid
  variation_level: high
  seed: SEED_HERE
  active_claimants:
    - CLAIMANT_1
    - CLAIMANT_2
    - CLAIMANT_3
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
    route_identity: ROUTE_ID_HERE
    fixed_archetype_summary:
      genre_ontology: ONTOLOGY_HERE
      role_pressure: ROLE_PRESSURE_HERE
      primary_truth_style_family: TRUTH_STYLE_HERE
      primary_evidence_family: EVIDENCE_FAMILY_HERE
      voice_family: VOICE_FAMILY_HERE
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

- Preserve canonical claimant identity.
- Drift only in expression.
- Never change ontology, role pressure, route identity, or forbidden traits.
- Reject any active claimant set that violates hard no-cross constraints.
- Score only valid claimant sets.
- Prefer the highest-separated valid set, not the most novel set.
- If no valid set survives, write a validation or ambiguity report instead of weakening the rules silently.

## What This Artifact Must Make Clear

- what is fixed by archetype law
- what was selected as expressive drift
- what text-surface contamination behavior was selected for this work instance
- why the set passed balancing
- how each claimant remains different from the others
- how the output can be reproduced from the same seed
