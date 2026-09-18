---
name: evidence-gated-research-reports
description: "Use when building cited research dossiers for handoff."
version: 1.0.0
---

# Evidence-Gated Research Reports

Class: multi-source web research synthesized into a verifiable dossier deliverable,
then handed downstream (design, build, QA) without rewriting the content. The
ledger mechanics live in the `grounded-citations` skill — always load it and
follow it; this skill is the workflow around it.

## Workflow

1. **Set up the project workspace first.** One folder: `README.md` (pipeline
   rules), `RESEARCH_DOSSIER.md` (content authority), `ledger.json`, `sources/`
   (full-text archive), role handoff briefs. The README states downstream rules:
   the dossier is the content authority; citation ids are immutable; disputed
   framings must survive into design. Reset the citation ledger at the project
   path (`--ledger <project>/ledger.json`) so numbering survives the session.

2. **Sweep broadly before extracting.** One `web_search` query per chronology
   segment or sub-topic, run in parallel; save raw result JSON to the project
   folder. Register every URL in the ledger at retrieval time — never from the
   draft afterwards.

3. **Archive full text for every source.** `web_extract` saves full page text to
   disk only when the page exceeds `char_limit`; under-limit pages return inline
   with no file. To force a file for every page, extract with a small
   `char_limit` (e.g. 600), parse the footer path, copy to `sources/` under a
   sanitized name. Batch ≤5 URLs with at most one per domain — same-domain
   pages rate-limit (429) mid-batch; failed URLs succeed on retry after a
   cooldown. Verify the archive inventory (count + sizes) before synthesizing.

4. **Attach evidence quotes mechanically.** Find each quote by regex INSIDE the
   archived file and pass the matched substring to `quote --from` — retyped
   quotes fail the verbatim gate on markup mismatch (bold markers, curly
   quotes, inline links). Run the ledger script from the terminal, never via
   subprocess from an embedded Python kernel: its import chain depends on the
   shell environment and dies with a traceback inside kernel subprocesses.

5. **Synthesize with contested-claim framing.** Three registers, kept separate:
   verified history, attributed reportage ("as many as", named source), and
   tradition/legend (state the story, then state its evidentiary status in the
   same sentence). Never adjudicate scholar disagreements — present both
   readings, each with its own citation. Aggregate figures (e.g. regional
   population loss) must not be presented as subgroup-specific tolls.

6. **Verify, then audit the warnings before acting on them.**

   | `verify` output | Real meaning | Action |
   |---|---|---|
   | ">3 citations" warning | Counts newline fragments as sentences — one multi-sentence paragraph or bullet line trips it | Audit per true sentence; ≤3 ids per sentence is the rule |
   | Low coverage % | List bullets count as prose; headings/tables don't | Read the `info: stats:` line before moving thresholds |
   | Sources-block URL mismatch on a URL containing `(` | Matching truncates at the literal paren | Re-register that URL percent-encoded (`%28…%29`) and re-point the id |

   Render the Sources block with `render --cited-in --replace-in` only; after
   any edit, re-render before re-verifying or the block lags the draft.

7. **Hand off downstream through files, not conversation.** Write one brief per
   role (`HANDOFF_DESIGN.md`, `HANDOFF_BUILD.md`): input authority (the
   dossier), output filename, component requirements, a verification bar the
   role must meet before reporting done, and the rule "do not change claims or
   citations". Subagents see none of this conversation — the brief plus the
   dossier must be fully self-contained, with absolute paths. Dispatch only the
   first dependent role; dispatch the next after the previous one returns and
   its output is verified on disk. Verify the final deliverable yourself
   before reporting completion.

## Pitfalls

- Registering sources after drafting — the ledger exists to prevent
  memory-sourced URLs; register from tool output at retrieval time.
- Quoting from search snippets instead of archived pages — snippet text cannot
  pass the verbatim gate and hides what the source actually says.
- Hand-editing the Sources block or ledger — always `render`; hand-typed URLs
  are unverified claims.
- Letting downstream roles "improve" prose — design and build wrap content;
  any wording accommodation is proposed in the design spec, not applied.
