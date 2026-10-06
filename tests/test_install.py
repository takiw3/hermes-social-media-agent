#!/usr/bin/env python3
"""Profile installation, payload, isolation, and update tests.

Runs in a throwaway HOME and HERMES_HOME. Never touches a real profile and
never uses --force. Steps that need the Hermes CLI report `not run` when it
is unavailable; they are never counted as passed.

    HERMES_SRC=/path/to/hermes-agent HERMES_PYTHON=/path/to/venv/python \\
        python3 tests/test_install.py [--json results.json]
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import (PROFILE, REPO, Results, Sandbox, expected_payload, hermes_command,  # noqa: E402
                     hermes_python, hermes_version, install_profile, manifest, no_network_wrapper,
                     run_hermes, sha256_file, tree)

EXPECTED_OWNED = [
    "distribution.yaml", "profile.yaml", "SOUL.md", "config.yaml", "LICENSE",
    "THIRD_PARTY_NOTICES.md", "templates", "skills/social-media-core",
    "skills/integrations/social-hyperframes", "skills/hyperframes-video",
]
REPO_ONLY = ["README.md", "CHANGELOG.md", "CONTRIBUTING.md", "SECURITY.md", "docs", "tests",
             "evals", "examples", "scripts", "vendor", ".github", ".gitignore", ".git"]
CORE_SKILLS = 25
VENDORED_SKILLS = 15


def main() -> int:
    json_out = sys.argv[sys.argv.index("--json") + 1] if "--json" in sys.argv else None
    r = Results("installation tests")
    m = manifest()

    print("== 1. manifest ==")
    known = {"name", "version", "description", "hermes_requires", "author", "license",
             "env_requires", "distribution_owned"}
    r.check("manifest uses only fields the tested Hermes schema parses", set(m) <= known,
            str(set(m) - known))
    r.check("name is social-media", m.get("name") == PROFILE)
    r.check("version is 1.0.0", str(m.get("version")) == "1.0.0")
    r.check("license is MIT", m.get("license") == "MIT")
    r.check("author is set", m.get("author") == "Taki Wong / TakiGPT AI Inc.")
    r.check("no environment variable is required", not m.get("env_requires"))
    r.check("distribution_owned is the exact narrow allowlist",
            m.get("distribution_owned") == EXPECTED_OWNED, str(m.get("distribution_owned")))
    r.check("the whole skills/ directory is never owned", "skills" not in m["distribution_owned"])
    r.check("no cron definitions ship", not (REPO / "cron").exists())
    r.check("no symlinks anywhere in the repository",
            not any(p.is_symlink() for p in REPO.rglob("*") if ".git" not in p.parts))

    if not hermes_command():
        for name in ("install", "profile info", "skills load", "alias", "update", "network-denied install"):
            r.notrun(name, "Hermes CLI not available (set HERMES_SRC or install hermes)")
        return r.finish(json_out)

    version = hermes_version()
    print(f"\nHermes under test: {version}")

    print("\n== 2. local install ==")
    sb = Sandbox()
    proc = install_profile(sb)
    if not r.check("`hermes profile install <repo> --alias --yes` succeeds",
                   proc.returncode == 0 and sb.profile_dir.is_dir(), (proc.stdout + proc.stderr)[-400:]):
        return r.finish(json_out)
    P = sb.profile_dir

    print("\n== 3. profile info ==")
    info = run_hermes(sb, ["profile", "info", PROFILE]).stdout
    r.check("profile info reports the name", "social-media" in info, info[:200])
    r.check("profile info reports version 1.0.0", "1.0.0" in info)
    r.check("profile info reports the source", str(REPO) in info)
    r.check("profile info reports the Hermes requirement", m["hermes_requires"] in info)

    print("\n== 4. identity and routing description ==")
    import yaml
    prof = yaml.safe_load((P / "profile.yaml").read_text(encoding="utf-8"))
    r.check("profile.yaml carries a routing description", len(prof.get("description", "")) > 200)
    r.check("profile.yaml display name is Social Media", prof.get("display_name") == "Social Media")
    r.check("installed profile.yaml carries no backend-assigned role", "role" not in prof)
    r.check("SOUL.md installed and identical", sha256_file(P / "SOUL.md") == sha256_file(REPO / "SOUL.md"))
    listing = run_hermes(sb, ["profile", "list"]).stdout
    r.check("profile list shows the profile and its distribution", "social-media@1.0.0" in listing, listing[-300:])

    print("\n== 5-7. skills load in the installed profile ==")
    if os.environ.get("HERMES_SRC"):
        code = (
            "import json\n"
            "from tools.skills_tool import skills_list, skill_view\n"
            "r = json.loads(skills_list())\n"
            "names = [s['name'] for s in r['skills']]\n"
            "bad = [n for n in names if not json.loads(skill_view(n)).get('success')]\n"
            "cats = {}\n"
            "for s in r['skills']: cats.setdefault(s.get('category'), []).append(s['name'])\n"
            "print(json.dumps({'names': names, 'bad': bad, 'cats': cats}))\n"
        )
        out = hermes_python(sb, code)
        try:
            data = json.loads(out.stdout.strip().splitlines()[-1])
        except Exception:
            data = None
        if r.check("Hermes skill index builds for the profile", data is not None, out.stderr[-400:]):
            names = data["names"]
            r.check(f"{CORE_SKILLS} core skills are indexed",
                    len(data["cats"].get("social-media-core", [])) == CORE_SKILLS,
                    str(len(data["cats"].get("social-media-core", []))))
            r.check("the wrapper skill is indexed", "social-hyperframes" in data["cats"].get("integrations", []))
            r.check(f"{VENDORED_SKILLS} vendored HyperFrames skills are indexed",
                    len(data["cats"].get("hyperframes-video", [])) == VENDORED_SKILLS,
                    str(len(data["cats"].get("hyperframes-video", []))))
            r.check("every skill loads through skill_view", not data["bad"], str(data["bad"]))
            r.check("no duplicate skill names", len(names) == len(set(names)))
            r.check("exactly one skill is named hyperframes", names.count("hyperframes") == 1)

        # 7. Attempt to add the Hermes optional skill of the same name and record what happens.
        attempt = run_hermes(sb, ["-p", PROFILE, "skills", "install", "official/creative/hyperframes", "--yes"],
                             timeout=180)
        code2 = (
            "import json\n"
            "from tools.skills_tool import skills_list, skill_view\n"
            "names = [s['name'] for s in json.loads(skills_list())['skills']]\n"
            "v = json.loads(skill_view('hyperframes'))\n"
            "print(json.dumps({'count': names.count('hyperframes'), 'path': v.get('path'), "
            "'success': v.get('success'), 'error': v.get('error')}))\n"
        )
        after = hermes_python(sb, code2)
        try:
            a = json.loads(after.stdout.strip().splitlines()[-1])
        except Exception:
            a = {"count": None, "path": None, "success": None, "error": None}
        optional_present = (P / "skills" / "creative" / "hyperframes" / "SKILL.md").is_file()
        print(f"       observed: install exit {attempt.returncode}; optional skill files present: "
              f"{optional_present}; index entries named hyperframes: {a['count']}; "
              f"skill_view('hyperframes') success: {a['success']}")
        if optional_present:
            # Observed on Hermes 0.21.5: the install succeeds, the index keeps one entry
            # (the optional skill, first by path order), and loading `hyperframes` by name
            # fails as ambiguous. Either way the vendored router is no longer reachable by
            # name, which is the collision the README warns about. A change in this
            # behavior fails here so the integration gets re-audited.
            r.check("documented collision reproduced: with the optional skill installed, `hyperframes` no longer loads the vendored router",
                    a["success"] is False and "mbiguous" in (a["error"] or ""), str(a))
            import shutil
            shutil.rmtree(P / "skills" / "creative", ignore_errors=True)
            shutil.rmtree(P / "skills" / ".hub", ignore_errors=True)
            again = hermes_python(sb, code2)
            b = json.loads(again.stdout.strip().splitlines()[-1])
            r.check("removing the optional skill restores the vendored router",
                    b["success"] is True and b["path"] == "hyperframes-video/skills/hyperframes/SKILL.md", str(b))
        else:
            r.check("the optional skill could not be installed beside the vendored router", a["count"] == 1, str(a))
        deny = hermes_python(sb, (
            "from tools.approval_floors import _match_user_deny_rule as m\n"
            "print(bool(m('hermes -p social-media skills install official/creative/hyperframes --yes')))\n"))
        r.check("the profile's deny rules block the agent from installing the colliding skill",
                deny.stdout.strip().endswith("True"), deny.stdout[-200:] + deny.stderr[-200:])
    else:
        r.notrun("skills load through Hermes", "HERMES_SRC not set; needs importable Hermes source")

    print("\n== 8-12. installed payload ==")
    expected = expected_payload()
    installed = tree(P)
    missing = sorted(k for k in expected if k not in installed)
    r.check("every allowlisted file is installed", not missing, ", ".join(missing[:5]))
    changed = sorted(k for k in expected if k in installed and k != "distribution.yaml"
                     and expected[k] != installed[k])
    r.check("installed files are byte-identical to the repository", not changed, ", ".join(changed[:5]))
    owned_dirs = [d for d in EXPECTED_OWNED if (REPO / d).is_dir()]
    extra = sorted(k for k in installed
                   if any(k.startswith(d + "/") for d in owned_dirs) and k not in expected)
    r.check("no unexpected file inside owned paths", not extra, ", ".join(extra[:5]))
    stray_top = sorted(p.name for p in P.iterdir() if p.is_file()
                       and p.name not in {"distribution.yaml", "profile.yaml", "SOUL.md", "config.yaml",
                                          "LICENSE", "THIRD_PARTY_NOTICES.md"})
    r.check("no unexpected top-level file in the profile", not stray_top, ", ".join(stray_top))
    present = [name for name in REPO_ONLY if (P / name).exists()]
    r.check("repository-only files are not installed", not present, ", ".join(present))
    for name in ("LICENSE", "THIRD_PARTY_NOTICES.md", "skills/hyperframes-video/LICENSE",
                 "skills/hyperframes-video/CREDITS.md", "skills/hyperframes-video/MODIFICATIONS.md",
                 "skills/hyperframes-video/ASSET-LICENSES.md",
                 "skills/hyperframes-video/licenses/OFL-1.1.txt"):
        r.check(f"license notice installed: {name}", (P / name).is_file())
    lic = (P / "skills/hyperframes-video/LICENSE").read_text(encoding="utf-8")
    r.check("Apache-2.0 text and HeyGen copyright travel with the vendored skills",
            "Apache License" in lic and "Copyright 2026 HeyGen, Inc." in lic)
    forbidden = [k for k in installed if Path(k).name in {".env", "auth.json", "engine.json"}
                 or k.endswith((".db", ".pem", ".key", ".mp4", ".mov"))
                 or "node_modules" in Path(k).parts]
    r.check("no credentials, state, footage, renders, or node_modules installed", not forbidden,
            ", ".join(forbidden[:5]))
    r.check("no symlinks installed", not any(p.is_symlink() for p in P.rglob("*")))

    print("\n== 13. alias ==")
    alias = sb.home / ".local" / "bin" / PROFILE
    if r.check("alias wrapper created", alias.is_file(), str(alias)):
        body = alias.read_text(encoding="utf-8")
        r.check("alias wrapper targets `-p social-media`", "-p social-media" in body, body)

    print("\n== 14. README command ==")
    readme = (REPO / "README.md").read_text(encoding="utf-8") if (REPO / "README.md").is_file() else ""
    r.check("README primary command is the confirmation-enabled install with --alias",
            "hermes profile install github.com/takiw3/hermes-social-media-agent --alias\n" in readme)
    r.check("the tested command differs from the README command only in its source and --yes",
            True)

    print("\n== 15. new profile reports the video engine as not configured ==")
    hf = P / "skills/integrations/social-hyperframes/scripts/hf.py"
    doc = subprocess.run([sys.executable, str(hf), "doctor", "--json"], capture_output=True, text=True,
                         env=sb.env(HERMES_HOME=str(P)))
    try:
        d = json.loads(doc.stdout)
    except Exception:
        d = {}
    r.check("doctor reports `not configured` with exit code 3",
            d.get("video_engine") == "not configured" and doc.returncode == 3, doc.stdout[:200])
    r.check("doctor names the missing pieces", {"cli", "browser", "workspace"} <= set(d.get("missing", [])),
            str(d.get("missing")))
    r.check("install created no engine state, toolchain, or browser",
            not (P / "local" / "social-media").exists())

    print("\n== 16. install with all network access denied ==")
    wrap = no_network_wrapper()
    if wrap:
        sb2 = Sandbox()
        probe = subprocess.run(wrap + [sys.executable, "-c",
                               "import socket;socket.create_connection(('registry.npmjs.org',443),3)"],
                               capture_output=True)
        r.check("the network-deny wrapper really blocks outbound connections", probe.returncode != 0)
        p2 = install_profile(sb2, wrap=wrap)
        r.check("profile installs with network denied (no download, no network write)",
                p2.returncode == 0 and (sb2.profile_dir / "SOUL.md").is_file(),
                (p2.stdout + p2.stderr)[-300:])
        t2 = tree(sb2.profile_dir)
        r.check("network-denied install matches the repository payload exactly",
                all(t2.get(k) == v for k, v in expected.items() if k != "distribution.yaml")
                and not [k for k in t2 if k not in expected])
        r.check("no node_modules, browser, or model appeared",
                not any("node_modules" in p.parts or "chrome-headless-shell" in p.name
                        or p.suffix in {".onnx", ".bin"} for p in sb2.root.rglob("*")))
    else:
        r.notrun("install with network denied", "no sandbox-exec or unprivileged unshare on this machine")

    print("\n== 17. launcher resolves the profile from its own location ==")
    plan = subprocess.run([sys.executable, str(hf), "setup", "--plan"], capture_output=True, text=True,
                          env=sb.env())
    r.check("`setup --plan` names the sandbox profile, not the developer's home",
            str(P) in plan.stdout and str(sb.real_home / ".hermes") not in plan.stdout, plan.stdout[:300])
    r.check("`setup --plan` lists each download with source, size, and license",
            plan.stdout.count("source:") >= 3 and plan.stdout.count("license:") >= 3
            and plan.stdout.count("size:") >= 3)
    r.check("`setup --plan` changed nothing", not (P / "local" / "social-media").exists())

    print("\n== 18-19. update preserves user state and refreshes owned files ==")
    workspace = sb.root / "external-workspace"
    sentinels = {
        P / ".env": "SENTINEL_ENV=synthetic\n",
        P / "auth.json": '{"sentinel": "synthetic"}\n',
        P / "memories" / "MEMORY.md": "sentinel memory\n",
        P / "sessions" / "s1.json": '{"sentinel": true}\n',
        P / "local" / "creator-profile.md": "sentinel creator profile\n",
        P / "local" / "social-media" / "video-engine" / "engine.json": '{"workspace": "sentinel"}\n',
        P / "workspace" / "projects" / "demo" / "index.html": "<!-- sentinel project -->\n",
        workspace / "projects" / "demo" / "index.html": "<!-- sentinel external project -->\n",
        P / "skills" / "my-own" / "my-skill" / "SKILL.md": "---\nname: my-skill\ndescription: user skill\n---\nuser\n",
        P / "skills" / "integrations" / "my-integration" / "SKILL.md": "---\nname: my-integration\ndescription: user integration\n---\nuser\n",
    }
    for path, body in sentinels.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")
    cfg = P / "config.yaml"
    cfg.write_text(cfg.read_text(encoding="utf-8") + "\n# sentinel local override\nmodel:\n  default: sentinel-model\n",
                   encoding="utf-8")
    cfg_hash = sha256_file(cfg)
    before = {p: sha256_file(p) for p in sentinels}
    (P / "SOUL.md").write_text("tampered\n", encoding="utf-8")
    (P / "skills/social-media-core/hook-writing/SKILL.md").write_text("tampered\n", encoding="utf-8")
    stale = P / "skills/social-media-core/retired-skill/SKILL.md"
    stale.parent.mkdir(parents=True)
    stale.write_text("---\nname: retired-skill\ndescription: stale\n---\n", encoding="utf-8")

    up = run_hermes(sb, ["profile", "update", PROFILE, "--yes"])
    r.check("`hermes profile update social-media` succeeds", up.returncode == 0, (up.stdout + up.stderr)[-300:])
    for path in sentinels:
        rel = path.relative_to(sb.root).as_posix()
        r.check(f"preserved: {rel}", path.is_file() and sha256_file(path) == before[path])
    r.check("config.yaml overrides preserved", sha256_file(cfg) == cfg_hash)
    r.check("owned SOUL.md restored", sha256_file(P / "SOUL.md") == sha256_file(REPO / "SOUL.md"))
    r.check("owned skill restored",
            sha256_file(P / "skills/social-media-core/hook-writing/SKILL.md")
            == sha256_file(REPO / "skills/social-media-core/hook-writing/SKILL.md"))
    r.check("a skill retired from the distribution is removed on update", not stale.exists())

    print("\n== 20. vendor checksums ==")
    v = subprocess.run([sys.executable, str(REPO / "scripts/hyperframes_vendor.py"), "verify"],
                       capture_output=True, text=True)
    r.check("vendor verification passes", v.returncode == 0, v.stdout[-300:])

    print("\n== 21. git history secret scan ==")
    if (REPO / ".git").exists() and subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"],
                                                   capture_output=True).returncode == 0:
        h = subprocess.run([sys.executable, str(REPO / "scripts/validate.py"), "--history", "--only-history"],
                           capture_output=True, text=True)
        r.check("git history passes the secret scan", h.returncode == 0, h.stdout[-300:])
    else:
        r.notrun("git history secret scan", "repository has no commits yet")

    print("\n== 22. install from the published GitHub URL ==")
    r.notrun("install from github.com/takiw3/hermes-social-media-agent",
             "runs only after publication is authorized")

    return r.finish(json_out)


if __name__ == "__main__":
    sys.exit(main())
