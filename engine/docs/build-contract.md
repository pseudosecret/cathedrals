# Build Contract

## Purpose

This document defines how Astro should consume repo truth and render the current accepted executable slice without moving story structure into runtime code.

## Build Principles

- Astro only
- static output only
- no live API calls
- no server-side story state
- content-first rendering from repo files
- graph-driven ending-path behavior
- no reader-visible build or debug framing in default mode

## Canonical Inputs

The build layer reads from:

- `prose/scenes/*.mdx`
- `prose/artifacts/*.mdx`
- `prose/endings/*.mdx`
- `prose/interstitials/*.mdx` when present
- `schema-generation/decision-graph.json`

The build layer does not invent route structure.
The build layer also does not expose route-structure language to the normal reader unless an explicit debug view is enabled.

## Route Structure

Use these route families:

- `/` for the title page
- `/scenes/[sceneId]`
- `/artifacts/[artifactId]`
- `/endings/[endingId]`
- optional `/interstitials/[interstitialId]`

Do not embed story text directly in routes when it belongs in `prose/`.

Default reading flow should privilege:

1. title
2. prose
3. choices

Artifact routes remain lawful, but the default artifact behavior should be inline expansion inside scene flow unless the artifact diverts to a distinct track or requires a separate reading surface.

## Reader State

Reader state must be client-side only.

Use one stable local-storage namespace:

- `cathedrals:hospice-annex-v01:reader-state:v1`

Required state shape:

```json
{
  "visitedSceneIds": [],
  "visitedArtifactIds": [],
  "chosenEdgeIds": [],
  "currentEndingId": null,
  "accusedClaimant": null,
  "dominantRegime": "neutral",
  "contamination": 0,
  "indecisionCount": 0,
  "retractionCount": 0,
  "hiddenRouteUnlocked": false,
  "worldScars": [],
  "debugPathTrace": false
}
```

## Choice Rendering and Navigation

Playable choices must render as clearly separate action surfaces.

Requirements:

- default scene choices render as full-width buttons, stacked buttons, or another equally unambiguous action layout
- playable choices must not read as a single row of adjacent inline links
- closed or reserved sibling options must not be rendered as equivalent live choices during normal scene reading
- a consistent back action must be available in normal reader flow
- any reader-facing choice labels should remain short and legible on mobile

## Artifact Rendering

Default artifact behavior is inline expandable rendering.

Requirements:

- a scene may present an artifact preview in a framed container
- the preview should expose a short excerpt or first lines plus a clear expansion affordance
- activating the artifact should expand it in place into a larger readable container by default
- artifact navigation must not strand the reader on the wrong scene or present misleading return destinations
- standalone artifact pages are reserved for artifacts that genuinely divert the route or require a separate reading surface

## Ending Path Rendering

The ending-page path view must be derived from:

- `schema-generation/decision-graph.json`
- the reader's client-side `chosenEdgeIds`
- the current ending id

Rendering rules:

- show the taken path as the primary spine
- show closed sibling options at each taken decision point
- in normal mode, use reader-facing opened/closed language and avoid implementation labels such as `decision scar`, `mode`, or similar debug framing
- in debug mode, destination scene or ending titles may also appear
- the default visual treatment should be static, diagram-like, and visually authored without depending on Mermaid
- the normal reader version should feel like part of the ending, not a detached diagnostic panel

Do not render the full graph as the default reader view.

## Reserved Edge Rule

The build layer must tolerate reserved sibling edges in the graph.

Reserved edges:

- are visible to the ending-path system as closed alternatives
- are not linked as playable destinations unless the current milestone makes them playable
- may be labeled for debug or reflection purposes
- may remain internally named `reserved` for structural export, but normal reader language should prefer `closed`

## Graph-Driven State Effects

When an edge changes reader state materially, the graph export should carry that information directly.

Use per-edge `state_effects` to describe canonical state mutations such as:

- setting an accused claimant
- shifting dominant regime
- incrementing indecision
- adding world scars

Downstream page implementations should prefer graph-driven state effects over hardcoded claimant-specific edge behavior.

## Content Loading

Prefer predictable content loading:

- Astro content collections
- static imports
- or simple glob-based loading

Avoid opaque loaders or runtime fetches.

## Mobile and Theme Requirements

The first implementation must satisfy:

- readable body text on narrow phone screens
- no hover-only clues or interactions
- artifact layouts that stack cleanly on mobile
- light mode and dark mode from the start
- sufficient contrast in both themes
- a minimal visual theme control that uses stable day/night iconography rather than text-only toggle phrasing

## Debug Gating

Debug path-trace detail must not be loud in the default production reader experience.

Allowed debug controls:

- a local client-side toggle
- a non-prominent debug switch
- a query-param or dev-only affordance

Disallowed debug controls:

- server-only flags
- logic that changes canonical story structure at runtime

## Build Completion Condition

Build work is not complete until the site can render the current accepted executable slice from repo-managed prose and graph files without hand-authored story structure in `src/`.
