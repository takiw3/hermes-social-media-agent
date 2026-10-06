# Example: ten client questions turned into ranked idea cards

Synthetic example. The business, the people, the files, and every figure are invented to show the shape of the output. Nothing here is a real result, a benchmark, or a recommendation.

**Owner asks:** "Turn this week's client questions into ten ranked video ideas."

**Context on file:** four confirmed pillars, a five-hour weekly budget, one performance snapshot of 14 reels.

```yaml
ideas:
  - rank: 1
    title: Why your busiest month lost money
    pillar: job-costing
    audience_problem: Owners cannot tell which jobs made money
    angle: A full calendar is not the same as a profitable one
    format: talking head with one on-screen number
    platform: instagram
    hook_direction: contradiction
    proof_needed: one anonymized job sheet
    proof_held: true
    effort_owner_minutes: 35
    rank_reason: Both measured job-costing posts drew more saves than the owner's other posts in the same snapshot
    rank_basis: measured
    flags: ["sample of two, too small to call a pattern"]
    state: idea
  - rank: 2
    title: The deposit conversation, word for word
    pillar: cash-flow
    audience_problem: Owners start jobs with no money down
    angle: The script for asking, not the reason to ask
    format: talking head
    platform: instagram
    hook_direction: specific moment
    proof_needed: none beyond the owner's own practice
    proof_held: true
    effort_owner_minutes: 25
    rank_reason: Asked in five of this week's client questions
    rank_basis: owner_fact
    flags: []
    state: idea
  - rank: 7
    title: How one client fixed their margins
    pillar: client-stories
    audience_problem: Owners doubt the method works for a firm their size
    angle: Before and after, told by the numbers
    format: talking head with two callouts
    platform: instagram
    hook_direction: stake
    proof_needed: the client's figures and written consent
    proof_held: false
    effort_owner_minutes: 50
    rank_reason: Strong idea that cannot be made yet
    rank_basis: taste
    flags: ["consent", "claim check: before-and-after result"]
    state: idea
cut:
  - "Day in my life: no tie to a pillar or to proof the owner holds"
```

**What the agent says with it:** "Cards 1 and 2 are ready to script. Card 7 is blocked until your client agrees in writing and you confirm the figures. I ranked card 1 first on two measured posts, which is not enough to call a pattern. Want hooks for card 1?"
