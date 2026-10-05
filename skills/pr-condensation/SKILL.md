---
name: pr-condensation
description: "Use to condense PRs into one. Trigger: condense the PRs."
version: 1.0.0
author: Proteus (Protean Team)
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [github, pr, orchestration, protean, condensation]
    related_skills: [protean-system, protean-control-plane, github-draft-review-html, clean-writing]
---

# PR Condensation (Coagulation / Concentration)

## When to Use
Load this skill whenever the user asks to combine multiple hermes-agent PRs and/or issues into a single lean PR — phrases like "condense the PRs", "combine PRs into one", "coagulate these", "concentrate the PRs", or "Nous Research asked to merge these into one". It encodes the standing workflow Nous Research (maintainers of `NousResearch/hermes-agent`) requested.

Nous Research (creators and maintainers of hermes-agent, repo `NousResearch/hermes-agent`) ask contributors to combine several related PRs and issues into ONE lean, reviewable PR. This is the standing workflow. Reuse it for every condensation batch.

## Hard constraints (learned the hard way)
- **3-PR-per-account cap.** You usually CANNOT open a new PR. Pick ONE existing PR as the condensation target and force-push the combined branch to its head. Source PRs get integration-explainer comments, not new PRs.
- **Preserve authorship.** Cherry-pick source commits so git carries each author's name/email. Do NOT squash-merge authorship away. If you must consolidate, commit as the account owner but keep cherry-picked commits intact where possible.
- **NEVER put secrets in transcript/PR.** API keys, tokens, credentials -> `[REDACTED]`.
- **MAX 2 concurrent `delegate_task` children.** The runtime rejects 4. Batch in waves of 2.
- **Proteus orchestrates, never implements.** Do not read project source, patch files, or run git/build/test/branch-surgery yourself. Dispatch to role agents. The only direct surfaces from Proteus: `delegate_task`, read-only external verification (`gh`, `git ls-remote`), and delegating verification to Shaka. (Encoded in `protean-control-plane` §K and `protean-system`.)

## Role routing (strict)
- **Leo** — architecture: designs fix specs, re-architects on defect.
- **Mozi** — implementation: writes/patches code, extends tooling, commits (set `git config user.name/email` to the account owner before committing).
- **Shaka** — verification: reads REAL code, runs pytest, independent pass, SHIP/BLOCKER verdict. Does NOT implement.
- **Hazen** — copy: PR body, issue/PR comments, all user-facing writing. MUST load `clean-writing` and pass `check-prose.py` (incl. `--dupes`) before any `gh` post.
- Reviewer finds a blocker (Shaka, or external like gpt-forge / gpt-6.1-sol): do NOT self-fix. Route Leo (spec) -> Mozi (implement) -> Shaka (verify). Repeat until SHIP.

## Pipeline
1. **Locate skills.** `protean-github-draft` may not exist; the real one is `github-draft-review-html`. Load `clean-writing` + `check-prose.py` now — every writing step needs them.
2. **Gather.** `gh auth status`; `gh repo view` for remotes. For each source PR/issue: `gh api repos/NousResearch/hermes-agent/pulls/<N>` and `.../pulls/<N>/commits` (or `gh pr view` / `gh issue view`). Parse title, author, head branch, commit SHAs. Record authors (preserved via cherry-pick).
3. **Fetch + diff.** `git fetch upstream main` and the fork branches. `git diff --stat upstream/main...<branch>` per source. Save diffs.
4. **Base branch.** `git checkout -B <combined> upstream/main`. The condensation-target PR's head ref is where you force-push at the end.
5. **Cherry-pick in dependency order.** Clean picks first (least conflict), then the target PR's own commit(s). On conflict: read both sides, keep the stronger design (unified roots over duplicated; leaner function over verbose), keep both test blocks if both add value. `git add` + `git cherry-pick --continue`.
6. **Apply the issue fix** (if an issue is part of the combo) as its own commit on the combined branch.
7. **Delegate hardening wave(s).** Leo+Mozi (architecture + implementation) first; Shaka+Hazen (verify + copy) next. Never 4 at once.
8. **Reviewer-fix loop.** After Shaka and/or an external reviewer reports findings: triage P1/P2. Route each blocker Leo -> Mozi -> Shaka. Re-run until Shaka verdict = SHIP. (This session: gpt-forge found 2 P2 Hub regressions — active-staging reclaim by age, leftover quarantine copy. Leo re-architected the liveness lock as a SIBLING file after Mozi's first attempt leaked `.active.lock` into installs; Mozi implemented; Shaka verified SHIP.)
9. **PR body (Hazen).** Maintainer register: terse opener; `## Root cause`; `## Changes` with `path::symbol`; `## Validation` table; `## Follow-ups`; `Closes #`. MUST pass `check-prose.py` exit 0. Publish via `gh pr edit <target> --body-file <file>` (write file, never inline-escaped string; fetch back + compare).
10. **Force-push the verified head** to the target PR's head ref: `git push --force origin <combined>:<target-head-branch>`. Verify with `git ls-remote origin <target-head-branch>`.
11. **Integration comments (Hazen).** On EACH salvaged PR and fixed issue (NOT your own target PR), post a terse comment: what was integrated, the `file::symbol` where it now lives, link back to the target PR. **Reference the target PR EXACTLY ONCE** — use the URL as the single reference, never both `#N` and the URL. Load clean-writing; pass `check-prose.py --dupes` (exit 0); post via `gh pr comment` / `gh issue comment`; then FETCH the comment back and grep to PROVE the reference count. Edit in place if wrong.

## Verification discipline (non-negotiable)
- Shaka verifies against REAL code + live test runs, not summaries.
- After any `gh` post, re-fetch the live text and check it (dupes, content). Self-certification ("exit 0, done") is how a twice-linked comment slipped through once — require fetched proof.
- The `--dupes` gate normalizes `#NNN` and its github PR/issue URL to one key; a text with both is a duplicate (exit 1).

## Pitfalls (from the first run)
- A `delegate_task` steer queued AFTER the child finished -> the clean-writing mandate was missed and comments shipped un-gated. Fix: put the clean-writing mandate IN the task brief from the start; if a child reports it posted without the gate, make it re-fetch + re-pass + edit in place.
- Mozi's first lock attempt put the lock INSIDE `staging_dir`; the swap `move` carried it into `install_dir`, leaking a stray file. Re-architect to a sibling lock. Lesson: when a child's commit note reveals a design flaw, route re-architecture back to Leo; don't patch it yourself.
- Repo is `NousResearch/hermes-agent`, NOT `teknium1/hermes-agent` (latter 404s). Confirm via `gh` before posting.
- Don't re-plan an already-executed action; the tool result is the receipt.

## Deliverable checklist
- [ ] Combined branch on `upstream/main`, all source commits cherry-picked (authorship intact)
- [ ] Issue fix applied as its own commit
- [ ] Shaka verdict SHIP on the code
- [ ] PR body vN published, `check-prose.py` exit 0
- [ ] Head force-pushed + `git ls-remote` confirmed
- [ ] Integration comments on every salvaged PR/issue, single PR reference, fetched-proof clean
