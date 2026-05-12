# Customer Segment Report for SpiceBox

## Problem/Feature Description

SpiceBox is a monthly spice and recipe subscription box that has built up a customer base of 3,840 customers over two years. The marketing team is about to invest in a series of lifecycle email campaigns and wants to know exactly who they're talking to before building the flows in Klaviyo. They also want to know which segments to prioritize for paid social lookalike audiences.

The team's analytics lead has already run the Shopify customer queries and exported the results into `inputs/segment_counts.json`, along with brand configuration (AOV, median repeat cycle) in `inputs/brand_config.json`. Using this data, produce a complete customer segmentation report that the team can take directly into their campaign planning.

The marketing director has asked for three things: (1) a clear scoreboard of all customer segments with sizes and estimated revenue opportunity, (2) guidance on how to recreate each segment in Klaviyo for email targeting, and (3) direction on which segments to use for paid social (lookalike seeds and suppression audiences).

## Output Specification

Produce the segment report at `segments/segments-2026-05-12.md`. The report should include:

- A segment scoreboard table covering all named customer segments with their definition, count, estimated revenue opportunity, and recommended action
- A "How to apply" section with subsections for Klaviyo, paid social (Meta/TikTok), and Shopify admin
- Sample customers listed for each segment so the team can sanity-check the segment composition
- A brief TL;DR and ranked list of recommended actions

Use the brand's AOV and median repeat cycle from the config file to calibrate all thresholds and opportunity estimates.
