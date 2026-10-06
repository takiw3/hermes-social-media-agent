# HyperFrames integration

## What is pinned

| Item | Value |
| --- | --- |
| Upstream | https://github.com/heygen-com/hyperframes |
| Tag | `v0.8.138`, published 2026-10-06 |
| Commit | `0ca28db4f8671a2e2262594e03c566222d695920` |
| npm package | `hyperframes@0.8.138` |
| npm integrity | `sha512-1xeNRkGeCobo9wbNht4BH1Y3FdSswHuo5R8UgCB8ea5eGqdRyQ7GkK8B6MGAbrhu9o7+jV7qUa2kRxjQ9KSGmg==` |
| License | Apache-2.0, Copyright 2026 HeyGen, Inc. No `NOTICE` file exists at the pinned tag. |

The lock file is `vendor/hyperframes.lock.yaml`. The same pin ships in the runtime at `skills/integrations/social-hyperframes/toolchain/pin.json`.

## The decision: Option B, a recorded derivative

Three options were on the table: install the upstream skills unchanged, derive a patched copy, or fall back to the single condensed skill Hermes ships as `official/creative/hyperframes`.

**Unchanged upstream fails** on the tagged source, for these reasons:

- The router tells the agent to run `npx hyperframes@latest upgrade --project .` when it resumes a project. That is an unpinned command.
- The router and each workflow tell the agent to run `npx hyperframes skills update <name>` first. The CLI writes skills to `~/.claude/skills` and `~/.agents/skills`, outside the profile, so the update would change nothing Hermes loads.
- The CLI skill tells the agent to send a feedback report after each render. Feedback goes to a public channel.
- Publish, HeyGen-hosted cloud render, Lambda, and Cloud Run are documented as normal commands.
- All 420 command examples are a bare `npx hyperframes`, which resolves to whatever npm serves that day.
- Bundled helper scripts in `media-use` spawn `npx hyperframes` themselves, and two helper loaders run `npm install` at run time.
- `hyperframes init` writes a `package.json` with a `publish` script into every new project.

**The Hermes optional skill is not used.** Hermes' own install scan flags it for `sudo_usage` and `unpinned_npm_install`. Its setup installs `hyperframes@>=0.4.2` globally. It is a single condensed skill without the caption, talking-head, or motion-graphics workflows. And it is named `hyperframes`, the same as the upstream router: with both installed on Hermes 0.21.5, loading `hyperframes` by name fails as ambiguous. Never install `official/creative/hyperframes` into this profile. A deny rule blocks the agent from doing it.

## How the derivative is built

`scripts/hyperframes_vendor.py` has four commands.

- `import --upstream <checkout>` copies the selected skills from a checkout of the pinned commit into `vendor/upstream/hyperframes/`, byte for byte, and refuses any other commit.
- `derive` rebuilds `skills/hyperframes-video/` from that copy by applying the rules below.
- `lock` writes the lock file.
- `verify` checks every vendored checksum, rebuilds the derivative in a temporary folder, and requires a byte-identical match with what is committed. A hand edit to a derived file fails the build.

## The rules

| Rule | What it does |
| --- | --- |
| `hermes-frontmatter` | Adds `version`, `author`, `license`, and `metadata.hermes` to each `SKILL.md`. `name` and `description` are unchanged. |
| `runtime-rules-banner` | Puts the profile's runtime rules directly under the frontmatter of each skill. |
| `pin-cli` | Replaces every unpinned CLI invocation with the launcher. |
| `launcher-scripts` | Routes `node <bundled script>` through the launcher's `script` command. |
| `neutralize-external-commands` | Rewrites every command-form mention of a prohibited subcommand to an inert `[unavailable in this profile: ...]` marker. |
| `neutralize-shell-pipelines` | Does the same for the bundled shell pipelines, which start Node helpers outside the launcher. |
| `router-profile-rules` | Replaces the router's usage check, upgrade section, install step, and desktop-app section, and lists bundled and not-bundled workflows. |
| `no-freshness-step`, `no-lazy-install` | Removes the skill self-update steps. |
| `local-render-only` | Removes cloud, publish, feedback, upgrade, telemetry, capture, and skills instructions from the CLI references. |
| `withheld-assets` | Removes references to two files that are not shipped. |
| `stub-unavailable` | Replaces five whole files with a short statement, keeping them so links resolve. |

87 of the 605 vendored skill files are modified. Each carries a prominent change notice, as Apache-2.0 section 4 requires. The full list is in `skills/hyperframes-video/MODIFICATIONS.md` and in the lock file. The other 518 skill files, and the upstream `LICENSE`, `CREDITS.md`, and `plugin.json`, are byte-identical to upstream.

## Files not shipped

| File | Why |
| --- | --- |
| `talking-head-recut/assets/fonts/Virgil.woff2` | The font's embedded metadata says "Freeware for personal use! For commercial license ...", while the Excalidraw Virgil repository publishes Virgil under OFL-1.1. Two incompatible statements, so it is treated as having no identifiable license. |
| `talking-head-recut/assets/vendor/gsap.min.js` | GSAP 3.15.0 under the GSAP Standard License. The license grants use, reproduction, display, and implementation, and does not expressly grant redistribution of the file inside another project. The workflow loads the same version from jsDelivr instead. |
| `media-use/.gitignore`, `embedded-captions/.gitignore` | Nested ignore files would hide files from this repository's Git index and so from a git-URL install. |
| `skills/python-encoding.test.mjs` | A loose upstream test file, not part of any skill. |

Their upstream checksums are recorded in the lock file.

## Skills bundled

Core: `hyperframes`, `hyperframes-core`, `hyperframes-animation`, `hyperframes-keyframes`, `hyperframes-creative`, `hyperframes-cli`, `hyperframes-audio`, `hyperframes-registry`, `hyperframes-studio`, `media-use`.

Workflows: `talking-head-recut`, `embedded-captions`, `motion-graphics`, `faceless-explainer`, `general-video`.

Not bundled: `pr-to-video`, `remotion-to-hyperframes`, `slideshow`, `figma` (out of scope for organic social in v1); `product-launch-video` (its input is a live website capture, a network read the default mode does not perform, and it was not rendered in a test); `music-to-video` (about 6 MB of assets and not rendered in a test).

## Why plugin mode alone was not enough

Upstream defines a plugin mode: when a `plugin.json` naming `hyperframes` sits two folders above a loaded `SKILL.md`, the skills stop self-updating and use a bundled launcher that pins the CLI version. This repository keeps that layout, and upstream helper scripts that locate the CLI themselves do find the manifest and resolve the pinned release.

But plugin mode is an instruction the agent has to follow, it does not cover the `@latest` upgrade probe or publish and cloud commands, and its launcher runs `npx --yes hyperframes@<version>` with floating dependencies. So the profile adds its own launcher and deny rules on top.

## What the launcher enforces

See `skills/integrations/social-hyperframes/references/command-reference.md`. In short: one lockfile-installed CLI version, five environment switches verified against the tagged source, a subcommand allowlist, a workspace boundary on the working directory and every path argument, credential-looking environment variables removed, a profile-local `HOME`, PATH shims for `npx`, `npm`, `pip` and similar, draft before final, a license record for every asset before final, a checksum check on registered source footage, and owner-approved render-time hosts only.

## How Hermes loads it

Verified on Hermes 0.21.5:

- Skill discovery walks to any depth, so `skills/hyperframes-video/skills/<name>/SKILL.md` is found. The category is the first path component, `hyperframes-video`.
- Upstream frontmatter (only `name` and `description`) loads. The added fields are the ones Hermes documents.
- `skill_view` refuses `..` in a file path. A cross-skill link such as `../media-use/references/x.md` must be loaded as `skill_view("media-use", "references/x.md")`. The banner on every skill says so, and a test loads every cross-skill link that way.
- `skill_view` returns the skill's absolute directory as `skill_dir`, which resolves upstream's `<SKILL_DIR>` placeholder.
- Hermes bridges `HERMES_HOME` into terminal subprocesses, so `"$HERMES_HOME/skills/integrations/social-hyperframes/scripts/hf.py"` resolves inside the profile with no substitution.
- `${HERMES_SKILL_DIR}` substitution exists and is on by default, but applies only to `SKILL.md` bodies, not to reference files. The profile does not depend on it.
- Hermes has no configuration key for profile-scoped environment variables that reaches a local terminal. The switches are therefore set by the launcher, not by `config.yaml`.

## Regression fixture

`tests/fixtures/compat-baseline-2026-10-06.yaml` records what was observed at the starting baseline (Hermes 0.21.5, HyperFrames 0.8.137) and at the pinned release (0.8.138, published the same day). `scripts/check_upstream_contract.py` re-checks the observations this integration depends on against the vendored copy and fails if one no longer holds.
