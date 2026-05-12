---
name: shopify-journey-segments
description: Use this skill when the user wants to define actionable customer segments on their Shopify store and pipe them to Klaviyo or ads — phrases like "build customer segments", "find my VIPs", "win-back segment", "high-value customers", "lapsed customers", "create a segment for ads". Defines named segments (VIP, lapsed one-timer, recent first-time, high-AOV-low-frequency, dormant), counts each, and outputs definitions ready to recreate in Klaviyo or push as a custom audience.
---

# Shopify journey segments

Translate raw customer data into a small set of named, actionable segments. Each segment has a clear definition, a count, an estimated revenue opportunity, and a recommended next action (a Klaviyo flow, a campaign, or a paid lookalike seed).

## Prerequisites

- Shopify MCP connected (`mcp__9bf46487-...__list-customers`, `graphql_query`)
- (Optional) Klaviyo MCP if pushing the segment definitions over
- Brand-specific repeat cycle from `shopify-journey-cohort-retention` (informs lapsed thresholds)

## The default segment library

Six segments cover ~95% of activation needs. Tune dollar and day thresholds to the brand's AOV and median repeat cycle.

### A. VIP (top spenders, highly engaged)
- **Criteria**: `orders_count:>=4 AND total_spent:>=<2x AOV × 4>`
- **Action**: `klaviyo-campaign-create` for early-access / private launches; lookalike seed for paid

### B. Recent first-time (the activation window)
- **Criteria**: `orders_count:1 AND created_at:>'<today minus 60d>'`
- **Action**: `klaviyo-flow-build` for second-order nudge sequence

### C. Lapsed one-timer (the win-back pool)
- **Criteria**: `orders_count:1 AND created_at:<'<today minus 1.5x median repeat cycle>'`
- **Action**: `klaviyo-flow-build` for win-back; possibly excluded from paid prospecting

### D. Dormant repeater (used to be active, now silent)
- **Criteria**: `orders_count:>=2 AND last_order_date:<'<today minus 2x median repeat cycle>'`
- **Action**: stronger offer than C; consider personal outreach for the top tier

### E. High-AOV / low-frequency (price-driven, infrequent)
- **Criteria**: `total_spent:>=<3x AOV> AND orders_count:<=2`
- **Action**: bundle / replenishment campaign; subscription pitch if applicable

### F. Marketing-engaged but no purchase (warm leads)
- **Criteria**: `email_marketing_state:subscribed AND orders_count:0`
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

**Validation checkpoint**: If the sample looks wrong (e.g., wholesalers or staff dominate VIP, or lapsed counts seem implausibly high), adjust the relevant thresholds and re-run from Step 1 before proceeding. Common fixes: raise the `total_spent` floor to exclude wholesale accounts, or tighten the date window if the lapsed pool is larger than the active base.

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

Write a report to `<repo>/segments/segments-<YYYY-MM-DD>.md` using this structure:

- **TL;DR** — 2-3 sentences: total customers, % of base covered by segments, biggest single opportunity.
- **Segment scoreboard** — table with columns: Segment | Definition | Count | % of base | Est. opportunity | Recommended action.
- **Sample customers per segment** — 5-10 examples per segment for sanity-checking.
- **Recommendations** — top 3 prioritised actions (usually ordered by estimated opportunity).
- **How to apply** — three sub-sections: Klaviyo (paste-ready segment definitions), Meta / TikTok ads (lookalike seeds + suppression lists), Shopify (tag / metafield surfacing if useful).
- **Caveats** — note that counts are point-in-time, revenue estimates are directional, and ads exclusion lists should be re-pulled before each campaign launch.

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

## Notes on the `query` filter dates

`list-customers` accepts ISO dates with `:>` / `:<`. Always convert relative ("60 days ago") to absolute ISO before calling. Today is whatever the runtime context says — see the `currentDate` system context.
