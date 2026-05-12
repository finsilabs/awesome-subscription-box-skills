---
name: shopify-journey-product-path
description: Use this skill when the user wants to understand how products participate in the customer journey — phrases like "what's my entry product", "which products bring people in", "what drives the second purchase", "product affinity", "merchandising review", "which products are dead ends". Identifies entry products (most common first-purchase), repeat-driver products (correlate with a second order), dead-end products (high first-purchase but no repeat), and cross-sell pairs.
---

# Shopify journey product path

A product-level lens on the customer journey: which SKUs serve as **entry points** (the first thing customers buy), which are **repeat drivers** (the customers who bought X are the most likely to come back), and which are **dead ends** (high first-purchase share but low repeat). The output drives merchandising, PDP investment, and post-purchase upsell decisions.

## When to use

- Annual / quarterly merchandising review, or before a launch to identify pairing opportunities
- "Which products should we promote in paid?" — entry products usually have higher new-customer ROAS
- After cohort retention shows decay — find which SKUs to push for the second purchase

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

**Validation:** If the query returns 0 rows, confirm the store has sales data in the last 90 days and that the MCP connection is authenticated. If fewer than 5 distinct products appear, note this in the report — analysis will be directional only.

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

**Validation:** Before proceeding, verify that at least 100 customers were returned and that line items are populated. If `lineItems` is empty for most customers, check store permissions for the `read_orders` scope. If the total customer count is below 200, note in the report that repeat-driver signal will be weak.

### 3. Repeat-driver products (which entry SKU correlates with a 2nd order)

Fetch first **and** second orders together for each customer, then compute repeat lift per entry product:

```graphql
query FirstAndSecondOrders($cursor: String) {
  customers(first: 50, query: "orders_count:>=1", after: $cursor) {
    pageInfo { hasNextPage endCursor }
    edges {
      node {
        id
        numberOfOrders
        orders(first: 2, sortKey: CREATED_AT) {
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

Paginate through all customers (or the 1k sample). For each customer, `orders.edges[0]` is the first order and `orders.edges[1]` (if present) is the second. Then compute:

- `entry_customers_count[product]` — customers whose first order contained that product
- `repeat_customers_count[product]` — subset of those where `numberOfOrders >= 2`
- `repeat_lift[product]` = `repeat_customers_count / entry_customers_count`
- `avg_repeat_lift` = total customers with ≥ 2 orders / total customers

Output column `repeat_lift` ranks SKUs by how well they "convert" a first-time buyer into a repeat customer.

| Product | First orders | Repeated | Repeat % | vs avg |
|---|---|---|---|---|
| Apex Box | 412 | 178 | 43% | +12 pp |
| Sticker Pack | 89 | 11 | 12% | -19 pp |

A product with high entry count but low repeat % is a **dead end** (it brings people in but they don't come back). A product with merely OK entry count and high repeat % is a **hidden gem** — promote it.

**Validation:** If fewer than 200 customers have `numberOfOrders >= 2`, flag the repeat-driver results as low-confidence in the report. If pagination returns errors (e.g., rate limits), implement exponential backoff and resume from the last valid `endCursor`.

### 4. Cross-sell affinity (what gets bought next)

Reuse the paginated `FirstAndSecondOrders` results from step 3. For each customer with ≥ 2 orders, emit every (first-SKU → second-SKU) pair:

```graphql
# No additional query needed — use the step 3 results already paginated.
# For each customer node where orders.edges.length >= 2:
#   first_skus  = orders.edges[0].node.lineItems.edges[*].node.title
#   second_skus = orders.edges[1].node.lineItems.edges[*].node.title
#   for a in first_skus:
#     for b in second_skus:
#       affinity[a][b] += 1
#
# lift(a→b) = affinity[a][b] / entry_customers_count[a]
#           / (total_second_order_appearances[b] / total_repeat_customers)
```

Sort each `a`-row by `lift` descending; surface the top cross-sell pair per entry product. Require ≥ 30 pairs per cell before reporting lift — below that threshold flag as "insufficient data".

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

**Validation:** If `order_referrer_source` is null for > 50% of rows, note that channel attribution is incomplete and treat channel × product findings as directional only.

### 7. Output

Write the report using the template at `journey-reports/product-path-template.md`. Save the completed report to `<repo>/journey-reports/product-path-<YYYY-MM-DD>.md`. The template covers: TL;DR, top products by revenue, entry products, repeat drivers, hidden gems, dead ends, cross-sell affinity, channel × entry product, prioritized recommendations (P0/P1/P2), and caveats (sample size, minimum cell counts, subscription filtering).

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
- **Bundle / multi-SKU first orders** — If most first orders contain 3+ SKUs, use the most-expensive line item as the proxy entry product, or aggregate at category level instead of SKU level.
- **Subscription / consumables stores** — Filter out auto-renewal orders (e.g., by `tag:subscription` or `source_name`) before computing repeat %; otherwise subscription SKUs will appear as artificial repeat drivers.

## Quick interpretation rules

- Entry product with **high repeat %** → invest in it (paid, PDP, supply)
- Entry product with **low repeat %** but high volume → fix the post-purchase experience or sunset paid promotion of it
- Hidden gem (low entry count, high repeat %) → boost discoverability (feature on homepage, promote in email)
- Cross-sell pair with > 3x lift over base rate → put it in the post-purchase flow this week
