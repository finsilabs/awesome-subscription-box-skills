---
name: klaviyo-calendar-plan
description: Use this skill when the user wants to plan a marketing email/SMS calendar for their brand — phrases like "plan my Klaviyo calendar", "build a quarterly email plan", "schedule my campaigns", "what campaigns should I send this year", "marketing calendar for the brand". Plans the full year (or quarter) of campaigns + flows that make sense for the brand's category, lifecycle stage, and audience.
---

# Klaviyo calendar planner

Build a strategic email/SMS marketing calendar — not just a list of dates, but the right cadence, themes, and segments for the brand's lifecycle stage. The output is a structured calendar markdown file the user can review and execute against (one campaign per row, mapped to flows where appropriate).

## When to use

- Brand is launching or relaunching
- Quarterly planning sessions (Q1 / Q2 / Q3 / Q4 calendars)
- Brand has been sending ad-hoc emails and wants a system
- Pre-Black-Friday planning (start in September for BFCM)

## What the skill produces

A file at `~/.claude/brand-voice-vault/<brand>/calendar/<period>.md` with:
- One row per send (date, time, channel, audience, purpose, template/flow ref)
- Cadence rules (max sends per week, blackout dates)
- Cohort/segment definitions
- Notes on what's NOT included and why

## Steps

### 1. Establish brand context

Read from `~/.claude/brand-voice-vault/<brand>/`:
- `voice.md` (cadence implied by tone — terse brands send less often)
- `audience.md` (what triggers the audience)
- `principles.md` (what's on/off brand)

If the vault doesn't exist, ask the user:
- Brand category (subscription / DTC retail / SaaS / lifestyle)
- Audience size and stage (cold / warm / paying)
- Current sending baseline (none / weekly / daily)
- Open-rate / click-rate benchmarks if they have them

### 2. Pick the cadence

Recommended baseline by lifecycle stage:

| Brand stage | Email | SMS | Why |
|---|---|---|---|
| Pre-launch | 1/wk | none | Build anticipation without burning the list |
| Launch month | 2-3/wk | 1 launch + 1 ship-day | Earn the moment |
| Post-launch (months 2-6) | 1-2/wk | 1/mo (cycle reminder) | Retention focus |
| Mature (month 6+) | 2-3/wk segmented | 2-4/mo by segment | Optimize by cohort |
| BFCM season (Nov) | 4-7/wk | 2-3/wk | Industry max |

### 3. Map the year (or quarter)

Calendar building blocks for most B2C brands:

**Always-on (flows handle these — see `klaviyo-flow-build`):**
- Welcome / signup nurture
- Browse abandonment
- Checkout abandonment
- Order confirmation
- Box/order shipped
- Post-purchase feedback (10 days after)
- Cancellation save
- Win-back (90 days post-cancel)

**Time-bound campaigns (calendar items):**

| Date | Type | Description |
|---|---|---|
| Jan first week | New year letter | "Here's what we're building this year" — founder voice |
| Valentine's Day (Feb 14) | Gift campaign | If gift-suitable category |
| Spring (Mar/Apr) | Curation reveal / category launch | Per-product/per-month |
| Mother's / Father's Day | Gift campaign | If applicable |
| Summer (Jul/Aug) | Audience-specific | E.g., "track-day season" for car brands |
| Back-to-school (Aug/Sep) | If applicable | School-relevant brands |
| Sep | BFCM warm-up | "Save the date" |
| Oct | BFCM teaser + waitlist | Build the early-access list |
| Nov 1-25 | Pre-BFCM tease + email cleanup | List hygiene |
| Nov 28 - Dec 2 | BFCM core | 5-7 emails over 5 days |
| Dec 1-23 | Holiday gift push | Last-day-to-order is the deadline |
| Dec 26 (Boxing Day) | Post-Christmas sale | If catalog-wide discount viable |
| Dec 28-31 | Year-end recap / 2026 preview | Founder voice |

For subscription boxes specifically, add:
- 10th of every month: cycle-reminder
- 15th of every month: ship-day (handled by flow, not campaign)
- Month-anniversary unboxing roundups (quarterly)

### 4. Layer in cohort sends

Don't blast everything to everyone. Segment by:
- Time-since-last-order (< 30 days, 30-90, 90+, never bought)
- Tier (Pit Stop / Apex / Podium)
- Geography for events (e.g., "Cars & Coffee in your city")
- Engagement (opened-3-of-last-5 vs. dormant)
- Source (paid vs. organic)

Each campaign in the calendar should declare which segment it goes to.

### 5. Flag conflicts and blackouts

- Don't send the day of a major industry event (e.g., a F1 race for a car brand) unless you're tying in
- Don't send during major news cycles (national tragedies, elections)
- Cap at 1 send per recipient per 24h unless BFCM
- Avoid Sundays before noon, Mondays before 9am

### 6. Format the output

Write to `~/.claude/brand-voice-vault/<brand>/calendar/<period>.md`. Format:

```markdown
# <Brand> Marketing Calendar — <Q1 2026 | full year>

## Always-on flows
| Flow | Trigger | Template |
|---|---|---|
| Welcome | Subscribe to list | GHB · 01 |
| ...

## Cadence rules
- Max sends per week: 2 (3 during BFCM, 4 BFCM peak)
- Blackouts: <list>
- Time slots: 9am ET (Tues/Wed/Thu primary), 10am ET (Sun for stories)

## Campaign calendar

### Q1 (Jan-Mar)

| Date | Time (ET) | Channel | Audience | Purpose | Template/Notes |
|---|---|---|---|---|---|
| 2026-01-07 | 09:00 | Email | All subs | New year founder note | (draft) |
| 2026-02-08 | 09:00 | Email | All subs | Valentine's gift push | Use Apex tier |
| ...

### Q2 (Apr-Jun)
...

### Q3 (Jul-Sep)
...

### Q4 (Oct-Dec)
...

## Notes
- What's NOT in this calendar (and why):
  - <Items deliberately excluded>
- Open questions for next planning round:
  - <e.g., "Should we add SMS for Father's Day?">
```

### 7. Suggest next actions

After saving the calendar, offer to:
- Build any campaigns due in the next 14 days via `klaviyo-campaign-create`
- Build flows that don't yet exist via `klaviyo-flow-build`
- Generate hero images for upcoming campaigns via Nano Banana

## Cross-skill links

- `brand-voice-extract` for voice context
- `klaviyo-campaign-create` for individual campaign creation
- `klaviyo-flow-build` for the always-on flow setup

## Tradeoffs

- **Plan a year vs. plan a quarter** — quarterly planning is more accurate but takes more time. Annual planning is strategic; quarterly is tactical.
- **Per-segment vs. per-channel** — segmenting by audience is higher-ROI but more work. Channel-segmenting (everyone gets every email but SMS is a subset) is simpler.
- **AI-suggested ideas vs. user-led** — when stuck, the skill should suggest 5+ campaign angles per quarter, not just rubber-stamp the user's existing list.

## Reference example

For Gear Head Box, a Q3 2026 calendar would prioritize: Pre-launch hype (May/Jun), Launch (Aug 4), First-box reveal (Aug 15), Founders' anniversary content. The full BFCM blitz starts in Sept.
