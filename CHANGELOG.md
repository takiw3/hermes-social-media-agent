# Changelog

All notable changes to this profile are recorded here. The project follows semantic versioning.

## 1.0.0 - 2026-10-06

First release. Release status: **draft-and-render release**.

### Added

- Native Hermes Profile Distribution for a `social-media` profile, tested on Hermes 0.21.5 (tag `v2026.9.24`).
- `SOUL.md`: role, team boundaries, evidence hierarchy, content states, video statuses, escalation shape, task and result contracts, coaching method.
- 25 core skills covering intake, onboarding, research, pillars, ideation, hooks, short-form and long-form scripts, post copy, filming briefs, edit plans, render review, packaging, repurposing, rights and disclosure, analytics intake, video and account analysis, experiments, competitor research, comment analysis, calendars, coaching, handoffs, and the weekly review.
- `social-hyperframes` wrapper skill and a pinned launcher (`hf.py`).
- 15 HeyGen HyperFrames skills, derived from `v0.8.138` (commit `0ca28db`) with recorded patches, under Apache-2.0.
- A toolchain lockfile pinning `hyperframes@0.8.138` and 170 further packages with integrity hashes.
- 20 templates, 11 documents, 78 behavior evaluation fixtures, 7 synthetic examples.
- Validation, vendoring, installation, and integration test tooling, and a CI workflow with actions pinned to commit SHAs.
- A dated platform facts file covering YouTube, Instagram, Facebook, TikTok, LinkedIn, and FTC endorsement guidance.

### Security

- `config.yaml` deny rules block every route around the launcher, the launcher's owner-only `setup` command, known media download tools, and the colliding Hermes optional skill.
- The launcher refuses cloud render, Lambda, Cloud Run, publish, sign-in, feedback, upgrade, and skill update, removes credential-looking environment variables, and confines paths to the owner-approved workspace.

### Not included

- No publishing, scheduling, commenting, or messaging mode. No hard action gate exists that covers every publishing path.
- No analytics connector. Analysis uses owner-provided exports, screenshots, and pasted figures.
- No voice, avatar, music, or image generation.
- Two upstream files are not shipped for license reasons: `Virgil.woff2` and a vendored `gsap.min.js`.

### Known limits

- The upstream `embedded-captions`, `talking-head-recut`, `faceless-explainer`, `motion-graphics`, and `general-video` workflows load but were not run end to end. The renders that were tested follow the core composition contract.
- X specifications and policies are not verified. X's help pages refused automated reads.
- Model-backed behavior evaluations and an end-to-end Kanban test were not run.
