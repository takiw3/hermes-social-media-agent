# Render presets

A preset sets the canvas. It does not promise acceptance by a platform. Every platform statement below comes from `skills/social-media-core/platform-packaging/references/platform-facts.yaml`, where its official URL and access date are recorded. If a row says `not verified`, tell the owner and ask them to confirm in the app.

| Preset | Canvas | Frame rate | `init --resolution` | Fits (per the facts file) |
| --- | --- | --- | --- | --- |
| `vertical` | 1080 x 1920 (9:16) | 30 | `portrait` | YouTube Shorts: square or vertical, up to three minutes, maximum 1080p (verified). Instagram Reels: aspect ratio between 1.91:1 and 9:16, minimum 30 frames per second, minimum 720 pixels (verified). Facebook Reels: any orientation, 1080p recommended (verified). LinkedIn: aspect ratio within 1:2.4 to 2.4:1 (verified). TikTok file specs: not verified. X: not verified. |
| `landscape` | 1920 x 1080 (16:9) | 30 | `landscape` | YouTube long-form: 16:9 is the standard aspect ratio (verified). LinkedIn: within range (verified). Facebook: any orientation (verified). X: not verified. |
| `square` | 1080 x 1080 (1:1) | 30 | `square` | Instagram and LinkedIn aspect ranges include 1:1 (verified). On YouTube, a square video of up to three minutes is categorized as a Short (verified). |

4:5 (1080 x 1350) is inside Instagram's verified aspect range. No 4:5 render was tested in this release, so treat it as `not tested`.

## Rules

- Output is MP4 with H.264 video and AAC audio, the pinned CLI's default. YouTube and Facebook list that combination as recommended (verified).
- Duration limits differ by platform and change. Check the facts file for the destination, not this table.
- Safe margins are the owner's confirmed values in `local/brand-and-visual-identity.md`. No official numeric safe-zone figure is recorded for any platform. Ask the owner to screenshot their own posts and confirm margins that clear the interface.
- `--stage draft` uses the CLI's `draft` quality. `--stage final` defaults to `delivery`.
