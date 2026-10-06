# Hermes social media agent

A Hermes profile that runs organic social for one business. It researches, plans, scripts, edits and renders video locally, analyzes the numbers you give it, and coaches you into a better creator.

It drafts and it renders. It does not post.

Release status: **draft-and-render release**, version 1.0.0.

## Contents

- [What it is](#what-it-is)
- [Install](#install)
- [Set up video rendering](#set-up-video-rendering)
- [Use it](#use-it)
- [What it can do](#what-it-can-do)
- [What it cannot verify](#what-it-cannot-verify)
- [Platforms and formats](#platforms-and-formats)
- [Video workflows](#video-workflows)
- [HyperFrames version and provenance](#hyperframes-version-and-provenance)
- [Permission model](#permission-model)
- [Working with the rest of your agent team](#working-with-the-rest-of-your-agent-team)
- [Skills](#skills)
- [Analytics](#analytics)
- [Media rights and disclosure](#media-rights-and-disclosure)
- [Sensitive cases](#sensitive-cases)
- [Prompt injection](#prompt-injection)
- [Data, retention, and privacy](#data-retention-and-privacy)
- [Tenant boundaries](#tenant-boundaries)
- [Update and remove](#update-and-remove)
- [Troubleshooting](#troubleshooting)
- [Test status](#test-status)
- [Contributing and security](#contributing-and-security)
- [Licensing](#licensing)

## What it is

A native [Hermes Profile Distribution](https://hermes-agent.nousresearch.com/docs/user-guide/profile-distributions). Installing it creates a persistent profile named `social-media` with its own identity, skills, configuration, and state.

It behaves like a head of content who is also a working editor and a blunt, generous coach.

**Who it is for:** business owners, entrepreneurs, and executives running companies from $250,000 to $50 million a year. One installed profile serves one brand or creator.

**What it owns in an agent team:** organic social. Audience and niche research, content pillars, ideation, hooks, scripts, filming briefs, edit plans, video editing and rendering through HyperFrames, packaging, repurposing, performance analysis, analytics-based strategy, content experiments, and coaching.

It takes campaign direction from your `marketing` profile and escalates sponsorship, legal, rights, and reputation questions to your Executive or Chief of Staff profile.

## Install

**Prerequisite:** Hermes 0.21.5 or newer. That is the version this release was tested on.

```bash
hermes profile install github.com/takiw3/hermes-social-media-agent --alias
```

Hermes shows you the manifest and asks you to confirm.

That one command installs the profile and its 41 skills. It does not install Node.js, FFmpeg, a browser, the HyperFrames CLI, or any npm package. It downloads no browser, speech model, font, or media. It signs in to nothing, copies no credentials from another profile, configures no model, starts no gateway, starts no onboarding, starts no server or render, schedules nothing, gives the profile no authority over another profile, and touches no social account. Installation was tested with all network access denied.

### Trusted automation only

```bash
hermes profile install github.com/takiw3/hermes-social-media-agent --alias --yes
```

`--yes` skips the manifest preview. Use it only in automation where you already trust this exact repository and revision. It is not the safer default.

### Model setup

The profile ships no model, provider, or credential. Configure one the way you did for your main Hermes install:

```bash
hermes -p social-media model
```

**Model-provider data disclosure:** whatever the agent reads to do a task, including your scripts, transcripts, pasted analytics, and comment text, is sent to the model provider you choose. Check that provider's data terms.

## Set up video rendering

Installing the profile and setting up rendering are two separate steps. Until you do the second, the profile runs in `offline` mode, reports the video engine as `not configured`, and does everything except render.

You run setup yourself, in your own terminal. The agent cannot: its configuration denies it the `setup` command, and the launcher refuses a download that is not approved at an interactive prompt.

**System requirements you install yourself:** Node.js 22 or newer with npm, and FFmpeg. About 235 MB of disk for the CLI, about 190 MB for headless Chrome, and about 650 MB more if you want local transcription.

```bash
HF="python3 $HOME/.hermes/profiles/social-media/skills/integrations/social-hyperframes/scripts/hf.py"

$HF setup --plan                              # list every download; changes nothing
$HF setup --workspace ~/Videos/social-media   # approve a dedicated folder
$HF setup --install-cli                       # pinned CLI, from a lockfile
$HF setup --download-browser                  # or: --use-browser /path/to/chrome-headless-shell
$HF setup --allow-host cdn.jsdelivr.net       # the host compositions load GSAP from
$HF doctor                                    # should report: toolchain verified
```

### Every post-install download

| Item | Source | Size | License |
| --- | --- | --- | --- |
| HyperFrames CLI `hyperframes@0.8.138` and its dependencies (171 packages in the lockfile) | registry.npmjs.org, with `npm ci --ignore-scripts` | about 235 MB on disk | Apache-2.0 for HyperFrames (Copyright 2026 HeyGen, Inc.); each dependency under its own license |
| Headless Chrome (`chrome-headless-shell`, the build the CLI pins) | Chrome for Testing, downloaded by the pinned CLI | about 190 MB on disk | Chromium open-source licenses |
| Parakeet speech model, optional, for local transcription | Hugging Face, downloaded by the pinned CLI | about 650 MB | CC-BY-4.0 (NVIDIA) |
| GSAP animation library, fetched by the renderer at render time | cdn.jsdelivr.net | one script file | GSAP Standard License (Webflow). Not open source. |

Each download asks for your approval and is recorded with its source, size, and license. Sizes were measured on macOS arm64. Full walkthrough: [docs/hyperframes-setup.md](docs/hyperframes-setup.md).

### Workspace and the read-only footage rule

The workspace is the one folder video work happens in. The launcher refuses a home folder, a filesystem root, or the profile folder. Inside it:

- `footage/` holds your originals. They are read-only. The agent registers each one's checksum, works on a copy inside the project, and never edits, moves, renames, or deletes an original. A changed original blocks the final render.
- `projects/<name>/` holds one HyperFrames project per video, with its `renders/`, `receipts/`, and `asset-rights-register.yaml`.

### Telemetry and update checks

The HyperFrames CLI has anonymous telemetry, an update check, a self-update, and a skill refresh. The launcher turns all four off on every call by setting `HYPERFRAMES_NO_TELEMETRY=1`, `DO_NOT_TRACK=1`, `HYPERFRAMES_NO_UPDATE_CHECK=1`, `HYPERFRAMES_NO_AUTO_INSTALL=1`, and `HYPERFRAMES_SKIP_SKILLS=1`. Each switch was verified against the tagged CLI source. Hermes has no configuration key that sets environment variables for a local terminal, so the launcher sets them.

### Optional providers

Voice, music, image, and avatar providers are all off, and this release has no switch to turn them on. The launcher removes provider keys from the CLI's environment and refuses the commands that call them. For reference, upstream's voice providers would send your script text off the machine, and its music and image providers would send a text prompt.

## Use it

### First run

```bash
hermes -p social-media chat
```

With `--alias`, `social-media chat` does the same.

Onboarding starts in that first conversation, not at install. The agent explains the short setup, asks one question at a time, never repeats a question you answered, and lets you skip, correct, pause, resume, or hand over documents. It asks before reading footage or data, summarizes at the end, and saves only after you confirm. Details: [docs/creator-onboarding.md](docs/creator-onboarding.md).

### Things to ask it

- Turn this week's client questions into ten ranked video ideas.
- Write a 45-second script in my voice with five hook options.
- Build a filming brief I can shoot alone in one hour.
- Add captions to this talking-head clip in my caption style and render it vertical.
- Package this interview clip with lower-thirds and two data callouts.
- Make a ten-second animated stat card for this number.
- Review this draft and give me the top three fixes.
- Analyze last month's export and tell me what to stop making.
- Design a clean test for two hook styles.
- Repurpose this long-form video into five short pieces.
- Check this sponsored script for disclosure and claim problems.
- Prepare a redacted handoff to Marketing on the objections showing up in comments.

Worked examples with synthetic data are in [examples/](examples/).

## What it can do

- Interview you and build a creator profile, visual identity, and pillars.
- Research your audience from your own notes and from bounded public pages.
- Produce ranked idea cards, hooks with named mechanisms, and speak-ready scripts with separate spoken, on-screen, visual, and edit tracks.
- Write filming briefs and edit plans.
- Render video locally, draft first, and write a receipt with the file's path, duration, resolution, frame rate, size, and SHA-256.
- Review a render by looking at frames.
- Write a packaging sheet per platform.
- Normalize an analytics export and analyze it with stated definitions, windows, samples, and limits.
- Design one-variable experiments.
- Score your drafts on a fixed scorecard, give three fixes at most, and set one practice goal a week.
- Create redacted Kanban handoffs.

## What it cannot verify

It says so when it does not know. It never guesses:

- A metric, a benchmark, a "good" threshold, or a best posting time.
- A trend, or how any platform's system ranks content.
- Your voice, a price, an offer, or a client result.
- A license status.
- Whether a video rendered correctly, without looking at frames.
- Whether a video was posted. Only you can tell it.
- Whether a video performed, or why, without your data.
- Growth. It forecasts no followers, views, reach, or revenue.

## Platforms and formats

In scope: Instagram, TikTok, YouTube (Shorts and long-form), LinkedIn, X, and Facebook. You choose which apply during onboarding.

Every spec and policy the agent may state lives in one dated file, [platform-facts.yaml](skills/social-media-core/platform-packaging/references/platform-facts.yaml), with its official URL and the date it was read. A fact that is not verified is reported as unverified.

| Platform | Status on 2026-10-06 |
| --- | --- |
| YouTube | Verified: Shorts definition and resolution, upload encoding, how views are counted, paid promotion disclosure, AI content disclosure |
| Instagram | Verified: Reels specs, insight definitions, branded content. Not verified: AI label conditions, caption limits, safe zones |
| Facebook | Verified: Reels specs, branded content. Not verified: metric definitions, AI label, safe zones |
| TikTok | Verified: video length, content disclosure setting, branded content policy, AI content labeling. Not verified: file specs, metric definitions, safe zones |
| LinkedIn | Verified: video file requirements, brand partnership label. Not verified: metric definitions, AI label |
| X | Not verified. X's help pages refused every automated read. The official URLs are recorded for you to read. |

No official numeric safe-zone figure is recorded for any platform. Safe margins are yours, confirmed from screenshots of your own posts.

Tested canvases: 9:16 (1080 by 1920) and 16:9 (1920 by 1080). 4:5 and 1:1 are inside verified aspect ranges and were not rendered in a test.

## Video workflows

Video is rendered by [HyperFrames](https://github.com/heygen-com/hyperframes) by HeyGen, which renders video from HTML compositions through headless Chrome and FFmpeg.

"Rendered and inspected" below means a composition was rendered from an installed temporary profile through the pinned launcher and its frames were checked by pixel. It does not mean an exit code was zero.

| Path | Status |
| --- | --- |
| Captions over an existing talking-head clip, 9:16, footage untouched | rendered and inspected |
| Designed overlays on an existing clip, 9:16: lower-third and data callout | rendered and inspected |
| Short unnarrated motion graphic (animated stat card) | rendered and inspected |
| 16:9 composition | rendered and inspected |
| Local lint, check, snapshot, preview, and render | tested |
| Upstream `general-video` and `motion-graphics` workflows | loaded only. The renders above follow the same core contract and were not produced by running these workflows end to end. |
| Upstream `talking-head-recut` workflow | loaded only |
| Upstream `embedded-captions` workflow (captions composited behind the subject) | loaded only. Its matting step needs extra downloads this release does not automate. |
| Upstream `faceless-explainer` workflow | loaded only. It needs narration from a voice provider, which is off. |

Current detail: [workflow-status.md](skills/integrations/social-hyperframes/references/workflow-status.md).

### Unsupported video operations

Not claimed, because none was rendered in a test or because this release cannot do it:

- Cutting, trimming, reordering, retiming, color grading, or reframing source footage
- Multi-camera editing or multi-shot caption embedding
- Posting, scheduling, or uploading to any platform
- Pulling analytics from any platform
- Downloading other people's videos
- Voice cloning or avatar generation
- Editing inside CapCut, Premiere, DaVinci Resolve, or Final Cut
- Live streaming
- Thumbnail image generation
- Cloud, Lambda, or Cloud Run rendering

A composition file is not a rendered video. A draft render is not a final render. A rendered file is not a posted video. A posted video is not a performing video.

## HyperFrames version and provenance

| Item | Value |
| --- | --- |
| Upstream | https://github.com/heygen-com/hyperframes |
| Release | `v0.8.138`, published 2026-10-06 |
| Commit | `0ca28db4f8671a2e2262594e03c566222d695920` |
| npm | `hyperframes@0.8.138` |
| License | Apache-2.0, Copyright 2026 HeyGen, Inc. |
| Integration | Option B: a derivative with recorded patches |

**Bundled (15):** `hyperframes`, `hyperframes-core`, `hyperframes-animation`, `hyperframes-keyframes`, `hyperframes-creative`, `hyperframes-cli`, `hyperframes-audio`, `hyperframes-registry`, `hyperframes-studio`, `media-use`, `talking-head-recut`, `embedded-captions`, `motion-graphics`, `faceless-explainer`, `general-video`.

**Not bundled:** `pr-to-video`, `remotion-to-hyperframes`, `slideshow`, `figma`, `product-launch-video`, `music-to-video`. When a task needs one, the agent says it is not bundled and offers the closest bundled path. It does not download it.

The upstream skills are not installed unchanged. Unchanged, they tell an agent to run an unpinned upgrade, to update themselves before each workflow, to send a feedback report after each render, and they document publish and cloud rendering as normal commands. The repository keeps an exact upstream copy for audit and generates a patched derivative from it. 87 of 605 skill files are modified, each marked as modified, and CI rebuilds the derivative to prove no unrecorded change exists. Two upstream files are not shipped for license reasons. Full account: [docs/hyperframes-integration.md](docs/hyperframes-integration.md).

**Do not install `official/creative/hyperframes` into this profile.** It has the same name as the bundled router. On Hermes 0.21.5, with both installed, loading `hyperframes` by name fails as ambiguous. A deny rule blocks the agent from installing it.

## Permission model

**Default mode: `draft_and_render`**, once the toolchain is verified. Before that, `offline`.

**Default external-action policy: no external writes.**

**There is no publishing mode, and no hard action gate exists for one.** Hermes instruction text is not a technical gate, and no deny list can name every route to a social platform. So this release ships no way to post, schedule, comment, or message, approved or otherwise. When you ask it to post, it gives you the packaging sheet and you post by hand. Do not give this profile credentials or tools for your social accounts.

Enforced in code, by the launcher and by `config.yaml` deny rules that hold even under yolo:

- One pinned CLI version, installed from a lockfile. No `npx`, no global binary, no latest.
- No skill self-update, upgrade, telemetry, or feedback.
- No cloud render, Lambda, Cloud Run, publish, or sign-in.
- No provider credentials passed to the CLI.
- Every launcher path inside your approved workspace.
- Draft before final. A license record for every asset before final. Owner-approved render-time hosts only.
- Setup and every download are yours to run.
- Memory and skill changes staged for your approval.

Enforced by instruction only, which means it depends on the model following its rules: not reaching a social platform by some route the deny rules do not name, writing only inside the workspace with tools other than the launcher, evidence labeling, one question at a time, and keeping audience data out of Kanban.

No cron jobs ship. Weekly review, analytics intake, and trend research run only when you ask. Recurring work is a separate setup you would do yourself.

Full detail: [docs/permissions-and-security.md](docs/permissions-and-security.md).

## Working with the rest of your agent team

| Profile | Owns |
| --- | --- |
| Executive or Chief of Staff | Business priorities, brand risk, budget, sponsorship and partnership decisions, cross-functional coordination |
| `marketing` | Marketing strategy, positioning, campaigns, email, funnels, website copy, offer messaging |
| `ads`, when installed | Paid media |
| `customer-support`, when installed | Customer inquiries |
| `social-media` | Organic social |

A distribution cannot change another profile during installation, and this one does not. It confirms the exact installed profile IDs with you before assigning anything.

### Chief-of-Staff and Kanban usage

```bash
hermes kanban create "Write a 45-second Reels script on job costing" --assignee social-media
```

Every task returns a structured result with a status of `complete`, `needs_input`, `blocked`, `escalated`, or `approval_required`. Task and result shapes: [docs/team-integration.md](docs/team-integration.md).

### Handoffs to Marketing, Ads, and Support

```bash
hermes kanban create "Objection showing up in organic comments" --assignee marketing --body-file handoff.yaml
```

The agent asks before creating a task. Handoffs carry counts and paraphrased wording only. Raw comment or DM exports, audience handles and contact details, raw analytics exports, sponsor contracts and rates, unconsented stories, and footage of identifiable people without consent status never go into Kanban.

### The overlap with the marketing profile

The `marketing` profile may already ship skills for social scripts, calendars, carousels, and social performance. When you run both, use this routing rule:

- Organic social ideation, scripting, video production, performance analysis, and coaching go to `social-media`.
- Campaign-level messaging and cross-channel planning stay with `marketing`.

Apply the rule in your Executive profile's routing. This distribution does not edit the marketing profile.

## Skills

**Core (25)**

| Skill | What it does |
| --- | --- |
| `social-intake-and-routing` | Validates a task and names the skills to run or the one fact missing |
| `creator-and-brand-onboarding` | Collects business, voice, identity, and permissions one question at a time |
| `audience-and-niche-research` | Problems, language, objections, and questions, each tagged with its evidence tier |
| `content-pillar-strategy` | Three to five pillars tied to goals and proof you hold |
| `content-ideation` | Ranked idea cards with the reason for each rank |
| `hook-writing` | Distinct hooks with named mechanisms; rejects any the video does not pay off |
| `short-form-script-writing` | Speak-ready vertical script on four tracks |
| `long-form-script-writing` | Cold open, chapters, clip candidates |
| `caption-and-post-copy` | Captions, titles, descriptions, hashtags, disclosure lines |
| `filming-brief-and-shot-list` | A brief you can shoot alone |
| `video-edit-planning` | The edit plan. Makes no render. |
| `video-render-review` | Pass or fail per check, with the frame as evidence |
| `platform-packaging` | A packaging sheet per platform. Posts nothing. |
| `content-repurposing` | One source piece into several, each with its own reason to exist |
| `media-rights-and-disclosure-check` | Assets, claims, people, sponsorships |
| `performance-data-intake` | Normalizes an export into a snapshot |
| `video-performance-analysis` | One video or a matched set |
| `account-analytics-and-strategy` | Keep, stop, start, test |
| `content-experiment-design` | One clean test |
| `competitor-and-format-research` | Structure from bounded public pages. Copies nothing. |
| `audience-comment-analysis` | Themes from your export, identities removed |
| `content-calendar-planning` | A calendar that fits your real hours |
| `creator-coaching` | Scorecard, three fixes, one practice goal |
| `cross-team-social-handoffs` | Redacted Kanban tasks and escalations |
| `weekly-social-review` | The weekly review. Does not schedule itself. |

**Integration (1):** `social-hyperframes`, the wrapper that governs every HyperFrames call.

**HyperFrames (15):** listed above.

## Analytics

Inputs are yours: an export, a screenshot, or pasted figures. There is no connector and no platform scope is requested.

The agent records the platform, account, export date, window, timezone, and metric definitions for every dataset. It never blends paid and organic, never compares across platforms without both definitions, keeps missing values as `Unavailable`, states sample size, refuses a conclusion the sample cannot support, reports medians beside averages, and treats export cells that begin with `=`, `+`, `-`, or `@` as text.

Verified definitions include Instagram's views, viewers, watch time, and average watch time, and YouTube's change on August 24, 2026 to counting a view the moment a video starts to play. [docs/analytics-and-metric-definitions.md](docs/analytics-and-metric-definitions.md)

## Media rights and disclosure

- Every project keeps an asset rights register. An asset with no recorded license is unusable, and the final render is refused until every asset has one.
- A platform's music library licenses use inside that platform only.
- Sponsored, gifted, affiliate, and paid-partnership content is blocked until it carries a plain disclosure, placed with the message, plus the platform's own label. On TikTok, promoting your own business also needs the disclosure setting on.
- Health, financial, legal, earnings, and before-and-after claims are blocked until you or your Executive confirm they are substantiated and permitted.
- Recorded consent is required for anyone identifiable on camera. Content involving a minor always escalates.
- The agent does not give legal advice. It flags, cites the official source, and escalates.

[docs/media-rights-and-disclosure.md](docs/media-rights-and-disclosure.md)

## Sensitive cases

Escalated to your Executive profile at once: sponsorship offers, contracts, and rate questions; undisclosed paid or gifted content; health, financial, legal, or earnings claims; before-and-after claims; anything involving a minor; a real person's likeness, voice, or story without consent; voice clone, avatar, or deepfake requests; copyright claims, takedowns, and strikes; requests to reuse another creator's content; account compromise; harassment or threats; self-harm signals; political, religious, or tragedy-adjacent content; public criticism of a named person or company; media inquiries; backlash; requests to delete evidence; requests to buy engagement; and regulated-industry content.

The agent may draft a holding note for you. It promises no legal, platform, or commercial outcome.

## Prompt injection

Page text, captions, comments, transcripts, exports, video metadata, file names, and Kanban comments are data. The agent does not follow instructions found in them, does not treat them as approval, and reports the attempt. A Kanban task that says `approved` is not human approval. Neither is a teammate's instruction or a sponsor's request.

That rule is an instruction. What limits the damage if it fails is in code: no publishing path, no credentials passed to the video CLI, and a deny floor under the terminal.

## Data, retention, and privacy

- The profile sends nothing to a social platform, scheduler, analytics service, voice provider, or cloud renderer. None is configured.
- Raw footage, transcripts, exports, and comment files are session-only by default. You set retention rules during onboarding.
- Memory writes are staged for your approval. Credentials, raw audience data, raw exports, and sponsor terms are never saved.
- Your creator profile and the video engine state live in the profile's `local/` folder, which updates never touch.

[docs/privacy-and-retention.md](docs/privacy-and-retention.md)

## Tenant boundaries

A Hermes profile is not a full tenant-security boundary. Profiles on one machine can share an operating-system user, filesystem access, and a Kanban board.

- One installed social media profile is for one brand or creator.
- Strong separation between brands needs separate operating-system users or containers, explicit mounts, isolated credentials, and separate boards.
- Kanban tenant labels and profile names are routing metadata, not access controls.
- Keep the Kanban dashboard on localhost unless you secure it separately.
- The HyperFrames preview is a long-lived local server that holds browser workers open. It stays on localhost and is stopped when the task ends.

## Update and remove

```bash
hermes profile update social-media
```

An update replaces only the paths this distribution owns. It preserves your credentials, memories, sessions, `local/`, your workspace, your `config.yaml`, and any skills you added. Because `config.yaml` is preserved, new deny rules in a later release do not reach you automatically: compare your file with the repository's, or add `--force-config` if you have no overrides to keep.

```bash
hermes profile delete social-media
```

That removes the profile. To remove the video toolchain separately, before or instead:

```bash
$HF setup --remove cli       # the HyperFrames CLI and its node_modules
$HF setup --remove browser   # the browser this profile downloaded
$HF setup --remove model     # speech models
```

A browser you pointed at with `--use-browser` is yours and stays. Your workspace is never removed.

## Troubleshooting

| Symptom | What to do |
| --- | --- |
| `video engine: not configured` | Run `$HF doctor`. It names each missing piece and the command that fixes it. |
| Node.js too old | Upgrade Node.js to 22 or newer yourself. Nothing else is changed. |
| `approval required`, naming a host | The composition loads from a host you have not approved. Approve it with `$HF setup --allow-host <host>` or remove the reference. |
| Final render refused | Read the message: no draft receipt, an asset with no license record, or a changed original. |
| Slow render | Normal on modest hardware. A 6-second 1080 by 1920 draft took about 9 seconds on an Apple M2 in testing, and time grows with length and quality. |
| Render fails offline | Compositions that load GSAP from a CDN need network. |
| Orphaned preview process | Run `$HF preview-stop`. It stops every preview, ends leftover processes that belong to this profile, and lists what remains. |
| A command is `BLOCKED` by a deny rule | That is the profile working. If an output file name tripped a rule, rename the file. |
| `hyperframes` skill is ambiguous | You installed `official/creative/hyperframes`. Remove `skills/creative/hyperframes` from the profile. |

## Test status

<!-- test-status:start -->
Recorded on 2026-10-06, macOS 26.6.2 (arm64, Apple M2), Node v22.23.1, FFmpeg 8.1, Python 3.10.9, against Hermes 0.21.5 (tag v2026.9.24, commit f97608f) and `hyperframes@0.8.138`.

| Suite | Result |
| --- | --- |
| Repository validation (`scripts/validate.py --history`) | pending |
| Vendor provenance and derivative rebuild (`scripts/hyperframes_vendor.py verify`) | pending |
| Upstream contract (`scripts/check_upstream_contract.py`) | pending |
| Eval fixtures (`scripts/run_evals.py`) | pending |
| Installation tests, in a temporary profile | 75 pass, 0 fail, 2 not run |
| HyperFrames integration tests, from an installed temporary profile, with real renders | 108 pass, 0 fail, 0 not run |
| Install from the published GitHub URL | not run. Runs after publication. |
| Model-backed behavior evaluation | not run. No model credentials in the test environment. |
| End-to-end Kanban test with live Executive, Marketing, and Social Media profiles | not run. Needs model access and a dispatcher. |
| Linux and Windows | not run. Tested on macOS arm64 only. CI runs the no-render suites on Ubuntu. |
| Speech model download and local transcription | not run. The refusal path without a model is tested. |
| Browser download through `setup --download-browser` | not run. Renders used a headless Chrome already on the machine, recorded with `--use-browser`. |
<!-- test-status:end -->

Full record, including the commands and the environment: [docs/evaluations.md](docs/evaluations.md).

## Contributing and security

Contribution rules are in [CONTRIBUTING.md](CONTRIBUTING.md). Report a vulnerability privately through the repository's Security tab; see [SECURITY.md](SECURITY.md).

## Licensing

Original work in this repository is under the MIT License, Copyright (c) 2026 TakiGPT AI Inc. See [LICENSE](LICENSE).

The HyperFrames skills under `skills/hyperframes-video/` and `vendor/upstream/hyperframes/` are under the Apache License 2.0, Copyright 2026 HeyGen, Inc., and are not relicensed. Fonts and sound effects inside them carry their own licenses. GSAP, which most compositions load at render time, is under the GSAP Standard License and is not open source. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

This project is not affiliated with or endorsed by HeyGen or Nous Research.

## Agentic AI Academy

Learn how to build your full AI workforce inside the Agentic AI Academy for $97/month: https://www.skool.com/agenticaiacademy/about
