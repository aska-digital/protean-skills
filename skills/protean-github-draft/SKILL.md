---
name: protean-github-draft
description: "Use when a GitHub issue, PR, review, or comment needs human review before posting."
version: 1.0.0
author: ASKA Digital
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [GitHub, Draft, Review, HTML, Markdown, SOP]
---

# GitHub Draft Review HTML

Render every GitHub post draft as a self-contained GitHub-dark HTML file before posting it.
The HTML is the review artifact. The Markdown source remains the posting source.

## Use this skill when

- A GitHub issue, pull request, review, reply, or release note needs human review.
- The text will be posted by `gh` or the GitHub API.
- Formatting, code fences, tables, links, or quoted evidence must be checked before posting.

## Required procedure

1. Pull the live repository, issue, or PR state before drafting.
2. Write the exact postable text to a Markdown source file.
3. Run `scripts/draft_pipeline.py` once for that source.
4. Open the generated HTML file and review the rendered result.
5. If the text changes, rerun the pipeline with the previous draft as its baseline.
6. Post only after explicit human approval.
7. Read the live GitHub body or comment back after posting. Compare it with the approved Markdown source. Only a final newline difference is acceptable.

## Build command

Run from the skill directory or pass absolute paths:

```bash
python3 scripts/draft_pipeline.py \
  --src <draft.md> \
  --slug <slug> \
  --tab "pull request draft" \
  --title "<title>" \
  --repo "owner/repository" \
  --drafts-root <drafts-root> \
  --batch "YYYY-MM-DD - HHhMMm" \
  --owners <posting-account>
```

Use `--tab "issue draft"` for issue text. Use `--verify-against <file>` for every quoted code or source block. Use `--evidence <file>` for quoted command output. Use `--diff-base <previous.md>` when revising a draft.

## Runtime dependencies

The renderer requires the Python packages `markdown` and `pygments`. The standard library is otherwise sufficient. Install them in the interpreter used for the pipeline:

```bash
python3 -m pip install markdown pygments
```

If either package is unavailable, rendering stops with a clear dependency error and the pipeline keeps any existing HTML artifact unchanged. Do not use a hand-edited fallback HTML file.

## Gates

The pipeline must pass all gates:

- prose and identifier checks
- verbatim evidence checks
- final oversight line
- GitHub-dark rendering
- source-to-HTML text fidelity
- required palette and dark color scheme
- self-contained HTML with no external assets
- visible change banner on revisions

A non-zero result blocks posting. Do not bypass a failed gate by hand-editing the HTML.

## Public-safety rules

- common private paths, local endpoints, secret assignments, and private-key markers are rejected by the automated scan
- manual review remains required for internal names, hostnames, connection strings, and other sensitive text that cannot be detected reliably by a generic pattern
- Keep the poster account in the HTML chrome, not in the post body unless GitHub requires it.
- Do not claim CI, review, merge, release, or install results without live evidence.
- Add this exact final line to every post:

> Automated posting by agentic team with human oversight.

## Output layout

Create one dated batch directory under the chosen drafts root:

```text
<drafts-root>/YYYY-MM-DD - HHhMMm/<slug>.html
```

Keep the Markdown source beside the working evidence, not as the review artifact. Do not deliver `.prev.html` files for review.

## Posting read-back

For a PR body:

```bash
gh pr view <number> --repo <owner/repository> --json body --jq .body
```

For a comment:

```bash
gh api repos/<owner>/<repository>/issues/comments/<comment-id> --jq .body
```

Compare the returned text with the approved source. Record the live URL, object ID, target head SHA, and any difference.

## What the HTML contains

The renderer creates one local file with:

- GitHub-dark repository and tab chrome
- `DRAFT - NOT POSTED` badge
- rendered Markdown headings, lists, tables, links, quotes, and code fences
- inline CSS and embedded syntax highlighting
- revision change banner when a baseline exists

The page must work offline. It must not fetch a stylesheet, script, font, or image.
