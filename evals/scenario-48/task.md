# VIP Customer Export for Lookalike Advertising — GloBox

## Problem/Feature Description

GloBox is a monthly glow-up subscription box for skincare enthusiasts. Their paid social team is about to launch a prospecting campaign on Meta and wants to seed their lookalike audiences with the highest-quality customers — those who have placed multiple orders and represent the top of the customer pyramid.

The analytics lead has pulled the VIP customer list from Shopify and saved it to `inputs/vip_customers.json`. This file contains 143 VIP customers with their email addresses and order history.

The paid social team needs a clean email list formatted for upload to Meta Ads Manager's Custom Audience tool. The marketing team also wants a clear record of the export so they can repeat it monthly without confusion.

## Output Specification

Using the data in `inputs/vip_customers.json`, produce two outputs:

1. A CSV file at `segments/vip-2026-05-12.csv` containing one email address per line, suitable for upload to Meta Ads Manager as a custom audience seed (no headers needed — just emails, one per line)
2. A brief summary at `segments/segments-2026-05-12.md` documenting the VIP segment definition, the count of customers exported, and how the team should use this file (upload manually to Meta/TikTok — do not share via API or third-party tools)

The paid team will handle the upload themselves.
