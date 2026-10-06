# Architecture

## What this repository is

A native Hermes Profile Distribution. Installing it creates a persistent profile named `social-media` with its own identity, configuration, skills, and state. A Hermes profile is a persistent named agent. It is not a short-lived child created through task delegation.

## Layout

| Path | Installed | Purpose |
| --- | --- | --- |
| `distribution.yaml` | yes | Manifest and the explicit ownership allowlist |
| `profile.yaml` | yes | Display name and the routing description Kanban reads |
| `SOUL.md` | yes | The agent's identity and rules |
| `config.yaml` | yes, preserved on update | Provider-neutral settings and the deny rules |
| `templates/` | yes | 20 templates the skills fill |
| `skills/social-media-core/` | yes | 25 original skills (MIT) |
| `skills/integrations/social-hyperframes/` | yes | The wrapper skill, the launcher, and the toolchain lockfile (MIT) |
| `skills/hyperframes-video/` | yes | 15 derived HeyGen HyperFrames skills (Apache-2.0) |
| `LICENSE`, `THIRD_PARTY_NOTICES.md` | yes | License notices that travel with the runtime |
| `vendor/upstream/hyperframes/` | no | Exact upstream copy, for audit |
| `vendor/hyperframes.lock.yaml` | no | Pin, checksums, patches, asset licenses |
| `scripts/`, `tests/`, `evals/`, `examples/`, `docs/`, `.github/` | no | Tooling and documentation |

## Decisions

**One profile, one brand.** The creator profile, voice, pillars, and workspace are singular by design.

**Skills are separate and small.** 25 core skills with distinct triggers and output contracts, not one large prompt. Hermes shows roughly the first 60 characters of a description in its skill index, so every description starts with its trigger.

**HyperFrames is derived, not vendored unchanged (Option B).** The unchanged upstream skills tell an agent to run `npx hyperframes@latest upgrade`, to run `skills update` before each workflow, to send a feedback report after each render, and they document publish and cloud rendering. Bundled helper scripts also spawn a bare `npx hyperframes`. None of that is acceptable in a pinned, local-only profile. So the repository keeps an exact upstream copy and generates a patched derivative from it with recorded rules. See `hyperframes-integration.md`.

**Upstream's plugin layout is kept.** The derivative sits at `skills/hyperframes-video/plugin.json` beside `skills/hyperframes-video/skills/<name>/`. Upstream helper scripts look two folders above themselves for a plugin manifest; with this layout they find one and resolve the pinned release. That is the one place the installed tree differs from a flat `skills/hyperframes-video/<name>/` layout, and it is required by the HyperFrames contract.

**One launcher, three layers.** Every HyperFrames call goes through `hf.py`. The same guarantees are held three ways: the derived instructions only name the launcher; the launcher enforces a subcommand allowlist, a workspace boundary, environment switches, and PATH shims in code; and `config.yaml` deny rules block the routes around the launcher at the Hermes approval floor, even under yolo.

**The CLI installs from a lockfile.** Upstream's own plugin launcher runs `npx --yes hyperframes@<version>`, which pins one package and lets every dependency float. This profile ships a `package-lock.json` with 171 packages, each with an integrity hash, and installs with `npm ci --ignore-scripts`.

**Setup belongs to the owner.** Installing the profile downloads nothing. The launcher's `setup` command is denied to the agent and refuses a download unless it is approved at an interactive terminal.

**No publishing mode.** Hermes instruction text is not a technical action gate, and a deny list cannot enumerate every way to reach a social platform. No hard gate that covers every publishing path exists, so `approved_publishing` is not shipped.

**Facts are dated.** Every platform spec and policy the agent may state lives in one file with its official URL, access date, and status. Unverified facts are reported as unverified.

## Data flow

1. A task arrives in direct chat or as a Kanban task.
2. `social-intake-and-routing` validates it and names the skills to run.
3. Core skills produce local drafts from the creator profile and owner-provided data.
4. For video, `social-hyperframes` checks the engine, and the launcher runs the pinned CLI inside the workspace.
5. `video-render-review` inspects frames. `platform-packaging` writes the sheet.
6. The result returns in the structured shape. Cross-team findings move through Kanban, redacted.

Nothing in that flow writes to a network service.
