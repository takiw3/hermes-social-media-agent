# Video toolchain setup

Installing the profile installs skills. It does not install Node.js, FFmpeg, a browser, the HyperFrames CLI, or any npm package, and it does not download a model, a font, or media. Until you do the steps below, the profile runs in `offline` mode and reports the video engine as `not configured`. Everything except rendering still works.

You run these steps yourself, in your own terminal. The agent cannot: `config.yaml` denies the `setup` command to it, and the launcher refuses a download that is not approved at an interactive prompt.

## What you need first

Install these yourself. The profile never does.

- **Node.js 22 or newer**, with npm.
- **FFmpeg**, which provides `ffmpeg` and `ffprobe`.
- **Disk space**: about 235 MB for the CLI and its dependencies, about 190 MB for headless Chrome, and about 650 MB more if you want local transcription.

## The launcher

```bash
HF="python3 $HOME/.hermes/profiles/social-media/skills/integrations/social-hyperframes/scripts/hf.py"
```

Adjust the path if your Hermes home is elsewhere. The launcher finds the profile from its own location.

## Steps

See everything that would be downloaded, with source, size, and license. This changes nothing:

```bash
$HF setup --plan
```

Approve a dedicated folder for video work. The launcher refuses a home folder, a filesystem root, or the profile folder:

```bash
$HF setup --workspace ~/Videos/social-media
```

It creates `footage/` for originals and `projects/` for one folder per video.

Install the pinned CLI. This runs `npm ci --ignore-scripts` against the shipped lockfile, into the profile's `local/` folder. It asks you to approve the download:

```bash
$HF setup --install-cli
```

Get a headless browser. Either let the pinned CLI download the Chrome build it pins:

```bash
$HF setup --download-browser
```

or point at one you already have, with no download:

```bash
$HF setup --use-browser /path/to/chrome-headless-shell
```

Approve the hosts your compositions load at render time. Most HyperFrames compositions load the GSAP animation library from jsDelivr. GSAP is under the GSAP Standard License, which is not an open-source license; read it at https://gsap.com/standard-license before approving:

```bash
$HF setup --allow-host cdn.jsdelivr.net
```

Check the result:

```bash
$HF doctor
```

`video engine: toolchain verified` means the profile can render.

## Optional

Local transcription. Downloads the Parakeet speech model (CC-BY-4.0) and its runtime. Without it, give the agent a transcript or captions file:

```bash
$HF setup --install-model parakeet
```

Registry blocks. Lets the agent download HyperFrames registry blocks. Each block still needs a license entry before it can be used in a final render:

```bash
$HF setup --allow-registry
```

## Every download, in one table

| Item | Source | Size | License |
| --- | --- | --- | --- |
| HyperFrames CLI `hyperframes@0.8.138` and its dependencies (171 packages in the lockfile) | registry.npmjs.org, by `npm ci` from the shipped lockfile | about 235 MB on disk | Apache-2.0 for HyperFrames (Copyright 2026 HeyGen, Inc.); each dependency under its own license |
| Headless Chrome (`chrome-headless-shell`, the build the CLI pins) | Chrome for Testing, downloaded by the pinned CLI | about 190 MB on disk | Chromium open-source licenses; read the terms at the source |
| Parakeet TDT 0.6B v3 speech model, optional | Hugging Face, downloaded by the pinned CLI | about 650 MB | CC-BY-4.0 (NVIDIA); the sherpa-onnx runtime is Apache-2.0 |
| GSAP, at render time, per render | cdn.jsdelivr.net | one script file | GSAP Standard License (Webflow), not open source |

Sizes were measured on macOS arm64 on 2026-10-06 and will differ by platform.

## Where things land

Everything goes under the profile, in `local/social-media/video-engine/`:

- `engine.json`: your workspace, browser path, approved hosts, and a record of each approval.
- `toolchain-0.8.138/`: the CLI and its `node_modules`.
- `home/`: the CLI's own home folder, so it never sees a sign-in from your real home.
- `shims/`: small scripts that stop a child process from reaching an unpinned `npx` or `npm`.

Profile updates never touch `local/`.

## Removing things

```bash
$HF setup --remove cli       # the CLI toolchain and shims
$HF setup --remove browser   # the browser this profile downloaded
$HF setup --remove model     # speech models
$HF setup --remove all
```

A browser you recorded with `--use-browser` is yours and is left in place. Your workspace is never removed. Removing the profile with `hermes profile delete social-media` removes `local/` with it, and still leaves your workspace alone if it lives outside the profile.

## Troubleshooting

- **`needs_setup`**: run `$HF doctor`. It names each missing piece and the command that fixes it.
- **Node.js too old**: upgrade Node.js yourself to 22 or newer. Nothing else changes.
- **`approval required` naming a host**: your composition loads from a host you have not approved. Approve it with `--allow-host` or remove the reference.
- **Slow renders**: normal on modest hardware. The CLI opens one or more browser workers and encodes every frame. A 6-second 1080 by 1920 draft took about 9 seconds on an Apple M2 in testing. Longer and higher-quality renders scale up from there.
- **Offline**: lint and check-free commands work. A composition that loads GSAP or fonts from a CDN cannot render without network.
- **Orphaned preview**: run `$HF preview-stop`. It stops every preview and ends any leftover process that belongs to this profile, then lists what remains.
- **Pinned version unavailable**: the install fails and nothing falls back to another version. Wait, or update the profile.
