---
name: citation-ledger-field-notes
description: "Use when running a grounded-citations evidence ledger."
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [research, citations, pitfalls]
---

# Citation Ledger Field Notes (companion to grounded-citations)

Field lessons from running the full evidence gate end-to-end (China-Islam report, Sep 2026). This file adds what bit in practice to the bundled `grounded-citations` skill.

## Environment
- Run `sources.py` via `terminal`, never via `execute_code` subprocesses: the import chain crashes there (`hermes_constants` union-type error) and `add` silently registers nothing (rc=0, zero registrations).
- Long batches: write a script file, run it from `terminal`.

## Duplicate-id trap
- Re-registering the same page with different URL encoding (literal `(` vs `%28…%29`) mints a NEW id for the same resource. If the draft ends up citing the new id, the old one becomes orphaned.
- Plain `verify` PASSES even when a cited id has no evidence quotes (it checks ids and Sources-block agreement, not evidence). The final gate must be `verify --evidence`.
- When an id migration happens: re-attach quotes to the new id from the same archived `--from` file, re-render the Sources block, then re-verify.

## Stats line is not truth
- Bullet-list lines are not counted as prose sentences, so a fully-cited draft can report 52% coverage.
- The >3-citations warning counts line-level ids — a source-inventory bullet listing many sources triggers it. Sentence-level audit with your own script before "fixing" anything.
- `registered but not cited` warnings = real (uncited sources); fix those.

## Mechanical quoting
- Locate every quote by regex INSIDE the archived page file and pass the exact matched substring with `quote --text ... --from <file>`. Retyped quotes fail the verbatim gate on typography (curly quotes, bold/link markup, hyphenation).
- Markdown artifacts (bold markers, inline-link syntax) live in the extracted text — write regex tolerant of them, and let the regex's matched text (never a paraphrase) become the quote.
- Quotes must come from archived full-text captures, not search snippets or chat memory.

## Archive hygiene
- web_extract returns content inline without a disk footer when under char_limit — for archival passes use a SMALL char_limit so full text lands on disk, then copy into the project `sources/` dir and keep an id→file map in the batch script.
- Count the archive and reconcile against the ledger at the end (every ledger id should have a captured file unless extraction failed for a stated reason).

## Downstream handoff
- Hand builders the rendered dossier (Sources block generated via `render --replace-in`), never raw ledger ids. Tell them to copy the Sources block verbatim and warn about URL-encoding differences (%28 vs `(`) so a hand-edit doesn't trip verify.