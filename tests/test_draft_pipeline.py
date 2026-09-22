import importlib.util
import subprocess
from pathlib import Path


ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "skills/protean-github-draft/scripts/draft_pipeline.py"
spec = importlib.util.spec_from_file_location("draft_pipeline", SCRIPT)
dp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dp)


def test_markdown_table_rows_compare_rendered_cells_without_pipe_markers():
    markdown = "| Name | Status |\n| --- | --- |\n| alpha | ready |\n"
    rendered = "<table><tr><th>Name</th><th>Status</th></tr><tr><td>alpha</td><td>ready</td></tr></table>"
    assert dp.fidelity_gate(markdown, rendered) == (True, [])


def test_fenced_text_preserves_markdown_special_markers():
    markdown = "```text\nrunning pytest tests/test_draft_pipeline.py\npath_with_underscores/*.py `literal` ~tilde~ *asterisk*\n```\n"
    rendered = (
        "<pre><code>running pytest tests/test_draft_pipeline.py\n"
        "path_with_underscores/*.py `literal` ~tilde~ *asterisk*\n</code></pre>"
    )
    assert dp.fidelity_gate(markdown, rendered) == (True, [])


def test_missing_prose_checker_is_a_hard_failure(tmp_path, monkeypatch):
    monkeypatch.setattr(dp, "SKILL_DIR", tmp_path)
    source = tmp_path / "draft.md"
    source.write_text("draft\n", encoding="utf-8")
    passed, note = dp.prose_gate(source, "python3")
    assert not passed
    assert "required" in note


def test_failed_render_keeps_existing_canonical_artifact(tmp_path, monkeypatch, capsys):
    source = tmp_path / "draft.md"
    source.write_text("> Automated posting by agentic team with human oversight.\n", encoding="utf-8")
    root = tmp_path / "drafts"
    batch = "fixed-batch"
    canonical = root / batch / "sample.html"
    canonical.parent.mkdir(parents=True)
    canonical.write_text("previous canonical artifact", encoding="utf-8")

    def fake_run(cmd, **kwargs):
        if str(dp.RENDERER) in cmd:
            output = Path(cmd[cmd.index("--out") + 1])
            output.write_text("<html><body>not faithful</body></html>", encoding="utf-8")
            return subprocess.CompletedProcess(cmd, 0, stdout="wrote temp", stderr="")
        return subprocess.CompletedProcess(cmd, 0, stdout="check-prose: clean", stderr="")

    monkeypatch.setattr(dp, "run", fake_run)
    result = dp.main([
        "--src", str(source), "--slug", "sample", "--tab", "issue draft",
        "--title", "Sample", "--repo", "owner/repo", "--drafts-root", str(root),
        "--batch", batch,
    ])
    assert result == 1
    assert canonical.read_text(encoding="utf-8") == "previous canonical artifact"
    assert not list(canonical.parent.glob(".sample.*.html"))
    assert "BLOCKED" in capsys.readouterr().out
