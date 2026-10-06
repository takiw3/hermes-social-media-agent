# Security

## Reporting a problem

Report a vulnerability privately through GitHub: open the repository's **Security** tab and choose **Report a vulnerability**. Please do not open a public issue for a security problem.

Include what you did, what happened, what you expected, and the Hermes and profile versions. If the report involves footage, analytics, or audience data, describe it and do not attach it.

## What counts

- A way for the agent to post, schedule, comment, message, upload, or sign in.
- A way to run a HyperFrames version other than the pinned one, or to reach its skill self-update, cloud render, publish, feedback, or sign-in commands.
- A way around the workspace boundary through the launcher.
- A download that happens during profile installation, or without owner approval during setup.
- Credentials, audience data, footage, or analytics ending up in the repository, in an installed profile, in memory, or in Kanban.
- A prompt injection that leads to an external action.
- A vendored file that differs from its recorded checksum, or a bundled asset with no license record.

## What this profile does not claim

Read `docs/permissions-and-security.md`. In short: a Hermes profile is not a tenant boundary, the deny rules cannot list every route to an external service, and several rules rest on the model following instructions. Reports that show one of those instruction-level rules failing are still welcome.

## Scope

This repository only. Report problems in Hermes to Nous Research and problems in HyperFrames to HeyGen.

## Secrets

Nothing in this repository is a secret. If you find one, report it as above. The vendored HyperFrames skills contain one public analytics client key from upstream; the launcher disables the telemetry that would use it.
