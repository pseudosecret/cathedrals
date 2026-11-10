# Branching Architecture Contract

## Purpose

This document turns the desired branching feel of the work into explicit structural law.

Use it during deterministic preparation, generated architecture, forward packets,
validation, and building.
Its role is to prevent the system from collapsing into three shallow claimant spines with cosmetic variation.

## Core Model

The work should read like:

1. a reader-perspective introduction
2. linear chapters and a first meaningful branch when the story earns it
3. branches with two to five distinct successors
4. selective reconvergence where prior state still matters
5. terminal final or premature endings earned by their own incoming paths

The engine must treat this as authored structure, not optional flavor.

## Introduction Segment

Requirements:

- begin from the reader's perspective rather than a detached overview
- let story pressure determine the number of scenes before the first branch
- keep the introduction eventful and pressure-bearing
- allow up to roughly 1.5 pages total of reflection interspersed across the opening sequence
- do not require the full claimant roster to be introduced before the first choice

Disallowed failures:

- a claimant menu disguised as an introduction
- exposition that summarizes the mystery without dramatizing it
- reflection that stalls the story instead of sharpening dread, judgment, or anticipation

## Opening Choice Hub

Requirements:

- the first live branch presents two to five meaningful options; preceding linear scenes have one continuation
- each option label should summarize the scene-level decision the reader is making
- each option must lead to a materially different onward scene or branch emphasis
- the opening hub may lean toward different claimants without reducing to a bare claimant picker

Disallowed failures:

- a fake three-way hub where all choices immediately collapse into the same scene with no meaningful difference
- labels that describe destinations instead of decisions

## Decision Cardinality

Rules:

- every meaningful decision must present at least two live options
- four live options is the soft maximum
- five live options is the hard maximum
- reserved, closed, or debug-only siblings do not count toward the live-option minimum

Interpretation rule:

- a single clickable action is navigation, not a choice

## Branch Topology

Rules:

- backward expansion derives earlier scenes from existing successor requirements; branches and linear chapters may alternate
- different branches may end at different depths
- reconvergence is lawful when the shared scene still reflects prior path history through state, pressure, or closed alternatives
- a literally shared scene is lawful if inbound state remains meaningful
- progression is acyclic; browser history and start_over are separate from story edges

Disallowed failures:

- three neat route ladders that never split again
- reconvergence that erases the consequences of earlier decisions
- uniform terminal depth across all branches without dramatic reason

## Major Decision Hesitation

For accusation, irreversible commitment, route lock, or comparable threshold choices:

- include a hesitation or reflection surface before the final commit
- let the reader experience dread, anxiety, counterfactual imagining, or projected consequence
- provide a commitment option and a hesitation/reconsideration option
- treat hesitation as a stateful act that can mutate pressure, reopen context, or create a new path

Disallowed failures:

- instant irreversible commitment with no interior pressure
- hesitation that behaves like a cost-free reset
- reflection that is purely lyrical and does not alter structural consequence

## Ending Families

Allowed ending behaviors:

- favorable or costly resolution
- bad ending or foreclosure
- contamination implication
- a premature ending earned before the main resolution

Rules:

- not every ending must be terminal in the same way
- endings should feel like selection and consequence, not merely stopping points
- final and premature endings are terminal under scaffold planning; neither redirects nor runtime continuation is permitted

## Navigation Semantics

Rules:

- if a top-level control resets the experience, label it `start_over`
- do not label a reset control as `back` or `return` when it does not restore the prior page state
- hesitation inside the story is not the same as global reset and must remain distinct in wording and state effects

## Generation-Protocol Implications

The committed architecture and packet records must collectively encode:

- which scenes belong to the introduction sequence
- where linear scenes continue and meaningful branches provide two to five options
- branch depth and branch role for each scene
- where reconvergence is allowed
- which decisions are major and require hesitation surfaces
- each terminal outcome and its alternative sufficient entry cases

Deterministic preparation may fix abstract slots, edge cardinalities, branch depths,
reconvergence capacity, and state laws. Generated architecture develops a backward causal scaffold, then compiles actual
slots, navigation, dependencies, promises, and ending attractors; later literary packets
instantiate content without revising canon. Noncanonical packet priority and
future-feasibility assignments may be recomputed after each commit.

## Graph Implications

The compiled graph must explicitly encode:

- the introduction entry path
- the opening hub sibling group
- multi-option decision groups with live-option counts
- reconvergent nodes with multiple inbound edges
- terminal outcomes with no outgoing story edges

Technical scene and ending slots are the stable cross-packet linking layer. An edge
to unwritten content commits a `destination` with `kind: technical_slot`; generated
literary IDs are used only after their content exists. Projection resolves each slot
exactly once without editing the earlier edge. Missing, duplicate, or unknown slots
are terminal mechanical failures.
- state effects that preserve path consequence through reconvergence

## Build Implications

The reader-facing build must:

- make the introduction feel like story, not setup metadata
- render branches as real decisions and linear chapters with their authored continuation
- distinguish `start_over` from in-story hesitation
- support path-trace display for opened and closed alternatives even after reconvergence
- avoid implying browser-history semantics when only reset is available
