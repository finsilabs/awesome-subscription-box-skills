# Father's Day Email Campaign for GearHead Box

## Problem/Feature Description

GearHead Box is a monthly subscription box for motorsport enthusiasts, curating performance car accessories, trackday gear, and automotive collectibles. Father's Day is approaching, and the brand wants to capitalise on the gifting moment with a targeted email campaign aimed at their subscriber list.

The marketing manager wants a Father's Day campaign created as a Klaviyo draft, ready for internal review before scheduling. She needs both the email content and the technical implementation. The campaign should position the Apex tier ($99/mo) as the ideal gift for the automotive-obsessed dad. The Klaviyo account ID and list ID are available in the `.env` file. The campaign should be scheduled for 9am Eastern on a suitable weekday closest to Father's Day (June 15, 2026).

## Output Specification

Produce two files:

1. `campaign_fathers_day.html` — the full HTML email template, ready to upload to Klaviyo
2. `push_campaign.py` — a Python script that creates the email template in Klaviyo, creates the campaign, and links them together using the Klaviyo API

The HTML template should be complete and immediately usable. The Python script should follow the three-step pattern: create template → create campaign → assign template to campaign. The campaign should be set to send to the main email list and not yet published — the marketing manager will review and activate it herself in the Klaviyo dashboard.

Include a comment in `push_campaign.py` showing the Klaviyo dashboard URL pattern where the campaign will appear after creation.
