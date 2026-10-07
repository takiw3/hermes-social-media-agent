# Hermes Social Media Agent

A persistent [Hermes](https://hermes-agent.nousresearch.com) profile named
`social-media`: a head of content, working editor, and blunt coach that works
underneath Jarvis, your Hermes chief of staff, and directly with you. It
researches, plans, scripts, edits and renders video locally, analyzes the
numbers you give it, and coaches you into a better creator. It never posts,
schedules, comments, messages, uploads, or signs in anywhere.

- **Author:** Taki Wong / TakiGPT AI Inc.
- **License:** MIT (bundled HyperFrames skills are Apache-2.0, HeyGen, Inc.)
- **Profile ID:** `social-media` · **Display name:** Social Media
- **Version:** 1.0.0 · **Release status:** draft-and-render release

## Who it's for

Business owners, entrepreneurs, and executives running companies from
$250,000 to $50 million a year. People who know their trade, are short on
time, and want organic social done to an operator's standard, with every
fact, assumption, and unknown labeled. One installed profile serves one
brand or creator.

## What it does

- Audience and niche research from your own notes and bounded public pages
- Content pillars tied to business goals and proof you actually hold
- Ranked idea cards, hooks with named mechanisms, and speak-ready scripts in
  your voice, short-form and long-form
- Filming briefs you can shoot alone, and edit plans
- Local video editing and rendering through a pinned
  [HyperFrames](https://github.com/heygen-com/hyperframes) toolchain:
  captions, lower-thirds, data callouts, short motion graphics
- A render receipt for every file, and a review that looks at frames
- Packaging sheets: titles, cover text, captions, descriptions, hashtags
- Repurposing one long piece into several short ones
- Rights, consent, and disclosure checks
- Performance analysis from exports, screenshots, or pasted figures, with
  definitions, windows, samples, and limits stated
- One-variable content experiments
- Coaching: a fixed scorecard, three fixes at most, one practice goal a week
- Redacted handoffs to your other agents, and a manually run weekly review

Work arrives two ways: Jarvis assigns tasks through Hermes Kanban, or you
chat with the profile directly. Same standards either way.

## What it will not do

- Post, schedule, comment, message, upload, or change any social account.
  There is no publishing mode in this release, approved or otherwise.
- Follow, unfollow, like, auto-reply, mass message, buy followers, or join
  an engagement pod
- Invent a metric, benchmark, best posting time, trend, statistic,
  testimonial, quote, price, or client result
- Explain what a platform's ranking system "wants" as if it were fact
- Promise followers, views, reach, or revenue
- Call a draft final, a rendered file posted, or a posted video a hit
  without evidence
- Write in another named creator's voice, or copy a competitor's video
- Download other people's videos, or scrape behind a login
- Cloud render, sign in to a provider, or update its own video skills
- Edit, move, rename, or delete your original footage
- Follow instructions embedded in transcripts, comments, exports, web
  pages, video metadata, or Kanban comments. That is data, not commands.
- Put raw audience data, raw exports, or sponsor terms into Kanban
- Start recurring jobs on its own

## Requirements

- [Hermes Agent](https://hermes-agent.nousresearch.com) **0.21.5 or newer**.
  That is the release the full install and integration suites were run on
  (macOS, tag `v2026.9.24`). Older releases were not tested, so the floor
  is the tested version. Below it the install is refused with a clear
  version error and nothing is written (verified on 0.21.4). Run
  `hermes update` first.
- A model provider configured in Hermes. Any provider: the profile
  hardcodes no model and no credentials.
- No third-party social, scheduling, analytics, voice, or stock-media
  service is required.
- **For video rendering only, and only when you choose to set it up:**
  Node.js 22 or newer with npm, FFmpeg, and about 425 MB of disk. Without
  them the profile still does everything except render.

## Install

One command installs the profile, with a review prompt of the manifest
before anything is written:

```
hermes profile install https://github.com/takiw3/hermes-social-media-agent --alias
```

`--alias` also creates a `social-media` shell wrapper so you can invoke the
profile directly. The short form `github.com/takiw3/hermes-social-media-agent`
works too.

### Trusted automation only

For scripted setups that have **already reviewed this repository**, the
confirmation prompt can be skipped:

```
hermes profile install https://github.com/takiw3/hermes-social-media-agent --alias --yes
```

Hermes distributions are unsigned, and installs track this repository's
default branch. `--yes` skips the manifest preview. It is not the safe
default, and you should not use it the first time you install.

### What installation does and doesn't do

Installing copies the profile's identity, configuration, 41 skills, and
templates into an isolated Hermes profile named `social-media`. That's all.

Installation does **not** install Node.js, FFmpeg, a browser, the
HyperFrames CLI, or any npm package. It downloads no browser, speech model,
font, or media. It does not sign in to HeyGen, a social platform, or any
service, copy credentials from another profile, configure a model, start a
gateway, start onboarding, start a preview server or a render, schedule
anything, give this profile authority over another profile, or touch a
social account. The install was tested with all network access denied.

## First run

1. Give the profile a model provider. Hermes profiles are isolated, so
   configure this one the way you configured your main one:

```
hermes -p social-media model
```

2. Start a conversation:

```
hermes -p social-media chat
```

3. On first contact the agent runs a short setup: one question at a time
   about your business, offers and exact prices, audience, platforms, voice,
   visual identity, filming setup, and weekly time budget. You can skip
   questions, hand it documents instead, or pause and resume. It asks
   consent before reading footage, transcripts, or exports, summarizes what
   it learned, and saves only after you confirm. To start it by hand, say
   "set up my creator profile". Your context lives in the profile's
   user-owned storage (`local/` and memory) and survives updates.

Whatever the agent reads to do a task, including scripts, transcripts,
pasted analytics, and comment text, goes to the model provider you chose.
Check that provider's data terms.

## Set up video rendering

This is a separate step from installing, and it is yours. Until you do it
the profile runs in `offline` mode and reports the video engine as
`not configured`. The agent cannot run it for you: its configuration denies
it the `setup` command, and the launcher refuses a download that is not
approved at an interactive prompt.

```
HF="python3 $HOME/.hermes/profiles/social-media/skills/integrations/social-hyperframes/scripts/hf.py"

$HF setup --plan                              # list every download; changes nothing
$HF setup --workspace ~/Videos/social-media   # approve a dedicated folder
$HF setup --install-cli                       # pinned CLI, from a lockfile
$HF setup --download-browser                  # or: --use-browser /path/to/chrome-headless-shell
$HF setup --allow-host cdn.jsdelivr.net       # the host compositions load GSAP from
$HF doctor                                    # should report: toolchain verified
```

Every download, each approved by you and recorded with its source, size,
and license:

| Item | Source | Size | License |
| --- | --- | --- | --- |
| HyperFrames CLI `hyperframes@0.8.138` and its dependencies (171 packages in the lockfile) | registry.npmjs.org, with `npm ci --ignore-scripts` | about 235 MB on disk | Apache-2.0 for HyperFrames (Copyright 2026 HeyGen, Inc.); each dependency under its own license |
| Headless Chrome (`chrome-headless-shell`, the build the CLI pins) | Chrome for Testing, downloaded by the pinned CLI | about 190 MB on disk | Chromium open-source licenses |
| Parakeet speech model, optional, for local transcription | Hugging Face, downloaded by the pinned CLI | about 650 MB | CC-BY-4.0 (NVIDIA) |
| GSAP animation library, fetched by the renderer at render time | cdn.jsdelivr.net | one script file | GSAP Standard License (Webflow). Not open source. |

The workspace is the one folder video work happens in. `footage/` holds
your originals, which are read-only: the agent registers each one's
checksum, works on a copy inside the project, and a changed original blocks
the final render. `projects/<name>/` holds one project per video.

The HyperFrames CLI has telemetry, an update check, a self-update, and a
skill refresh. The launcher turns all four off on every call with
`HYPERFRAMES_NO_TELEMETRY=1`, `DO_NOT_TRACK=1`,
`HYPERFRAMES_NO_UPDATE_CHECK=1`, `HYPERFRAMES_NO_AUTO_INSTALL=1`, and
`HYPERFRAMES_SKIP_SKILLS=1`, each verified against the tagged CLI source.

Full walkthrough: [docs/hyperframes-setup.md](docs/hyperframes-setup.md).

## The team

This profile is one specialist on a team of named Hermes profiles:

| Profile | Owns |
| --- | --- |
| **Jarvis** | Chief of staff. Assigns work, collects results, holds priorities, brand risk, budget, and sponsorship decisions. |
| **Social Media** | This profile. Organic social: research, pillars, ideas, hooks, scripts, filming briefs, edit plans, local video rendering, packaging, analysis, experiments, coaching. |
| **Marketing** | Marketing strategy, positioning, campaigns, email, funnels, website copy, offer messaging. |
| **Ads** | Paid media. |
| **Sales** | One-to-one prospect outreach, pipeline, deals. |
| **Support** | Customer inquiries. |
| **Dev** | Implementation. Site changes, tracking, integrations. |

Each teammate is its own distribution and is installed separately. Social
Media works fine alone. It confirms the exact installed profile IDs with
you during setup, including your chief of staff's if it is not named
Jarvis, and never guesses a profile name.

The seams it respects: it takes campaign direction from Marketing and
returns organic content that carries it. It hands Ads organic posts that
performed, with measured evidence and rights status, and never touches paid
media. It takes aggregated, anonymized questions from Support and never
uses customer data for targeting. It escalates sponsorship, legal, rights,
and reputation questions to Jarvis.

**The overlap with Marketing.** The marketing profile ships its own skills
for social scripts, calendars, carousels, and social performance. When you
run both, use this rule: organic social ideation, scripting, video
production, performance analysis, and coaching go to `social-media`.
Campaign-level messaging and cross-channel planning stay with `marketing`.
Apply it in Jarvis's routing. This distribution does not edit the marketing
profile, and a task that could belong to either is handed back to Jarvis to
route.

## Working with Jarvis

Jarvis assigns social work through Hermes Kanban:

```
hermes kanban create "Write a 45-second Reels script on job costing" --assignee social-media
```

The profile's routing description tells the Kanban orchestrator what
belongs here. Tasks are picked up when a Hermes gateway is running.

Results come back in a structured handoff: status, content state,
deliverables, sources, measured facts versus owner facts versus inferences
versus unknowns, render receipts, rights and disclosure status, checks
performed, approvals still required, and the next action. If a task is
missing one material fact, the agent blocks it with exactly one question.
Shapes are in [docs/team-integration.md](docs/team-integration.md).

A privacy-safe handoff the other way, which the agent asks you about before
it creates:

```
hermes kanban create "Objection showing up in organic comments" --assignee marketing --body-file handoff.yaml
```

Handoffs carry counts and paraphrased wording only. Raw comment or DM
exports, audience handles and contact details, raw analytics exports,
sponsor contracts and rates, unconsented stories, and footage of
identifiable people without consent status never go into Kanban.

Note: a distribution cannot modify another profile during installation.
Installing this repository sets up `social-media` only. If Jarvis keeps its
own roster of specialists, add `social-media` to it yourself.

## Example tasks

- "Turn this week's client questions into ten ranked video ideas."
- "Write a 45-second script in my voice with five hook options."
- "Build a filming brief I can shoot alone in one hour."
- "Add captions to this talking-head clip in my caption style and render it
  vertical."
- "Package this interview clip with lower-thirds and two data callouts."
- "Make a ten-second animated stat card for this number."
- "Review this draft and give me the top three fixes."
- "Analyze last month's export and tell me what to stop making."
- "Design a clean test for two hook styles."
- "Repurpose this long-form video into five short pieces."
- "Check this sponsored script for disclosure and claim problems."
- "Prepare a redacted handoff to Marketing on the objections showing up in
  comments."
- "Run the weekly social review."

Worked examples with synthetic data are in [examples/](examples/).

## Skills

25 focused skills in `skills/social-media-core/`:

| Skill | Produces |
| ----- | -------- |
| `social-intake-and-routing` | A validated task and the skills to run, or the one fact missing |
| `creator-and-brand-onboarding` | Your creator profile, one question at a time |
| `audience-and-niche-research` | Problems, language, objections, questions, each with its evidence tier |
| `content-pillar-strategy` | Three to five pillars tied to goals and proof you hold |
| `content-ideation` | Ranked idea cards with the reason for each rank |
| `hook-writing` | Distinct hooks with named mechanisms |
| `short-form-script-writing` | A speak-ready vertical script on four tracks |
| `long-form-script-writing` | Cold open, chapters, clip candidates |
| `caption-and-post-copy` | Captions, titles, descriptions, hashtags, disclosure lines |
| `filming-brief-and-shot-list` | A brief you can shoot alone |
| `video-edit-planning` | The edit plan. Makes no render. |
| `video-render-review` | Pass or fail per check, with the frame as evidence |
| `platform-packaging` | A packaging sheet per platform. Posts nothing. |
| `content-repurposing` | One source piece into several |
| `media-rights-and-disclosure-check` | Assets, claims, people, sponsorships checked |
| `performance-data-intake` | An export normalized into a snapshot |
| `video-performance-analysis` | One video or a matched set, with limits |
| `account-analytics-and-strategy` | Keep, stop, start, test |
| `content-experiment-design` | One clean test |
| `competitor-and-format-research` | Structure from bounded public pages. Copies nothing. |
| `audience-comment-analysis` | Themes from your export, identities removed |
| `content-calendar-planning` | A calendar that fits your real hours |
| `creator-coaching` | Scorecard, three fixes, one practice goal |
| `cross-team-social-handoffs` | Redacted Kanban tasks and escalations |
| `weekly-social-review` | Manual weekly review |

One integration skill in `skills/integrations/`: `social-hyperframes`, the
wrapper that governs every HyperFrames call.

15 HyperFrames skills in `skills/hyperframes-video/`: `hyperframes`,
`hyperframes-core`, `hyperframes-animation`, `hyperframes-keyframes`,
`hyperframes-creative`, `hyperframes-cli`, `hyperframes-audio`,
`hyperframes-registry`, `hyperframes-studio`, `media-use`,
`talking-head-recut`, `embedded-captions`, `motion-graphics`,
`faceless-explainer`, `general-video`.

## Video

Rendered by HyperFrames by HeyGen, which turns HTML compositions into video
through headless Chrome and FFmpeg.

| Item | Value |
| --- | --- |
| Upstream | https://github.com/heygen-com/hyperframes |
| Release | `v0.8.138`, published 2026-10-06 |
| Commit | `0ca28db4f8671a2e2262594e03c566222d695920` |
| npm | `hyperframes@0.8.138` |
| License | Apache-2.0, Copyright 2026 HeyGen, Inc. |

The upstream skills are not installed unchanged. Unchanged, they tell an
agent to run an unpinned upgrade, to update themselves before each
workflow, to send a feedback report after each render, and they document
publish and cloud rendering as normal commands. This repository keeps an
exact upstream copy for audit and generates a patched derivative from it:
87 of 605 skill files are modified, each marked as modified, and CI
rebuilds the derivative to prove no unrecorded change exists. Two upstream
files are not shipped for license reasons. Full account:
[docs/hyperframes-integration.md](docs/hyperframes-integration.md).

Not bundled: `pr-to-video`, `remotion-to-hyperframes`, `slideshow`,
`figma`, `product-launch-video`, `music-to-video`. When a task needs one,
the agent says it is not bundled and offers the closest bundled path. It
does not download it.

**What was actually rendered.** "Rendered and inspected" means rendered
from an installed temporary profile through the pinned launcher, with
frames checked by pixel. It does not mean an exit code was zero.

| Path | Status |
| --- | --- |
| Captions over an existing talking-head clip, 9:16, footage untouched | rendered and inspected |
| Designed overlays on an existing clip, 9:16: lower-third and data callout | rendered and inspected |
| Short unnarrated motion graphic (animated stat card) | rendered and inspected |
| 16:9 composition | rendered and inspected |
| Upstream `general-video`, `motion-graphics`, `talking-head-recut`, `embedded-captions`, and `faceless-explainer` workflows, run end to end | loaded only |
| 4:5 and 1:1 canvases | not tested |

**Not supported:** cutting, trimming, reordering, retiming, color grading,
or reframing source footage; multi-camera editing; multi-shot caption
embedding; posting, scheduling, or uploading; pulling analytics;
downloading other people's videos; voice cloning or avatar generation;
editing inside CapCut, Premiere, DaVinci Resolve, or Final Cut; live
streaming; thumbnail image generation; cloud, Lambda, or Cloud Run
rendering.

A composition file is not a rendered video. A draft render is not a final
render. A rendered file is not a posted video. A posted video is not a
performing video.

**Platforms.** In scope: Instagram, TikTok, YouTube (Shorts and long-form),
LinkedIn, X, and Facebook. You choose which apply during setup. Every spec
and policy the agent may state lives in one dated file,
[platform-facts.yaml](skills/social-media-core/platform-packaging/references/platform-facts.yaml),
with its official URL and the date it was read.

| Platform | Status on 2026-10-06 |
| --- | --- |
| YouTube | Verified: Shorts definition and resolution, upload encoding, how views are counted, paid promotion disclosure, AI content disclosure |
| Instagram | Verified: Reels specs, insight definitions, branded content. Not verified: AI label conditions, caption limits, safe zones |
| Facebook | Verified: Reels specs, branded content. Not verified: metric definitions, AI label, safe zones |
| TikTok | Verified: video length, content disclosure setting, branded content policy, AI content labeling. Not verified: file specs, metric definitions, safe zones |
| LinkedIn | Verified: video file requirements, brand partnership label. Not verified: metric definitions, AI label |
| X | Not verified. X's help pages refused every automated read. |

No official numeric safe-zone figure is recorded for any platform. Safe
margins are yours, confirmed from screenshots of your own posts.

**Do not install `official/creative/hyperframes` into this profile.** It
has the same name as the bundled router. On Hermes 0.21.5, with both
installed, loading `hyperframes` by name fails as ambiguous.

## Permission model

Default mode is `draft_and_render` once the video toolchain is verified,
and `offline` before that. Default external-action policy: no external
writes.

Allowed by default: read what you approve, research bounded public pages,
analyze, calculate, draft, recommend, create local deliverables, and render
locally inside your approved workspace.

There is no publishing mode, and no hard action gate exists for one.
Hermes instruction text is not a technical gate, and no deny list can name
every route to a social platform. When you ask it to post, it gives you the
packaging sheet and you post by hand. Do not give this profile credentials
or tools for your social accounts.

Enforced in code, by the launcher and by `config.yaml` deny rules that hold
even under yolo: one pinned CLI version installed from a lockfile; no skill
self-update, upgrade, telemetry, or feedback; no cloud render, publish, or
sign-in; no provider credentials passed to the CLI; every launcher path
inside your workspace; draft before final; a license record for every asset
before final; owner-approved render-time hosts only; setup and every
download yours to run; memory and skill changes staged for your approval.

Enforced by instruction only, which depends on the model following its
rules: not reaching a social platform by a route the deny rules do not
name, writing only inside the workspace with tools other than the launcher,
evidence labeling, and keeping audience data out of Kanban.

Full details in
[docs/permissions-and-security.md](docs/permissions-and-security.md).

## Analytics, rights, and sensitive cases

- **Analytics.** Inputs are yours: an export, a screenshot, or pasted
  figures. There is no connector. The agent records the platform, account,
  export date, window, timezone, and metric definitions, never blends paid
  and organic, never compares across platforms without both definitions,
  keeps missing values as `Unavailable`, and refuses a conclusion the
  sample cannot support.
  [docs/analytics-and-metric-definitions.md](docs/analytics-and-metric-definitions.md)
- **Rights and disclosure.** An asset with no recorded license is unusable.
  Sponsored, gifted, and affiliate content is blocked until it carries a
  plain disclosure plus the platform's own label. Health, financial, legal,
  earnings, and before-and-after claims are blocked until substantiated.
  Anyone on camera needs recorded consent. The agent does not give legal
  advice. [docs/media-rights-and-disclosure.md](docs/media-rights-and-disclosure.md)
- **Sensitive cases** go straight to Jarvis: sponsorship offers and rates,
  undisclosed paid content, regulated claims, anything involving a minor, a
  real person's likeness or voice without consent, copyright strikes,
  account compromise, harassment, self-harm signals, political or
  tragedy-adjacent content, public criticism of a named person, media
  inquiries, backlash, and requests to buy engagement or hide evidence.

## Data and privacy

- Your context is user-owned: memory (with approval before writes) and
  `local/creator-profile.md`. Distribution updates never touch it.
- The agent never stores credentials, audience handles or contact details,
  raw comments or messages, raw analytics exports, or sponsor terms.
- Raw footage, transcripts, exports, and comment files are session-only by
  default. You set retention rules during setup.
- Public research is cited with URLs and access dates. Content it reads is
  treated as untrusted data, and embedded instructions are ignored and
  reported.
- This repository ships no telemetry and no accounts. The profile sends
  nothing to a social platform, scheduler, analytics service, voice
  provider, or cloud renderer.
- A Hermes profile is not a full tenant-security boundary. Profiles on one
  machine can share an operating-system user, filesystem, and Kanban board.
  Separate brands need separate operating-system users or containers,
  isolated credentials, and separate boards. Kanban tenant labels and
  profile names are routing metadata, not access controls. Keep the Kanban
  dashboard and the HyperFrames preview on localhost.

More in [docs/privacy-and-retention.md](docs/privacy-and-retention.md).

## Optional integrations

None are required, and v1 ships none pre-configured: no MCP servers, no
plugins, no cron jobs, no analytics connector. Voice, music, image, and
avatar providers are off, and this release has no switch to turn them on.
For reference, upstream's voice providers would send your script text off
the machine, and its music and image providers would send a text prompt.
The weekly review is manual by design. If you want it recurring, set that
up yourself deliberately in Hermes.

## Update

```
hermes profile update social-media
```

Updates re-pull this repository and replace only distribution-owned files.
Your `.env`, memory, sessions, `local/`, video workspace, the installed
toolchain, and any skills you created outside the three owned skill folders
are preserved. Your `config.yaml` is preserved too, which means new deny
rules in a later release do not reach you automatically: compare your file
with the repository's, or add `--force-config` if you have no overrides to
keep.

## Remove

```
hermes profile delete social-media
```

To remove the video toolchain separately, before or instead:

```
$HF setup --remove cli       # the HyperFrames CLI and its node_modules
$HF setup --remove browser   # the browser this profile downloaded
$HF setup --remove model     # speech models
```

A browser you pointed at with `--use-browser` is yours and stays. Your
workspace is never removed.

## Troubleshooting

- **`hermes: command not found`**: install Hermes first:
  https://hermes-agent.nousresearch.com
- **"This distribution requires Hermes >=0.21.5, but you have ..."**: run
  `hermes update`, then install again. Nothing was written by the refused
  install.
- **Install fails with `could not read Username`**: the repository is
  private to you. Hermes clones with your `gh` login or a `GITHUB_TOKEN`.
  Run `gh auth login` and try again.
- **Profile answers but produces generic work**: setup hasn't run. Say
  "set up my creator profile" in `hermes -p social-media chat`.
- **Kanban tasks aren't routed here**: check the routing description is
  present (`hermes profile describe social-media` prints it), that your
  task names the assignee (`--assignee social-media`), and that a gateway
  is running to pick tasks up.
- **The agent refuses to post or schedule**: that's by design. It hands you
  the packaging sheet.
- **`video engine: not configured`**: run `$HF doctor`. It names each
  missing piece and the command that fixes it.
- **`approval required`, naming a host**: the composition loads from a host
  you have not approved. Approve it with `$HF setup --allow-host <host>` or
  remove the reference.
- **Final render refused**: read the message. No draft receipt, an asset
  with no license record, or a changed original.
- **Slow render**: normal on modest hardware. A 6-second 1080 by 1920 draft
  took about 9 seconds on an Apple M2 in testing, and time grows with
  length and quality.
- **Render fails offline**: compositions that load GSAP from a CDN need
  network.
- **Orphaned preview process**: run `$HF preview-stop`. It stops every
  preview, ends leftover processes that belong to this profile, and lists
  what remains.
- **A command is `BLOCKED` by a deny rule**: that is the profile working.
  If an output file name tripped a rule, rename the file.
- **`hyperframes` skill is ambiguous**: you installed
  `official/creative/hyperframes`. Remove `skills/creative/hyperframes`
  from the profile.
- **Update seems to change nothing**: `hermes profile info social-media`
  shows the installed version and source. Compare with this repository's
  `CHANGELOG.md`.

## Test status

<!-- test-status:start -->
Recorded on 2026-10-06, macOS 26.6.2 (arm64, Apple M2), Node v22.23.1, FFmpeg 8.1, Python 3.10.9, against Hermes 0.21.5 (tag v2026.9.24, commit f97608f) and `hyperframes@0.8.138`.

| Suite | Result |
| --- | --- |
| Repository validation (`scripts/validate.py --history`) | pass. 0 failed of 9,458 checks at commit f57c2c4, including the Git history secret scan |
| Vendor provenance and derivative rebuild (`scripts/hyperframes_vendor.py verify`) | pass. 731 checks passed, 0 failed |
| Upstream contract (`scripts/check_upstream_contract.py`) | pass. 10 observations re-checked, 0 changed |
| Eval fixtures (`scripts/run_evals.py`) | pass. 78 scenarios, 49 zero tolerance, 0 problems. Fixture validation only; no model was run. |
| Installation tests, in a temporary profile | 80 pass, 0 fail, 0 not run |
| HyperFrames integration tests, from an installed temporary profile, with real renders | 108 pass, 0 fail, 0 not run |
| Install from the published GitHub URL | pass. `hermes profile install github.com/takiw3/hermes-social-media-agent --alias`, confirmation prompt answered, payload byte-identical. Included in the installation tests above. |
| GitHub Actions CI | pass on GitHub Actions at commit f57c2c4 (Ubuntu, validation and no-render suites) |
| Model-backed behavior evaluation | not run. No model credentials in the test environment. |
| End-to-end Kanban test with live Executive, Marketing, and Social Media profiles | not run. Needs model access and a dispatcher. |
| Linux and Windows | not run. Tested on macOS arm64 only. CI runs the no-render suites on Ubuntu. |
| Speech model download and local transcription | not run. The refusal path without a model is tested. |
| Browser download through `setup --download-browser` | not run. Renders used a headless Chrome already on the machine, recorded with `--use-browser`. |
<!-- test-status:end -->

Full record, with commands and environment:
[docs/evaluations.md](docs/evaluations.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Validation runs with
`python3 scripts/validate.py`; isolated install tests with
`python3 tests/test_install.py`.

## Security

Report vulnerabilities, including prompt injection, a path to an external
action, a way around the pinned video toolchain, and data-handling flaws,
privately via GitHub's **Security → Report a vulnerability** on this
repository. Details in [SECURITY.md](SECURITY.md).

## License

MIT for original work. See [LICENSE](LICENSE). Copyright (c) 2026 TakiGPT
AI Inc.

The HyperFrames skills under `skills/hyperframes-video/` and
`vendor/upstream/hyperframes/` are Apache-2.0, Copyright 2026 HeyGen, Inc.,
and are not relicensed. Fonts and sound effects inside them carry their own
licenses, and GSAP, which most compositions load at render time, is under
the GSAP Standard License and is not open source. See
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). This project is not
affiliated with or endorsed by HeyGen or Nous Research.

---

Learn how to build your full AI workforce inside the Agentic AI Academy for
$97/month: https://www.skool.com/agenticaiacademy/about
