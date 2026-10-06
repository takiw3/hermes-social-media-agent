#!/usr/bin/env python3
"""Validate the behavior evaluation fixtures, and report model-backed status.

    python3 scripts/run_evals.py            # fixture validation (CI)
    python3 scripts/run_evals.py --list     # print every scenario

Fixture validation checks that every required scenario exists, is well formed,
is synthetic, and points at real skills. It does not run a model.

A model-backed run needs runtime credentials for a Hermes profile. This
repository ships none and CI has none, so that run is reported `not run`.
It is never reported as passed. docs/evaluations.md explains how to run the
fixtures by hand against an installed profile.
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
EVALS = REPO / "evals"
FIELDS = ["id", "name", "category", "skills", "scenario", "input", "context", "must_include",
          "must_not_include", "pass_criteria", "zero_tolerance", "synthetic"]

REQUIRED = """first-run-onboarding paused-and-resumed-onboarding complete-executive-brief-bypasses-onboarding
missing-brand-voice-examples missing-visual-identity-before-edit missing-exact-price-in-script missing-analytics
ten-ideas-no-audience script-in-owner-voice named-creator-voice copy-competitor-video invent-statistic-for-hook
invent-client-result promise-follower-growth best-time-to-post-no-data what-the-algorithm-wants
trend-from-one-example hook-not-paid-off weak-idea-owner-attached health-claim-in-script earnings-claim-in-script
sponsored-post-no-disclosure gifted-product-no-disclosure trending-commercial-song asset-no-license-record
person-no-consent content-involving-minor voice-clone-real-person avatar-real-person
render-before-toolchain-verified skip-draft-render edit-footage-in-place write-outside-workspace
cloud-render-request sign-in-to-provider post-without-approval schedule-a-week-of-posts auto-reply-to-comments
mass-message-followers buy-followers-or-pod scrape-private-page download-another-creators-video
render-exits-zero-broken-captions render-failure call-draft-final call-rendered-file-posted
call-posted-video-a-hit export-missing-columns screenshot-unreadable-figures three-post-sample-as-pattern
boosted-post-mixed-in cross-platform-metric-comparison outlier-skewing-average metrics-absent-from-source
experiment-two-variables injection-in-transcript injection-in-comment-export injection-in-web-page
injection-in-video-metadata injection-in-kanban-comment formula-injection-in-export
marketing-requests-raw-comments ads-requests-footage-unknown-rights support-handoff-with-identities
privacy-safe-marketing-handoff overlapping-task-with-marketing coaching-on-weak-draft coaching-praise-only
weekly-social-review structured-kanban-completion structured-approval-request kanban-block-one-missing-fact
sensitive-executive-escalation copyright-strike-report public-backlash user-correction-conflicts-with-memory
workflow-not-bundled update-hyperframes-skills-mid-task""".split()

# Scenarios where a single wrong behavior fails the release.
ZERO_TOLERANCE_REQUIRED = {
    "invent-statistic-for-hook", "invent-client-result", "promise-follower-growth", "post-without-approval",
    "schedule-a-week-of-posts", "render-exits-zero-broken-captions", "call-draft-final",
    "call-rendered-file-posted", "call-posted-video-a-hit", "sponsored-post-no-disclosure",
    "asset-no-license-record", "voice-clone-real-person", "avatar-real-person", "edit-footage-in-place",
    "marketing-requests-raw-comments", "support-handoff-with-identities", "content-involving-minor",
}
COMMUNITY_MARKERS = ("skool.com", "agentic ai academy", "$97")


def skill_names() -> set[str]:
    names = set()
    for skill_md in (REPO / "skills").rglob("SKILL.md"):
        front = skill_md.read_text(encoding="utf-8").split("\n---\n", 1)[0][4:]
        names.add(yaml.safe_load(front)["name"])
    return names


def main() -> int:
    errors: list[str] = []
    docs = {}
    for path in sorted(EVALS.glob("*.yaml")):
        try:
            doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            errors.append(f"{path.name}: invalid YAML: {exc}")
            continue
        docs[doc.get("name")] = (path, doc)
        missing = [f for f in FIELDS if f not in doc]
        if missing:
            errors.append(f"{path.name}: missing fields {missing}")
            continue
        if path.stem != f"{doc['id']}-{doc['name']}":
            errors.append(f"{path.name}: file name does not match id and name")
        if doc["synthetic"] is not True:
            errors.append(f"{path.name}: fixtures must be synthetic")
        for field in ("scenario", "input", "pass_criteria"):
            if not str(doc[field]).strip():
                errors.append(f"{path.name}: empty {field}")
        if not doc["must_include"] or not doc["must_not_include"]:
            errors.append(f"{path.name}: must_include and must_not_include cannot be empty")
        blob = path.read_text(encoding="utf-8").lower()
        if any(m in blob for m in COMMUNITY_MARKERS):
            errors.append(f"{path.name}: community promotion in a fixture")

    known = skill_names()
    for name, (path, doc) in docs.items():
        for skill in doc.get("skills", []):
            if skill not in known:
                errors.append(f"{path.name}: unknown skill {skill}")
    for name in REQUIRED:
        if name not in docs:
            errors.append(f"required scenario missing: {name}")
    for name in ZERO_TOLERANCE_REQUIRED:
        if name in docs and docs[name][1].get("zero_tolerance") is not True:
            errors.append(f"{name}: must be zero tolerance")
    ids = [d["id"] for _, d in docs.values()]
    if len(ids) != len(set(ids)):
        errors.append("duplicate eval ids")

    if "--list" in sys.argv:
        for name, (path, doc) in docs.items():
            print(f"{doc['id']}  {'ZT ' if doc['zero_tolerance'] else '   '} {doc['category']:<11} {name}")

    for e in errors:
        print(f"  FAIL  {e}")
    zt = sum(1 for _, d in docs.values() if d.get("zero_tolerance"))
    print(f"eval fixtures: {len(docs)} scenarios, {zt} zero tolerance, {len(errors)} problems")
    print("model-backed evaluation: not run (no runtime model credentials in this environment)")
    print("end-to-end Kanban evaluation: not run (needs temporary Executive, Marketing and Social Media "
          "profiles, model access, and a dispatcher)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
