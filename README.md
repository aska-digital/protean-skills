# hermes-skills

Agent skills we use daily, packaged as a public Hermes tap.

## Install

```bash
hermes skills tap add ahrazzle/hermes-skills
hermes skills install ahrazzle/hermes-skills/merge-reconciler
```

Any skill in this repo installs the same way — replace the last segment:

```bash
hermes skills install ahrazzle/hermes-skills/subagent-oversight
hermes skills install ahrazzle/hermes-skills/citation-ledger-field-notes
hermes skills install ahrazzle/hermes-skills/evidence-gated-research-reports
hermes skills install ahrazzle/hermes-skills/macos-harness
```

Built by [ASKA Digital](https://askadigital.com) — we build agent teams.

## Skills

| Skill | What it does |
|---|---|
| [merge-reconciler](skills/merge-reconciler/SKILL.md) | Neutral third-party resolution of agent merge conflicts. |
| [subagent-oversight](skills/subagent-oversight/SKILL.md) | Orchestrating delegate_task subagents — dispatch, monitor, verify, unblock. |
| [citation-ledger-field-notes](skills/citation-ledger-field-notes/SKILL.md) | Field lessons for running a grounded-citations evidence ledger. |
| [evidence-gated-research-reports](skills/evidence-gated-research-reports/SKILL.md) | Building cited research dossiers for handoff. |
| [macos-harness](skills/macos-harness/SKILL.md) | Driving the user's real logged-in Chrome (CDP) and composing multi-step logic in one persistent Python process. |

## Licence

MIT — see [LICENSE](LICENSE). Copyright holder: **ASKA Digital**.

## Layout

Standard Hermes tap layout: `skills/<name>/SKILL.md`, installable via `hermes skills tap add` and indexed by skills.sh. No registry sign-up.

