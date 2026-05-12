# Weekly Ads Performance Review for RunBox

## Problem/Feature Description

RunBox is a monthly subscription box for runners, featuring gear, nutrition samples, and training accessories. Their paid social campaigns on Meta have been running for three weeks, and this is the second weekly performance review. The marketing manager wants to know what's working, what's not, and what the team should do in the next 7 days.

The campaign performance data for the past 7 days has been pulled from Meta Ads and saved to `inputs/campaign_metrics.json`. The file contains metrics for four active ad sets — two prospecting and two retargeting — along with industry benchmark ranges for reference.

The marketing manager has a $300/day total budget and is specifically wondering: are any ad sets ready to scale, and are any dragging down overall ROAS to the point where they should be paused? They also want to understand the root cause of the underperformance so the team can brief the creative team correctly.

## Output Specification

Using the data in `inputs/campaign_metrics.json`, produce a weekly ads performance report at `ads-reports/2026-05-12.md`. The report should:

- Summarize overall campaign performance with key headline metrics
- Identify what's working and what's not, with specific ad-set-level findings
- Apply a systematic bottleneck diagnosis to explain the root cause of any underperformance
- Make clear scaling and pausing recommendations based on the data, with the specific thresholds that justify each decision
- Provide prioritized next actions for the team (P0, P1, P2)
