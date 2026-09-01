# Branching Architecture Contract

## Purpose

This document turns the desired branching feel of the work into explicit structural law.

Use it during deterministic preparation, the single creative transaction, validation,
and building.
Its role is to prevent the system from collapsing into three shallow claimant spines with cosmetic variation.

## Core Model

The work should read like:

1. a reader-perspective introduction
2. an exact three-option opening hub
3. a branching tree that splinters further
4. selective reconvergence where prior state still matters
5. endings that may terminate, condemn, vindicate, or redirect into a new beginning

The engine must treat this as authored structure, not optional flavor.

## Introduction Segment

Requirements:

- begin from the reader's perspective rather than a detached overview
- deliver 3 to 5 scene-pages before the first live choice hub
- keep the introduction eventful and pressure-bearing
- allow up to roughly 1.5 pages total of reflection interspersed across the opening sequence
- do not require the full claimant roster to be introduced before the first choice

Disallowed failures:

- a claimant menu disguised as an introduction
- exposition that summarizes the mystery without dramatizing it
- reflection that stalls the story instead of sharpening dread, judgment, or anticipation

## Opening Choice Hub

Requirements:

- the first live hub must present exactly three options
- each option label should summarize the scene-level decision the reader is making
- each option must lead to a materially different onward scene or branch emphasis
- the opening hub may lean toward different claimants without reducing to a bare claimant picker

Disallowed failures:

- only one live opening action
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

- opening branches must splinter again at least once before the architecture feels complete
- different branches may end at different depths
- reconvergence is lawful when the shared scene still reflects prior path history through state, pressure, or closed alternatives
- a literally shared scene is lawful if inbound state remains meaningful
- the graph may include redirective endings that become new beginnings on another branch

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
- redirective ending that opens a new beginning elsewhere in the graph

Rules:

- not every ending must be terminal in the same way
- endings should feel like selection and consequence, not merely stopping points
- redirective endings must be graph-explicit and not improvised at runtime

## Navigation Semantics

Rules:

- if a top-level control resets the experience, label it `start_over`
- do not label a reset control as `back` or `return` when it does not restore the prior page state
- hesitation inside the story is not the same as global reset and must remain distinct in wording and state effects

## Generation-Bundle Implications

The single generated bundle must explicitly encode:

- which scenes belong to the introduction sequence
- which scene or hub is the first exact three-option decision
- branch depth and branch role for each scene
- where reconvergence is allowed
- which decisions are major and require hesitation surfaces
- which endings are terminal and which are redirective

Deterministic preparation may fix abstract slots, edge cardinalities, branch depths,
reconvergence capacity, and state laws. It must not decide the actual choices, events,
branch purposes, claimant influence, revelations, or endings.

## Graph Implications

The compiled graph must explicitly encode:

- the introduction entry path
- the opening hub sibling group
- multi-option decision groups with live-option counts
- reconvergent nodes with multiple inbound edges
- redirective ending edges when an ending becomes a new beginning
- state effects that preserve path consequence through reconvergence

## Build Implications

The reader-facing build must:

- make the introduction feel like story, not setup metadata
- render choices as real decisions, not lone continuation buttons
- distinguish `start_over` from in-story hesitation
- support path-trace display for opened and closed alternatives even after reconvergence
- avoid implying browser-history semantics when only reset is available
