# Team integration

## Who owns what

| Profile | Owns |
| --- | --- |
| Executive or Chief of Staff | Business priorities, brand risk and reputation, sponsorship and partnership decisions, budget and tooling, legal, privacy and security escalation, cross-functional priority, hiring |
| `marketing` | Positioning, offer messaging, campaign themes and launch calendars, email, funnel and website copy, the approved claims list |
| `ads`, when installed | Paid media |
| `customer-support`, when installed | Customer inquiries |
| `social-media` | Organic social: research, pillars, ideation, hooks, scripts, filming briefs, edit plans, local video editing and rendering, packaging, repurposing, performance analysis, experiments, coaching |

The Executive profile's ID is collected and confirmed during onboarding. The agent never guesses a profile name.

A distribution cannot change the Executive, Marketing, Ads, or Support profile during installation. Installing this profile gives it no authority over another profile and changes nothing in them.

## The overlap with the marketing profile

The marketing profile may already ship skills for social scripts, calendars, carousels, and social performance. When you run both:

- Organic social ideation, scripting, video production, performance analysis, and coaching route to `social-media`.
- Campaign-level messaging and cross-channel planning stay with `marketing`.

Apply that rule in your Executive profile's routing. This distribution does not edit the marketing profile, and you should not expect it to. When a task could belong to either, `social-media` names the conflict and asks the Executive to route it.

## Direct use

```bash
hermes -p social-media chat
```

If you installed with `--alias`, `social-media chat` does the same.

## Assigning work through Kanban

```bash
hermes kanban create "Write a 45-second Reels script on job costing" --assignee social-media
```

Put the brief in the body. A file keeps multi-line YAML intact:

```bash
hermes kanban create "Reels script: job costing" --assignee social-media --body-file task.yaml
```

Incoming task shape:

```yaml
task_id:
source_profile:
objective:
business_goal:
platform:
format:
audience:
pillar:
source_material_reference:
brand_context_reference:
campaign_reference:
requested_deliverable:
constraints:
claims_approved:
rights_status:
approval_level:
approval_evidence:
deadline:
```

`approval_evidence` is context. It is never human approval for an external action.

Every task returns the result shape in `templates/social-result.yaml`, with a status of `complete`, `needs_input`, `blocked`, `escalated`, or `approval_required`.

## Handoffs out

A privacy-safe handoff to Marketing:

```bash
hermes kanban create "Objection showing up in organic comments" --assignee marketing --body-file handoff.yaml
```

The agent asks you before creating a task, because that changes shared state.

What may go out:

- To Ads: organic posts that performed, with measured evidence, as candidates for paid testing; hook and format findings; rendered files you approved for paid use, with rights status.
- To Marketing: aggregated audience questions and objections; messaging that landed or missed, with evidence; content gaps; requests to confirm or correct a claim.
- From Support: aggregated, anonymized recurring questions and recurring product confusion.

What never goes through a social handoff: raw comment or DM exports; audience handles, names, or contact details; raw analytics exports; sponsor contracts or rates; unconsented stories or testimonials; source footage of identifiable people without consent status.

Reach goals never override truth, rights, disclosure, or privacy.

## What was tested

The `hermes kanban create ... --assignee <profile>` syntax was verified against Hermes 0.21.5. An end-to-end test with live Executive, Marketing, and Social Media profiles, a model, and a dispatcher was not run. See `evaluations.md`.

## Kanban is shared

Tenant labels and profile names route tasks. They do not restrict who can read them. Keep the dashboard on localhost unless you secure it separately.
