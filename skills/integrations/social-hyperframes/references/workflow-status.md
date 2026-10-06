# Video workflow status in this release

Status words: `rendered and inspected`, `loaded only`, `failed`, `not tested`, `not bundled`.

"Rendered and inspected" means a composition was rendered from an installed temporary profile through the pinned launcher, and frames across the timeline were looked at, not that an exit code was zero. The exact runs are recorded in `docs/evaluations.md` in the repository.

| Path | Status | What that covers |
| --- | --- | --- |
| Captions over an existing talking-head clip, 9:16, captions in front of the footage | rendered and inspected | A composition written to the `hyperframes-core` contract: the clip as a video layer, timed caption boxes from an owner-provided transcript. The footage file is not changed. |
| Designed overlays on an existing clip, 9:16: lower-third and data callout | rendered and inspected | Same contract, with overlay cards. |
| Short unnarrated motion graphic (animated stat card) | rendered and inspected | A standalone composition, no footage. |
| 16:9 composition | rendered and inspected | Landscape canvas. |
| `general-video` workflow | loaded only as a workflow; its underlying path is the one rendered above | The workflow text loads and routes. The renders above follow the same core contract it uses. |
| `motion-graphics` workflow | loaded only | The stat card above was authored to the core contract, not by running this workflow's full process with its catalog. |
| `talking-head-recut` workflow | loaded only | Needs a transcript. Two upstream assets are not shipped: the Virgil font (license conflict) and the vendored GSAP file (loaded from a CDN instead). Not rendered end to end. |
| `embedded-captions` workflow, captions composited behind the subject | loaded only | Its matting step needs a model and runtime package downloaded on first use, and its preview helpers need extra packages installed into the project. Those are owner-approved downloads this release does not automate, and the launcher refuses `remove-background`. |
| `faceless-explainer` workflow | loaded only | Needs narration from a voice provider. Voice generation is off by default. |
| `product-launch-video`, `music-to-video`, `pr-to-video`, `slideshow`, `remotion-to-hyperframes`, `figma` | not bundled | Say so and offer the closest bundled path. Do not download them. |

## Not supported, do not claim

- Cutting, trimming, reordering, retiming, color grading, or reframing source footage. Upstream routes these to `general-video` as custom edits. None was rendered in a test.
- Multi-camera editing and multi-shot caption embedding.
- Posting, scheduling, or uploading to any platform.
- Pulling analytics from any platform.
- Downloading other people's videos.
- Voice cloning or avatar generation.
- Editing inside CapCut, Premiere, DaVinci Resolve, or Final Cut.
- Live streaming.
- Thumbnail image generation.
- Cloud, Lambda, or Cloud Run rendering.

## Network at render time

Most compositions load GSAP from `cdn.jsdelivr.net`, and some load fonts from a font CDN. The renderer fetches those when it renders. The launcher refuses to render a composition that references a host the owner has not approved. A machine with no network cannot render a composition that depends on a CDN.
