#!/usr/bin/env python3
"""Write the recorded test results into README.md and docs/evaluations.md.

Reads docs/test-results/install.json and docs/test-results/integration.json,
which the two test suites write with --json. Nothing here runs a test; it only
reports what was recorded, so a test that did not run stays `not run`.

    python3 scripts/update_test_status.py --environment "macOS 26.6.2 arm64, Node v22.23.1, FFmpeg 8.1"
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / "docs" / "test-results"


def load(name: str) -> dict:
    return json.loads((RESULTS / name).read_text(encoding="utf-8"))


def counts(d: dict) -> str:
    c = d["counts"]
    return f"{c['pass']} pass, {c['fail']} fail, {c['not run']} not run"


def table(d: dict) -> str:
    rows = ["| Test | Result | Note |", "| --- | --- | --- |"]
    for t in d["tests"]:
        note = t["detail"].replace("|", "/").replace("\n", " ")[:160] if t["status"] != "pass" else ""
        rows.append(f"| {t['name'].replace('|', '/')} | {t['status']} | {note} |")
    return "\n".join(rows)


def main() -> int:
    env = sys.argv[sys.argv.index("--environment") + 1] if "--environment" in sys.argv else "not recorded"
    install, integ = load("install.json"), load("integration.json")
    meta = json.loads((RESULTS / "run.json").read_text(encoding="utf-8")) if (RESULTS / "run.json").is_file() else {}
    meta.setdefault("environment", env)
    if "--environment" in sys.argv:
        meta["environment"] = env

    block = f"""Recorded on {meta.get('date', 'unknown date')}, {meta['environment']}, against Hermes {meta.get('hermes', 'unknown')} and `hyperframes@{meta.get('hyperframes', 'unknown')}`.

| Suite | Result |
| --- | --- |
| Repository validation (`scripts/validate.py --history`) | {meta.get('validate', 'not run')} |
| Vendor provenance and derivative rebuild (`scripts/hyperframes_vendor.py verify`) | {meta.get('vendor', 'not run')} |
| Upstream contract (`scripts/check_upstream_contract.py`) | {meta.get('contract', 'not run')} |
| Eval fixtures (`scripts/run_evals.py`) | {meta.get('evals', 'not run')} |
| Installation tests, in a temporary profile | {counts(install)} |
| HyperFrames integration tests, from an installed temporary profile, with real renders | {counts(integ)} |
| Install from the published GitHub URL | {meta.get('published_install', 'not run')} |
| Model-backed behavior evaluation | not run. No model credentials in the test environment. |
| End-to-end Kanban test with live Executive, Marketing, and Social Media profiles | not run. Needs model access and a dispatcher. |
| Linux and Windows | not run. Tested on macOS arm64 only. CI runs the no-render suites on Ubuntu. |
| Speech model download and local transcription | not run. The refusal path without a model is tested. |
| Browser download through `setup --download-browser` | not run. Renders used a headless Chrome already on the machine, recorded with `--use-browser`. |"""

    readme = REPO / "README.md"
    text = readme.read_text(encoding="utf-8")
    text = re.sub(r"<!-- test-status:start -->.*?<!-- test-status:end -->",
                  lambda m: f"<!-- test-status:start -->\n{block}\n<!-- test-status:end -->", text, flags=re.S)
    readme.write_text(text, encoding="utf-8")

    evaluations = REPO / "docs" / "evaluations.md"
    head = (REPO / "docs" / "evaluations.head.md").read_text(encoding="utf-8")
    evaluations.write_text(
        head.rstrip("\n") + "\n\n## Summary\n\n" + block
        + "\n\n## Installation tests\n\n" + table(install)
        + "\n\n## HyperFrames integration tests\n\n" + table(integ) + "\n", encoding="utf-8")
    print("updated README.md and docs/evaluations.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
