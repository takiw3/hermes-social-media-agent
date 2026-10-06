# Analytics and metric definitions

## Inputs

The profile reads what you give it: a platform export, a screenshot of your insights, or figures pasted into chat. It has no connector, requests no platform scopes, and pulls nothing. No read-only analytics connector was built or tested for this release, so none is claimed.

For every dataset the agent records the platform, account, export date, time window, timezone, and the definition of each metric.

## Rules it follows

- A view on one platform is not a view on another. No cross-platform comparison without both definitions stated.
- Paid and organic are never blended. A boosted post is marked and separated.
- A figure read from an image is marked `read from image, unverified`.
- A missing value stays `Unavailable`. Nothing is estimated.
- Sample size is stated on every comparison. A conclusion the sample cannot support is declined, with the number of posts needed.
- Correlation is not cause. Posting time, topic, hook, length, and format move together.
- Content age is controlled. A three-day-old video and a ninety-day-old video are not compared on lifetime totals.
- Outliers are identified, and results are reported with and without them. Medians go beside averages.
- Content metrics are tied to business outcomes only when you supply the outcome data and the link is traceable.
- No prediction that a video will go viral. No benchmark, "good" threshold, or best posting time unless it comes from your own data and is labeled so.
- An export cell that begins with `=`, `+`, `-`, or `@` is treated as text and is neutralized when written to a CSV or sheet.

## Definitions verified for this release

Read from the official pages on 2026-10-06. The source of record is `skills/social-media-core/platform-packaging/references/platform-facts.yaml`.

| Platform | Metric | Definition | Source |
| --- | --- | --- | --- |
| Instagram | Views | The number of times content was played or displayed. For a reel, the number of times it starts to play or replay. | https://help.instagram.com/202865988324236 |
| Instagram | Viewers | Unique accounts that have seen the reel on screen at least once, whether or not it was played. Instagram labels this estimated and in development. | same |
| Instagram | Watch time | Total time the reel was played, including replays. | same |
| Instagram | Average watch time | Watch time divided by the number of initial views. | same |
| YouTube | Views | Beginning August 24, 2026, counted the moment a video starts to play, across Shorts, long-form videos, and live streams. | https://support.google.com/youtube/answer/2991785 |

The YouTube change matters in practice: view counts from before and after August 24, 2026 are not directly comparable, and any analysis that spans that date says so.

## Not verified

No metric definition was verified for TikTok, Facebook, LinkedIn, or X. For those, the agent uses the header and help text of your export if they define the metric, or lists the metric as undefined and does not interpret it.

## What every analysis contains

Sources and export dates. Time window and timezone. Metric definitions. Sample size. Method. Findings, each tagged measured, inferred, or hypothesis. What the data cannot show. The recommended next test.
