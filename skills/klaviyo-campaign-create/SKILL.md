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

If the user hasn't specified, suggest 3-5 campaign angles based on the brand context (e.g., launch/open-order, seasonal, curation reveal, founder note, member-only drop, customer story). For each angle provide a one-line "why this works for the brand" rationale.

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

Apply tone and vocabulary directly from the brand voice vault loaded in Step 2. No generic defaults — let the vault files drive all copy decisions.

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

**Before pushing, validate the rendered HTML:**
- Confirm `{% unsubscribe` appears in the template string — abort with a clear error if missing.
- Confirm a postal address block is present in the footer.
- Log a warning if the rendered HTML is under 500 chars (likely a render failure).

### 5. Push the template + campaign via API

Run `uv run scripts/klaviyo_push_campaigns.py --name '<campaign_name>' --list-id '<list_id>' --subject '<subject>' --preview '<preview_text>' --from-email '<verified_sender>' --from-label '<sender_name>' --send-at '<ISO-8601>'`

The script handles three sequential API calls: `POST /api/templates/` → `POST /api/campaigns/` → `POST /api/campaign-message-assign-template/`. See `~/dev/gearheadbox/scripts/klaviyo_push_campaigns.py` for the full implementation.

Critical schema details required by the API:
- `send_strategy.method` = `"static"` and `datetime` (ISO 8601)
- `audiences.included` = `[<list_id>]`, `audiences.excluded` = optional
- `tracking_options.add_tracking_params` = `true`
- Campaign-message `attributes.definition.content` holds subject/preview/from_email/from_label
- API revision header: `"2025-10-15"`

### 6. Output for the user

Show:
- Campaign ID + Klaviyo URL (`https://www.klaviyo.com/campaign/<id>`)
- Subject and preview text
- Send time (placeholder if not given)
- Template ID it's pointing at
- Reminder: the campaign is in DRAFT, user must click Send in Klaviyo UI

## Cross-skill links

- `brand-voice-extract` → vault is the voice source of truth
- `klaviyo-calendar-plan` → larger calendar context
- `klaviyo-flow-build` → if this triggered behavior should become a recurring flow, not a one-off

## Reference example

`~/dev/gearheadbox/scripts/klaviyo_push_campaigns.py` creates the "GHB · Launch announcement" campaign for August 4, 2026, with template attached, in draft.

## Embedded in this skill folder

Scripts (copy to your project's `scripts/` directory and run with `uv run`):
- `scripts/generate_email_templates.py`
- `scripts/klaviyo_push_campaigns.py`
- `scripts/klaviyo_push_templates.py`

Reference templates / examples (copy or adapt):
- `references/01_newsletter_welcome.html`
