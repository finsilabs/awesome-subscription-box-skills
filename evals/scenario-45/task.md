# Customer Retention Analysis for BloomBox

## Problem/Feature Description

BloomBox is a monthly floral subscription box that has been operating for 18 months. The founder is evaluating whether to increase paid acquisition spend but wants to validate the unit economics first — specifically, whether newly acquired customers actually come back for a second and third order, and how long it takes them to do so.

The operations team has exported customer and order data from the Shopify store into the `inputs/` directory. The data includes individual customer records with their full order history, plus a weekly trend of the returning customer rate over the last six months.

The founder wants to understand: how well are customers being retained by acquisition month, how fast do they come back, what does lifetime value look like at different time horizons, and how large is the lapsed customer pool? This analysis will directly inform the email team's post-purchase flow sequencing and the paid team's CAC target.

## Output Specification

Using the data in `inputs/customers.json` and `inputs/returning_customer_rate.json`, produce a cohort retention report at `journey-reports/cohort-retention-2026-05-12.md`. The report should include:

- A headline summary of returning customer rate and key retention metrics
- A cohort-level breakdown by acquisition month with repeat purchase rates at multiple time intervals
- A distribution of how long customers take to place their second order
- Lifetime value estimates by cohort
- A pool estimate for customers who haven't reordered in a meaningful window
- Prioritized recommendations for the email and paid teams
