---
name: shopify-journey-segments
description: Use this skill when the user wants to define actionable customer segments on their Shopify store and pipe them to Klaviyo or ads — phrases like "build customer segments", "find my VIPs", "win-back segment", "high-value customers", "lapsed customers", "create a segment for ads". Defines named segments (VIP, lapsed one-timer, recent first-time, high-AOV-low-frequency, dormant), counts each, and outputs definitions ready to recreate in Klaviyo or push as a custom audience.
---

# Shopify journey segments

Translate raw customer data into a small set of named, actionable segments. Each segment has a clear definition, a count, an estimated revenue opportunity, and a recommended next action (a Klaviyo flow, a campaign, or a paid lookalike seed).

## When to use

- Building a new Klaviyo flow / campaign and need the audience defined
- Building Meta / TikTok lookalike seeds (export VIPs)
- Quarterly customer-base health check
- After cohort-retention analysis surfaces a lapsed pool
- Before a launch — segment by purchase pattern to target the right offer

## Prerequisites

- Shopify MCP connected (`mcp__9bf46487-...__list-customers`, `graphql_query`)
- (Optional) Klaviyo MCP if pushing the segment definitions over
- Brand-specific repeat cycle from `shopify-journey-cohort-retention` (informs lapsed thresholds)

## The default segment library

Six segments cover ~95% of activation needs. Each has standard criteria; tune the thresholds to brand category.

### A. VIP (top spenders, highly engaged)
- **Criteria**: `orders_count:>=4 AND total_spent:>=<2x AOV × 4>`
- **Use**: lookalike seed for paid; concierge / early access; loyalty upsell
- **Action**: `klaviyo-campaign-create` for early-access / private launches

### B. Recent first-time (the activation window)
- **Criteria**: `orders_count:1 AND created_at:>'<today minus 60d>'`
- **Use**: post-purchase nurture flow; "second order incentive" campaign
- **Action**: `klaviyo-flow-build` for second-order nudge sequence

### C. Lapsed one-timer (the win-back pool)
- **Criteria**: `orders_count:1 AND created_at:<'<today minus 1.5x median repeat cycle>'`
- **Use**: win-back flow with stronger offer
- **Action**: `klaviyo-flow-build` for win-back; possibly excluded from paid prospecting

### D. Dormant repeater (used to be active, now silent)
- **Criteria**: `orders_count:>=2 AND last_order_date:<'<today minus 2x median repeat cycle>'`
- **Use**: high-value win-back — these were good customers
- **Action**: stronger offer than C; consider a personal outreach for the top tier

### E. High-AOV / low-frequency (price-driven, infrequent)
- **Criteria**: `total_spent:>=<3x AOV> AND orders_count:<=2`
- **Use**: bundle / replenishment campaigns; subscription pitch if applicable
- **Action**: targeted "you might also like" upsell campaign

### F. Marketing-engaged but no purchase (warm leads)
- **Criteria**: `email_marketing_state:subscribed AND orders_count:0`
- **Use**: stronger first-purchase incentive; product-discovery flow
- **Action**: welcome flow audit; first-purchase incentive escalation

### Optional: Geo / channel sub-segments
For ads exclusions (don't re-prospect existing customers) or geo-specific campaigns.

## Steps

### 1. Pull headline counts for each segment

For each segment, run `list-customers` with the matching `query` filter, set `first: 1` to get the count without payload bloat. Then for sizing the activation opportunity, pull `first: 50` of the highest-priority ones for spot-check.

Example calls:

```
list-customers query: "orders_count:>=4 AND total_spent:>=400"
list-customers query: "orders_count:1 AND created_at:>'2026-03-07'"
list-customers query: "orders_count:1 AND created_at:<'2026-01-07'"
list-customers query: "orders_count:>=2 AND last_order_date:<'2026-01-07'"
list-customers query: "total_spent:>=300 AND orders_count:<=2"
list-customers query: "email_marketing_state:subscribed AND orders_count:0"
```

(Substitute real dates and dollar thresholds based on the brand's AOV and median repeat cycle.)

### 2. Estimate revenue opportunity per segment

For each segment:
- **Reactivation segments (C, D)**: opportunity = `count × historical_AOV × assumed_reactivation_rate (5-10%)`
- **Upsell segments (A, E)**: opportunity = `count × incremental_AOV (e.g., 0.5 × AOV) × adoption_rate (15-25%)`
- **Activation segments (B, F)**: opportunity = `count × first_purchase_AOV × conversion_lift (5-15%)`

These are rough. Caveat in the output that these are directional, not forecasts.

### 3. Pull a sample list per segment (first 50 by `total_spent` desc)

This lets the user eyeball the segment to confirm it's not absurd (e.g., the "VIP" segment shouldn't be all employees / wholesalers).

### 4. (Optional) Push to Klaviyo

If the user wants the segments live in Klaviyo:
- Klaviyo's segment definitions are different from Shopify queries — translate the criteria
- For each defined segment, draft the Klaviyo segment definition (in Klaviyo's filter syntax) and present for the user to paste, OR use the Klaviyo MCP if a `klaviyo_create_segment` tool exists
- (As of this skill version, Klaviyo MCP exposes `klaviyo_get_segments` but not create — confirm at runtime; if no create endpoint, output the definition for the user to add manually)

### 5. (Optional) Export for paid

For lookalike seeds:
- Pull email addresses for the VIP segment via `list-customers` + GraphQL
- Format as a CSV (one email per line)
- Save to `<repo>/segments/<segment-name>-<YYYY-MM-DD>.csv` for the user to upload to Meta / TikTok manually
- **Never** transmit the file to a third-party endpoint — the user uploads themselves

### 6. Output

```markdown
# Customer segments · <Brand> · <date>

## TL;DR
<2-3 sentences: total customers X, defined segments cover Y% of base, biggest opportunity is segment Z worth ~$W>

## Segment scoreboard

| Segment | Definition | Count | % of base | Est. opportunity | Recommended action |
|---|---|---|---|---|---|
| A. VIP | orders ≥ 4, spent ≥ $400 | … | … | $… | early access campaign |
| B. Recent first-time | 1 order, < 60d ago | … | … | $… | 2nd-order nudge flow |
| C. Lapsed one-timer | 1 order, > 60d ago | … | … | $… | win-back flow |
| D. Dormant repeater | ≥ 2 orders, dormant > 90d | … | … | $… | strong win-back + outreach |
| E. High-AOV low-freq | spent ≥ $300, ≤ 2 orders | … | … | $… | upsell / subscription pitch |
| F. Subscribed non-buyer | subscribed, 0 orders | … | … | $… | first-purchase incentive |

## Sample customers per segment
<5-10 examples per segment so the user can sanity-check>

## Recommendations
1. <Top action — usually the biggest-opportunity segment>
2. <Second action>
3. <Third action>

## How to apply

### In Klaviyo
<paste-ready segment definitions per segment>

### In Meta / TikTok ads
<which segments to use as lookalike seeds, which to exclude as suppression>

### In Shopify
<which segments to surface in admin via tags / metafields if useful>

## Caveats
- Counts are point-in-time — segments are dynamic and customers move between them
- Revenue estimates are directional, not forecasts
- For ads exclusion: re-pull the customer list before each campaign launch
```

### 7. Save

Write segment definitions to `<repo>/segments/segments-<YYYY-MM-DD>.md` for re-use.

## Cross-skill links

- `shopify-journey-cohort-retention` — provides the median repeat cycle for tuning lapsed thresholds
- `shopify-journey-acquisition` — channel × segment for paid suppression and prospecting
- `klaviyo-flow-build` — turn each segment into a flow trigger
- `klaviyo-campaign-create` — one-off campaign per segment
- `ads-campaign-create` — push VIP segment as a lookalike seed; push customer base as suppression
- `klaviyo-calendar-plan` — sequence segment campaigns across the year

## Tradeoffs

- **Static vs dynamic** — Shopify customer queries are dynamic (re-evaluated each call). Klaviyo segments can be either. For ads custom audiences, the export is a snapshot — re-export weekly to keep it fresh.
- **Segment sprawl** — More than ~8 segments becomes operationally painful. Keep the library tight; refine before adding.
- **Privacy** — Don't share the email list with third-party endpoints; let the user upload to ad platforms themselves. Storing the CSV locally is fine.
- **Threshold tuning** — The dollar / day thresholds in the default library are starting points. Recalibrate against the brand's AOV and median repeat cycle before reporting.

## Notes on the `query` filter dates

`list-customers` accepts ISO dates with `:>` / `:<`. Always convert relative ("60 days ago") to absolute ISO before calling. Today is whatever the runtime context says — see the `currentDate` system context.
