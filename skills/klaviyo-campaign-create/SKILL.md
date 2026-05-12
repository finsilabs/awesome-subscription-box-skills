---
name: klaviyo-campaign-create
description: Use this skill when the user wants to create a Klaviyo email campaign (one-off send) aligned to a brand's voice and theme — phrases like "create a Klaviyo campaign", "set up a launch email", "send a Black Friday blast", "make a campaign in Klaviyo". Generates campaign ideas if needed, builds the email template, and pushes the campaign as a draft via the Klaviyo API.
---

# Klaviyo campaign creator

Build a brand-voice-aligned email campaign in Klaviyo: pick the angle, write the copy, generate a template, attach it to a campaign, schedule it. The campaign is created in DRAFT — user reviews and clicks Send.

## When to use

- One-off email sends (launch, holiday, new product, win-back blast)
- Brainstorming campaign ideas based on the brand's positioning
- Building a campaign from a brand-voice-vault entry

## Prerequisites

- `KLAVIYO_API_KEY` in `.env` with template/campaign write scopes
- Klaviyo Account → Default sender email is verified
- Brand voice vault at `~/.claude/brand-voice-vault/<brand>/` recommended

## Steps

### 1. Decide on the angle (if not given)

If the user hasn't specified, suggest 3-5 campaign angles based on the brand context. Examples for a subscription-box brand:

| Angle | Trigger / time |
|---|---|
| Launch / open-order | Pre-launch + day-of launch |
| Curation reveal | The day a new month's box is announced |
| Seasonal (BFCM, Father's Day, Holiday) | Calendar-based |
| Audience-segment story (e.g., "for the guy who track-days") | Quarterly |
| Founder note (low-frequency, high-impact) | Once or twice a year |
| Member-only drop | Inventory-driven |
| "What's coming next month" | Monthly cadence |
| Customer story / unboxing roundup | Monthly |
| Black Friday / Cyber Monday / Boxing Day | Annual |

Each angle gets a one-line "why this works for the brand" rationale.

### 2. Read brand voice

Load from `~/.claude/brand-voice-vault/<brand>/` if it exists:
- `voice.md` for tone, vocabulary
- `principles.md` for the brand position
- `examples/source-quotes.md` for phrasing patterns

### 3. Draft the email

Email body structure that works for most campaigns:

```
1. Subject line (under 50 chars)
2. Preview text (under 100 chars, doesn't repeat subject)
3. Hero (1-line headline + 1-2 sentence opening)
4. The point (1-3 paragraphs, ~300 words total)
5. Single CTA button (action-oriented label)
6. Sign-off + secondary link (e.g., "questions? hit reply")
```

Voice rules — same as `shopify-blog-post` skill:
- Concrete first lines, not "in today's fast-paced world"
- Active voice
- Match the brand's typical reading level

### 4. Build the HTML template

Use the same shell as the brand's existing email templates if any exist. If starting fresh, follow the pattern in `~/dev/gearheadbox/scripts/generate_email_templates.py`:

```python
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
def render(*, preview_text, heading, body_html, cta_label, cta_url, ...):
    return f"""<!DOCTYPE html>
    <html lang="en">
    <head>...</head>
    <body style="background:{COLORS['page']};...">
      <table>... brand header ...</table>
      <table>... body content ...</table>
      <table>... brand footer with {{% unsubscribe %}} ...</table>
    </body>
    </html>"""
```

Key inclusions:
- `{% unsubscribe 'Unsubscribe' %}` tag (Klaviyo will reject without it)
- Postal address in footer (CAN-SPAM)
- Hidden preview-text div at top of body

### 5. Push the template + campaign via API

Endpoint: `POST https://a.klaviyo.com/api/templates/` (template), `POST /api/campaigns/` (campaign), `POST /api/campaign-message-assign-template/` (link them).

Pattern in `~/dev/gearheadbox/scripts/klaviyo_push_campaigns.py`:

```python
# Headers
headers = {
    "Authorization": f"Klaviyo-API-Key {api_key}",
    "revision": "2025-10-15",
    "Accept": "application/json",
    "Content-Type": "application/json",
}

# 1. Create template (POST /api/templates/) — get template_id
# 2. Create campaign (POST /api/campaigns/) — pass message with subject/preview/from
# 3. Assign template (POST /api/campaign-message-assign-template/) with relationship
```

Critical schema details:
- `send_strategy.method` = `"static"` and `datetime` (ISO 8601)
- `audiences.included` = `[<list_id>]`, `audiences.excluded` = optional
- `tracking_options.add_tracking_params` = `true`
- Campaign-message `attributes.definition.content` holds subject/preview/from_email/from_label

### 6. Output for the user

Show:
- Campaign ID + Klaviyo URL (`https://www.klaviyo.com/campaign/<id>`)
- Subject and preview text
- Send time (placeholder if not given)
- Template ID it's pointing at
- Reminder: the campaign is in DRAFT, user must click Send in Klaviyo UI

## Send time guidance

- Tuesday / Wednesday / Thursday tend to outperform Mon / Fri
- 9am–11am local time is the sweet spot for most B2C
- BFCM and time-pressure sends: 9am Eastern is the standard
- Anniversary / story sends: Sunday morning works (low promo competition)
- Avoid: Sundays before noon, holidays themselves (send before)

## Cross-skill links

- `brand-voice-extract` → vault is the voice source of truth
- `klaviyo-calendar-plan` → larger calendar context
- `klaviyo-flow-build` → if this triggered behavior should become a recurring flow, not a one-off

## Tradeoffs

- **One-off campaign vs. recurring flow** — campaigns send once to a static audience. Flows trigger continuously based on events. Use a campaign for time-bound moments (launches, holidays); use a flow for "every customer who does X gets Y."
- **Template per campaign vs. master template** — for high-volume sends, use a master template with editable regions. For 1-2 campaigns/month, separate templates are fine and easier to debug.

## Reference example

`~/dev/gearheadbox/scripts/klaviyo_push_campaigns.py` creates the "GHB · Launch announcement" campaign for August 4, 2026, with template attached, in draft.

## Embedded in this skill folder

Scripts (copy to your project's `scripts/` directory and run with `uv run`):
- `scripts/generate_email_templates.py`
- `scripts/klaviyo_push_campaigns.py`
- `scripts/klaviyo_push_templates.py`

Reference templates / examples (copy or adapt):
- `examples/01_newsletter_welcome.html`
