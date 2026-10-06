# Example: what to stop making

Synthetic example. The business, the people, the files, and every figure are invented to show the shape of the output. Nothing here is a real result, a benchmark, or a recommendation.

**Owner asks:** "Analyze last month's export and tell me what to stop making."

**Sources:** one Instagram export, 31 organic reels and 1 boosted reel, exported on a stated date, window of 60 days, owner's timezone. Saves and shares present. Watch time present. No outcome data.

```yaml
account_review:
  window: {start: "synthetic", end: "synthetic", timezone: "America/Toronto"}
  sample_size: 31          # the boosted reel is reported separately
  groups:
    - {by: pillar, name: tool-tips, posts: 9, judgeable: true}
    - {by: pillar, name: job-costing, posts: 12, judgeable: true}
    - {by: pillar, name: cash-flow, posts: 7, judgeable: true}
    - {by: pillar, name: client-stories, posts: 3, judgeable: false, posts_needed: 7}
  recommendations:
    - action: stop
      claim: Tool-tips reels are the weakest group on saves in this window
      evidence_tier: 1
      source_and_date: "Owner's Instagram export"
      sample_and_window: "9 of 31 posts, 60 days, compared at day 7"
      confidence: medium
      would_change_if: "The next export shows replies or bookings traced to this pillar"
      cheapest_test: "Pause the pillar for four weeks and compare total saves"
      owner_time_cost: "Frees about 70 minutes a week"
      label: measured
    - action: test
      claim: Opening on a client moment holds attention better than opening on a tip
      evidence_tier: 4
      sample_and_window: "Too few matched posts to judge"
      confidence: low
      cheapest_test: "Four and four, same topic and length, hook changed only"
      label: hypothesis
  conflicts:
    - "Tool-tips has the highest median views and the lowest median saves. Views alone are weak evidence, so the recommendation follows saves."
  cannot_show:
    - "Whether any reel produced a booking. No outcome data was provided."
    - "Why any reel performed. Topic, length, and posting day changed together."
```

**What the agent says with it:** "Stop tool tips. That is the one call this data supports. Client stories has three posts, which is not enough to judge. I cannot tell you what drove bookings because I have no booking data."
