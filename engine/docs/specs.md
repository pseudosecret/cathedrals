# Specs

## 1. Delivery Model

- The final artifact is a static website.
- All content is generated at build time.
- No live API calls or server-side logic are required in the final reader experience.

## 2. Reader Experience Contract

The reader should feel like they are exploring evidence, interviews, records, and unstable spaces in order to determine what happened. The interface should gradually reveal that they are not merely exploring but judging.

## 3. Page Types

- Title page
- Scene page
- Artifact page
- Accusation page
- Retraction page
- Ending page
- Optional interstitial or threshold page

## 4. Default Reader Surface

The default reading surface should present in this order:

1. title
2. prose
3. choices

Normal reader-facing pages must not expose build patterning, route metadata, graph jargon, debug labels, or operational scaffolding as part of the primary reading surface.

Scene pages should read as authored pages, not as tool output.
By default, route identifiers, beat names, claimant labels, and similar process metadata belong to implementation or debug layers, not the normal reader view.

## 5. Navigation Rules

- Navigation may be strange, but it must remain legible and intuitive enough to prevent user struggling.
- The reader must always have enough orientation to know they are making choices.
- Confusion may be aesthetic, but not logistical.
- Choices must be visually separate enough that each option reads as its own action.
- The default interaction pattern should make each playable option read like a full button or equivalent strong action surface, not a cluster of adjacent links.
- A consistent back action should be present in normal reading flow.

## 6. State Representation

Because the final build is static, route/state must be represented through prebuilt page variants, URL structure, local client-side state, or both. State must be minimal and inspectable by the system even if the reader does not fully understand it.

## 7. Mobile / Responsive Constraints

- All pages must be readable on mobile.
- Artifacts must degrade gracefully into stacked layouts.
- No puzzle or artifact may require hover.
- No clue may be available only through desktop-only interaction.

## 8. Artifact Rules

Artifacts are not decorative. Each artifact must do at least one of:

- supply evidence
- bias interpretation
- contradict another source
- reveal regime drift
- pressure accusation or indecision

Default artifact behavior should be inline and expandable inside the reading flow when the artifact does not divert the reader onto a different track.

The default artifact pattern is:

1. framed preview
2. short excerpt or first lines
3. explicit expansion affordance such as `read more`
4. expansion into a larger in-place container

Standalone artifact pages remain lawful when the artifact truly needs a separate reading surface or diverts to a distinct route context.

## 9. Accessibility / Readability

- Text must remain readable on phone screens.
- Contrast must be sufficient.
- There must be a light and dark mode.
- Any visual distortion must not destroy legibility.
- Important clues cannot depend on sound, animation, or hidden gestures.
- Theme switching may be visually minimal, but it should use stable, legible day/night iconography rather than ad hoc instructional wording.

## 10. Hidden Route Rules

The hidden route is unlocked by thematically meaningful reader behavior, not arbitrary tricks. Repeated refusal to commit, exhaustive traversal without commitment, or contamination-like browsing patterns are valid triggers.

## 11. Non-Goals

- No inspect-element gimmicks
- No ARG dependency
- No external tools required
- No UI novelty that weakens the reading experience
- No reader-facing labels that make the work sound like a build artifact
- No default page chrome that competes with the prose more than the choices do

## 12. Ending Path View

Ending pages should include a path view by default.
This view exists for reflection and consequence, not just debugging.

Requirements:

- The structural source must be generated from structured route and scene data.
- The rendered view must show only the path actually taken as the primary spine.
- At each decision point on that path, alternate options must appear as closed sibling branches.
- In default mode, the view should use reader-facing opened/closed language rather than implementation jargon.
- In debug mode, alternate branches may also show the scene titles they would have led to.
- The feature must use client-side state only to determine the taken path.
- The feature must not require server-side processing or live API calls.
- The default visual treatment should be static, interesting, and diagram-like, but must not depend on Mermaid specifically.
- On mobile, the view may collapse into a stacked or simplified path-trace layout.
- Debug detail may be hidden behind a subtle debug affordance in production.
