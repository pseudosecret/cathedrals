# Human Decision Contract

## Purpose

This document defines when the human must be asked because repo policy cannot lawfully derive the answer.

Normal project defaults do not live here.
Machine-resolvable decisions must be encoded in `engine/data/work-instance.yaml`.
This file exists to prevent chat-only canon from replacing repo truth.

## Rule

Ask the human only when the answer cannot be derived from:

- authored canon
- claimant law
- state law
- work-instance scope and milestone truth
- generation-resolution policy in `engine/data/work-instance.yaml`

Escalate only when the missing answer would materially change:

- lawful planning structure
- prose truth
- build behavior
- validation acceptance

Do not resolve repo-truth gaps in chat alone.

## Escalation Triggers

Ask the human if the change would require:

- claimant roster change
- ontology change
- central transgression class change
- milestone expansion beyond canonical deliverables
- explicit named-character specificity beyond current work-instance policy
- validation-proven widening of policy envelopes

## Forbidden Shortcuts

Do not:

- invent new defaults here instead of updating `engine/data/work-instance.yaml`
- treat chat memory as canon
- answer unresolved canon questions only in Linear
- bypass work-instance policy because a generated output "seems fine"

## Recording Rule

When escalation is necessary:

- update `engine/data/work-instance.yaml` first
- then regenerate or revise downstream artifacts as needed
- note the change in validation or tracking only after repo truth is current
