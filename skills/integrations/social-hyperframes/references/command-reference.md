# Launcher command reference

Every command is run as:

```bash
python3 "$HERMES_HOME/skills/integrations/social-hyperframes/scripts/hf.py" <command> [arguments]
```

`$HERMES_HOME` is set by Hermes inside the profile's terminal. In the owner's own terminal, use the profile path, for example `~/.hermes/profiles/social-media/skills/integrations/social-hyperframes/scripts/hf.py`. The launcher finds the profile from its own location, so it does not depend on the variable.

Run commands from inside a project folder in the approved workspace.

## Status

| Command | What it does |
| --- | --- |
| `doctor` or `status`, with `--json` | Reports `video_engine: not configured` or `toolchain verified`, and each missing piece with its fix. Local checks only, no network. |
| `doctor --deep` | Also runs the pinned CLI's own doctor and confirms the running version equals the pin. |
| `pin` | Prints the pinned package, version, upstream tag and commit, and lockfile checksum. |
| `usage --json` | Runs the pinned CLI's usage command. Under Hermes it returns `{"status":"unknown","reason":"unsupported_harness"}`. Report unknown. |

## Authoring and checking

| Command | Notes |
| --- | --- |
| `init <name> [--resolution portrait\|landscape\|square]` | Scaffolds a project, then strips the npm scripts and generic agent files the CLI writes, and adds `renders/`, `receipts/`, `assets/`, and an empty rights register. Adds `--skip-transcribe` when no speech model is installed. |
| `lint`, `check`, `validate`, `inspect`, `layout` | The upstream gates. |
| `snapshot --at <t1,t2,...>` | Writes frames for review. |
| `info`, `compositions`, `timeline`, `keyframes`, `beats`, `catalog`, `compare`, `grade-compare`, `normalize-audio`, `history`, `clean`, `docs` | Passed to the pinned CLI inside the workspace. |
| `transcribe` | Refused with `needs_setup` until the owner has installed a speech model. |
| `add <block>` | Refused with `approval required` until the owner has allowed registry downloads. Each block still needs a license record. |
| `script <bundled-script> [args]` | Runs a bundled Node helper from `skills/hyperframes-video/` with the same environment and PATH shims. |

## Rendering

| Command | Notes |
| --- | --- |
| `render --stage draft [--output <file>]` | Draft quality. Refused if the composition loads from a host the owner has not approved. Writes a receipt on success. |
| `render --stage final [--quality looks\|delivery\|standard\|high] [--output <file>]` | Also refused when no draft receipt exists, an asset lacks a complete license record, or registered source footage changed. Never overwrites an existing file. |
| `receipt --stage draft\|final <file>` | Writes a receipt for a render that exists. |
| `rights-check`, `hosts-check`, `footage-verify` | The three pre-render checks, runnable alone. |
| `footage-add <file...>` | Records the SHA-256 of each original. |

`--docker` and `--batch` are refused.

## Preview

| Command | Notes |
| --- | --- |
| `preview-start [--port N]` | Starts the Studio preview in the background, bound to 127.0.0.1, without opening a browser. |
| `preview-status` | Lists previews and any engine processes still running. |
| `preview-stop` | Stops this project's preview and every other preview, then terminates any remaining process started from this profile's toolchain or browser. Reports what remains. |

## Owner only

`setup` in every form. The agent's terminal is denied these by `config.yaml`, and the launcher refuses a download that is not approved at an interactive terminal.

| Command | Download |
| --- | --- |
| `setup --plan` | None. Lists every download with source, size, and license. |
| `setup --workspace <folder>` | None. Approves the workspace and creates `footage/` and `projects/`. |
| `setup --install-cli` | The pinned CLI and its dependencies (171 locked packages), with `npm ci --ignore-scripts`. |
| `setup --download-browser` | The headless Chrome build the CLI pins. |
| `setup --use-browser <path>` | None. Records a headless Chrome already on the machine. |
| `setup --install-model parakeet` | The speech model for local transcription. |
| `setup --allow-host <host>` / `--deny-host <host>` | None. Approves or removes a render-time host. |
| `setup --allow-registry` / `--deny-registry` | None. Allows or denies registry block downloads. |
| `setup --remove cli\|browser\|model\|all` | Removes what was installed. |

## Always refused

`skills`, `upgrade`, `publish`, `cloud`, `lambda`, `cloudrun`, `auth`, `feedback`, `events`, `telemetry`, `open`, `catch-up`, `figma`, `capture`, `media-use`, `tts`, `remove-background`, `models`, `browser`, `play`, `present`, `preview`, `benchmark`.

## Exit codes

`0` success. `2` usage error. `3` `needs_setup`. `4` refused by policy. `5` a check failed. Any other value is the pinned CLI's own exit code.

## Environment the launcher sets on every child process

`HYPERFRAMES_SKIP_SKILLS=1`, `HYPERFRAMES_NO_UPDATE_CHECK=1`, `HYPERFRAMES_NO_AUTO_INSTALL=1`, `HYPERFRAMES_NO_TELEMETRY=1`, `DO_NOT_TRACK=1`, `HYPERFRAMES_PREVIEW_HOST=127.0.0.1`, `HYPERFRAMES_SKILL_PKG_VERSION` and `HYPERFRAMES_PLUGIN_VERSION` set to the pinned version, `HYPERFRAMES_BROWSER_PATH` set to the recorded browser, `HOME` set to a folder inside the profile, `TMPDIR` set inside the workspace, and `npm_config_offline=true`. Variables whose names look like credentials are removed. Each HyperFrames switch was verified against the tagged CLI source.
