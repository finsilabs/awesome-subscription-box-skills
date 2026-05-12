# Channel Revenue Attribution Report for SnackHaven

## Problem/Feature Description

SnackHaven is a subscription snack box that has been running for 18 months and currently acquires customers across paid social, organic search, email, and direct traffic. The head of growth is preparing for a quarterly marketing budget review and needs a clear picture of which channels are actually driving quality revenue — not just traffic volume — so the team can make a defensible case for where to shift spend.

The analytics team has already pulled the raw ShopifyQL outputs from the store into JSON files in the `inputs/` directory. The data covers the last 30 days and includes session counts, conversion rates, order counts, revenue, and average order value broken down by referral source, individual named sources, and weekly trends.

The growth team is particularly worried that their paid social budget may be underperforming — they see lots of social sessions but aren't sure if those visitors actually convert. They also suspect email is quietly outperforming its perceived role.

## Output Specification

Using the analytics data in `inputs/`, produce a channel attribution report at `journey-reports/acquisition-2026-05-12.md`. The report should give the team a complete picture of channel quality and clear, prioritized actions. Include a summary of which channels are rising or declining in traffic volume over the 8-week trend period.

The report should be immediately actionable for a budget reallocation meeting — covering what's working, what's broken, and a ranked list of recommended actions.
