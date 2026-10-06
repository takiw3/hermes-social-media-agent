# Example: a 45-second script with five hook options

Synthetic example. The business, the people, the files, and every figure are invented to show the shape of the output. Nothing here is a real result, a benchmark, or a recommendation.

**Owner asks:** "Write a 45-second script in my voice with five hook options."

```yaml
script:
  content_id: KB-2026-041
  platform: instagram
  format: reel
  target_seconds: 45
  estimated_seconds: 44
  pace_words_per_minute: 142     # measured from the owner's voice memo, not an assumption
  pillar: job-costing
  goal: bookings
  hooks:
    - {text: "Your best month might be your worst.", mechanism: contradiction, claim_flag: none}
    - {text: "You were flat out in March and still couldn't make payroll.", mechanism: specific moment, claim_flag: none}
    - {text: "Which job last month actually made you money?", mechanism: question the audience already asks, claim_flag: none}
    - {text: "Stop pricing jobs off what the last guy charged.", mechanism: mistake named plainly, claim_flag: none}
    - {text: "Every job you can't cost is a job you might be paying to do.", mechanism: stake, claim_flag: none}
  beats:
    - t: "0-3"
      spoken: "Your best month might be your worst."
      on_screen: "Best month. Worst month."
      visual: "Owner to camera, desk setup"
      edit_note: "Caption on from frame one"
    - t: "3-14"
      spoken: "I open books every week where the calendar was full and the bank account wasn't. Busy isn't the same as paid."
      on_screen: "Busy is not paid"
      visual: "Hold on owner"
      edit_note: "No cut"
    - t: "14-30"
      spoken: "Here's the habit. Before the job starts, write down what you think it costs. When it ends, write down what it did cost. Same sheet. Two numbers."
      on_screen: "Guess. Then actual."
      visual: "B-roll: a job sheet with two columns, client name covered"
      edit_note: "Callout card on 'two numbers'"
    - t: "30-40"
      spoken: "Do that for ten jobs and you'll know which work to chase and which to price up."
      on_screen: "Ten jobs"
      visual: "Back to owner"
      edit_note: ""
    - t: "40-44"
      spoken: "Comment COSTING and I'll send you the sheet."
      on_screen: "Comment COSTING"
      visual: "Owner to camera"
      edit_note: "Hold two seconds after the last word"
  call_to_action: "Comment COSTING"
  claims:
    - text: "Most contractors underprice by a fifth"
      status: needs source
      source: "Removed from the spoken track. Replaced with the owner's own observation."
  filming_notes:
    - "Beat three is the long one. Film it as its own take."
  state: script_drafted
```

**What the agent says with it:** "This is drafted, not approved. I pulled one line because I could not source the figure. Tell me which hook you want and whether the script is approved as written."
