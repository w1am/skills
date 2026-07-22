---
name: naming-review
description: >-
  Fix names in recently-changed code, including when the right fix is to delete
  or split the symbol rather than rename it. Catches drift (identifiers that
  stopped matching what they hold, one concept named twice, one name hiding two,
  UI or wire words in domain names) and structural tells (nouns naming actions,
  boolean blobs, single-use wrappers, optional params fusing two operations).
  Trigger on "review vocab", "simplify the names", "check naming", "are these
  names consistent", "this name bothers me", "what would you call this", or after
  any rename or refactor. Propose concrete changes, preserve behavior.
---

# Naming review

A name is a claim about what a thing is. Code changes silently turn some of those
claims false, and every future reader pays the comprehension tax.

Two lenses. **Drift**: the name was once right, then the code moved and nobody
updated the label. **Simplicity**: the name was never the plainest one that fits.
Run the structural check below first — a name that resists every candidate you
try is usually attached to a symbol that shouldn't exist, and no rename fixes
that.

## First: should this symbol exist?

Before proposing a replacement, ask whether the thing needs a name at all.

- **Single-use wrapper.** A module-level function called once, wrapping a query
  or a fold. Inline it. The local variable it feeds needs only one plain word,
  because the surrounding lines supply the context that a module-level name had
  to restate.
- **Predicate over one query.** `isX(ctx, thing)` that runs a query and folds it
  to a boolean. Return the rows and test them where they're read —
  `rows.length === 1` needs no name at all.
- **Optional trailing parameter.** `f(ctx, input, maybeThing?)` usually fuses two
  operations that ask different questions. The fused body then needs a boolean to
  work out which case it's in, and *that* boolean is the name you can't get
  right. Split by caller and the predicate evaporates.
- **Projection helper over a flat bag.** `xFields(input)`, `toX(input)` — hands
  back a subset of a wide record. These can only be named after the shovelling.
  If the input gained structure they would become field access. Say that instead
  of renaming the shovel.

Deleting or splitting a symbol is a bigger change than renaming it. Propose it
with its cost attached; don't quietly do it under the heading of a rename.

## Stopping rule

**Two rejected candidates for the same symbol means stop generating names.** The
symbol is the problem, not the label. Go back to the structural check. Serial
guessing burns the reviewer's patience and converges on nothing — they end up
supplying the insight you were hired for.

## Scope

Default to the recently-changed surface: `git diff`, `git diff --staged`, or the
files touched this session. Renaming untouched code balloons the blast radius for
little gain.

Read enough surrounding code to know what each name actually holds and how the
local code already talks. You are matching this codebase's idiom, not imposing a
house style.

## Read the reviewer too

When someone says where they're coming from — "I come from DDD", "this is a Go
shop", "we follow Rails conventions" — that is a constraint on acceptable names,
not small talk. Infer the idiom before proposing, and don't make them reject
three names to discover it:

- **DDD / C#** — verb-first methods, domain nouns, no dangling prepositions, no
  `isThingRelatedToOtherThing` blobs.
- **Go** — short receivers, no `Get` prefix, package name carries the context.
- **Rails / Ruby** — `x_for(y)` and `?` predicate suffixes are idiomatic; don't
  "fix" them.

When their stated idiom conflicts with the local codebase, say so and ask which
wins rather than silently picking.

## What to look for

### Drift

- **Stale after a refactor.** The value's meaning changed, the label didn't. Look
  hardest here immediately after a rename or extraction.
- **One concept, two names.** `user` here, `account` there; `fetch` / `get` /
  `load` for one operation. Pick one word. When the stored data uses one word and
  the function uses another, the function usually moves.
- **One name, two concepts.** One `status` covering a lifecycle and a review
  outcome. Split them so each carries one idea.
- **Layer leak.** Presentation or transport words in domain names — a domain enum
  holding CSS variants, or `fields` (a database word) in a domain module.
- **Name/behavior divergence.** `isValid` that writes a cache; a `get` that
  mutates; a `normalize` that also throws on five invariants. Rename to the
  truth, or flag the behavior as the actual bug.

### Simplicity

- **Wordy where short is unambiguous in context.** Scope sets the bar: a
  module-level export must stand alone, a local has three lines holding it up.
- **Awkward identifier for a plain idea.** `notApproved` → `rejected`.
- **Noise qualifiers.** `listingData`, `userObject`, `dataManager`, `theList`.
- **Double negatives.** `isNotDisabled` → `isEnabled`.
- **Inconsistent family.** Related names should share a root.
- **Non-standard abbreviations.** `usr`, `calc`, `mgr` — unless local idiom.

### Structural tells

These present as style problems and are usually structure problems:

- **Noun naming an action.** A bare noun is fine for a pure derivation —
  `addressKey(input)`, `particulars(input)` compute and return, nothing else.
  Anything that performs I/O is an action and wants a verb: `propertyAt(ctx, x)`
  → `findProperty`. Use `find` when the miss is a null and `get` when it throws.
  A trailing preposition is the usual symptom (`addressKeyFor`, `listingsOn`) but
  not the cause — `listingsOn(ctx, propertyId)` reads as perfectly good English
  and is still the wrong shape. Ask whether the function touches the world, not
  whether it scans nicely.
- **`is` + compound noun phrase** — `isSoleListingOnProperty`. One identifier
  carrying a whole sentence. `is` plus a single adjective is fine; `is` plus a
  compressed clause is not.
- **Generic verb over a multi-branch body** — `resolveX`, `handleX`, `processX`.
  Name the branches, not the umbrella.

## How to propose

One line per change, highest-signal first:

```
old → new    — why (false claim removed, ambiguity resolved, noise cut)
```

Group families — a whole `Status*` → `State*` sweep is one decision, not five.
List the names you are **keeping** and why: "already right" is a real finding and
it tells the reviewer you looked rather than skipped.

When a name is contested, offer two or three candidates with the trade-off
visible in one pass. Don't feed them one at a time.

Separate two kinds:

- **Safe local renames** — the identifier lives entirely within the changed code.
  Apply together.
- **Contract changes** — exports, serialized keys, DB columns, API params, route
  names. Flag separately and confirm first. Often the right answer is to rename
  the internal symbol and leave the public one alone: the mutation is named for
  the button, the model function for the state it writes.

## Guardrails

- **Behavior must not change.** Every reference moves together. Afterwards run
  typecheck and grep for the old name; a rename that strands a reference is worse
  than none. When a rename comes with a reorder, walk the branches and state
  which one would have broken.
- **Don't manufacture justification.** If a rename is worth making, one plain
  reason exists. Inventing a second — a domain term-of-art collision, a
  hypothetical misreading — to make it sound principled is a tell that the first
  reason was thin. Verify any claimed collision before asserting it. Being
  confidently wrong about someone's domain costs more than the rename was worth.
- **Only rename when clearly better.** A fixed false claim, a resolved ambiguity,
  or genuine noise removed. Merely-different is churn. Silence means it was fine.
- **Retract in one line.** When a proposal turns out to be wrong, say so plainly
  and move on. No re-litigating, no salvage attempt.
- **Context beats rules.** Everything here is a heuristic. The surrounding code's
  conventions win.

## Example

A Convex module with an address-keyed property lookup. The reviewer objects to
`isSoleListingFor`.

**Wrong:** propose `isSoleListingOnProperty`. Rejected — `is` plus a compressed
sentence. Propose `isShared`. Rejected — bare `is` prefix reads as unconventional
to them. Extract `listingsOn`. Rejected — a noun naming a query. Three rounds,
three rejections, because every candidate assumed the predicate should exist.

**Right:** after the second rejection, stop naming and look at the symbol.

```ts
async function resolveProperty(ctx, input, listing?)  // optional param fuses
                                                      // create with edit
```

Creating takes two branches; editing takes four, because an address change has to
decide whether to rename the existing property or repoint the listing at another
one. The fused function needs a boolean to ask which case it is in — and that
boolean is the name nobody can get right.

```
resolveProperty  → findProperty / registerProperty / reassignProperty
isSoleListingFor → deleted; the query inlines, and `rows.length === 1` tests it
```

Nothing left to name. Every remaining identifier is a verb, because every one of
them touches the database; the pure projections beside them keep their nouns.
