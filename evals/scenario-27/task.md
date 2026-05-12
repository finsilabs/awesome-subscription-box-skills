# Welcome Email Series for PawBox

## Problem/Feature Description

PawBox is a subscription box for dog owners. They've just launched and want to build an automated welcome series for new subscribers who join their Klaviyo email list. The series needs to feel like a warm introduction to the brand — not a generic sales push — and should drip out over several days to give new subscribers time to discover the brand before the first subscription pitch.

The brand's developer has already created two email templates in Klaviyo and has their template IDs: the first is a warm welcome email (template ID: `tmpl_welcome_01`) and the second is a "what's in your first box" reveal email (template ID: `tmpl_box_reveal_01`). The welcome series should send the welcome email immediately when someone joins the list, wait two days, then send the box reveal email.

The list ID for the main subscriber list is `list_pawbox_main`. The API key is available in `.env` as `KLAVIYO_API_KEY`.

## Output Specification

Produce `create_welcome_flow.py` — a Python script that creates this welcome series flow in Klaviyo via the Flows API.

The script should:
- Build the complete flow payload with both email steps and the time delay between them
- Create the flow via the Klaviyo API
- After creating the flow, query the API to verify the action graph was created correctly
- Print the flow ID and a confirmation that the action count matches expectations

Include enough comments in the script that a developer unfamiliar with the Klaviyo Flows API can understand the payload structure.
