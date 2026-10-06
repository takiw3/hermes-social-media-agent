# Privacy and retention

## What the profile reads

Only what you give it or approve: your answers, documents you hand over, footage and transcripts inside the approved workspace, analytics and comment exports you provide, and bounded public pages you ask it to study. It asks before reading footage, transcripts, exports, or any audience data.

## What leaves your machine

The profile itself sends nothing to a social platform, a scheduler, an analytics service, a voice or avatar provider, or a cloud renderer. None is configured.

Two things do leave, and you should know both:

- **Your model provider.** Whatever the agent reads to do a task, including scripts, transcripts, pasted analytics, and comment text, is sent to the model provider you configured for this profile. That is how any Hermes profile works. Check your provider's data terms, and keep material out of the conversation if you do not want it sent there.
- **Render-time fetches.** A composition that loads GSAP or fonts from a CDN makes the renderer request those files. The request carries no project content. It happens only for hosts you approved.

The HyperFrames CLI has anonymous telemetry and an update check. The launcher disables both on every call, with `HYPERFRAMES_NO_TELEMETRY=1`, `DO_NOT_TRACK=1`, and `HYPERFRAMES_NO_UPDATE_CHECK=1`, and refuses the `telemetry`, `events`, and `feedback` commands.

## Optional providers

All off by default, and none can be switched on from inside this release:

| Capability | Upstream provider | What it would send |
| --- | --- | --- |
| Voice (text to speech) | HeyGen, ElevenLabs, Gemini | The script text |
| Music generation | Provider-backed or a local model | A text prompt |
| Image generation | Gemini and others | A text prompt |
| Background matting | A local model downloaded on first use | Nothing, but it is a download |

The launcher removes provider keys from the CLI's environment and refuses the commands that call these. Enabling any of them is future work that would need its own tests.

## Memory

Memory writes are staged for your approval. The profile never saves audience handles, names, or contact details; raw comment or DM content; raw analytics exports; credentials; sponsor contracts or rates; private information about people on camera; or unreleased business information you have not approved.

What it may save, with approval: your corrections, voice and style decisions, reviewed scripts and edits, measured outcomes of posted content, completed experiments, and aggregated, anonymized audience patterns.

## Retention

Raw footage, transcripts, exports, and comment files are session-only by default. You choose retention rules during onboarding for footage, transcripts, exports, and renders, and they are recorded in your creator profile.

Files the profile writes stay where you can see them:

- `local/` in the profile: your creator profile, visual identity, pillars, and the video engine state.
- Your workspace: projects, renders, receipts, and the footage checksum manifest.

## Kanban

Tasks are readable by every profile on the board. The agent keeps raw exports, audience identities, footage of identifiable people, and sponsor terms out of them, and uses opaque content IDs for sensitive cases.

## Removing your data

`hermes profile delete social-media` removes the profile, including `local/`, memories, and sessions. Your workspace is yours and is not removed if it lives outside the profile.
