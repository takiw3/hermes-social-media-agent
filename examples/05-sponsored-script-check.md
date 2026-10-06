# Example: checking a sponsored script

Synthetic example. The business, the people, the files, and every figure are invented to show the shape of the output. Nothing here is a real result, a benchmark, or a recommendation.

**Owner asks:** "Check this sponsored script for disclosure and claim problems."

```yaml
rights_and_disclosure:
  content_id: KB-2026-052
  material_connection: paid
  disclosure:
    required: true
    present: false
    placement_ok: false
    platform_setting: "Instagram paid partnership label; tag the business partner"
    source: "https://www.facebook.com/business/help/788160621327601"
    accessed: "2026-10-06"
  claims:
    - {text: "This app saves you ten hours a week", category: other, result: block}
    - {text: "My clients make more money with it", category: earnings, result: block}
  people:
    - {role: owner, consent: recorded, minor: false}
  assets:
    - {asset: assets/app-screen-recording.mp4, register_entry: missing, result: block}
  verdict: escalate
```

**What the agent says with it:** "Blocked, and escalated to your Executive profile. Three things. One, there is no disclosure. It needs a plain line at the start of the video and the caption, plus the platform label. Two, both claims need substantiation from the sponsor before they can be said. Three, the screen recording has no license record. I have not seen the contract and I am not giving legal advice. I can draft the disclosed version once the claims are settled."

The sponsor's terms and rate do not appear in the escalation or in any Kanban task.
