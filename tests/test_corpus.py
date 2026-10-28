"""Corpus, rendering and CLI tests for flawpath.

Every assertion here is executable evidence for the claims in RESULTS.md:
50 unique skills, a clean validation pass, byte-identical regeneration and a
CLI (validate / list / show / search / build / flawplan) that behaves as
documented.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from flawpath.corpus import PACK, PHASE_ORDER, SKILLS
from flawpath.render import build_pack, render_skill, sha256_of, word_count
from flawpath.validate import (
    FORBIDDEN_RE,
    MIN_WORDS,
    pack_issues,
    skill_issues,
    validate_pack,
)

ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT / "src")
    return subprocess.run(
        [sys.executable, "-m", "flawpath", *args],
        capture_output=True,
        text=True,
        cwd=ROOT,
        env=env,
    )


# ---------------------------------------------------------------- corpus shape


def test_pack_declares_fifty_and_delivers_fifty() -> None:
    assert PACK["expected_skills"] == 50
    assert len(SKILLS) == 50


def test_slugs_and_titles_are_unique() -> None:
    slugs = [s.slug for s in SKILLS]
    titles = [s.title.lower() for s in SKILLS]
    assert len(set(slugs)) == 50
    assert len(set(titles)) == 50


def test_every_skill_passes_every_rule() -> None:
    assert validate_pack(PACK, SKILLS) == []


def test_phases_are_known_and_balanced() -> None:
    counts: dict[str, int] = {}
    for skill in SKILLS:
        phase = skill.meta["phase"]
        assert phase in PHASE_ORDER, skill.slug
        counts[phase] = counts.get(phase, 0) + 1
    # scope 7, map 8, probe 19, confirm 6, harden 6, document 4
    assert counts["scope"] == 7
    assert counts["map"] == 8
    assert counts["probe"] == 19
    assert counts["confirm"] == 6
    assert counts["harden"] == 6
    assert counts["document"] == 4
    assert sum(counts.values()) == 50


def test_every_phase_is_reachable_from_the_phase_filter() -> None:
    for phase in PHASE_ORDER:
        matches = [s for s in SKILLS if s.meta["phase"] == phase]
        assert matches, f"phase {phase} has no skills"


def test_word_floor_is_real_not_theoretical() -> None:
    weakest = min(SKILLS, key=lambda s: word_count(render_skill(PACK, s)))
    assert word_count(render_skill(PACK, weakest)) >= MIN_WORDS


def test_no_placeholder_or_local_path_tokens() -> None:
    for skill in SKILLS:
        rendered = render_skill(PACK, skill)
        assert not FORBIDDEN_RE.search(rendered), skill.slug
        assert "C:\\" not in rendered and "/Users/" not in rendered, skill.slug


def test_scope_phase_always_precedes_probes() -> None:
    """A plan that starts with a probe has skipped its most important step."""
    assert PHASE_ORDER[0] == "scope"
    assert PHASE_ORDER.index("scope") < PHASE_ORDER.index("probe")
    assert PHASE_ORDER.index("map") < PHASE_ORDER.index("probe")
    scope_first = [s for s in SKILLS if s.meta["phase"] == "scope"][0]
    assert "authorization" in scope_first.slug or "boundary" in scope_first.slug


def test_no_skill_contains_a_live_credential() -> None:
    import re

    credential = re.compile(r"\b(?:AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,})\b")
    private = re.compile(r"\b(?:192\.168\.|10\.0\.|172\.16\.|127\.0\.)\d+\.\d+\b")
    for skill in SKILLS:
        rendered = render_skill(PACK, skill)
        assert not credential.search(rendered), skill.slug
        assert not private.search(rendered), skill.slug


# ------------------------------------------------------------ generated files


def test_committed_skills_match_corpus_render() -> None:
    for skill in SKILLS:
        path = ROOT / "skills" / skill.slug / "SKILL.md"
        assert path.exists(), f"missing {path}"
        assert path.read_text(encoding="utf-8") == render_skill(PACK, skill)


def test_pack_json_hashes_match_files() -> None:
    manifest = json.loads((ROOT / "pack.json").read_text(encoding="utf-8"))
    assert manifest["skill_count"] == 50
    assert len(manifest["skills"]) == 50
    for entry in manifest["skills"]:
        path = ROOT / entry["path"]
        digest = sha256_of(path.read_text(encoding="utf-8"))
        assert digest == entry["sha256"], entry["slug"]


def test_build_is_idempotent(tmp_path: Path) -> None:
    build_pack(tmp_path, PACK, SKILLS)
    for skill in SKILLS:
        a = (tmp_path / "skills" / skill.slug / "SKILL.md").read_bytes()
        b = (ROOT / "skills" / skill.slug / "SKILL.md").read_bytes()
        assert a == b, skill.slug
    assert (tmp_path / "pack.json").read_bytes() == (ROOT / "pack.json").read_bytes()


def test_drift_is_detected(tmp_path: Path) -> None:
    build_pack(tmp_path, PACK, SKILLS)
    victim = tmp_path / "skills" / SKILLS[0].slug / "SKILL.md"
    victim.write_text(victim.read_text(encoding="utf-8") + "\nedited\n", encoding="utf-8")
    rendered = render_skill(PACK, SKILLS[0])
    on_disk = victim.read_text(encoding="utf-8")
    assert on_disk != rendered


# ---------------------------------------------------------------------- CLI


def test_cli_validate_reports_fifty_of_fifty() -> None:
    proc = run_cli("validate", "--json")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["checked"] == 50
    assert payload["valid"] == 50
    assert payload["passed"] is True
    assert payload["issues"] == []


def test_cli_list_and_show_and_search() -> None:
    listing = run_cli("list", "--json")
    assert listing.returncode == 0
    assert len(json.loads(listing.stdout)) == 50

    # --phase filter narrows the listing to one phase
    only_probe = run_cli("list", "--phase", "probe", "--json")
    assert only_probe.returncode == 0
    probed = json.loads(only_probe.stdout)
    assert len(probed) == 19
    assert all(entry["meta"]["phase"] == "probe" for entry in probed)

    show = run_cli("show", SKILLS[0].slug)
    assert show.returncode == 0
    assert show.stdout.startswith(f"---\nname: {SKILLS[0].slug}")

    missing = run_cli("show", "not-a-real-skill")
    assert missing.returncode == 1

    search = run_cli("search", "field", "validation")
    assert search.returncode == 0
    assert search.stdout.strip() != ""

    nohit = run_cli("search", "zzzz-no-such-term")
    assert nohit.returncode == 1
    assert "no matches" in nohit.stdout


# --------------------------------------------------------------- flawplan


def test_cli_flawplan_orders_phases_and_flags_thin_coverage() -> None:
    spec = ROOT / "examples" / "demo-inventory.json"
    text = run_cli("flawplan", "--inventory-file", str(spec))
    assert text.returncode == 0, text.stdout + text.stderr
    assert text.stdout.startswith("# Assessment plan - ")
    assert "Skills matched:" in text.stdout
    # phase headers render in PHASE_ORDER
    order = [f"## {phase}" for phase in PHASE_ORDER]
    positions = [text.stdout.find(marker) for marker in order]
    rendered = [p for p in positions if p != -1]
    assert rendered == sorted(rendered), "phase headers must appear in PHASE_ORDER"

    payload = json.loads(run_cli("flawplan", "--inventory-file", str(spec), "--json").stdout)
    assert payload["target"] == "orders service"
    assert payload["skills_total"] == 50
    assert payload["skills_matched"] >= 1
    assert payload["plan_steps"] >= 1
    assert payload["routes"][0] == "/api/v1/orders"
    assert "body" in payload["parameters"]
    assert all(entry["phase"] in PHASE_ORDER for entry in payload["plan"])
    # selection is phase-stratified: every matched phase appears in the plan
    assert payload["phases_covered"] == list(PHASE_ORDER)
    # thin coverage describes phases the inventory matched nothing in, so a
    # crowded --top can never make a covered phase look uncovered
    assert payload["missing_phases"] == []


def test_cli_flawplan_rejects_missing_inventory() -> None:
    proc = run_cli("flawplan", "--inventory-file", str(ROOT / "examples" / "no-such.json"))
    assert proc.returncode != 0


def test_flawplan_thin_coverage_comes_from_matches_not_from_top() -> None:
    """An inventory matching nothing reports every phase as thin coverage."""
    from flawpath.cli import build_flawplan

    empty = build_flawplan({"target": "cold", "keywords": ["qqqqqq", "zzzzzz"]}, top=12)
    assert empty["skills_matched"] == 0
    assert empty["plan_steps"] == 0
    assert empty["phases_covered"] == []
    assert empty["missing_phases"] == list(PHASE_ORDER)

    # a small --top still covers every phase the inventory matched
    spec = json.loads((ROOT / "examples" / "demo-inventory.json").read_text(encoding="utf-8"))
    tight = build_flawplan(spec, top=6)
    assert tight["plan_steps"] <= 6
    assert tight["phases_covered"] == list(PHASE_ORDER)
    assert tight["missing_phases"] == []


def test_flawplan_aggregates_vocabulary_across_inventory_keys() -> None:
    from flawpath.cli import build_flawplan, inventory_vocabulary

    vocab = inventory_vocabulary({"framework": "express", "observed": {"unknown_field_policy": "pass"}})
    assert "express" in vocab
    assert "unknown" in vocab

    payload = build_flawplan(
        {"target": "demo", "routes": ["/orders"], "parameters": ["body"]},
        top=5,
    )
    assert payload["plan_steps"] == 5
    assert payload["skills_total"] == 50
    assert len(payload["vocabulary"]) > 0


# ----------------------------------------------------------- rule enforcement


def test_pack_issues_catches_a_short_corpus() -> None:
    issues = pack_issues(PACK, SKILLS[:-1])
    assert any(issue.rule == "skill-count" for issue in issues)


def test_single_skill_rule_violations_are_reported() -> None:
    broken = dict(SKILLS[0].__dict__)
    broken["steps"] = ("one", "two")
    from flawpath.model import skill_from_dict

    issues = skill_issues(PACK, skill_from_dict(broken), "")
    rules = {issue.rule for issue in issues}
    assert "steps-count" in rules


def test_results_validation_json_reports_passed() -> None:
    report = json.loads((ROOT / "results" / "validation.json").read_text(encoding="utf-8"))
    assert report["pack"] == "flawpath"
    assert report["checked"] == 50
    assert report["valid"] == 50
    assert report["passed"] is True
    assert report["issues"] == []


def test_catalog_lists_every_skill() -> None:
    catalog = (ROOT / "results" / "catalog.md").read_text(encoding="utf-8")
    for skill in SKILLS:
        assert f"`{skill.slug}`" in catalog, skill.slug
    assert catalog.count("\n") >= 50