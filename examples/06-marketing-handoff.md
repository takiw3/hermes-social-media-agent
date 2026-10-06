# Example: a redacted handoff to Marketing

Synthetic example. The business, the people, the files, and every figure are invented to show the shape of the output. Nothing here is a real result, a benchmark, or a recommendation.

**Owner asks:** "Prepare a redacted handoff to Marketing on the objections showing up in comments."

**Recipient confirmed:** the installed Marketing profile ID is `marketing`.

```yaml
task_id:
source_profile: social-media
objective: Decide whether offer messaging should answer the "only for big contractors" objection
business_goal: bookings
platform: instagram
audience: Trades contractors, owner-operated
source_material_reference: "comment-analysis-2026-w40 (aggregated, held by social-media)"
requested_deliverable: A position on firm size for organic content to carry
constraints: No change to pricing copy requested
claims_approved: none
rights_status: not applicable
approval_level: draft
cross_team_signal:
  theme: "Viewers assume the service is for larger firms"
  kind: objection
  count: 31
  of_comments: 212
  window: "six reels, synthetic window"
  examples_paraphrased:
    - "Assumes a one-truck business is too small to need this"
    - "Asks whether there is a minimum number of employees"
  label: measured
  cannot_show: "Whether the people commenting are in the target audience"
```

```bash
hermes kanban create "Objection in organic comments: only for big contractors" --assignee marketing --body-file handoff.yaml
```

**What the agent says with it:** "This contains counts and paraphrased wording only. No handles, no raw comments. Do you want me to create the task?"
