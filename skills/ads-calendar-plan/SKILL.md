---
name: ads-calendar-plan
description: Use this skill when the user wants to plan a paid-ads calendar — phrases like "plan my ads calendar", "ads calendar for the year", "ads budget plan", "schedule paid campaigns", "ad spend plan". Allocates budget across funnel stages and platforms, defines audience segments per campaign, sets creative refresh cadence, assigns flight dates to key seasonal moments, and produces a structured markdown calendar of planned paid campaigns. Coordinates with klaviyo-calendar-plan so paid + owned channels reinforce each other.
---

# Ads calendar planner

Plan a year (or quarter) of paid ads campaigns: budget allocation, audience cycles, creative refresh cadence, and synchronization with email cadence.

## When to use

- Annual / quarterly budget planning
- Brand has been running ads ad-hoc and wants a system
- Pre-Black-Friday planning (start in August for BFCM ads)
- Coordinating paid + owned (email/SMS) channels

## Output

A markdown file at `~/.claude/brand-voice-vault/<brand>/calendar/ads-<period>.md` with budget, audiences, and campaign timing mapped to a calendar.

## Steps

### 1. Establish baselines

If existing ads data is available, run `ads-performance-analysis` first to get current CPA, ROAS, and best variants.

Pull industry benchmarks if the platform MCP exposes a benchmark tool (e.g., `ads_insights_industry_benchmark`). This call is platform-dependent and may not be available; if unavailable, rely on the defaults below.

If brand-new with no ads history, set conservative starting budgets:
- Cold acquisition: $30-50/day per ad set
- Retargeting: $10-20/day per ad set
- Catalog dynamic: $20-40/day per product set

### 2. Budget framework

Plan total monthly budget then allocate by funnel:

| Funnel | Default % of total | Use for |
|---|---|---|
| Cold acquisition | 60-70% | Lookalikes, broad interest |
| Retargeting | 15-25% | Site visitors, email subs, cart abandoners |
| Brand / awareness | 5-10% | Video views, page likes (low priority for DTC) |
| Catalog dynamic | 0-15% | If catalog ads make sense for SKU count |

Adjust based on lifecycle:

| Stage | Acquisition | Retarget | Brand |
|---|---|---|---|
| Pre-launch (no list) | 80% | 10% | 10% |
| Launch (first 30 days) | 70% | 25% | 5% |
| Scaling (next 60 days) | 60% | 30% | 10% |
| Mature (post-90 days) | 50% | 35% | 15% |

**Validation checkpoint:** After choosing allocations, verify the percentages across Cold acquisition + Retargeting + Brand + Catalog sum to 100%. If they do not, adjust before proceeding.

### 3. Map calendar moments

Always-on:
- Cold acquisition (running continuously)
- Retargeting (running continuously)

Time-bound:

| Period | Focus | Budget bump |
|---|---|---|
| Launch month | Concentrated push, hero hooks | +50-100% |
| Father's Day / Mother's Day | Gift-focused creative | +30% |
| Mid-summer (Jul) | Seasonal angle (e.g., "track-day season") | flat |
| Back-to-school (Aug-Sep) | Audience-specific if applicable | +20% |
| Pre-BFCM (early Nov) | Awareness + waitlist | +30% |
| BFCM core (Nov 28-Dec 2) | Promo creative | +200-300% |
| Holiday gift (Dec) | Gift creative | +50% |
| Boxing Day / NYE | Year-end deals | +30-50% |
| January slump | Pause non-essentials, focus on retargeting | -30% |

### 4. Creative refresh cadence

Meta auction rewards new creative; old creative fatigues. Plan rotation:

| Funnel stage | Creative refresh |
|---|---|
| Cold acquisition | New variants every 2 weeks |
| Retargeting | New variants every 3-4 weeks |
| Catalog | Rule-based product set rotation, image format every 6-8 weeks |
| Promo / BFCM | Always-fresh, sometimes daily during BFCM week |

### 5. Audience refresh cadence

| Audience | Refresh cadence |
|---|---|
| 1% Lookalike (high intent) | Every 60-90 days |
| Interest stack | Every 30-45 days; rotate interests |
| Custom audience (site visitors) | Live (auto-updates) |
| Custom audience (email subs) | Sync from Klaviyo monthly |
| Email-engagers lookalike | Sync monthly |

### 6. Coordinate with Klaviyo calendar

The most powerful campaigns combine paid + owned:

- BFCM: paid awareness build → email teaser → paid retargeting → email send → paid retargeting
- Launch: paid acquisition + email pre-launch sequence + landing-page-specific paid creative + email reveal day
- New product: paid awareness → email reveal → paid retargeting

**Validation checkpoint:** Before referencing the Klaviyo calendar, check whether the file `~/.claude/brand-voice-vault/<brand>/calendar/<period>.md` exists. If it does not exist, note in the output that the Klaviyo calendar has not been generated yet and flag it as an open question. Do not block calendar creation — proceed with placeholder sync points that can be filled in once `klaviyo-calendar-plan` is run.

When the file exists, read it and align ad pulses with email sends.

### 7. Format the output

```markdown
# <Brand> Paid Ads Calendar — <period>

## Always-on baseline
| Campaign | Daily budget | Audience | Creative cadence |
|---|---|---|---|
| Cold acquisition · Lookalike | $50 | 1% LAL of email subs | Refresh weekly |
| Cold acquisition · Interest stack | $50 | Track-day, F1, BMW M | Refresh every 2 weeks |
| Retargeting · 30-day site visitors | $25 | Site visitors, last 30d | Refresh every 3 weeks |
| Retargeting · Cart abandoners | $15 | ATC + checkout-no-purchase | Daily refresh |

## Quarterly schedule

### Q1 (Jan-Mar)
| Period | Action | Budget delta | Notes |
|---|---|---|---|
| Jan 1-15 | Reduce cold spend, focus on retargeting | -30% | Slump period |
| Feb 1-14 | Valentine's gift push | +20% | Apex tier focus |
| Mar 15-31 | Spring season ramp-up | +10% | New creative rotation |

### Q2 (Apr-Jun)
...

### Q3 (Jul-Sep)
...

### Q4 (Oct-Dec)
| Oct 1-15 | BFCM warm-up (waitlist) | flat | Test BFCM creatives |
| Oct 16-31 | BFCM teaser | +30% | Early-access angle |
| Nov 1-25 | Pre-BFCM pulse | +30% | Cold + retargeting |
| Nov 28 - Dec 2 | BFCM core | +200% | Multi-creative blitz |
| Dec 3-23 | Holiday gift | +50% | Last-day-to-order CTA |
| Dec 26-31 | Year-end | +30% | Boxing Day deals |

## Total budget pacing

| Month | Budget | Notes |
|---|---|---|
| Jan | $X | |
| Feb | $X | |
...

## Coordinated email touchpoints
- See klaviyo calendar at `~/.claude/brand-voice-vault/<brand>/calendar/<period>.md`
- Key paid+email moments:
  - <date>: <event> — paid push + email reveal

## Creative production schedule
| Asset due | Campaign | Brief from |
|---|---|---|
| Mar 15 | Spring rotation | ads-brief-create / spring-2026 |
| Jul 1 | Father's Day (late) | ads-brief-create / fathers-day-2026 |
| ... | | |

## Open questions
- <e.g., "Are we adding TikTok or YouTube paid this year?">
- <e.g., "Should we test Pinterest for the gift-buyer audience?">
```

**Validation checkpoint:** After writing the file, confirm it was saved successfully by reading it back. If the write failed, surface the error to the user before proceeding to step 8.

### 8. Suggest next actions

After saving the calendar:
- Brief any campaigns due in next 30 days via `ads-brief-create`. To trigger it, say: "Create an ads brief for the [campaign name] campaign from the [period] calendar."
- Generate creative imagery for upcoming campaigns via Nano Banana
- Sync the Klaviyo calendar so paid + email align. If not yet created, say: "Run klaviyo-calendar-plan for [brand] [period] so we can align email sends with the paid schedule."

## Multi-platform notes

This skill defaults to Meta (Facebook/Instagram). The same calendar structure applies to TikTok Ads, Google Search/Shopping, YouTube, and Pinterest — each with different CPA profiles and format requirements. For multi-platform brands, structure the calendar per-platform with shared coordinated dates.

## Tradeoffs

- **Plan a year vs. plan a quarter** — Annual is strategic; quarterly is more honest for brands with < 6 months of ads data.
- **Always-on vs. burst** — Always-on retargeting is non-negotiable; cold can be either, but burst campaigns produce fragmented learning data.

## Reference example

For Gear Head Box Q3 2026:
- Aug: launch month — $200/day total ($140 cold, $60 retargeting), 4-creative rotation
- Sep: regular cadence — $150/day, refresh creative weekly
- Sync points with Klaviyo: launch announcement (Aug 4), first-box ship (Aug 15), Father's-Day-late campaign tied to Apex tier

## Cross-skill links

- `ads-brief-create` — for each campaign in the calendar
- `ads-campaign-create` — execution of briefs
- `ads-performance-analysis` — review performance vs. plan
- `klaviyo-calendar-plan` — sync paid + owned cadences
