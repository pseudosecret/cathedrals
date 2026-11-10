# Build Contract

## Static publication

The root `cathedrals` launcher projects committed records into a dependency-free
static HTML reader. No Node, npm, Astro, runtime model, API, database or server-side
story state is needed to build or read the published work.

Publication happens only after complete-work mechanical validation and static-build
validation pass. The projector never invents story structure or changes literary
bytes. Only the new `generated-work/<generation-id>/` tree is published.

## Canonical inputs and rendering

`web/public/work.json` contains committed scenes, endings, artifacts, resolved edges,
and the entry content ID. `web/public/source/<content-id>.md` preserves each literary
field's exact UTF-8 bytes. The build copies these into `web/dist/`, alongside the
reader pages, CSS and client-side scripts. Projection metadata names `static_html`.

Literary fields retain their historical `*_mdx` names but contain constrained
Markdown. The standard-library renderer escapes all authored text, renders heading
blocks and paragraphs, and preserves line breaks. It does not execute HTML or MDX,
interpret raw URLs, or fetch resources. Source exports retain richer Markdown
syntax verbatim; display rendering remains deliberately limited. Mechanical
validation also rejects authored HTML before commit.

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

## Generated Art Direction

The Genesis foundation commits one bounded `web_art_direction` informed by the frozen brief. The
model selects only known typography classes, six parsed colors, density, border,
surface, artifact, transition, ending, and route-pressure enums. Contrast validation
runs before the Genesis foundation commit. The deterministic projector maps those values to CSS
variables and known declarations inside a stable prose-first Cathedrals layout.
The alternate reading theme is deterministically tinted from the committed palette;
foregrounds are darkened only as far as needed to meet the same contrast floors.
Arbitrary generated CSS, JavaScript, font URLs, layout declarations, and assets are
not protocol fields.

## Pages and navigation

The reader emits `/`, `/scenes/<scene-id>/`, `/endings/<ending-id>/`, and
`/artifacts/<artifact-id>/`. The title page links to the committed opening.
Every scene and ending has its own page; artifacts expand inline and have
standalone evidence pages. Prose remains the primary reading surface, with choices
below it and a clear theme control.

The frozen causal scaffold supplies navigation. One authored exit is a chapter
continuation; two to five exits form a branch. Endings are terminal in the current
planner. No separate introduction length or opening-hub width overrides the
scaffold. Projection resolves technical destinations to committed content IDs
without mutating the original edges. Missing, duplicate or nonexistent destinations
fail validation. Only playable edges become reader links.

## Reader state

State is client-side, in `cathedrals:<generation-id>:reader-state:v1`, as
`{"path": [], "values": {}}`. A newly entered scene or ending appends its content
ID and applies its state effects. Choices test graph-supplied conditions and apply
graph-supplied effects before navigation. Reset clears this generation's reader
state. Theme preference uses its own local-storage key.

State behavior comes from typed protocol conditions/effects; it cannot add story
facts or routes. The engine verifies reachable state alternatives before publication.
Debug or development UI must not change canonical story meaning.

## Mobile and Theme Requirements

The first implementation must satisfy:

- readable body text on narrow phone screens
- no hover-only clues or interactions
- artifact layouts that stack cleanly on mobile
- light mode and dark mode from the start
- sufficient contrast in both themes
- a minimal visual theme control that uses stable day/night iconography rather than text-only toggle phrasing
- enough retained visual identity in both themes that neither mode feels like an unstyled fallback

## Build completion

The build must emit every assigned page and preserve all literary source files,
work data and reader assets. Validation checks visible prose, local link targets,
source bytes and asset bytes. Missing prose, a placeholder page, an escaping link,
or incomplete coverage fails the build and prevents publication.

Build defects may be fixed in engine machinery; committed prose, artifacts, facts
and graph meaning may not be edited to make a build pass. Partial play and runtime
generation remain forbidden. Finalization retains `npm_enhancement: NOT_RUN`
because the publisher has no npm step. Artistic review is advisory, with its
actual run status recorded separately from the mechanical publication gates.
