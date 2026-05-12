---
name: klaviyo-calendar-plan
description: Plans a full-year or quarterly Klaviyo email/SMS marketing calendar for a brand — generating campaign briefs, recommending send cadences by lifecycle stage, mapping automated flows to the always-on calendar, suggesting seasonal and category-specific promotions, and producing a structured markdown calendar file the brand can execute against. Use when the user wants to plan a marketing email/SMS calendar — phrases like "plan my Klaviyo calendar", "build a quarterly email plan", "schedule my campaigns", "what campaigns should I send this year", "marketing calendar for the brand".
---

# Klaviyo calendar planner

Build a strategic email/SMS marketing calendar — the right cadence, themes, and segments for the brand's lifecycle stage. The output is a structured calendar markdown file the user can review and execute against (one campaign per row, mapped to flows where appropriate).

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

| Brand stage | Email | SMS |
|---|---|---|
| Pre-launch | 1/wk | none |
| Launch month | 2-3/wk | 1 launch + 1 ship-day |
| Post-launch (months 2-6) | 1-2/wk | 1/mo (cycle reminder) |
| Mature (month 6+) | 2-3/wk segmented | 2-4/mo by segment |
| BFCM season (Nov) | 4-7/wk | 2-3/wk |

### 3. Map the year (or quarter)

**Always-on (flows handle these — see `klaviyo-flow-build`):**
- Welcome / signup nurture
- Browse abandonment
- Checkout abandonment
- Order confirmation / shipped
- Post-purchase feedback (10 days after)
- Cancellation save
- Win-back (90 days post-cancel)

**Core time-bound campaigns:**

| Period | Campaign type | Notes |
|---|---|---|
| Jan week 1 | New year founder letter | What's being built this year |
| Feb 14 | Valentine's gift push | Gift-suitable categories only |
| Mar/Apr | Spring curation / category launch | Per-product cadence |
| May/Jun | Mother's / Father's Day | If applicable |
| Jul/Aug | Summer audience-specific | Tie to seasonal use-case |
| Sep | BFCM warm-up | "Save the date" |
| Oct | BFCM teaser + early-access waitlist | Build the early-access list |
| Nov 1-25 | Pre-BFCM tease + list hygiene | Email cleanup before peak |
| Nov 28 – Dec 2 | BFCM core | 5-7 emails over 5 days |
| Dec 1-23 | Holiday gift push | Last-day-to-order is the hard deadline |
| Dec 26 | Post-Christmas sale | If catalog-wide discount is viable |
| Dec 28-31 | Year-end recap / next-year preview | Founder voice |

For subscription boxes, add monthly rhythm: cycle-reminder campaign on the 10th; ship-day flow (not campaign) on the 15th; quarterly unboxing roundup.

### 4. Layer in cohort sends

Every campaign must declare its segment — no default "all subscribers" without justification. Segment by:
- Time-since-last-order (< 30 days / 30-90 / 90+ / never bought)
- Tier (e.g., Pit Stop / Apex / Podium)
- Geography for event-tied sends
- Engagement (opened 3-of-last-5 vs. dormant)
- Acquisition source (paid vs. organic)

### 5. Flag conflicts and blackouts

- Don't send the day of a major industry event unless tying in
- Avoid sends during major news cycles (national tragedies, elections)
- Cap at 1 send per recipient per 24h (except BFCM peak)
- Avoid Sundays before noon and Mondays before 9am

### 6. Validate the draft calendar

Before writing output, check the full draft against all four gates:
- **Cadence rules**: No recipient exceeds max sends/week for their lifecycle stage
- **Blackout compliance**: No sends land on flagged dates or windows
- **Segment coverage**: Every campaign row has a declared audience segment
- **Flow gaps**: Every always-on trigger is either covered by an existing flow or flagged for creation via `klaviyo-flow-build`

If any check fails, resolve it before proceeding.

### 7. Format the output

Write to `~/.claude/brand-voice-vault/<brand>/calendar/<period>.md` using this structure:

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
| ...

### Q2–Q4
(same table structure per quarter)

## Notes
- What's NOT in this calendar and why
- Open questions for next planning round
```

### 8. Suggest next actions

After saving the calendar, offer to:
- Build campaigns due in the next 14 days via `klaviyo-campaign-create`
- Build missing flows via `klaviyo-flow-build`
- Generate hero images for upcoming campaigns via Nano Banana

## Cross-skill links

- `brand-voice-extract` for voice context
- `klaviyo-campaign-create` for individual campaign creation
- `klaviyo-flow-build` for the always-on flow setup

## Reference example

For Gear Head Box, a Q3 2026 calendar would prioritize: Pre-launch hype (May/Jun), Launch (Aug 4), First-box reveal (Aug 15), Founders' anniversary content. The full BFCM blitz starts in Sept.
