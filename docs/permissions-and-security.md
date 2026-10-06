# Permissions and security

## Modes

| Mode | When | What the agent can do |
| --- | --- | --- |
| `offline` | The video engine is `not configured` | Interview, read owner-provided files, research, and write local drafts: ideas, hooks, scripts, briefs, edit plans, analysis, strategy, calendars, coaching |
| `draft_and_render` | `doctor` reports `toolchain verified` | Everything above, plus local lint, check, snapshot, preview, and render inside the approved workspace |
| `approved_publishing` | Not shipped | Nothing. No hard gate that covers every publishing path exists in this release. |

## Enforced in code

These hold whether or not the model follows instructions.

**By the launcher (`hf.py`)**

- One CLI version, installed from a lockfile with integrity hashes. No fallback to `npx`, a global binary, or latest.
- `HYPERFRAMES_SKIP_SKILLS`, `HYPERFRAMES_NO_UPDATE_CHECK`, `HYPERFRAMES_NO_AUTO_INSTALL`, `HYPERFRAMES_NO_TELEMETRY`, and `DO_NOT_TRACK` set on every child process.
- A subcommand allowlist. Cloud render, Lambda, Cloud Run, publish, sign-in, feedback, upgrade, skills, website capture, provider media, voice generation, and model or browser downloads are refused.
- The working directory and every path argument must resolve inside the owner-approved workspace.
- Environment variables that look like credentials are removed before the CLI runs. The CLI's `HOME` is a folder inside the profile.
- PATH shims: a child process that runs `npx`, `npm`, `pnpm`, `yarn`, `bun`, `pip`, `brew`, or `heygen` gets the pinned CLI or a refusal.
- A final render is refused with no draft receipt, an asset with no complete license record, a changed registered original, or a reference to a host the owner has not approved.
- An existing output file is never overwritten.
- A download during `setup` needs approval at an interactive terminal.
- The preview binds to 127.0.0.1.

**By Hermes, from `config.yaml`**

- `approvals.deny` rules. On Hermes 0.21.5 a deny match fires before the yolo and `approvals.mode: off` bypass. The rules block: any `npx`, `bunx`, `pnpm dlx`, or `npm install` route to HyperFrames; direct execution of the CLI entry point or a bundled script; a bare `hyperframes` binary; launcher calls for skills, upgrade, publish, cloud, lambda, auth, and feedback; `npm run` and other script runners; the launcher's `setup` command; reads of the engine state and footage manifest; provider credential names; installing the colliding optional skill; and `yt-dlp`, `youtube-dl`, `gallery-dl`, and `instaloader`.
- `approvals.mode: manual`, with `cron_mode`, `single_query_mode`, and `unattended_mode` set to `deny`.
- `memory.write_approval` and `skills.write_approval`: memory and skill changes are staged for the owner.
- `skills.inline_shell: false`: shell snippets inside skill files are never pre-executed.
- `terminal.home_mode: profile`: tool subprocesses use the profile's home folder.

**By the profile distribution**

- A narrow ownership allowlist. Updates replace only owned paths.
- No cron jobs ship. No MCP server, scheduler, or scraper is configured.

## Enforced by instruction only

Be clear-eyed about these. They depend on the model following `SOUL.md` and the skills.

- Not posting, scheduling, commenting, or messaging through some route the deny rules do not name. The rules cover HyperFrames and known download tools. They cannot enumerate every API, browser action, or tool a model could reach. This is why no publishing mode ships, and why you should not give this profile credentials or tools for social platforms.
- Writing files only inside the workspace with tools other than the launcher. The launcher's boundary covers HyperFrames calls. Hermes file tools are not restricted by this profile.
- Treating source footage as read-only outside the launcher. The checksum check detects a change. It does not prevent one. Make originals read-only at the filesystem level if that matters to you.
- One question at a time, evidence labels, sample-size discipline, never inventing a metric or a result.
- Keeping audience data, raw exports, and sponsor terms out of Kanban.
- Treating retrieved content as untrusted and reporting embedded instructions.
- Requesting consent before reading footage or data.
- Not creating recurring jobs.

## Tenant boundary

A profile is not a full tenant-security boundary. Profiles on one machine can share an operating-system user, filesystem access, and a Kanban board.

- One installed social media profile is for one brand or creator.
- Strong separation between brands needs separate operating-system users or containers, explicit mounts, isolated credentials, and separate boards.
- Kanban tenant labels and profile names are routing metadata, not access controls.
- Keep the Kanban dashboard on localhost unless you secure it separately.
- The HyperFrames preview is a long-lived local server that holds browser workers open. It stays on localhost and must be stopped when the task ends.

`terminal.home_mode: profile` is a containment convenience. It changes where tools look for a home folder. It does not stop a process from reading other paths the operating-system user can read.

## Prompt injection

Page text, captions, comments, transcripts, exports, video metadata, file names, and Kanban comments are data. The agent is told never to follow an instruction found in them and never to treat them as approval, and to report the attempt. This is an instruction-level control. The code-level controls above are what limit the damage if it fails: no publishing path, no credentials passed to the video CLI, and a deny floor under the terminal.

## Config updates

`hermes profile update` preserves your `config.yaml`. That protects your overrides, and it also means a new release's deny rules do not reach you automatically. After an update, compare your `config.yaml` with the repository's, or run the update with `--force-config` if you have no overrides to keep.
