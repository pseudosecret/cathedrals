# Cathedrals

Table of contents

- [Cathedrals](#cathedrals)
  - [An apology in advance](#an-apology-in-advance)
  - [Pre-considerations](#pre-considerations)
  - [What this is](#what-this-is)
    - [Aesthetic choices](#aesthetic-choices)
  - [Repo structure](#repo-structure)
  - [Where can I read the stories?](#where-can-i-read-the-stories)
  - [Final words](#final-words)

The Arts.

I. Love. The Arts.

I also have been smitten with generative AI since I've been using it a few years back. I think it's fascinating, but what people explore doing with it is not always as interesting or as beautiful as could be.

## An apology in advance

A lot of people hate on AI and claim it can't do art. I agree in principle up to a point way down towards the end of the line. Leaving aside ethical concerns of copyright, etc., AI does not generate art; it generates _entertainment_.

Entertainment can be beautiful, but it is not art.

Something that is art becomes art when it's framed as such. To frame a work, the question needs to be posed by the self or someone else: "Is this art?" If the answer is yes, it passes the _art challenge_ and it becomes art; if not, it fails the _art challenge_ and is not.

How we frame things in our experience is the determining factor of whether something is art.

Authorial information, either leaked into the framing by the work itself or discourse around it, can turn the framing such that it no longer passes the art challenge. AI, perhaps unsuprisingly, tends to poison the framing.

There are a _lot_ of reasons for this. E.g.,

- some people believe only humans can create art
- more time spent honing the craft and creating the work makes a work matters
  - i.e., more time equates to a work being more worthy to pass the art challenge
- effort matters, and AI seems effortless
- humans have emotionality and originality
  - what exactly that means is to far aside to really get into here

Like I said, though: I believe—or at least want to believe—that it's possible to create _some kind_ of work using generative AI that could not only pass the art challenge in spite of AI, but be appreciated more because of it.

## Pre-considerations

So to reiterate: I want to create a work that passes the art challenge, where AI is both involved and the work would not be possible without it.

There were a few things I wanted to take into account when cooking this project up.

- visual art just ain't my area, so I didn't want to go there
- generative AI has a weird relationship with audio right now, and I just didn't want to go there either
- the best way to make AI a necessary piece is to have it do things people can't do, such as:
  - live back-and-forth
  - rapid, on-demand, heavily customized production

Regarding the first two bullets, this mean my chosen medium is: _literature_. As in, _high arts_, (perhaps nauseatingly) fancy literature—when creative writing transcends itself.

Regarding the last main bullet, those felt like cheating to me for this challenge, so I decided not to go that route.

Which brings me to a description of what I _did_ decide to make.

## What this is

In as few words as possible: a sprawling fractal-like labyrinth in the form of a choose-your-own-adventure styled work, presented as a static website.

I chose a few hard-mode limitations:

- generative AI must be author of all poetry and prose
  - i.e., I cannot write, edit, or delete any of the poetry or prose generated
- the work must be generated in one pass
  - that is, I cannot use AI to go back and revise the work after initial generation
  - nor can I write a prompt for one scene, generate, then the next, generate, etc.
  - the AI must generate all scenes, arcs, artifacts—everything—in a single pass
- the work cannot use any form of serverside interaction besides hosting
  - no API calls, no databases—absolutely nothing but what lives directly in the browser
- I cannot determine scene-by-scene activity, or even fully determine activity for a given arc
  - while I can set up rails, the AI must do this on its own
- the scale and complexity needs to be utterly inhuman while remaining aesthetically/thematically coherent
  - please be reminded: context is an enormous problem in early 2026's AI
    - context not withstanding, my experience is that AI has poor ability to evolve plot
    - when AI writes narrative at larger scale, it can get horribly, horribly lost and tends to linger

And last but certainly not least:

- the work **must** stand on its own, full stop

The best way I can put it is: I am carefully aligning a prism on a pendulum to catch the sunlight in order to burn seemingly random—but ultimately controlled—designs onto a canvas.

My hope is that what this projects entails is a work that stands on its own, but knowing AI a required force in its creation enhances appreciation for it.

### Aesthetic choices

I don't want to spoil much in case anyone wants to read any part of what I ultimately have obliquely created, but the central theme I've settled on that is reinforced in the narrative concepts (in which I have defined neither character nor plot) centering around a singular theme:

"**Saying 'yes' is the biggest 'no' you can say to everything else.**"

Additionally, I want to explore poetic forms that are normally difficult and tedious. For instance, I _love_ contrapuntal writing. I think it's beautiful, fascinating, and it's something that I started experimenting with in my mid 20's before I knew it was a thing. I also love many other kinds of form-poetry, like cinquains and pantoums and ghazals. I want to weave that into storytelling in meaningful ways.

Meaningful ways that I have no real control over.

There are other things I want to feel out, too: for instance, I want to explore the fractal nature of storytelling; I want to explore the sonder of human life, our interconnection; the relationship between closing, opening, and the threshold between the two.

I also want to explore multiple genres, mixed and mashed within the same story. The tug and pull of gravity that everyone's life has in varying degrees in different orbits—how everyone's personal story feels a little or a lot different, depending on scope, but it all carries the same air of a shared, lived reality.

So I suppose, unsurprisingly, the work I'm wanting to create—my humble submission to the spirit of Art—is of what I consider beautiful.

Hopefully you'll find those things beautiful, too.

## Repo structure

I don't want to talk about the implementation much because it's... that's not the point. While I'm sure there are some people who would be interested in what does what, that's why the main branch will never contain a story—so you can look through the starting files and see what rules and guidelines and guardrails are in place to wrangle the LLMs.

What I want to emphasize, though, is that my intent is to have branches that contain all of the different stories created. They will contain the items the main branch used in creation of what it created, so you can see where the prism was in the air when it burned the canvas that particular time. There may be something worth pulling out of it later—not sure—but doing it this way.

I figure this ultimately made more sense than having a ton of different repos or having different repos for different stories or versions or whatever across the way-too-many github accounts I have.

## Where can I read the stories?

This is probably the most important question. As of the time of writing this `README.md` file, I have spent probably several days or so creating the architecture to do a build and have only generated _one_ story—and it's intentionally just a very specific branch with no choices.

So, as of 3/20/2026, there is nothing worth reading.

However, my goal is to ultimately post the best ones to a website, maybe with different subdomains for each of the actual end artifacts generated? I don't know exactly how I'm doing it yet; I'll worry about that when I get there.

As soon as such a thing exists, you'll be able to find a link to it on the Projects page of [my website](https://lorselq.com/), and I'll update this page to include that information.

## Final words

"Take it sleazy." There! I said it! I got to say it!

Please take care of you and yours. If you want to talk about this or other projects of mine ([especially this one because what I wouldn't do for some guidance](https://github.com/lorselq/enochian_language_modeling)), feel free to send me a [discord message](https://discord.com/users/lorslq).
