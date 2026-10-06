# Example: captions on a talking-head clip, planned and rendered

Synthetic example. The business, the people, the files, and every figure are invented to show the shape of the output. Nothing here is a real result, a benchmark, or a recommendation.

**Owner asks:** "Add captions to this talking-head clip in my caption style and render it vertical."

**Engine status first.** `doctor` reports `toolchain verified`.

**Edit plan (confirmed by the owner before anything was written):**

```yaml
edit_plan:
  content_id: KB-2026-041
  video_engine: toolchain verified
  workflow: captions over existing footage, core composition path
  workflow_status: rendered_and_inspected
  platform: instagram
  canvas: {width: 1080, height: 1920, frame_rate: 30}
  duration_seconds: 44
  safe_margins: {top: 220, right: 90, bottom: 420, left: 90}   # owner-confirmed from her own screenshots
  source_footage:
    - {file: footage/kb-041-take3.mp4, sha256: "registered with footage-add"}
  transcript_source: owner-provided
  caption_style: {font: Inter, size: 64, colors: "#111111 on #ffffff", position: "lower third, inside margins", max_chars_per_line: 22}
  overlays:
    - {type: data_callout, text: "Guess. Then actual.", t_start: 22.0, duration: 4.0, position: upper right}
  audio: {speech: source clip, music: none, music_license: not applicable}
  assets:
    - {asset: assets/source.mp4, rights_status: recorded}
  not_in_scope: ["cutting or reordering speech", "color grading"]
  confirmed_by_owner: true
  state: edit_planned
```

**What happened, in order:**

1. First draft render refused: `approval required`. The composition loads GSAP from `cdn.jsdelivr.net` and the owner had not approved that host. The agent stopped and told her the command to run.
2. Host approved by the owner in her terminal. Draft rendered.
3. Review of sampled frames: one caption crossed the bottom margin. Verdict fail. Status stayed `draft rendered`.
4. Composition fixed, second draft rendered, review passed on every sampled frame.
5. Final rendered.

**Final receipt, written by the launcher:**

```yaml
receipt_version: 1
status: "final rendered with file path"
stage: "final"
inspected: false
output_relative: "renders/kb-2026-041-final.mp4"
sha256: "<sha-256 of the file>"
size_bytes: 9412233
duration_seconds: 44.0
width: 1080
height: 1920
frame_rate: 30.0
video_codec: "h264"
audio_codec: "aac"
quality: "delivery"
render_seconds: 71.4
engine: "hyperframes@0.8.138"
```

**What the agent says with it:** "Final is rendered and passed review on nine frames. Source footage checksum is unchanged. Nothing was posted. Do you want the packaging sheet?"
