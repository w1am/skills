---
name: business-context
description: >-
  Explain business terms, requirements, rules, calculations, and workflows in
  plain language grounded in their real business setting. Use when a user asks
  what a business concept means, wants requirements or documentation made
  understandable to a newcomer, requests onboarding-friendly definitions, or
  needs technical wording rewritten so readers understand the actors, event,
  purpose, and outcome before implementation details.
---

# Business context

Explain the business reality first. Treat formulas, data structures, and software
behavior as supporting detail.

## Build the explanation

1. Establish the relevant business setting from the conversation and available
   project material. Do not invent missing policy. Label reasonable inferences and
   call out material ambiguity.
2. Lead with a one-sentence contextual definition:

   > **[Term]** means **[familiar meaning]** in **[business process or situation]**.

   Add its business purpose or consequence when that helps the reader understand
   why it matters.
3. Give one small, concrete example using recognizable actors, events, or
   quantities.
4. Explain the operational rule after the example: what triggers it, who or what
   acts, and what result follows.
5. Add a formula, system rule, or implementation detail only after the business
   meaning is clear and only when useful.
6. Define unavoidable jargon and acronyms on first use.

Prefer a short paragraph over a list when one sentence and one example are
sufficient.

## Rewrite requirements

Preserve the original rule while making the business event and outcome explicit.
Use this pattern where it fits:

> When **[business event or condition]**, **[actor or system]** must
> **[observable action]**, producing **[business outcome]**.

Include applicable scope, timing, exceptions, and source of truth when they are
known. Do not add a rationale, policy, threshold, or exception that the source
does not establish.

If the original wording permits materially different interpretations, explain the
ambiguity before proposing a rewrite.

## Separate conceptual layers

Present information in this order:

1. **Business meaning** — what the concept represents in the real operation.
2. **Concrete example** — how a person encounters it.
3. **Business rule** — when it applies and what happens.
4. **Technical detail** — formulas, fields, validations, or implementation.

Omit later layers when the user only needs the meaning.

## Apply the newcomer test

Before answering, check that a new team member can identify:

- What the term or rule refers to.
- Where it occurs in the business.
- Why it matters or what outcome it affects.
- What happens in a typical example.

Avoid:

- Circular definitions that repeat the term.
- Replacing one unfamiliar phrase with another.
- Starting with database fields, formulas, or architecture.
- Assuming company-specific knowledge.
- Presenting an inferred rule as documented fact.

## Example

Implementation-first wording:

> Calculate overdue days from the due date.

Business-context explanation:

> **Overdue days** are the number of days a customer payment is late after an
> invoice reaches its payment due date. For example, if payment was due on
> 10 June and remains unpaid on 15 June, it is five days overdue. The system
> calculates this value so the team can identify invoices that need collection
> follow-up.
