# Conversion Funnel Audit for PetBox Subscription

## Problem/Feature Description

PetBox is a monthly subscription box for pet owners with three tiers (cat, small dog, large dog). The team has been running a steady $8,000/month paid social budget for the past two months and is now preparing to evaluate whether to double it. Before committing to the spend increase, the founder wants a thorough audit of the store's conversion funnel to ensure they're not paying to send traffic into a leaky store.

The analytics team has pulled the most recent 30-day funnel data from Shopify into the `inputs/` directory. The data includes aggregate funnel stage counts, a device breakdown, and a week-over-week comparison against the prior 30-day period.

The founder is particularly concerned about mobile performance — a large portion of their paid social audience browses on mobile, and they have a nagging suspicion the mobile experience may be hurting conversions. They want to know exactly where people are dropping off and what to fix first.

## Output Specification

Using the data files in `inputs/`, produce a conversion funnel report at `journey-reports/funnel-2026-05-12.md`. The report should:

- Show the full funnel with stage-to-stage conversion rates and how they compare to industry norms
- Identify the single biggest drop-off point and quantify the revenue being lost there each month
- Surface any meaningful patterns in the device or period-over-period data
- Provide a prioritized list of fixes, with the most urgent items at the top
