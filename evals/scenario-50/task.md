# Mid-Test Review for FitBox Hook A/B Test

## Problem/Feature Description

FitBox is a monthly subscription box for fitness enthusiasts. Their growth team launched a creative A/B test on Meta on May 7th, testing three different ad hook variants to find the best-performing creative for prospecting campaigns. The test has now been running for 5 days and the marketing manager is getting pressure from leadership to declare a winner and double down on the best ad.

The performance data for the three variants has been exported to `inputs/ab_test_metrics.json`. The manager wants a clear recommendation: which hook is winning, should they pause the losers and scale the winner now, and what would the analysis look like once they do have enough data?

## Output Specification

Using the data in `inputs/ab_test_metrics.json`, produce an ads performance report at `ads-reports/2026-05-12.md`. The report should:

- Review the current performance of all three hook variants against the target CPA and ROAS
- Make a clear recommendation about whether it's appropriate to act on this data right now
- Explain the conditions under which the team should take action — whether that means pausing, scaling, or waiting
- Highlight which variant is currently leading and why, even if the data isn't yet conclusive
- Provide a prioritized action list (P0, P1, P2)
