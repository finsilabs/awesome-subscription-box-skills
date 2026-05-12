# Post-Purchase Feedback Flow for GreenLeaf Organics

## Problem/Feature Description

GreenLeaf Organics ships a monthly organic snack subscription box. They want to follow up with customers after every order to collect feedback and encourage a second order from first-time buyers. Their head of retention wants to set up an automated Klaviyo flow that fires after a customer places an order.

The flow should wait 10 days after the order is placed (long enough for the box to arrive and be opened), then send a feedback and "what's coming next month" email. The template for this email has already been created in Klaviyo with ID `tmpl_postpurchase_feedback`. The metric that should trigger the flow is the "Placed Order" metric, which has Klaviyo metric ID `R4HMGZ`.

The Klaviyo API key is in `.env` as `KLAVIYO_API_KEY`. The from email is `hello@greenleaforganics.com` and the from label is "GreenLeaf Organics".

## Output Specification

Produce `create_postpurchase_flow.py` — a Python script that creates this post-purchase flow in Klaviyo.

The script should:
- Build the flow payload with the correct trigger, time delay, and email send step
- Create the flow via the Klaviyo API
- Print the resulting flow ID to stdout

The script should handle the case where the API returns a 429 rate-limit response and retry appropriately.
