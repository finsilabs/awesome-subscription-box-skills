---
name: ads-brief-create
description: Use this skill when the user wants to create a creative brief for a paid ads campaign — phrases like "create an ads brief", "write a brief for Meta ads", "draft a creative brief", "brief the campaign". Outputs a structured brief covering objective, audience, message, hooks, copy variants, asset specs, and success metrics. Brand-voice-aligned if a vault entry exists.
---

# Ads creative brief

Generate a paid-media creative brief that's structured enough to hand to a designer/copywriter (or to feed directly into `ads-campaign-create`). The brief is the bridge between strategic intent and execution-ready ads.

## When to use

- Starting a new ad campaign (Meta, TikTok, Google, etc.)
- Stakeholders need alignment before assets get produced
- Pre-flighting a campaign for handoff to the platform's create flow

## Output

A markdown file at `~/.claude/brand-voice-vault/<brand>/briefs/<campaign-slug>.md` (or in the project repo if user prefers) with the structure below.

## Steps

### 1. Gather inputs

Ask if not given:
- **Campaign objective** — what action should the ad drive? (purchase / lead / signup / app install / brand awareness / video view / engagement)
- **Funnel stage** — cold / warm / retargeting (informs creative tension)
- **Audience** — demographic + psychographic + interests + lookalike sources if available
- **Offer** — what's being promoted (subscription, gift card, sale, new product)
- **Budget tier** — affects ad count and variant count to brief
- **Run dates** — when the campaign goes live
- **Constraints** — anything off-limits (e.g., "no humor", "no comparison to competitors", legal restrictions)

### 2. Read brand voice

If `~/.claude/brand-voice-vault/<brand>/` exists, load:
- `voice.md` — tone, vocabulary, dos/don'ts
- `principles.md` — what's on/off-brand
- `audience.md` — primary triggers and motivations
- `palette.json` + `visual.md` — for the asset spec section

### 3. Generate the brief

Use this structure verbatim:

```markdown
# Brief: <Campaign name>

## One-liner
<1-sentence summary: who we're targeting, with what offer, to drive what action>

## Objective
- **Primary KPI**: <e.g., subscriptions, ROAS 2.0+, CPL < $X>
- **Secondary KPI**: <e.g., CTR > 1.5%, frequency capped at 3>
- **Success threshold**: <when to scale, when to kill>

## Audience
- **Primary**: <demo + interests + lookalikes>
- **Secondary**: <fallback if primary underperforms>
- **Exclusions**: <existing customers, recent buyers, etc.>
- **Estimated audience size**: <if known>

## Funnel stage
<Cold / Warm / Retargeting / Mixed>
<+ what they know about the brand at this stage>

## Core message
- **Promise**: <the one thing the ad makes someone feel/believe>
- **Reason to believe**: <why it's true — proof, demo, testimonial>
- **Call to action**: <verb-led, urgent if appropriate>

## Hook variants (3-5)
1. **Curiosity**: "<angle>"
2. **Pain-point**: "<angle>"
3. **Social proof**: "<angle>"
4. **Promise / aspirational**: "<angle>"
5. **Contrarian**: "<angle>"

## Copy variants

### Primary text (3 versions)
1. <30-90 word version>
2. <Short punchy version, 25-50 words>
3. <Long-form version with line breaks, 100-200 words>

### Headlines (5 versions)
1. <under 40 chars>
2. <under 40 chars>
3. <under 40 chars>
4. <under 40 chars>
5. <under 40 chars>

### Descriptions (3 versions, for placements that show them)
- <under 30 chars each>

## Asset specs

### Images required
- **1:1** (1080×1080) — feed primary
- **9:16** (1080×1920) — Stories / Reels
- **4:5** (1080×1350) — feed alt (mobile-optimized)

### Image direction
- **Subject**: <what's in the frame>
- **Mood**: <one or two adjectives>
- **Color**: <reference brand palette.json>
- **Type treatment**: <if any — overlay copy, lower-thirds>
- **What to avoid**: <stock-photo look / over-edited / etc.>

### Video (if applicable)
- **Length**: <15s / 30s / 60s>
- **Aspect**: <9:16 / 1:1 / 16:9>
- **First 3 seconds**: <what hooks the viewer>
- **CTA placement**: <when in the video>

## Landing destination
- **URL**: <full URL the click goes to>
- **Page goal alignment**: <does the LP support this offer?>
- **UTM parameters**: utm_source=<platform> utm_medium=<paid> utm_campaign=<slug>

## Tone guardrails
- DO: <list from voice.md>
- DON'T: <list from voice.md>

## Approval gates
- [ ] Brief reviewed by <name/role>
- [ ] Assets reviewed before production
- [ ] Ad copy reviewed before launch
- [ ] First 48 hours monitored, kill switch defined

## Notes
<Additional context — competitor reference ads, platform-specific requirements, regional considerations>
```

### 4. Suggest hook frameworks

If the user is stuck on hooks, offer these proven angles:

- **Problem → Promise**: "Tired of X? We do Y."
- **Status framing**: "For the [identity] who [action]"
- **Founder voice / authentic**: "Two years ago, I was..."
- **Reverse**: "Most [category] do X. We don't, because Y."
- **Specific number**: "8 things in your <product>"
- **Social proof lead**: "5,000 [audience] subscribe to..."

### 5. Variant strategy

Brief at least 3-5 variants per element (hook, copy, image) for testing. Meta especially rewards creative variation in the first 48 hours of a campaign.

## Cross-skill links

- `brand-voice-extract` — get the voice vault before briefing
- `ads-campaign-create` — execute the brief into actual campaigns
- `ads-performance-analysis` — compare vs. brief KPIs after launch
- `ads-calendar-plan` — slot this brief into the larger calendar

## Tradeoffs

- **Brief depth vs. speed** — for cold-traffic acquisition, invest in a thorough brief (15+ variants). For retargeting, less is fine (1-2 hooks, 3-5 copy variants).
- **Brand-voice strict vs. test what works** — start strict, then break voice rules in 1-2 variants to test. Voice rules exist for a reason; data > opinion when there's enough volume.

## Reference example

For Gear Head Box pre-launch:
- Objective: subscriptions, target CPA < $50
- Primary audience: men 38-55, US, interests = "track day", "Cars & Coffee", "F1", "BMW M", "Porsche 911", lookalike of email subscribers
- Hooks: "For the guy who'd rather be at the track" / "Monthly. Curated. Cancel anytime." / Founder voice: "Started this in my garage in Charlotte"
- Asset direction: cinematic GT3-style imagery, tire-gray palette, F1-red accent, no people's faces
