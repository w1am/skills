---
description: Simplify code by simplifying the business logic and underlying model, not by extracting reusable methods. Use when business rules feel tangled, conditionals sprawl, or a hidden concept is suspected.
argument-hint: [path or component or "what feels complex"]
allowed-tools: Read, Grep, Glob, Task, Edit, Bash(git status:*), Bash(git diff:*)
---

# Simplify the Logic, Not Just the Code

Target: **$ARGUMENTS**

You are reducing *problem* complexity (the business logic + model), which in turn
collapses *code* complexity. You are NOT extracting helpers, renaming, or
de-duplicating. Those are out of scope.

The shift you're hunting: a hidden concept or a better model that, once made explicit,
makes a pile of conditionals and special cases disappear at once. Sometimes the win is
deleting a rule that didn't need to exist.

## Phase 1 - Map the territory

Read the target. List the business rules actually encoded and where complexity lives:
sprawling conditionals, boolean/flag arguments, special cases, rules duplicated across
the codebase, logic in the wrong place.

## Phase 2 - Fan out (parallel investigation)

Launch these subagents IN PARALLEL via the Task tool. One message, multiple Task calls.
Each gets the target context + relevant code. Each returns findings only, NO edits.

1. **Hidden-concept hunter** - find a concept that exists in the logic but was never
   named. A cluster of booleans/enums/conditionals that is really one missing type,
   status, or rule object. The thing the team says out loud but the code doesn't model.
   Usually where the biggest simplification hides.

2. **Rule archaeologist** - extract every business rule. For each: essential or
   accidental? Duplicated? Contradicted? Dead? Over-specified beyond what's actually
   needed? Flag rules that may not need to exist at all (cheapest code = code you don't
   write).

3. **Misplaced-logic mapper** - where is logic in the wrong layer or object? What must
   always be true (invariants) but is enforced in scattered or leaky ways? Where does
   the current structure fight the rules instead of expressing them?

4. **Naming auditor** - mismatches between code names and how the team actually talks
   about the thing. Same concept named differently in different places. One name hiding
   two concepts. Naming drift signals a modeling gap.

(Optional 5th if tests exist: **behavior cartographer** - what behavior must be
preserved vs what's incidental, so the rework is safe.)

## Phase 3 - Synthesize

Look for the single change that fixes several findings at once. Often one new
well-named type or rule object deletes branches everywhere.

Present:
- **Current logic** - rules + where it's tangled, briefly
- **The hidden concept(s)** found, made explicit
- **Proposed model** and why it's simpler
- **What collapses** - which conditionals / duplication / special cases vanish
- **What gets deleted** - rules or features that needn't exist
- **Risk + behavior preservation** notes

## Phase 4 - Apply (only after I confirm)

STOP and present the synthesis first. Do not edit yet.
After I approve, implement it. Preserve behavior unless a rule was identified as
removable (call those out separately, never silently drop). Keep diffs reviewable. Run
tests if present.

If you catch yourself reframing this as "just extract a method," that's the wrong move.
The win is simpler logic, not better-organized code.
