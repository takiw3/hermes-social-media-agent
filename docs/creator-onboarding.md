# Creator onboarding

Onboarding starts in your first direct conversation with the profile, or when a delegated task cannot finish because a fact is missing. Installing the profile does not start it. If your Executive profile sends a complete brief with valid source references, the agent does the task and skips onboarding.

## How it runs

- The agent explains the setup in a couple of sentences.
- It asks one question at a time and never repeats one you answered.
- You can skip a question, correct an answer, pause, resume later, or hand over documents instead of typing.
- It asks before reading footage, transcripts, analytics exports, comment exports, or any audience data.
- It summarizes the finished profile and asks you to confirm before saving anything.

## What it collects

Business name, website, market, location, and model. Offers with exact prices. The goal content should serve. Audience, their problems, and their words. Platforms, handles, and account types. Baseline figures you choose to share, with source and date. Pillars, and formats that worked or failed, with evidence. On-camera comfort, filming setup, weekly hours, and who films, edits, and approves. Voice examples, words you never use, and claims the agent must never make. Visual identity: colors, fonts, logo files, caption style, safe margins, lower-third and cover style, and reference videos. Approved calls to action. Competitors and adjacent creators. Licensed sources for music, footage, fonts, and images. Consent status for anyone on camera. Sponsorships and disclosure practice. Regulated-industry constraints. The video workspace. Hardware limits. Analytics exports you can provide. Reporting measures and review cadence. Permitted read, draft, and render levels. The installed profile IDs of your Executive, Marketing, Ads, and Support profiles. Retention rules.

## Where it goes

- The full profile is written to `local/creator-profile.md` and `local/brand-and-visual-identity.md`, and pillars to `local/content-pillars.yaml`. Profile updates never touch `local/`.
- Compact preferences are proposed for Hermes memory and staged for your approval.
- Credentials, raw audience data, and raw analytics exports are never stored in memory.

## How answers are classified

Owner-confirmed facts, measured data with source and date, official platform facts with URL and access date, calculations, inferences, hypotheses, unknowns, and permission boundaries. An unanswered question is recorded as `unknown`, not guessed.

## The video workspace

The agent will tell you the command to approve a workspace and set up the toolchain. You run it yourself. See `hyperframes-setup.md`.
