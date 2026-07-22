---
description: Write release notes for a version range and update the GitHub draft release
argument-hint: <new-version> [previous-version] [--style customers|developers|internal]
---

Write release notes for $ARGUMENTS and update the draft release on GitHub.

## Style
Pick with --style (default: customers). Definitions:

```
customers
  audience: external users
  voice:    plain, benefit-first, second person ("you can now...")
  length:   one line per item, no trailing period
  exclude:  hashes, internal refactors, dep bumps (unless behavior changes)
  include:  breaking changes, called out with a migration note

developers
  audience: people building on the API/SDK
  voice:    precise, terse, names methods/flags/types directly
  length:   one line per item
  exclude:  hashes, pure internal refactors
  include:  signature changes, new/changed flags, deprecations with migration notes

internal
  audience: the team
  voice:    shorthand fine, raw git subjects ok
  length:   one line per item
  exclude:  nothing by default
  include:  refactors, infra, build/CI, anything affecting how we ship
```

Everything below obeys the chosen preset. Add a preset by editing this block, not the prose.

## Flow

```
+--------+    +-------+    +-------+    +-------+
| gather | -> | group | -> | dedup | -> | write |
+--------+    +-------+    +-------+    +-------+
                                          |
                                          v
                        fail          +--------+
                    +------------------ | verify |
                    |                   +--------+
                    |                       | pass
                    v                       v
                (fix &               +---------+
                re-check)            | publish |
                                     +---------+
```

## Gather
0. Read --style from $ARGUMENTS (default customers). Use that preset's rules in Write and Verify.
1. `gh repo view --json nameWithOwner -q .nameWithOwner` for the repo.
2. `gh release list --limit 5` to see existing releases (the draft for <new> may or may not exist yet).
3. If <previous-version> wasn't passed, use the latest published (non-draft) release as <previous>.
4. `git log <previous>..<new> --oneline` for the commit range.
   If no prior release exists, treat every commit as a new feature.

## Group
Group commits by feature. A feature is "new" if no part of it existed in <previous>.

## Dedup rule (the important part)
For each fix / improvement / change, run this:

```
does the thing it touches exist in <previous>?
          |
    +-----+-----+
    |           |
   YES          NO
    |           |
list as     fold into the new feature's
own line    description (don't list it)
```

readers shouldn't see "fixed X" for an X they never had

## Write
Sections in order, omit any that are empty:

```
New features   <- features new in this range
Changes        <- behavior changed on existing things
Improvements   <- existing things made better
Bug fixes      <- existing things repaired
```

Tone, audience, phrasing, and what to exclude all come from the chosen preset in ## Style.

## Verify (before publish)
Spawn a subagent with ONLY these inputs (not the writing reasoning):
  - output of `git log <previous>..<new> --oneline`
  - the draft notes
  - the chosen preset from ## Style

Task it to report discrepancies, not to rewrite:

[ ] every commit is listed or deliberately dropped
[ ] no listed item touches something absent in <previous> (should be folded)
[ ] every "New features" entry has no part in <previous>
[ ] each line matches the preset (audience, voice, length)
[ ] preset excludes absent, includes present

It returns a list of problems (or "clean"). The main agent fixes and re-verifies.
Loop until clean, then publish.

If any fail, fix and re-check before publishing.

## Publish
If a release for <new> already exists (draft or otherwise):
  `gh release edit <new> --notes "..."`
else:
  `gh release create <new> --draft --title <new> --notes "..."`

(the <new> tag must already exist; otherwise gh tags HEAD of the default branch. pass `--target <branch-or-sha>` to control where it points.)
