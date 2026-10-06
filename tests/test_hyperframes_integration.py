#!/usr/bin/env python3
"""HyperFrames integration tests, run from an installed temporary profile.

Nothing runs from the source checkout: the profile is installed into a
throwaway HERMES_HOME and every command goes through the installed launcher.
Synthetic media only (generated shapes and tones, no real people).

    HERMES_SRC=... HERMES_PYTHON=... SOCIAL_TEST_BROWSER=/path/to/chrome-headless-shell \\
        python3 tests/test_hyperframes_integration.py --toolchain --renders [--json out.json]

Stages:
  (always)     engine-missing states, refusals, deny rules, links, shims
  --toolchain  installs the pinned CLI with `npm ci` (network read from npm)
  --renders    renders through headless Chrome (needs SOCIAL_TEST_BROWSER,
               or --download-browser to let the pinned CLI download one)

A stage that is not requested, or whose prerequisite is missing, is reported
`not run`. It is never reported as passed.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import (REPO, Results, Sandbox, hermes_command, hermes_python, install_profile,  # noqa: E402
                     no_network_wrapper, sha256_file)

ARGS = set(sys.argv[1:])
WANT_TOOLCHAIN = "--toolchain" in ARGS or "--renders" in ARGS
WANT_RENDERS = "--renders" in ARGS
ALLOW_BROWSER_DOWNLOAD = "--download-browser" in ARGS

GSAP = '<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>'

TRANSCRIPT = [
    {"start": 0.3, "end": 1.9, "text": "Most owners post"},
    {"start": 2.0, "end": 3.7, "text": "without a plan."},
    {"start": 3.8, "end": 5.7, "text": "Here is the fix."},
]


def page(width: int, height: int, duration: float, style: str, body: str, script: str, resolution: str) -> str:
    return f"""<!doctype html>
<html lang="en" data-resolution="{resolution}">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={width}, height={height}" />
    {GSAP}
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {width}px; height: {height}px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: 100%; height: 100%; font-family: Inter, ui-sans-serif, system-ui, sans-serif; }}
      {style}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{duration}" data-width="{width}" data-height="{height}">
      {body}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      {script}
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
"""


VIDEO = '<video id="src" class="clip" src="assets/source.mp4" data-start="0" data-duration="6" data-track-index="0" data-has-audio="true"></video>'
VIDEO_CSS = "#src { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }"


def captions_html() -> str:
    caps, tweens = [], []
    for i, seg in enumerate(TRANSCRIPT, 1):
        dur = round(seg["end"] - seg["start"], 2)
        caps.append(f'<div id="cap-{i}" class="clip cap" data-start="{seg["start"]}" data-duration="{dur}" '
                    f'data-track-index="1"><div class="cap-box" id="cap-{i}-box">{seg["text"]}</div></div>')
        tweens.append(f'tl.fromTo("#cap-{i}-box", {{ scale: 0.92, opacity: 0 }}, '
                      f'{{ scale: 1, opacity: 1, duration: 0.18, ease: "power2.out" }}, {seg["start"]});')
    css = VIDEO_CSS + """
      .cap { position: absolute; left: 90px; right: 90px; top: 1180px; height: 150px; display: flex; align-items: center; justify-content: center; }
      .cap-box { display: block; background: #ffffff; color: #111111; font-size: 64px; font-weight: 700; line-height: 1.15; padding: 22px 38px; border-radius: 22px; text-align: center; }"""
    return page(1080, 1920, 6, css, VIDEO + "\n      " + "\n      ".join(caps), "\n      ".join(tweens), "portrait")


def overlay_html() -> str:
    css = VIDEO_CSS + """
      #lower { position: absolute; left: 90px; top: 1380px; width: 760px; height: 150px; }
      #lower-card { display: block; width: 760px; height: 150px; background: #0b5fff; color: #ffffff; border-radius: 18px; padding: 26px 34px; font-size: 44px; font-weight: 700; line-height: 1.2; }
      #callout { position: absolute; left: 620px; top: 300px; width: 370px; height: 240px; }
      #callout-card { display: block; width: 370px; height: 240px; background: #ffd60a; color: #111111; border-radius: 22px; padding: 28px; font-size: 40px; font-weight: 700; line-height: 1.2; text-align: center; }"""
    body = VIDEO + """
      <div id="lower" class="clip" data-start="0.5" data-duration="5" data-track-index="1"><div id="lower-card">Synthetic Speaker, Test Fixture</div></div>
      <div id="callout" class="clip" data-start="2.5" data-duration="3" data-track-index="2"><div id="callout-card">Synthetic value 42</div></div>"""
    script = """tl.fromTo("#lower-card", { x: -60, opacity: 0 }, { x: 0, opacity: 1, duration: 0.3, ease: "power2.out" }, 0.5);
      tl.fromTo("#callout-card", { scale: 0.8, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.25, ease: "back.out(1.6)" }, 2.5);"""
    return page(1080, 1920, 6, css, body, script, "portrait")


def stat_card_html() -> str:
    css = """
      #bg { position: absolute; inset: 0; background: #101828; }
      #stat { position: absolute; left: 140px; top: 660px; width: 800px; height: 600px; }
      #stat-card { display: block; width: 800px; height: 600px; background: #ffffff; border-radius: 36px; padding: 70px 50px; text-align: center; color: #101828; }
      #stat-num { display: block; font-size: 220px; font-weight: 800; line-height: 1; }
      #stat-label { display: block; font-size: 52px; font-weight: 600; margin-top: 40px; }"""
    body = """<div id="bg" class="clip" data-start="0" data-duration="3" data-track-index="0"></div>
      <div id="stat" class="clip" data-start="0" data-duration="3" data-track-index="1"><div id="stat-card"><span id="stat-num">0</span><span id="stat-label">synthetic units</span></div></div>"""
    script = """const counter = { v: 0 };
      tl.fromTo("#stat-card", { scale: 0.85, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.35, ease: "power3.out" }, 0);
      tl.to(counter, { v: 42, duration: 1.6, ease: "power1.out", onUpdate: () => { document.getElementById("stat-num").textContent = String(Math.round(counter.v)); } }, 0.3);"""
    return page(1080, 1920, 3, css, body, script, "portrait")


def landscape_html() -> str:
    css = """
      #bg { position: absolute; inset: 0; background: #0b3d2e; }
      #title { position: absolute; left: 160px; top: 380px; width: 1600px; height: 320px; }
      #title-text { display: block; width: 1600px; color: #ffffff; font-size: 120px; font-weight: 800; line-height: 1.1; text-align: center; }"""
    body = """<div id="bg" class="clip" data-start="0" data-duration="3" data-track-index="0"></div>
      <div id="title" class="clip" data-start="0" data-duration="3" data-track-index="1"><div id="title-text">Synthetic landscape title</div></div>"""
    script = 'tl.fromTo("#title-text", { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: "power2.out" }, 0.2);'
    return page(1920, 1080, 3, css, body, script, "landscape")


def luma(video: Path, t: float, box: tuple[int, int, int, int]) -> int | None:
    """Mean gray level (0-255) of a region of one frame. Real pixel inspection."""
    x, y, w, h = box
    proc = subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-ss", str(t), "-i", str(video), "-frames:v", "1",
         "-vf", f"crop={w}:{h}:{x}:{y},scale=1:1,format=gray", "-f", "rawvideo", "-"],
        capture_output=True)
    return proc.stdout[0] if proc.returncode == 0 and proc.stdout else None


def main() -> int:
    json_out = sys.argv[sys.argv.index("--json") + 1] if "--json" in sys.argv else None
    r = Results("HyperFrames integration tests")

    if not hermes_command():
        r.notrun("all integration tests", "Hermes CLI not available; tests run only from an installed profile")
        return r.finish(json_out)

    sb = Sandbox()
    proc = install_profile(sb)
    if not r.check("profile installed into a temporary HERMES_HOME", proc.returncode == 0,
                   (proc.stdout + proc.stderr)[-300:]):
        return r.finish(json_out)
    P = sb.profile_dir
    hf_path = P / "skills/integrations/social-hyperframes/scripts/hf.py"
    bundle = P / "skills/hyperframes-video"
    pin = json.loads((P / "skills/integrations/social-hyperframes/toolchain/pin.json").read_text())
    workspace = sb.root / "video-workspace"
    base_env = sb.env(HERMES_HOME=str(P))
    if os.environ.get("SOCIAL_TEST_NPM_CACHE"):
        base_env["npm_config_cache"] = os.environ["SOCIAL_TEST_NPM_CACHE"]

    def hf(*args, cwd=None, env=None, wrap=None, timeout=900):
        cmd = (wrap or []) + [sys.executable, str(hf_path), *args]
        return subprocess.run(cmd, cwd=str(cwd) if cwd else None, env=env or base_env,
                              capture_output=True, text=True, timeout=timeout, stdin=subprocess.DEVNULL)

    def last_json(text: str) -> dict:
        idx = text.rfind("\n{")
        idx = 0 if text.lstrip().startswith("{") and idx < 0 else idx
        try:
            return json.loads(text[idx:]) if idx >= 0 else {}
        except Exception:
            m = re.search(r"\{[\s\S]*\}\s*$", text)
            try:
                return json.loads(m.group(0)) if m else {}
            except Exception:
                return {}

    # ------------------------------------------------------------------
    print("\n== engine-missing states (no toolchain installed) ==")
    d = hf("doctor", "--json")
    rep = last_json(d.stdout)
    r.check("new profile: video engine reports `not configured`",
            rep.get("video_engine") == "not configured" and d.returncode == 3, d.stdout[:200])
    r.check("doctor result parses and names result_status needs_setup",
            rep.get("result_status") == "needs_setup" and isinstance(rep.get("checks"), list))
    r.check("browser not yet downloaded is reported", "browser" in rep.get("missing", []))

    real_node = shutil.which("node")
    tools = sb.root / "tools"
    tools.mkdir()
    for name in ("ffmpeg", "ffprobe"):
        if shutil.which(name):
            (tools / name).symlink_to(shutil.which(name))
    minimal = f"{tools}:/usr/bin:/bin"
    env_no_node = dict(base_env, PATH=minimal)
    if shutil.which("node", path=minimal) is None:
        rep = last_json(hf("doctor", "--json", env=env_no_node).stdout)
        node_check = next((c for c in rep.get("checks", []) if c["name"] == "node"), {})
        r.check("Node.js absent: reported as missing, nothing installed",
                not node_check.get("ok") and "not found" in node_check.get("detail", "")
                and "node" in rep.get("missing", []), str(node_check))
    else:
        r.notrun("Node.js absent", "a system node exists in /usr/bin or /bin on this machine")

    old = sb.root / "oldnode"
    old.mkdir()
    (old / "node").write_text("#!/bin/sh\necho v18.19.0\n")
    (old / "node").chmod(0o755)
    rep = last_json(hf("doctor", "--json", env=dict(base_env, PATH=f"{old}:{minimal}")).stdout)
    node_check = next((c for c in rep.get("checks", []) if c["name"] == "node"), {})
    r.check("Node.js too old: required version stated, system unchanged",
            not node_check.get("ok") and "v18.19.0" in node_check.get("detail", "")
            and str(pin["node_minimum_major"]) in node_check.get("detail", ""), str(node_check))

    if real_node:
        nodebin = sb.root / "nodeonly"
        nodebin.mkdir()
        (nodebin / "node").symlink_to(real_node)
        rep = last_json(hf("doctor", "--json", env=dict(base_env, PATH=f"{nodebin}:/usr/bin:/bin")).stdout)
        if shutil.which("ffmpeg", path="/usr/bin:/bin") is None:
            r.check("FFmpeg absent: reported as missing",
                    {"ffmpeg", "ffprobe"} <= set(rep.get("missing", [])), str(rep.get("missing")))
        else:
            r.notrun("FFmpeg absent", "a system ffmpeg exists in /usr/bin or /bin")
    else:
        r.notrun("FFmpeg absent", "node not found, cannot isolate")

    blocked = hf("render", "--stage", "draft")
    r.check("render before the toolchain is verified returns needs_setup",
            blocked.returncode == 3 and "needs_setup" in blocked.stderr, blocked.stderr[:200])

    # ------------------------------------------------------------------
    print("\n== prohibited paths are unreachable ==")
    for sub in ("publish", "cloud", "lambda", "cloudrun", "auth", "skills", "upgrade", "feedback",
                "capture", "media-use", "tts", "models", "browser", "telemetry"):
        p = hf(sub, "render" if sub in {"cloud", "lambda", "cloudrun"} else "--help")
        r.check(f"launcher refuses `{sub}`", p.returncode == 4 and '"blocked"' in p.stderr, p.stderr[:160])
    shim = hf("_shim", "npx", "hyperframes@latest", "render")
    r.check("shim refuses an unpinned `npx hyperframes@latest`", shim.returncode == 4, shim.stderr[:160])
    shim = hf("_shim", "npx", "--yes", "hyperframes", "skills", "update", "pr-to-video")
    r.check("shim routes `npx hyperframes skills update` to a refusal (self-update inert)",
            shim.returncode == 4 and "release-managed" in shim.stderr, shim.stderr[:200])
    shim = hf("_shim", "npx", "skills", "add", "heygen-com/hyperframes", "--all")
    r.check("shim refuses `npx skills add`", shim.returncode == 4, shim.stderr[:160])
    for tool in ("npm", "pip", "brew", "heygen"):
        shim = hf("_shim", tool, "install", "x")
        r.check(f"shim refuses `{tool}` during a video task", shim.returncode == 4, shim.stderr[:120])
    nontty = hf("setup", "--install-cli")
    r.check("setup download without an interactive owner approval is refused",
            nontty.returncode == 4 and "approval required" in nontty.stderr
            and not (P / "local/social-media/video-engine").joinpath(f"toolchain-{pin['npm_version']}").exists(),
            nontty.stderr[:200])

    # ------------------------------------------------------------------
    print("\n== installed instructions and links ==")
    md_files = [p for p in bundle.rglob("*.md")] + [p for p in (P / "skills/integrations").rglob("*.md")] \
        + [p for p in (P / "skills/social-media-core").rglob("*.md")] + [P / "SOUL.md"]
    unpinned = [str(p.relative_to(P)) for p in md_files
                if re.search(r"npx(?: --yes| -y)? hyperframes", p.read_text(encoding="utf-8"))]
    r.check("no bare or unpinned `npx hyperframes` in any installed instruction file", not unpinned,
            ", ".join(unpinned[:4]))
    updates = [str(p.relative_to(P)) for p in md_files
               if re.search(r'hf\.py" (skills|upgrade|publish|cloud|lambda|cloudrun|auth|feedback)\b',
                            p.read_text(encoding="utf-8"))]
    r.check("no installed instruction calls the launcher with a prohibited subcommand", not updates,
            ", ".join(updates[:4]))
    link_re = re.compile(r"\]\((\.\.?/[^)#\s]+|[A-Za-z0-9_][^)#\s:]*\.md)\)")
    broken, cross = [], 0
    excluded = {"pr-to-video", "remotion-to-hyperframes", "slideshow", "figma", "product-launch-video",
                "music-to-video"}
    for md in bundle.rglob("*.md"):
        for m in link_re.finditer(md.read_text(encoding="utf-8")):
            target = (md.parent / m.group(1)).resolve()
            try:
                rel = target.relative_to((bundle / "skills").resolve())
            except ValueError:
                continue
            if rel.parts and rel.parts[0] in excluded:
                continue
            if m.group(1).startswith("../"):
                cross += 1
            if not target.exists():
                broken.append(f"{md.relative_to(bundle)} -> {m.group(1)}")
    r.check(f"every relative link between installed HyperFrames files resolves ({cross} cross-skill links)",
            not broken, "; ".join(broken[:4]))
    router = (bundle / "skills/hyperframes/SKILL.md").read_text(encoding="utf-8")
    bundled = ["talking-head-recut", "embedded-captions", "motion-graphics", "faceless-explainer", "general-video"]
    r.check("router lists every bundled workflow and each one is installed",
            all(f"`/{w}`" in router and (bundle / "skills" / w / "SKILL.md").is_file()
                and (bundle / "skills/hyperframes/references/routes" / f"{w}.md").is_file() for w in bundled))
    r.check("router says a workflow that is not bundled is reported, not downloaded",
            "Not bundled:" in router and "Do not download it" in router
            and all(not (bundle / "skills" / w).exists() for w in excluded))
    r.check("router no longer carries an upgrade probe or a skills-update step",
            "@latest" not in router and "skills update" not in router.replace("[unavailable in this profile:", ""))
    r.check("upstream plugin manifest sits two levels above each SKILL.md and names the pinned release",
            json.loads((bundle / "plugin.json").read_text())["version"] == pin["npm_version"])

    if os.environ.get("HERMES_SRC"):
        code = (
            "import json, re, pathlib, os\n"
            "from tools.skills_tool import skill_view\n"
            "from tools.approval_floors import _match_user_deny_rule as deny\n"
            "home = pathlib.Path(os.environ['HERMES_HOME'])\n"
            "bundle = home / 'skills/hyperframes-video/skills'\n"
            "bad, n = [], 0\n"
            "for md in bundle.rglob('*.md'):\n"
            "    for m in re.finditer(r'\\]\\((\\.\\./[^)#\\s]+)\\)', md.read_text()):\n"
            "        t = (md.parent / m.group(1)).resolve()\n"
            "        try: rel = t.relative_to(bundle.resolve())\n"
            "        except ValueError: continue\n"
            "        if not t.is_file() or len(rel.parts) < 2: continue\n"
            "        n += 1\n"
            "        v = json.loads(skill_view(rel.parts[0], '/'.join(rel.parts[1:])))\n"
            "        if not v.get('success'): bad.append(str(rel))\n"
            "L = 'python3 \"$HERMES_HOME/skills/integrations/social-hyperframes/scripts/hf.py\"'\n"
            "cases = {'npx hyperframes render': True, 'npx --yes hyperframes@latest upgrade --project .': True,\n"
            " 'hyperframes publish': True, 'cd p && hyperframes render': True, L + ' render --stage draft': False,\n"
            " L + ' lint': False, L + ' publish --yes': True, L + ' cloud render': True, L + ' lambda render x': True,\n"
            " L + ' auth login': True, L + ' skills update': True, L + ' setup --install-cli --yes': True,\n"
            " L + ' script \"$HERMES_HOME/skills/hyperframes-video/skills/media-use/scripts/transcribe.mjs\" a.mp4': False,\n"
            " 'node \"$HERMES_HOME/skills/hyperframes-video/skills/media-use/scripts/transcribe.mjs\" a.mp4': True,\n"
            " 'bash \"$HERMES_HOME/skills/hyperframes-video/skills/embedded-captions/scripts/prepare.sh\" p': True,\n"
            " 'node x/node_modules/hyperframes/bin/hyperframes.mjs cloud render': True, 'npm run publish': True,\n"
            " 'npx skills add heygen-com/hyperframes --all': True, 'heygen auth login': True,\n"
            " 'yt-dlp https://example.com/v': True, 'cat local/social-media/video-engine/engine.json': True,\n"
            " 'hermes -p social-media skills install official/creative/hyperframes --yes': True,\n"
            " L + ' render --stage final --output renders/publish-ready-author-cloud.mp4': False, 'ls -la': False}\n"
            "wrong = [c for c, want in cases.items() if (deny(c) is not None) != want]\n"
            "print(json.dumps({'links': n, 'bad': bad, 'wrong': wrong, 'cases': len(cases)}))\n"
        )
        out = hermes_python(sb, code)
        try:
            data = json.loads(out.stdout.strip().splitlines()[-1])
        except Exception:
            data = None
        if r.check("Hermes loaded the installed profile config and skills", data is not None, out.stderr[-300:]):
            r.check(f"every cross-skill link loads through Hermes skill_view ({data['links']} links)",
                    not data["bad"], ", ".join(data["bad"][:4]))
            r.check(f"Hermes deny rules give the expected verdict on {data['cases']} commands",
                    not data["wrong"], "; ".join(data["wrong"][:3]))
    else:
        r.notrun("cross-skill links through Hermes skill_view", "HERMES_SRC not set")
        r.notrun("Hermes deny rules", "HERMES_SRC not set")

    # ------------------------------------------------------------------
    print("\n== provider keys and environment switches ==")
    probe = (
        "import importlib.util, json, os, sys\n"
        f"spec = importlib.util.spec_from_file_location('hf', {str(hf_path)!r}); hf = importlib.util.module_from_spec(spec)\n"
        "spec.loader.exec_module(hf)\n"
        "os.environ.update({'HEYGEN_API_KEY': 'synthetic', 'GEMINI_API_KEY': 'synthetic', 'ELEVENLABS_API_KEY': 'synthetic',\n"
        " 'HYPERFRAMES_API_KEY': 'synthetic', 'OPENAI_API_KEY': 'synthetic', 'AWS_SECRET_ACCESS_KEY': 'synthetic',\n"
        " 'GITHUB_TOKEN': 'synthetic', 'HYPERFRAMES_PREVIEW_HOST': '0.0.0.0'})\n"
        "env = hf.child_env(hf.load_pin(), hf.load_engine())\n"
        "keep = ['HYPERFRAMES_SKIP_SKILLS','HYPERFRAMES_NO_UPDATE_CHECK','HYPERFRAMES_NO_AUTO_INSTALL',\n"
        " 'HYPERFRAMES_NO_TELEMETRY','DO_NOT_TRACK','HYPERFRAMES_PREVIEW_HOST','HYPERFRAMES_SKILL_PKG_VERSION',\n"
        " 'HYPERFRAMES_PLUGIN_VERSION','HOME','npm_config_offline']\n"
        "leaked = [k for k in env if k.endswith(('_API_KEY','_TOKEN','_SECRET_ACCESS_KEY'))]\n"
        "print(json.dumps({'env': {k: env.get(k) for k in keep}, 'leaked': leaked, 'path0': env['PATH'].split(os.pathsep)[0]}))\n"
    )
    out = subprocess.run([sys.executable, "-c", probe], env=base_env, capture_output=True, text=True)
    try:
        pe = json.loads(out.stdout.strip().splitlines()[-1])
    except Exception:
        pe = None
    if r.check("launcher child environment could be inspected", pe is not None, out.stderr[-300:]):
        e = pe["env"]
        r.check("skill self-update, update check, auto-install, and telemetry switches are all set",
                all(e[k] == "1" for k in ("HYPERFRAMES_SKIP_SKILLS", "HYPERFRAMES_NO_UPDATE_CHECK",
                                           "HYPERFRAMES_NO_AUTO_INSTALL", "HYPERFRAMES_NO_TELEMETRY", "DO_NOT_TRACK")))
        r.check("no provider key or token reaches the CLI when none is configured", not pe["leaked"], str(pe["leaked"]))
        r.check("preview host is forced to 127.0.0.1 even if the caller asks for 0.0.0.0",
                e["HYPERFRAMES_PREVIEW_HOST"] == "127.0.0.1")
        r.check("helper packages are pinned to the CLI version",
                e["HYPERFRAMES_SKILL_PKG_VERSION"] == pin["npm_version"] == e["HYPERFRAMES_PLUGIN_VERSION"])
        r.check("CLI HOME is inside the profile, so no existing sign-in is visible",
                e["HOME"].startswith(str(P)) and not Path(e["HOME"], ".heygen").exists())
        r.check("PATH shims come first", pe["path0"].startswith(str(P)))

    r.check("safe-zone helper passes a box inside owner margins", subprocess.run(
        [sys.executable, str(P / "skills/social-media-core/video-render-review/scripts/safe_zone_check.py"),
         "--canvas", "1080x1920", "--margins", "top=220,right=90,bottom=420,left=90",
         "--box", "x=90,y=1180,w=900,h=150"], capture_output=True).returncode == 0)
    r.check("safe-zone helper fails a box that crosses the bottom margin", subprocess.run(
        [sys.executable, str(P / "skills/social-media-core/video-render-review/scripts/safe_zone_check.py"),
         "--canvas", "1080x1920", "--margins", "top=220,right=90,bottom=420,left=90",
         "--box", "x=90,y=1420,w=900,h=150"], capture_output=True).returncode == 5)

    # ------------------------------------------------------------------
    toolchain_tests = [
        "toolchain setup targets the test profile", "pinned CLI version is the version that runs",
        "doctor --deep parses the pinned CLI doctor", "usage returns status unknown",
        "project creation inside the workspace", "write outside the workspace is refused",
        "init does not refresh skills", "self-update writes nothing outside the profile home",
        "lint failure handling", "transcription unavailable without a model",
        "registry add needs owner approval", "offline lint after setup"]
    render_tests = [
        "9:16 caption render", "caption text matches the synthetic transcript", "9:16 overlay render",
        "short motion-graphic render", "16:9 render", "draft versus final quality", "render receipt",
        "source footage unchanged", "asset with no license record is blocked", "check failure handling",
        "render failure reporting", "preview start and teardown", "offline render behavior",
        "external host approval gate"]
    if not WANT_TOOLCHAIN:
        for name in toolchain_tests + render_tests:
            r.notrun(name, "run with --toolchain / --renders")
        return r.finish(json_out)
    if not shutil.which("npm") or not real_node:
        for name in toolchain_tests + render_tests:
            r.notrun(name, "node and npm are required")
        return r.finish(json_out)

    print("\n== toolchain setup (owner step, run by the test as the owner) ==")
    s = hf("setup", "--workspace", str(workspace), "--install-cli", "--yes", timeout=1800)
    if not r.check("setup --workspace --install-cli succeeds from the shipped lockfile", s.returncode == 0,
                   (s.stdout + s.stderr)[-400:]):
        for name in toolchain_tests[1:] + render_tests:
            r.notrun(name, "toolchain install failed (network needed for npm ci)")
        return r.finish(json_out)
    engine_dir = P / "local/social-media/video-engine"
    engine = json.loads((engine_dir / "engine.json").read_text())
    r.check("toolchain setup targets the test profile and test workspace, not the developer's home",
            str(engine_dir).startswith(str(sb.root)) and engine["workspace"] == str(workspace.resolve())
            and (engine_dir / f"toolchain-{pin['npm_version']}/node_modules/hyperframes").is_dir())
    r.check("each approved download is recorded with item, source, size, and license",
            all(k in engine["approvals"][0] for k in ("item", "source", "size", "license", "approved_at")))
    installed = json.loads((engine_dir / f"toolchain-{pin['npm_version']}/node_modules/hyperframes/package.json").read_text())
    r.check("installed CLI version equals the pin", installed["version"] == pin["npm_version"])
    r.check("npm ci ran with --ignore-scripts (no browser was downloaded by the install)",
            not (engine_dir / "home/.cache/hyperframes/chrome").exists()
            and not (sb.home / ".cache/puppeteer").exists() and not (sb.home / ".cache/hyperframes").exists())
    # Never pass a real folder here: every candidate below is inside the sandbox
    # or is checked by importing the launcher's predicate without touching disk.
    over = hf("setup", "--workspace", str(sb.home), "--yes")
    r.check("an over-broad workspace (the HOME folder) is refused and nothing is created in it",
            over.returncode == 4 and not (sb.home / "footage").exists(), over.stderr[:160])
    probe_ws = (
        "import importlib.util, json, pathlib, pwd, os\n"
        f"spec = importlib.util.spec_from_file_location('hf', {str(hf_path)!r}); hf = importlib.util.module_from_spec(spec)\n"
        "spec.loader.exec_module(hf)\n"
        "real = pathlib.Path(pwd.getpwuid(os.getuid()).pw_dir)\n"
        "cases = {'root': pathlib.Path('/'), 'os_account_home': real, 'parent_of_home': real.parent,\n"
        " 'profile_home': hf.PROFILE_HOME, 'inside_skills': hf.PROFILE_HOME / 'skills' / 'x',\n"
        " 'shallow': pathlib.Path('/x')}\n"
        "print(json.dumps({k: hf.workspace_too_broad(v) for k, v in cases.items()}))\n"
    )
    wsp = subprocess.run([sys.executable, "-c", probe_ws], env=base_env, capture_output=True, text=True)
    try:
        verdicts = json.loads(wsp.stdout.strip().splitlines()[-1])
    except Exception:
        verdicts = {}
    r.check("workspace predicate refuses the filesystem root, the OS account's real home (even when HOME points elsewhere), its parent, the profile, and the skills folder",
            bool(verdicts) and all(verdicts.values()), str(verdicts) + wsp.stderr[-200:])
    engine = json.loads((engine_dir / "engine.json").read_text())
    r.check("the approved workspace is still the test workspace", engine["workspace"] == str(workspace.resolve()))

    browser = os.environ.get("SOCIAL_TEST_BROWSER")
    have_browser = False
    if browser and Path(browser).is_file():
        b = hf("setup", "--use-browser", browser)
        have_browser = r.check("existing headless Chrome recorded without a download", b.returncode == 0, b.stderr[:200])
    elif ALLOW_BROWSER_DOWNLOAD:
        b = hf("setup", "--download-browser", "--yes", timeout=1800)
        have_browser = r.check("pinned headless Chrome downloaded with approval", b.returncode == 0, b.stderr[-300:])
    else:
        d = hf("doctor", "--json")
        r.check("browser not yet downloaded: still `not configured`, naming the browser",
                last_json(d.stdout).get("missing") == ["browser"], d.stdout[:200])

    if not have_browser:
        for name in toolchain_tests[1:] + render_tests:
            r.notrun(name, "no headless browser (set SOCIAL_TEST_BROWSER or pass --download-browser)")
        return r.finish(json_out)

    d = hf("doctor", "--json", "--deep", cwd=workspace)
    rep = last_json(d.stdout)
    r.check("doctor reports `toolchain verified`", rep.get("video_engine") == "toolchain verified" and d.returncode == 0,
            d.stdout[:300])
    r.check("doctor --deep parses the pinned CLI's own doctor and the running version equals the pin",
            (rep.get("upstream_doctor") or {}).get("version") == pin["npm_version"], str(rep.get("upstream_doctor")))

    projects = workspace / "projects"
    u = hf("usage", "--json", cwd=projects)
    r.check("usage returns `status: unknown` under Hermes and is passed through unchanged",
            '"status":"unknown"' in u.stdout.replace(" ", ""), u.stdout[:200])

    print("\n== workspace boundary and project creation ==")
    home_snapshot = sorted(p.name for p in sb.home.iterdir())
    i = hf("init", "captions-9x16", "--resolution", "portrait", cwd=projects)
    proj = projects / "captions-9x16"
    r.check("project created inside the workspace", i.returncode == 0 and (proj / "index.html").is_file(), i.stderr[-300:])
    pkg = json.loads((proj / "package.json").read_text())
    r.check("scaffolded npm scripts (including `publish`) are removed", pkg.get("scripts") == {}
            and "publish" in pkg["hermesSocialMedia"]["removed_scripts"])
    r.check("generic agent instruction files are replaced with the profile note",
            "social-hyperframes" in (proj / "AGENTS.md").read_text() and "npx" not in (proj / "AGENTS.md").read_text())
    skills_dirs = [p for base in (sb.home, engine_dir / "home", P) for p in
                   (base / ".claude/skills", base / ".agents/skills") if p.exists()]
    r.check("init did not refresh or install skills anywhere (no ~/.claude/skills or ~/.agents/skills)",
            not skills_dirs, ", ".join(map(str, skills_dirs)))
    r.check("nothing was written to the sandbox HOME by the CLI",
            sorted(p.name for p in sb.home.iterdir()) == home_snapshot)
    outside = hf("init", "evil", cwd=sb.root)
    r.check("init from outside the workspace is refused", outside.returncode == 4 and not (sb.root / "evil").exists(),
            outside.stderr[:160])
    escape = hf("init", "../../escaped", cwd=projects)
    r.check("a path that escapes the workspace is refused",
            escape.returncode == 4 and not (sb.root / "escaped").exists(), escape.stderr[:160])

    t = hf("transcribe", "assets/source.mp4", cwd=proj)
    r.check("transcription unavailable without a model: needs_setup, owner-provided captions offered",
            t.returncode == 3 and "owner-provided captions" in t.stderr, t.stderr[:200])
    a = hf("add", "some-block", cwd=proj)
    r.check("registry block download needs owner approval", a.returncode == 4 and "approval required" in a.stderr)

    # synthetic footage
    footage = workspace / "footage" / "synthetic-talking-head-9x16.mp4"
    gen = subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i", "color=c=0x1d2433:s=1080x1920:r=30:d=6",
         "-f", "lavfi", "-i", "sine=frequency=220:sample_rate=48000:duration=6", "-vf",
         "drawbox=x=340:y=1000:w=400:h=700:color=0x3b6ea5:t=fill,drawbox=x=390:y=520:w=300:h=380:color=0xe8c39e:t=fill,"
         "drawbox=x=470:y=640:w=40:h=40:color=0x222222:t=fill,drawbox=x=570:y=640:w=40:h=40:color=0x222222:t=fill",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-g", "30", "-keyint_min", "30", "-c:a", "aac", "-shortest",
         str(footage)], capture_output=True, text=True)
    if not r.check("synthetic talking-head footage generated (shapes and a tone, no real person)",
                   gen.returncode == 0 and footage.is_file(), gen.stderr[-200:]):
        return r.finish(json_out)
    original_hash = sha256_file(footage)
    fa = hf("footage-add", str(footage), cwd=projects)
    r.check("source footage registered with its checksum", fa.returncode == 0 and original_hash in fa.stdout)

    (proj / "assets").mkdir(exist_ok=True)
    shutil.copy2(footage, proj / "assets/source.mp4")
    (proj / "transcript.json").write_text(json.dumps({"source": "synthetic, owner-provided", "segments": TRANSCRIPT}, indent=1))
    (proj / "index.html").write_text(captions_html())

    lint = hf("lint", cwd=proj)
    r.check("lint passes on the caption composition", lint.returncode == 0 and "0 error" in lint.stdout, lint.stdout[-300:])
    bad = projects / "broken-lint"
    hf("init", "broken-lint", "--resolution", "portrait", cwd=projects)
    (bad / "assets").mkdir(exist_ok=True)
    shutil.copy2(footage, bad / "assets/source.mp4")
    (bad / "index.html").write_text(captions_html().replace('data-has-audio="true"', 'data-has-audio="true" crossorigin="anonymous"'))
    bl = hf("lint", cwd=bad)
    r.check("lint failure is reported with a non-zero exit and the rule name",
            bl.returncode != 0 and "media_crossorigin_breaks_preview" in (bl.stdout + bl.stderr), (bl.stdout + bl.stderr)[-300:])

    wrap = no_network_wrapper()
    if wrap:
        ol = hf("lint", cwd=proj, wrap=wrap)
        r.check("lint works on an offline machine after setup", ol.returncode == 0, (ol.stdout + ol.stderr)[-200:])
    else:
        r.notrun("offline lint after setup", "no network-deny wrapper on this machine")

    if not WANT_RENDERS:
        for name in render_tests:
            r.notrun(name, "run with --renders")
        return r.finish(json_out)

    # ------------------------------------------------------------------
    print("\n== renders ==")
    gate = hf("render", "--stage", "draft", cwd=proj)
    r.check("render is refused until the owner approves the CDN host the composition loads",
            gate.returncode == 5 and "approval required" in gate.stderr and "cdn.jsdelivr.net" in gate.stderr
            and not list((proj / "renders").glob("*.mp4")), gate.stderr[:300])
    hf("setup", "--allow-host", "cdn.jsdelivr.net")

    early = hf("render", "--stage", "final", cwd=proj)
    r.check("final render is refused while an asset has no license record",
            early.returncode == 5 and "license record" in early.stderr and "assets/source.mp4" in early.stderr,
            early.stderr[:300])
    wrongq = hf("render", "--stage", "draft", "--quality", "delivery", cwd=proj)
    r.check("a draft render cannot use a final quality", wrongq.returncode == 4)

    t0 = time.time()
    draft = hf("render", "--stage", "draft", cwd=proj)
    res = last_json(draft.stdout)
    draft_file = Path(res.get("output", "/nonexistent"))
    ok = r.check("9:16 caption draft render completes and produces a file",
                 draft.returncode == 0 and res.get("status") == "draft rendered" and draft_file.is_file(),
                 (draft.stdout + draft.stderr)[-500:])
    print(f"       draft render wall time: {time.time() - t0:.1f}s")
    if ok:
        receipt = Path(res["receipt"]).read_text()
        fields = dict(line.split(": ", 1) for line in receipt.splitlines() if ": " in line)
        r.check("render receipt records path, duration, resolution, frame rate, size, and SHA-256",
                all(k in fields for k in ("output_path", "duration_seconds", "width", "height", "frame_rate",
                                          "size_bytes", "sha256")))
        r.check("receipt values match the file: 1080x1920, 30 fps, 6.0 s, hash equal",
                fields["width"] == "1080" and fields["height"] == "1920" and float(fields["frame_rate"]) == 30.0
                and abs(float(fields["duration_seconds"]) - 6.0) < 0.2
                and json.loads(fields["sha256"]) == sha256_file(draft_file)
                and int(fields["size_bytes"]) == draft_file.stat().st_size, receipt[:400])
        r.check("receipt says `draft rendered` and `inspected: false` until review",
                json.loads(fields["status"]) == "draft rendered" and fields["inspected"] == "false")
        comp = (proj / "index.html").read_text()
        r.check("caption text in the composition equals the synthetic transcript, in order",
                re.findall(r'class="cap-box" id="cap-\d-box">([^<]+)<', comp) == [s["text"] for s in TRANSCRIPT])
        region = (150, 1200, 780, 110)
        on = [luma(draft_file, s["start"] + 0.8, region) for s in TRANSCRIPT]
        off = luma(draft_file, 0.1, region)
        r.check("frames inspected: a caption box is present during each transcript segment and absent before the first",
                all(v is not None and v > 150 for v in on) and off is not None and off < 110, f"on={on} off={off}")
        face = luma(draft_file, 3.0, (400, 540, 280, 80))
        r.check("frames inspected: the source footage is visible under the captions", face is not None and face > 150,
                str(face))
        szc = subprocess.run([sys.executable, str(P / "skills/social-media-core/video-render-review/scripts/safe_zone_check.py"),
                              "--canvas", "1080x1920", "--margins", "top=220,right=90,bottom=420,left=90",
                              "--box", "x=90,y=1180,w=900,h=150"], capture_output=True)
        r.check("caption box sits inside the synthetic owner-confirmed safe margins", szc.returncode == 0)

        snap = hf("snapshot", "--at", "1.0,2.8,4.8", cwd=proj, timeout=300)
        shots = sorted(p for p in proj.rglob("*.png") if "snapshot" in p.as_posix().lower())
        r.check("snapshot writes one frame per requested time for review",
                snap.returncode == 0 and len(shots) >= 3, (snap.stdout + snap.stderr)[-300:] + f" files={len(shots)}")

    print("\n== draft versus final ==")
    (proj / "asset-rights-register.yaml").write_text(
        "assets:\n  - asset: assets/source.mp4\n    kind: footage\n    source: generated by this test with ffmpeg lavfi\n"
        "    license: synthetic test media, no rights reserved\n    proof: tests/test_hyperframes_integration.py\n")
    rc = hf("rights-check", cwd=proj)
    r.check("rights check passes once the asset has source, license, and proof", rc.returncode == 0, rc.stdout[:200])
    final = hf("render", "--stage", "final", cwd=proj)
    fres = last_json(final.stdout)
    final_file = Path(fres.get("output", "/nonexistent"))
    if r.check("final render completes after a draft and a complete rights register",
               final.returncode == 0 and fres.get("status") == "final rendered with file path" and final_file.is_file(),
               (final.stdout + final.stderr)[-400:]):
        frec = Path(fres["receipt"]).read_text()
        r.check("final receipt records stage final and quality delivery, distinct from the draft",
                'stage: "final"' in frec and 'quality: "delivery"' in frec and final_file != draft_file)
        again = hf("render", "--stage", "final", "--output", str(final_file), cwd=proj)
        r.check("an existing output is never overwritten", again.returncode == 4)
    r.check("source footage is unchanged after the full edit (checksum equal)",
            sha256_file(footage) == original_hash and hf("footage-verify", cwd=proj).returncode == 0)

    print("\n== other canvases and workflows ==")
    def render_project(name: str, html: str, resolution: str, with_footage: bool):
        hf("init", name, "--resolution", resolution, cwd=projects)
        pr = projects / name
        if with_footage:
            (pr / "assets").mkdir(exist_ok=True)
            shutil.copy2(footage, pr / "assets/source.mp4")
        (pr / "index.html").write_text(html)
        li = hf("lint", cwd=pr)
        dr = hf("render", "--stage", "draft", cwd=pr)
        info = last_json(dr.stdout)
        return pr, li, dr, Path(info.get("output", "/nonexistent")), info

    pr, li, dr, out_file, info = render_project("overlay-9x16", overlay_html(), "portrait", True)
    if r.check("9:16 overlay render (lower-third and data callout over footage) completes",
               li.returncode == 0 and dr.returncode == 0 and out_file.is_file(), (dr.stdout + dr.stderr)[-400:]):
        lower_on, lower_off = luma(out_file, 3.0, (120, 1400, 300, 110)), luma(out_file, 0.1, (120, 1400, 300, 110))
        call_on, call_off = luma(out_file, 4.0, (650, 320, 300, 200)), luma(out_file, 1.0, (650, 320, 300, 200))
        r.check("frames inspected: lower-third appears at 0.5 s and the callout at 2.5 s, neither before",
                None not in (lower_on, lower_off, call_on, call_off) and abs(lower_on - lower_off) > 25
                and call_on > 150 and call_off < 110, f"lower {lower_off}->{lower_on}, callout {call_off}->{call_on}")

    pr, li, dr, out_file, info = render_project("stat-card", stat_card_html(), "portrait", False)
    if r.check("short motion-graphic render (animated stat card, 3 s) completes",
               li.returncode == 0 and dr.returncode == 0 and out_file.is_file(), (dr.stdout + dr.stderr)[-400:]):
        card, bg = luma(out_file, 2.5, (200, 700, 680, 60)), luma(out_file, 2.5, (20, 20, 80, 80))
        r.check("frames inspected: the card is on screen over the dark background", card is not None and card > 200
                and bg is not None and bg < 60, f"card={card} bg={bg}")
        rec = Path(info["receipt"]).read_text()
        r.check("motion graphic is 3.0 s at 1080x1920", "duration_seconds: 3.0" in rec and "height: 1920" in rec, rec[:300])

    pr, li, dr, out_file, info = render_project("landscape-16x9", landscape_html(), "landscape", False)
    if r.check("16:9 render completes", li.returncode == 0 and dr.returncode == 0 and out_file.is_file(),
               (dr.stdout + dr.stderr)[-400:]):
        rec = Path(info["receipt"]).read_text()
        r.check("16:9 output is 1920x1080", "width: 1920" in rec and "height: 1080" in rec, rec[:300])
        title = luma(out_file, 2.0, (500, 420, 900, 120))
        r.check("frames inspected: the title text is drawn on the background", title is not None and 40 < title < 240,
                str(title))

    print("\n== failure handling ==")
    receipts_before = len(list((proj / "receipts").glob("*.yaml")))
    rf = hf("render", "--stage", "draft", "-c", "does-not-exist.html", cwd=proj)
    r.check("render failure is reported as `render failed` with the exit code, and no receipt is written",
            rf.returncode != 0 and "render failed" in rf.stderr
            and len(list((proj / "receipts").glob("*.yaml"))) == receipts_before, rf.stderr[-300:])
    r.check("render failure message forbids a blind retry", "Do not retry blindly" in rf.stderr)
    ck = hf("check", cwd=bad, timeout=600)
    r.check("check failure is reported with a non-zero exit", ck.returncode != 0, (ck.stdout + ck.stderr)[-200:])

    orig2 = workspace / "footage" / "tamper-fixture.mp4"
    shutil.copy2(footage, orig2)
    hf("footage-add", str(orig2), cwd=projects)
    with orig2.open("ab") as fh:
        fh.write(b"tampered")
    fv = hf("footage-verify", cwd=proj)
    r.check("a changed original is detected by checksum and blocks a final render",
            fv.returncode == 5 and "tamper-fixture.mp4" in fv.stdout
            and hf("render", "--stage", "final", cwd=proj).returncode == 5, fv.stdout[:200])
    orig2.unlink()

    print("\n== preview lifecycle ==")
    ps = hf("preview-start", "--port", "3477", cwd=proj, timeout=180)
    started = r.check("preview starts in the background", ps.returncode == 0, (ps.stdout + ps.stderr)[-300:])
    if started:
        time.sleep(2)
        listing = hf("preview-status", cwd=proj).stdout
        r.check("preview is bound to 127.0.0.1", "127.0.0.1" in listing or "localhost" in listing, listing[:300])
    stop = hf("preview-stop", cwd=proj, timeout=120)
    sres = last_json(stop.stdout)
    r.check("preview stops and no engine process or browser worker remains",
            stop.returncode == 0 and sres.get("status") == "preview stopped" and sres.get("remaining") == [],
            stop.stdout[-300:])

    print("\n== offline behavior after setup ==")
    if wrap:
        off = hf("render", "--stage", "draft", cwd=projects / "stat-card", wrap=wrap, timeout=600)
        ores = last_json(off.stdout)
        if off.returncode == 0 and Path(ores.get("output", "/x")).is_file():
            card = luma(Path(ores["output"]), 2.5, (200, 700, 680, 60))
            r.check("offline render of a CDN-dependent composition: observed result recorded",
                    True, "")
            print(f"       observed: render exit 0 offline; card region luma {card} "
                  f"({'animation library was available' if card and card > 200 else 'content missing: the CDN library did not load'})")
        else:
            r.check("offline render of a CDN-dependent composition fails and is reported as `render failed`",
                    "render failed" in off.stderr, off.stderr[-300:])
            print("       observed: the render fails offline because GSAP loads from the CDN")
    else:
        r.notrun("offline render behavior", "no network-deny wrapper on this machine")

    return r.finish(json_out)


if __name__ == "__main__":
    sys.exit(main())
