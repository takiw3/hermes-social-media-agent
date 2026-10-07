#!/usr/bin/env python3
"""Repository validation. Run before every commit and in CI.

    python3 scripts/validate.py              # working tree
    python3 scripts/validate.py --history    # also scan Git history for secrets
    python3 scripts/validate.py --history --only-history

Standard library plus PyYAML. No network access. Exit 1 on any failure.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
SELF = {"scripts/validate.py", "scripts/run_evals.py"}
GITHUB = "https://github.com/takiw3/hermes-social-media-agent"

CORE_SKILLS = """social-intake-and-routing creator-and-brand-onboarding audience-and-niche-research
content-pillar-strategy content-ideation hook-writing short-form-script-writing long-form-script-writing
caption-and-post-copy filming-brief-and-shot-list video-edit-planning video-render-review platform-packaging
content-repurposing media-rights-and-disclosure-check performance-data-intake video-performance-analysis
account-analytics-and-strategy content-experiment-design competitor-and-format-research
audience-comment-analysis content-calendar-planning creator-coaching cross-team-social-handoffs
weekly-social-review""".split()
VENDORED_SKILLS = """hyperframes hyperframes-core hyperframes-animation hyperframes-keyframes hyperframes-creative
hyperframes-cli hyperframes-audio hyperframes-registry hyperframes-studio media-use talking-head-recut
embedded-captions motion-graphics faceless-explainer general-video""".split()
TEMPLATES = """creator-profile.md brand-and-visual-identity.md content-pillars.yaml idea-card.yaml
script-short-form.md script-long-form.md filming-brief.md edit-plan.yaml render-receipt.yaml
packaging-sheet.yaml asset-rights-register.yaml metric-dictionary.yaml performance-snapshot.yaml
experiment-log.yaml content-calendar.yaml coaching-scorecard.md approval-request.yaml social-task.yaml
social-result.yaml report-template.md""".split()
DOCS = """architecture.md hyperframes-setup.md hyperframes-integration.md permissions-and-security.md
creator-onboarding.md analytics-and-metric-definitions.md media-rights-and-disclosure.md team-integration.md
privacy-and-retention.md updating-vendored-code.md evaluations.md""".split()
REQUIRED_FILES = [
    "distribution.yaml", "SOUL.md", "config.yaml", "profile.yaml", "README.md", "LICENSE",
    "THIRD_PARTY_NOTICES.md", "CHANGELOG.md", "CONTRIBUTING.md", "SECURITY.md", ".gitignore",
    ".github/workflows/ci.yml", "vendor/hyperframes.lock.yaml", "vendor/upstream/hyperframes/LICENSE",
    "skills/hyperframes-video/LICENSE", "skills/hyperframes-video/plugin.json",
    "skills/integrations/social-hyperframes/SKILL.md", "skills/integrations/social-hyperframes/scripts/hf.py",
    "skills/integrations/social-hyperframes/toolchain/package-lock.json",
    "skills/integrations/social-hyperframes/toolchain/pin.json",
    "skills/social-media-core/platform-packaging/references/platform-facts.yaml",
    "docs/test-results/install.json", "docs/test-results/integration.json",
] + [f"templates/{t}" for t in TEMPLATES] + [f"docs/{d}" for d in DOCS]
SKILL_SECTIONS = ["## When to use", "## When not to use", "## Inputs", "## Missing information",
                  "## Source handling", "## Procedure", "## Output contract", "## Checks before completion",
                  "## Permission boundaries", "## Blocked and failure behavior", "## Templates and references",
                  "## Example"]
GITIGNORE_REQUIRED = [".env", "auth.json", "node_modules/", "memories/", "sessions/", "logs/", "local/",
                      "*.db", "renders/", "footage/", "*.mp4", "*.mov", "exports/", "*.onnx"]

SECRET_PATTERNS = {
    "private key block": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----"),
    "AWS access key id": re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    "Slack token": re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b"),
    "Google API key": re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b"),
    "Anthropic or OpenAI key": re.compile(r"\bsk-(?:ant-|proj-)?[A-Za-z0-9_\-]{32,}\b"),
    "ElevenLabs or generic sk_ key": re.compile(r"\bsk_[a-f0-9]{40,}\b"),
    "Meta access token": re.compile(r"\bEAA[A-Za-z0-9]{40,}\b"),
    "JWT": re.compile(r"\beyJ[A-Za-z0-9_-]{15,}\.eyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{10,}\b"),
    "assigned secret": re.compile(
        r"(?i)\b(?:api[_-]?key|client[_-]?secret|access[_-]?token|refresh[_-]?token|password)\b\s*[:=]\s*"
        r"[\"'][A-Za-z0-9_\-/+=]{24,}[\"']"),
}
# Upstream ships one public analytics client key. It is not a credential, and
# the launcher disables the telemetry that would use it.
SECRET_ALLOW = [("media-use/scripts/lib/telemetry.mjs", "phc_")]
FORBIDDEN_NAMES = {".env", "auth.json", "state.db", "kanban.db", "engine.json", "footage-manifest.json",
                   "google_token.json", "mcp_tokens.json", "credentials"}
FORBIDDEN_SUFFIXES = {".db", ".db-wal", ".db-shm", ".pem", ".p12", ".key", ".mp4", ".mov", ".mkv", ".webm",
                      ".wav", ".onnx", ".gguf", ".safetensors", ".sqlite", ".csv", ".xlsx"}
FORBIDDEN_DIRS = {"node_modules", "memories", "sessions", "logs", "local", "renders", "footage", "exports",
                  "checkpoints", "cache", ".cache", "chrome", "browser_screenshots"}
MP3_ALLOWED_UNDER = ("skills/hyperframes-video/skills/media-use/audio/assets/sfx/",
                     "vendor/upstream/hyperframes/skills/media-use/audio/assets/sfx/")
COMMUNITY = [re.compile(r"skool\.com", re.I), re.compile(r"agentic ai academy", re.I), re.compile(r"\$97\b")]
KNOWN_HF_ENV = {"HYPERFRAMES_SKIP_SKILLS", "HYPERFRAMES_NO_UPDATE_CHECK", "HYPERFRAMES_NO_AUTO_INSTALL",
                "HYPERFRAMES_NO_TELEMETRY", "HYPERFRAMES_PREVIEW_HOST", "HYPERFRAMES_SKILL_PKG_VERSION",
                "HYPERFRAMES_PLUGIN_VERSION", "HYPERFRAMES_BROWSER_PATH", "HYPERFRAMES_API_KEY",
                "HYPERFRAMES_SKILL_NODE_MODULES"}
FABRICATION = {
    "ranking claim stated as fact": re.compile(r"(?i)\balgorithm (?:prefers|rewards|favou?rs|loves|prioriti[sz]es|pushes)\b"),
    "asserted best posting time": re.compile(r"(?i)\bbest time to post is\b"),
    "invented benchmark": re.compile(r"(?i)\b(?:industry|platform) (?:average|benchmark) (?:is|of)\b"),
    "growth guarantee": re.compile(r"(?i)\bguaranteed? (?:to )?(?:go viral|grow|double)|\bwill double your (?:followers|views|reach)\b"),
}
SPEC_NUMBER = re.compile(
    r"(?i)\b\d+(?:\.\d+)?\s?(?:GB|MB|KB|Mbps|Kbps|fps|frames per second|minutes?|seconds?|pixels|px)\b|\b\d{3,4}\s?(?:x|by)\s?\d{3,4}\b")
PLATFORM_WORD = re.compile(r"(?i)\b(instagram|reels?|tiktok|youtube|shorts?|linkedin|facebook)\b")

errors: list[str] = []
passed = 0


def check(cond: bool, label: str, detail: str = "") -> bool:
    global passed
    if cond:
        passed += 1
    else:
        errors.append(label + (f": {detail}" if detail else ""))
    return bool(cond)


def tracked_files() -> list[Path]:
    """Files Git would commit: tracked plus untracked-but-not-ignored."""
    try:
        out = subprocess.run(["git", "-C", str(REPO), "ls-files", "-co", "--exclude-standard", "-z"],
                             capture_output=True, check=True).stdout.decode()
        files = [REPO / p for p in out.split("\0") if p]
        if files:
            return [f for f in files if f.is_file() or f.is_symlink()]
    except Exception:
        pass
    return [p for p in REPO.rglob("*") if (p.is_file() or p.is_symlink()) and ".git" not in p.parts]


def rel(path: Path) -> str:
    return path.relative_to(REPO).as_posix()


def read(path: Path) -> str | None:
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if b"\0" in data:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None


def is_vendored(r: str) -> bool:
    return r.startswith(("vendor/upstream/", "skills/hyperframes-video/")) or r == "vendor/hyperframes.lock.yaml"


def frontmatter(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    try:
        return yaml.safe_load(text[4:text.index("\n---\n", 4)])
    except Exception:
        return None


BASE64_BLOB = re.compile(r"base64,[A-Za-z0-9+/=]{200,}")


def scan_secrets(text: str, where: str) -> list[str]:
    hits = []
    # Inlined fonts and images are megabytes of base64 in which any token
    # pattern eventually appears by chance. Scan the text around them.
    text = BASE64_BLOB.sub("base64,", text)
    for label, pattern in SECRET_PATTERNS.items():
        for m in pattern.finditer(text):
            if any(where.endswith(f) and m.group(0).startswith(p) for f, p in SECRET_ALLOW):
                continue
            hits.append(f"{label} in {where}")
            break
    return hits


def validate_tree() -> None:
    files = tracked_files()
    rels = {rel(f) for f in files}

    # required files
    for name in REQUIRED_FILES:
        check(name in rels, f"required file present: {name}")

    # data files parse
    for f in files:
        r = rel(f)
        if f.suffix in {".yaml", ".yml"}:
            try:
                yaml.safe_load(f.read_text(encoding="utf-8"))
                check(True, "")
            except Exception as exc:
                check(False, f"invalid YAML: {r}", str(exc)[:120])
        elif f.suffix == ".json" and not is_vendored(r):
            try:
                json.loads(f.read_text(encoding="utf-8"))
                check(True, "")
            except Exception as exc:
                check(False, f"invalid JSON: {r}", str(exc)[:120])

    # symlinks, forbidden files
    for f in files:
        r = rel(f)
        check(not f.is_symlink(), f"no symlink: {r}")
        parts = Path(r).parts
        check(not (set(parts[:-1]) & FORBIDDEN_DIRS), f"no runtime, user-state, or media directory committed: {r}")
        check(f.name not in FORBIDDEN_NAMES, f"no credential or state file committed: {r}")
        if f.suffix.lower() in FORBIDDEN_SUFFIXES:
            check(False, f"no database, key, footage, render, model, or export committed: {r}")
        if f.suffix.lower() == ".mp3":
            check(r.startswith(MP3_ALLOWED_UNDER), f"audio outside the licensed upstream sfx set: {r}")

    # secrets
    for f in files:
        r = rel(f)
        if r in SELF:
            continue
        text = read(f)
        if text is None:
            continue
        for hit in scan_secrets(text, r):
            check(False, hit)
    check(True, "secret scan complete")

    # .gitignore
    gi = (REPO / ".gitignore").read_text(encoding="utf-8") if (REPO / ".gitignore").is_file() else ""
    for entry in GITIGNORE_REQUIRED:
        check(any(line.strip() == entry for line in gi.splitlines()), f".gitignore lists {entry}")

    # manifest
    m = yaml.safe_load((REPO / "distribution.yaml").read_text(encoding="utf-8"))
    check(m.get("name") == "social-media" and str(m.get("version")) == "1.0.0" and m.get("license") == "MIT",
          "manifest name, version, license")
    check(not m.get("env_requires"), "manifest requires no environment variable")
    check("skills" not in m["distribution_owned"], "manifest never owns the whole skills directory")
    for owned in m["distribution_owned"]:
        check((REPO / owned).exists(), f"owned path exists: {owned}")
    check(not (REPO / "cron").exists(), "no cron jobs ship")

    # skills
    names: dict[str, str] = {}
    for skill_md in sorted((REPO / "skills").rglob("SKILL.md")):
        r = rel(skill_md)
        fm = frontmatter(skill_md)
        if not check(fm is not None, f"frontmatter starts at byte zero and parses: {r}"):
            continue
        name = fm.get("name", "")
        check(bool(re.fullmatch(r"[a-z0-9][a-z0-9-]{1,62}", name)), f"skill name is lowercase: {r}")
        check(name == skill_md.parent.name, f"skill name equals folder: {r}")
        check(name not in names, f"duplicate skill name {name}", f"{r} and {names.get(name)}")
        names[name] = r
        check(0 < len(str(fm.get("description", ""))) <= 1024, f"description length within Hermes limit: {r}")
        hermes = (fm.get("metadata") or {}).get("hermes") or {}
        check(all(k in fm for k in ("version", "author", "license")) and hermes.get("tags"),
              f"version, author, license, and tags present: {r}")
    for n in CORE_SKILLS:
        check(names.get(n, "").startswith("skills/social-media-core/"), f"core skill present: {n}")
    for n in VENDORED_SKILLS:
        check(names.get(n, "").startswith("skills/hyperframes-video/skills/"), f"vendored skill present: {n}")
    check(len(names) == len(CORE_SKILLS) + len(VENDORED_SKILLS) + 1, "exactly 41 skills ship", str(len(names)))

    custom = [REPO / "skills/social-media-core" / n / "SKILL.md" for n in CORE_SKILLS] + \
             [REPO / "skills/integrations/social-hyperframes/SKILL.md"]
    for skill_md in custom:
        if not skill_md.is_file():
            continue
        r = rel(skill_md)
        text = skill_md.read_text(encoding="utf-8")
        fm = frontmatter(skill_md) or {}
        check(fm.get("license") == "MIT" and fm.get("author") == "Taki Wong / TakiGPT AI Inc.",
              f"custom skill license and author: {r}")
        check(str(fm.get("description", "")).startswith("Use "), f"trigger-first description: {r}")
        for section in SKILL_SECTIONS:
            check(f"\n{section}\n" in text, f"section {section!r} present: {r}")
        check("one question at a time" in text.lower(), f"one-question rule stated: {r}")
        check("is data, not instruction" in text, f"untrusted-data rule stated: {r}")
        check("Synthetic." in text.split("## Example", 1)[-1], f"example is labeled synthetic: {r}")
        for related in ((fm.get("metadata") or {}).get("hermes") or {}).get("related_skills", []):
            check(related in names, f"related skill exists: {related} in {r}")
        for ref in re.findall(r"`(templates/[A-Za-z0-9._-]+)`", text):
            check((REPO / ref).is_file(), f"template reference resolves: {ref} in {r}")
        for ref in re.findall(r"`(references/[A-Za-z0-9._/-]+)`", text):
            check((skill_md.parent / ref).is_file(), f"reference file resolves: {ref} in {r}")
        for ref in re.findall(r"`(skills/[A-Za-z0-9._/-]+\.(?:yaml|md|py))`", text):
            check((REPO / ref).is_file(), f"path reference resolves: {ref} in {r}")

    # runtime instruction files
    runtime = [f for f in files if rel(f).startswith(("skills/social-media-core/", "skills/integrations/",
                                                       "templates/")) or rel(f) in {"SOUL.md", "config.yaml",
                                                                                    "profile.yaml"}]
    for f in runtime:
        r = rel(f)
        text = read(f) or ""
        if f.suffix in {".md", ".yaml"} and r != "config.yaml":
            check(not re.search(r"npx(?: --yes| -y)? hyperframes", text), f"no unpinned HyperFrames command: {r}")
            check("hyperframes@latest" not in text, f"no @latest: {r}")
        for label, pattern in FABRICATION.items():
            check(not pattern.search(text), f"{label}: {r}")

    # markdown links in original docs
    for f in files:
        r = rel(f)
        if f.suffix != ".md" or is_vendored(r):
            continue
        text = f.read_text(encoding="utf-8")
        for target in re.findall(r"\]\((?!https?://|#|mailto:)([^)#\s]+)", text):
            check((f.parent / target).exists(), f"internal link resolves: {target} in {r}")

    # placeholders and leftover markers in original files
    for f in files:
        r = rel(f)
        if is_vendored(r) or r in SELF or r.startswith("tests/") or f.suffix == ".json":
            continue
        text = read(f)
        if text is None:
            continue
        for token in ("<GITHUB_OWNER>", "<REPOSITORY_NAME>", "GITHUB_OWNER", "REPOSITORY_NAME", "lorem ipsum"):
            check(token.lower() not in text.lower(), f"unresolved placeholder {token}: {r}")
        check(not re.search(r"\b(?:TODO|FIXME|XXX|TBC)\b", text), f"leftover work marker: {r}")

    # examples
    examples = [f for f in files if rel(f).startswith("examples/")]
    check(len(examples) >= 6, "examples are present", str(len(examples)))
    for f in examples:
        text = read(f) or ""
        check(len(text.strip()) > 300, f"example is not empty: {rel(f)}")
        check("synthetic" in text.lower(), f"example is labeled synthetic: {rel(f)}")
        for label, pattern in FABRICATION.items():
            check(not pattern.search(text), f"{label}: {rel(f)}")

    # community promotion: README only, one section, link once
    readme = (REPO / "README.md").read_text(encoding="utf-8") if (REPO / "README.md").is_file() else ""
    check(readme.count("https://www.skool.com/agenticaiacademy/about") == 1, "community link appears exactly once in README")
    check(len(re.findall(r"(?i)agentic ai academy", readme)) <= 2, "community named in one README section only")
    check(readme.count("$97") == 1, "community price appears once in README")
    for f in files:
        r = rel(f)
        if r == "README.md" or r in SELF or r.startswith("tests/"):
            continue
        text = read(f)
        if text is None:
            continue
        check(not any(p.search(text) for p in COMMUNITY), f"community promotion outside the README: {r}")

    # README commands, flags, and environment variables
    check(f"hermes profile install {GITHUB} --alias\n" in readme, "README primary install command")
    check(f"hermes profile install {GITHUB} --alias --yes" in readme, "README documents the --yes form separately")
    first_plain = readme.find(f"hermes profile install {GITHUB} --alias\n")
    first_yes = readme.find(f"hermes profile install {GITHUB} --alias --yes")
    check(0 <= first_plain < first_yes, "confirmation-enabled command comes first")
    for cmd in ("hermes -p social-media chat", "hermes profile update social-media",
                "hermes profile delete social-media", "--assignee social-media", "--assignee marketing"):
        check(cmd in readme, f"README documents: {cmd}")
    launcher = (REPO / "skills/integrations/social-hyperframes/scripts/hf.py").read_text(encoding="utf-8")
    known_cmds = set(re.findall(r'"([a-z][a-z-]+)"', launcher.split("ALLOWED = {", 1)[1].split("}", 1)[0]))
    known_cmds |= {"doctor", "status", "pin", "setup", "script", "receipt", "footage-add", "footage-verify",
                   "rights-check", "hosts-check", "preview-start", "preview-status", "preview-stop"}
    setup_flags = set(re.findall(r'flag == "(--[a-z-]+)"', launcher)) | {"--plan", "--yes"}
    docs_text = {rel(f): f.read_text(encoding="utf-8") for f in files
                 if f.suffix == ".md" and not is_vendored(rel(f))}
    for r, text in docs_text.items():
        for m in re.finditer(r"(?:\$HF|hf\.py\"?) ([a-z][a-z-]+)((?: --?[a-z-]+(?: [^\s`|\\]+)?)*)", text):
            cmd = m.group(1)
            check(cmd in known_cmds or cmd in {"is", "in", "finds", "refuses", "and"},
                  f"documented launcher command exists: `{cmd}` in {r}")
            if cmd == "setup":
                for flag in re.findall(r"(--[a-z-]+)", m.group(2)):
                    check(flag in setup_flags, f"documented setup flag exists: {flag} in {r}")
        for var in set(re.findall(r"\bHYPERFRAMES_[A-Z_]+\b", text)):
            check(var in KNOWN_HF_ENV, f"documented environment variable is one the tagged CLI or launcher uses: {var} in {r}")

    # capability claims are backed by a recorded test
    results_path = REPO / "docs/test-results/integration.json"
    if results_path.is_file():
        results = {t["name"]: t["status"] for t in json.loads(results_path.read_text())["tests"]}
        status_doc = (REPO / "skills/integrations/social-hyperframes/references/workflow-status.md").read_text()
        claims = {
            "Captions over an existing talking-head clip": "9:16 caption draft render completes and produces a file",
            "Designed overlays on an existing clip": "9:16 overlay render (lower-third and data callout over footage) completes",
            "Short unnarrated motion graphic": "short motion-graphic render (animated stat card, 3 s) completes",
            "16:9 composition": "16:9 render completes",
        }
        for claim, test in claims.items():
            line = next((ln for ln in status_doc.splitlines() if ln.startswith(f"| {claim}")), "")
            if "rendered and inspected" in line:
                check(results.get(test) == "pass", f"claimed capability has a passing recorded render: {claim}",
                      str(results.get(test)))
        inspected = [n for n, s in results.items() if n.startswith("frames inspected") and s == "pass"]
        check(len(inspected) >= 4, "recorded renders were inspected by pixel, not by exit code", str(len(inspected)))
        check(not [n for n, s in results.items() if s == "fail"], "recorded integration results contain no failure")
        for other in ("talking-head-recut", "embedded-captions", "faceless-explainer", "motion-graphics`", "general-video`"):
            line = next((ln for ln in status_doc.splitlines() if ln.startswith(f"| `{other.rstrip('`')}`")), "")
            check("rendered and inspected |" not in line.split("|")[2] if line else True,
                  f"workflow not rendered end to end is not marked as rendered: {other}")

    # platform facts carry a source and a date
    facts = yaml.safe_load((REPO / "skills/social-media-core/platform-packaging/references/platform-facts.yaml").read_text())
    for fact in facts["facts"]:
        tag = f"{fact.get('platform')}/{fact.get('topic')}"
        check(str(fact.get("source_url", "")).startswith("https://"), f"platform fact has an official URL: {tag}")
        check(bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(fact.get("accessed", "")))), f"platform fact has an access date: {tag}")
        check(fact.get("status") in {"verified", "not_verified"}, f"platform fact has a status: {tag}")
    for f in files:
        r = rel(f)
        if f.suffix != ".md" or is_vendored(r) or r.startswith(("tests/", "evals/")):
            continue
        in_example = False
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.startswith("## "):
                in_example = line.strip() == "## Example"
            if in_example or not (PLATFORM_WORD.search(line) and SPEC_NUMBER.search(line)):
                continue
            sourced = ("http" in line or "verified" in line.lower() or "facts file" in line.lower()
                       or "synthetic" in line.lower() or "in testing" in line.lower())
            check(sourced, f"platform spec stated without a source or status: {r}", line.strip()[:110])

    # self-update, cloud, publish, sign-in unreachable
    allowed = set(re.findall(r'"([a-z][a-z-]+)"', launcher.split("ALLOWED = {", 1)[1].split("}", 1)[0]))
    prohibited = set(re.findall(r'^    "([a-z-]+)":', launcher.split("PROHIBITED = {", 1)[1].split("\n}", 1)[0], re.M))
    need = {"skills", "upgrade", "publish", "cloud", "lambda", "cloudrun", "auth", "feedback", "telemetry",
            "events", "capture", "media-use", "tts", "models", "browser"}
    check(need <= prohibited, "launcher refuses every external and self-update subcommand", str(need - prohibited))
    check(not (allowed & prohibited), "no subcommand is both allowed and prohibited", str(allowed & prohibited))
    for switch in ("HYPERFRAMES_SKIP_SKILLS", "HYPERFRAMES_NO_UPDATE_CHECK", "HYPERFRAMES_NO_AUTO_INSTALL",
                   "HYPERFRAMES_NO_TELEMETRY", "DO_NOT_TRACK"):
        check(f'"{switch}": "1"' in launcher, f"launcher sets {switch}=1")
    cfg = yaml.safe_load((REPO / "config.yaml").read_text(encoding="utf-8"))
    deny = cfg["approvals"]["deny"]
    for needle in ("*npx*hyperframes*", "*hyperframes.mjs*", "*hf.py publish*", "*hf.py cloud*", "*hf.py lambda*",
                   "*hf.py auth*", "*hf.py skills*", "*hf.py upgrade*", "*hf.py setup*", "*npm run*",
                   "*skills install*hyperframes*", "*yt-dlp*"):
        check(needle in deny, f"config deny rule present: {needle}")
    check(cfg["approvals"]["mode"] == "manual" and cfg["approvals"]["cron_mode"] == "deny", "approvals fail closed")
    check(cfg["terminal"]["home_mode"] == "profile", "terminal.home_mode is profile")
    check(cfg["memory"]["write_approval"] is True and cfg["skills"]["write_approval"] is True, "memory and skill writes staged")
    for key in ("model", "provider", "mcp_servers", "cron"):
        check(key not in cfg, f"config hardcodes no {key}")
    check(not re.search(r"(?m)^\s*[^#\n]*(/Users/|/home/|C:\\\\)", (REPO / "config.yaml").read_text()), "config has no absolute user path")

    # licenses
    lic = (REPO / "LICENSE").read_text(encoding="utf-8")
    check("MIT License" in lic and "Copyright (c) 2026 TakiGPT AI Inc." in lic, "MIT license and copyright line")
    tpn = (REPO / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8")
    for needle in ("Apache License", "Copyright 2026 HeyGen, Inc.", "GSAP Standard License", "OFL-1.1",
                   "Pixabay", "CC-BY-4.0", "vtake", "0ca28db4f8671a2e2262594e03c566222d695920"):
        check(needle in tpn, f"THIRD_PARTY_NOTICES covers: {needle}")
    check("MIT" not in (REPO / "skills/hyperframes-video/LICENSE").read_text()[:400], "vendored material is not relicensed as MIT")

    # CI actions pinned to a full commit
    ci = (REPO / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    for uses in re.findall(r"uses:\s*(\S+)", ci):
        check(bool(re.fullmatch(r"[\w.-]+/[\w./-]+@[0-9a-f]{40}", uses)), f"CI action pinned to a commit: {uses}")
    check("auto-merge" not in ci.lower() and "git push" not in ci.lower(), "CI never merges or pushes")

    # vendor verification and evals
    for script, label in (("hyperframes_vendor.py", "vendor checksums and derivative"),
                          ("check_upstream_contract.py", "upstream contract"), ("run_evals.py", "eval fixtures")):
        args = [sys.executable, str(REPO / "scripts" / script)] + (["verify"] if script == "hyperframes_vendor.py" else [])
        proc = subprocess.run(args, capture_output=True, text=True)
        check(proc.returncode == 0, label, proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else proc.stderr[-200:])


def validate_history() -> None:
    try:
        log = subprocess.run(["git", "-C", str(REPO), "log", "--all", "-p", "--no-color", "--format=commit %H"],
                             capture_output=True, check=True).stdout.decode("utf-8", errors="replace")
    except Exception as exc:
        check(False, "git history readable", str(exc)[:100])
        return
    commit, path = "?", "?"
    for line in log.splitlines():
        if line.startswith("commit "):
            commit = line[7:15]
        elif line.startswith("+++ b/"):
            path = line[6:]
            name = Path(path).name
            check(name not in FORBIDDEN_NAMES and Path(path).suffix.lower() not in (FORBIDDEN_SUFFIXES - {".csv"}),
                  f"history contains a forbidden file: {path} ({commit})")
        elif line.startswith("+") and path not in SELF:
            for hit in scan_secrets(line, f"{path} ({commit})"):
                check(False, f"history: {hit}")
    check(True, "git history secret scan complete")


def main() -> int:
    if "--only-history" not in sys.argv:
        validate_tree()
    if "--history" in sys.argv:
        validate_history()
    for e in errors:
        print(f"  FAIL  {e}")
    print(f"validate: {passed} checks passed, {len(errors)} failed")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
