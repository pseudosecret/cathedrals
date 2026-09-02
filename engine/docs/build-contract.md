# Build Contract

## Purpose

This document defines how Astro should consume repo truth and render the complete
accepted generated work without moving story structure into runtime code.

## Build Principles

- Astro only
- static output only
- no live API calls
- no server-side story state
- content-first rendering from repo files
- graph-driven ending-path behavior
- no reader-visible build or debug framing in default mode

## Aesthetic Quality Bar

The build must not stop at functional competence.
It should look intentionally art-directed enough that a human reader feels the work has a visual point of view.

Requirements:

- favor one or two strong visual ideas per page type over many weak decorative gestures
- make hierarchy obvious at a glance: title, prose body, artifacts, and choices should each have a distinct visual role
- keep the prose as the dominant reading surface while letting surrounding chrome frame pressure and consequence
- use typography with visible character and rhythm rather than default utilitarian stacks unless canon justifies plainness
- use color, texture, and contrast deliberately; avoid muddy low-contrast haze and avoid generic gradient wallpaper
- let route-sensitive accents or atmosphere sharpen claimant pressure without turning every route into a separate app
- prefer restraint over clutter; avoid gratuitous badges, pills, glass panels, or card piles that cheapen the reading surface
- treat ending pages as ceremonial consequence surfaces, not generic summary screens
- if the build is technically correct but visually generic, continue iterating

## Canonical Inputs

The executable projects immutable committed records into:

- `generated-work/<generation-id>/web/public/work.json`
- `generated-work/<generation-id>/web/public/source/<content-id>.md`

The same files are built in ignored run staging before the complete-work barrier and
published only after acceptance. They are deterministic projections of append-only
generation records; literary source files remain readable, diffable, and immutable.

The build layer does not invent route structure.
`work.json` carries the deterministic projection of committed generated architecture,
not hand-authored canon.
The build layer also does not expose route-structure language to the normal reader unless an explicit debug view is enabled.

## Markdown Projection

Literary fields retain their historical `*_mdx` names but contain constrained
Markdown, not executable MDX. Preserve their exact UTF-8 bytes under `public/source/`.
At Astro build time, render display HTML with the pinned `markdown-it` dependency,
with `html: false`, linkification disabled, and no browser runtime renderer. Mechanical
validation rejects authored HTML tags before commit; HTML-disabled rendering is
defense in depth.

## Generated Art Direction

Genesis commits one bounded `web_art_direction` informed by the frozen brief. The
model selects only known typography classes, six parsed colors, density, border,
surface, artifact, transition, ending, and route-pressure enums. Contrast validation
runs before genesis commit. The deterministic projector maps those values to CSS
variables and known declarations inside a stable prose-first Cathedrals layout.
The alternate reading theme is deterministically tinted from the committed palette;
foregrounds are darkened only as far as needed to meet the same contrast floors.
Arbitrary generated CSS, JavaScript, font URLs, layout declarations, and assets are
not protocol fields.

## Route Structure

Use these route families:

- `/` for the title page
- `/scenes/[sceneId]`
- `/artifacts/[artifactId]`
- `/endings/[endingId]`
- optional `/interstitials/[interstitialId]`

Do not make a route the sole source of story text; it belongs in projected work data
and verbatim source files.

Default reading flow should privilege:

1. title
2. reader-perspective introduction
3. prose
4. choices

Artifact routes remain lawful, but the default artifact behavior should be inline expansion inside scene flow unless the artifact diverts to a distinct track or requires a separate reading surface.

The executable structure should assume:

- a 3 to 5 page introduction before the first live choice hub
- an exact three-option first hub
- post-hub branch splintering and selective reconvergence
- variable terminal depth rather than uniform shallow claimant ladders

Edges may retain a frozen `destination` technical slot across packets. Static
projection resolves it to one committed scene or ending content ID without mutating
the edge. Missing, duplicate, or nonexistent slots fail mechanical validation.

## Reader State

Reader state must be client-side only.

Use one stable local-storage namespace:

- `cathedrals:<generation-id>:reader-state:v1`

Required state shape:

```json
{
  "visitedSceneIds": [],
  "visitedArtifactIds": [],
  "chosenEdgeIds": [],
  "currentEndingId": null,
  "accusedClaimantId": null,
  "dominantRegimeId": "neutral",
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
- every meaningful decision presents at least two live options
- the opening hub presents exactly three live options
- four live options is the soft maximum and five is the hard maximum
- playable choices must not read as a single row of adjacent inline links
- a single continuation button must not be framed as a decision
- closed or reserved sibling options must not be rendered as equivalent live choices during normal scene reading
- if the top control resets progress instead of restoring prior page state, label it `start_over`
- do not present fake back-navigation language when the system is actually resetting
- any reader-facing choice labels should remain short and legible on mobile
- major decisions should support a hesitation/reconsideration surface before final commitment when the graph marks them as such
- on wide scene layouts, the primary decision block should sit below the scene prose rather than being stranded in a distant side rail
- the reader should not have to scroll back upward through a long scene merely to reach the primary next action after finishing the current scene text

## Hesitation and Reflection Rendering

Major decision surfaces may include a brief reflective interval before commitment.

Requirements:

- hesitation copy should let the reader feel dread, anxiety, or projected consequence
- the hesitation surface must still move story state or path pressure
- hesitation and reconsideration must remain distinct from global reset
- if hesitation opens a mutated path, that path must come from graph/state data rather than ad hoc runtime logic

## Artifact Rendering

Default artifact behavior is inline expandable rendering.

Requirements:

- a scene may present an artifact preview in a framed container
- the preview should expose a short excerpt or first lines plus a clear expansion affordance
- activating the artifact should expand it in place into a larger readable container by default
- artifact navigation must not strand the reader on the wrong scene or present misleading return destinations
- standalone artifact pages are reserved for artifacts that genuinely divert the route or require a separate reading surface
- on wide layouts, persistent artifact context may live in a secondary right rail so long as the prose remains centered and the decision block stays in the primary reading column

## Ending Path Rendering

The ending-page path view must be derived from:

- resolved decision edges in projected `work.json`
- the reader's client-side `chosenEdgeIds`
- the current ending id

Rendering rules:

- show the taken path as the primary spine
- show closed sibling options at each taken decision point
- preserve reconvergence legibility when two earlier branches lead into the same later scene
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
- do not satisfy the minimum live-option rule for a decision set

## Graph-Driven State Effects

When an edge changes reader state materially, the graph export must carry that information directly.

Use typed per-edge `state_effects` from the generation-protocol contract rather than
claimant-specific runtime conditionals.

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
- enough retained visual identity in both themes that neither mode feels like an unstyled fallback

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

Build work is not complete until the site can render every lawful path in the complete
accepted work from repo-managed prose and graph files without hand-authored story
structure in `src/`.
It is also not complete if the result remains visually interchangeable with a generic content template.

Astro compilation failure is a mechanical generation failure. Build code may be fixed
when the defect is in the engine, but generated prose, artifacts, facts, and graph
meaning may not be edited to make a failed generation compile. Nothing is playable
until the complete static build passes; runtime generation and partial play are
forbidden.
