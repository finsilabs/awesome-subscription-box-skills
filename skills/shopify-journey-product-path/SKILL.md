---
name: shopify-journey-product-path
description: Use this skill when the user wants to understand how products participate in the customer journey — phrases like "what's my entry product", "which products bring people in", "what drives the second purchase", "product affinity", "merchandising review", "which products are dead ends". Identifies entry products (most common first-purchase), repeat-driver products (correlate with a second order), dead-end products (high first-purchase but no repeat), and cross-sell pairs.
---

# Shopify journey product path

A product-level lens on the customer journey: which SKUs serve as **entry points** (the first thing customers buy), which are **repeat drivers** (the customers who bought X are the most likely to come back), and which are **dead ends** (high first-purchase share but low repeat). The output drives merchandising, PDP investment, and post-purchase upsell decisions.

## When to use

- Annual / quarterly merchandising review
- Before a launch — figure out which existing product to pair with the new one
- "Which products should we promote in paid?" — entry products usually have higher new-customer ROAS
- After cohort retention shows decay — find which SKUs to push for the second purchase
- Subscription / consumables: which entry SKU produces the best LTV?

## Prerequisites

- Shopify MCP connected (`run-analytics-query`, `graphql_query`, `search_products`)
- Store has ≥ 60 days of order history with multiple SKUs
- Ideally ≥ 200 customers with 2+ orders for repeat-driver signal

## Steps

### 1. Top products by gross revenue (baseline)

```
FROM sales
SHOW gross_sales, net_sales, orders
GROUP BY product_title
ORDER BY gross_sales DESC LIMIT 20
SINCE -90d UNTIL today
```

This is the merchandising baseline — what's selling, full stop.

### 2. New-customer entry products

The cleanest cut: which products are most often in a customer's **first** order? Drop to GraphQL because ShopifyQL doesn't natively split by first-vs-repeat order in all stores:

```graphql
query FirstOrders($cursor: String) {
  customers(first: 50, query: "orders_count:>=1", after: $cursor) {
    pageInfo { hasNextPage endCursor }
    edges {
      node {
        id
        createdAt
        orders(first: 1, sortKey: CREATED_AT) {
          edges {
            node {
              createdAt
              lineItems(first: 10) {
                edges { node { title quantity originalUnitPriceSet { shopMoney { amount } } } }
              }
            }
          }
        }
      }
    }
  }
}
```

Aggregate: `entry_count[product] = number of customers whose first order contained that product`. Sort desc.

For large stores (> 50k customers), sample to 1000 random customers and document the sampling.

### 3. Repeat-driver products (which entry SKU correlates with a 2nd order)

Same query, but join in `numberOfOrders > 1`:

For each product in the entry list:
- `entry_customers_count` (from step 2)
- `repeat_customers_count` = customers whose first order contained X **and** who later placed a second order
- `repeat_lift` = `repeat_customers_count / entry_customers_count`

Output column `repeat_lift` ranks SKUs by how well they "convert" a first-time buyer into a repeat customer.

| Product | First orders | Repeated | Repeat % | vs avg |
|---|---|---|---|---|
| Apex Box | 412 | 178 | 43% | +12 pp |
| Sticker Pack | 89 | 11 | 12% | -19 pp |

A product with high entry count but low repeat % is a **dead end** (it brings people in but they don't come back). A product with merely OK entry count and high repeat % is a **hidden gem** — promote it.

### 4. Cross-sell affinity (what gets bought next)

For customers with ≥ 2 orders, compute the most common second-order product per first-order product:

```
For each customer:
  first_skus = lineItems(orders[0])
  second_skus = lineItems(orders[1])
  for each (a, b) in cross(first_skus, second_skus):
    affinity[a → b] += 1
```

Top cross-sell pairs feed:
- Post-purchase upsell (`klaviyo-flow-build`)
- Bundles / collections (`shopify-product-with-images`, `add-to-collection`)
- Recommendations on PDPs

### 5. Dead-end inventory (product is purchased but customer never returns)

Sort the entry-list table by `repeat % ASC` and surface the bottom 5 with high entry counts. These are the products that bring people in but kill repeat. Possible causes:

| Cause | Signal | Fix |
|---|---|---|
| Quality issue | bad reviews on that SKU | product fix or sunset |
| Wrong audience | acquired via discount paid social | rethink that ad targeting |
| One-and-done by nature (gift, novelty) | seasonal pattern | accept; pair with a repeat-driver in the same order |
| Underpriced (low margin → no follow-up offer) | low AOV | bundle with a repeat-driver |

### 6. Channel × product (where do entry products come from)

Cross with acquisition data:

```
FROM sales
SHOW orders, gross_sales
GROUP BY product_title, order_referrer_source
ORDER BY orders DESC LIMIT 50
SINCE -90d UNTIL today
```

If 70% of "Apex Box" first orders come from one channel, double down there. If a product has flat distribution across channels, it has broad appeal — different ad strategy.

### 7. Output

```markdown
# Product path · <Brand> · <date range>

## TL;DR
<2-3 sentences: top entry product is X, biggest repeat driver is Y, biggest dead end is Z>

## Top products by revenue (baseline)
| Product | Orders | Gross sales | % of revenue |
|---|---|---|---|

## Entry products (first orders only)
| Product | First orders | % of new customers |
|---|---|---|

## Repeat drivers (first-order SKU → likelihood of 2nd order)
| Product | First orders | Repeated | Repeat % | vs avg |
|---|---|---|---|---|

## Hidden gems
<products with above-average repeat %, under-promoted in current merchandising>

## Dead ends
<products with high entry count but below-average repeat %; suspected cause; suggested fix>

## Cross-sell affinity
| First-order product | Most common 2nd-order product | Lift |
|---|---|---|

## Channel × entry product
<which channels acquire each top entry product disproportionately>

## Recommendations (prioritized)

### P0 — Merchandising
1. <Action>

### P1 — Marketing
1. <Action>

### P2 — Product roadmap
1. <Action>

## Caveats
- Sampled to <N> customers if store > 50k — directional signal, not exact
- Cross-sell affinity needs ≥ 30 pairs per cell to be meaningful
- Subscription renewals filtered out (if applicable) to avoid false repeat inflation
```

### 8. Save

Write to `<repo>/journey-reports/product-path-<YYYY-MM-DD>.md`.

## Cross-skill links

- `shopify-journey-cohort-retention` — pairs with this; cohort tells you "do they repeat", this tells you "what makes them repeat"
- `shopify-journey-acquisition` — channel × entry product cross
- `shopify-journey-segments` — bundle "bought entry product X but didn't repeat" as a segment for win-back
- `klaviyo-flow-build` — sequence post-purchase flow with cross-sell affinity products
- `shopify-product-with-images` — promote hidden gems with better PDP imagery
- `add-to-collection` — build "best for first-time buyers" or "you might also like" collections from this analysis
- `ads-campaign-create` — run paid against entry products with the best repeat lift

## Tradeoffs

- **Sampling vs accuracy** — For stores with > 50k customers, full GraphQL traversal is slow. Sampling 1k random customers gives directional accuracy on top products but noise on long-tail SKUs. Always document the sample size in the report.
- **Bundle / multi-SKU first orders** — If most first orders contain 3+ SKUs, attribution to a single "entry product" gets fuzzy. Use the most-expensive line item in the order as the proxy entry product, OR aggregate at category level instead of SKU level.
- **Subscription / consumables stores** — Filter out auto-renewal orders (e.g., by `tag:subscription` or `source_name`) before computing repeat %. Otherwise every SKU that's on subscription will look like a "repeat driver" artificially.
- **Seasonality** — A product that's a holiday-only entry product will look weak on a 90-day window outside its season. Sanity check long-tail signals against the calendar.

## Quick interpretation rules

- Entry product with **high repeat %** → invest in it (paid, PDP, supply)
- Entry product with **low repeat %** but high volume → fix the post-purchase experience or sunset paid promotion of it
- Hidden gem (low entry count, high repeat %) → boost discoverability (feature on homepage, promote in email)
- Cross-sell pair with > 3x lift over base rate → put it in the post-purchase flow this week
