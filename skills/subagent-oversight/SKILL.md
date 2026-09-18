---
name: subagent-oversight
description: "Use when orchestrating delegate_task subagents."
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [orchestration, delegation, qa]
---

# Subagent Oversight (dispatch → monitor → verify → unblock)

Standing rule this encodes: the user expects active supervision of delegated work — periodic checks, on-disk verification, intervention on stalls. Never fire-and-forget.

## Dispatch
- Record `subagent_id` and the live transcript path from the dispatch result.
- Give children self-contained context: absolute paths, the source-of-truth file, binding decisions (rulings) as fixed constraints, and the verification bar you will enforce.

## Monitor
- Status: `delegate_task(action='list')` for run-time; `tail` the live transcript for what the child is actually doing.
- Judge by tool-activity pattern: recent tool lines = working (even if slow — a 17-min single-write design task is normal). No tool activity >10 min = stalled → steer. Same file touched repeatedly with no progress = looping → steer or stop.
- Silence is not failure: a child sat 11 min with zero tool calls, then delivered on a steer. Check the transcript before intervening.

## Intervene
- `action='steer'` lands at the child's next tool-result boundary (queued; a running call is never cut). A child that finishes before delivery reports `missed_steer`.
- Steer text: directive + specific + include a do-not-break list of what is already correct.
- `action='stop'` for dead ends (partial result still returns).
- In-session watchdog that works: background `terminal` loop (`background=true, notify=true`) that exits when the artifact appears/changes or on timeout. Cron `deliver='origin'` does NOT reach CLI sessions and needs the gateway running — never rely on it here.

## Verify (before downstream dispatch or any completion report)
- Child self-reports are claims. `ls -la` the path (size, mtime), then structural checks: section/heading counts, key content probes, and cross-checks against the source-of-truth file (e.g. every citation id resolves in both directions).
- Verify your own writes too: after ANY write, confirm size/line-count — `hermes_tools.write_file` REPLACES the whole file (it once clobbered a child's 32 KB spec; recovery cost a full re-dispatch).
- Never append to another agent's deliverable from the parent. Put parent rulings in a SEPARATE file (e.g. RULINGS.md) referenced by the downstream child; if one file is required, read-modify-write in a single call and verify the byte delta.

## Handoff discipline
- Launch the downstream child only after the upstream artifact verifies on disk. If a clobber/mistake is discovered mid-build, steer the child to HOLD immediately (it keeps working otherwise), fix upstream, then steer RESUME with re-verified inputs.

## Content-integrity audits of built artifacts
- Probe structure, not just presence: after an HTML/markdown build, extract actual heading elements and TOC labels — a builder's section splitter can drop title lines and wrap paragraphs in headings while all other checks (citations, assets, facts) pass green.
- When steering fixes, enumerate the correct list AND the must-not-regress list (what already passes), and raise the child's own verification bar to include the failed check.