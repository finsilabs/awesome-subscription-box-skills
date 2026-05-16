---
name: klaviyo-flow-build
description: Use this skill when the user wants to create complex multi-step Klaviyo flows via API — phrases like "build a Klaviyo flow", "set up multi-step welcome series", "create abandoned cart flow", "configure Klaviyo flow", "automate emails on event X". Creates flows with full action graphs (triggers + time delays + send-email + branching) using Klaviyo's stable Flows API at revision 2025-04-15.
---

# Klaviyo flow builder (multi-step, end-to-end)

Build complete Klaviyo flows via API — including time delays, multiple email steps, conditional branches — in DRAFT status, ready for the user to review and live-toggle.

## When to use

- Welcome series (multi-email with delays)
- Abandoned cart / browse abandonment flows
- Post-purchase automation (order confirmation → shipped → feedback)
- Cancellation save / win-back flows
- Any always-on email sequence triggered by an event, list-add, or segment-add

## Prerequisites

- `KLAVIYO_API_KEY` in `.env` with `flows:write` and `templates:write` scopes
- Klaviyo Account → Default sender email is **verified** (else flows can't be lived)
- Email templates already exist (use `klaviyo-campaign-create` or push them first)

## Critical gotchas (read before coding)

- **The send-email action data is nested**: `data.message.template_id`, NOT `data.template_id`. Many published examples and AI-generated code get this wrong. Symptom: `"field not valid"` error.
- **Date-based triggers (`type: date-based`) NOT supported via API** — date-anchored flows must be built in UI.
- **Empty `data: {}` returns 500** instead of a clear error. Always include the full FlowEmail object.
- **Flows can't be PATCHed for definition** — to change action graph, delete + recreate.
- **Time delays under 1 minute fail silently** — Klaviyo enforces a minimum of 1 minute.
- **`from_email` must be a verified sender** — flow create succeeds either way, but the flow can't be lived without verification.
- **Klaviyo auto-clones the template** when attached to a flow's send-email action — the flow gets its own private copy.

See `REFERENCE.md` (same folder) for the full schema rules, trigger type table, and action type reference.

## Steps to build a flow

### 1. Discover IDs needed

Query metric IDs, list IDs, segment IDs you'll reference:

```python
GET /api/metrics/             → find Placed Order, Fulfilled Order, etc.
GET /api/lists/               → find Email List, etc.
GET /api/segments/            → find Win-Back Opportunities, etc.
GET /api/templates/           → find your template IDs (if not in template_ids.json)
```

Save these IDs to constants in your script.

### 2. Compose the flow definition

Pattern (simple multi-step):

```python
def email_action(*, temp_id, next_id, template_id, subject, preview, name):
    return {
        "temporary_id": temp_id,
        "type": "send-email",
        "links": {"next": next_id},
        "data": {
            "message": {
                "from_email": "hello@brand.com",
                "from_label": "Brand",
                "reply_to_email": "hello@brand.com",
                "subject_line": subject,
                "preview_text": preview,
                "template_id": template_id,
                "smart_sending_enabled": True,
                "transactional": False,
                "add_tracking_params": True,
                "name": name,
            },
            "status": "draft",
        },
    }

def delay_action(*, temp_id, next_id, unit, value):
    return {
        "temporary_id": temp_id,
        "type": "time-delay",
        "links": {"next": next_id},
        "data": {"unit": unit, "value": value, "timezone": "profile"},
    }

# Welcome series: email → 2-day delay → email
actions = [
    email_action(temp_id="e1", next_id="d1", template_id="...", ...),
    delay_action(temp_id="d1", next_id="e2", unit="days", value=2),
    email_action(temp_id="e2", next_id=None, template_id="...", ...),
]

payload = {
    "data": {
        "type": "flow",
        "attributes": {
            "name": "Brand · Welcome series",
            "definition": {
                "triggers": [{"type": "list", "id": "<list_id>"}],
                "profile_filter": None,
                "entry_action_id": "e1",
                "actions": actions,
            },
        },
    }
}
```

**Action chaining**: Each action has `temporary_id` and `links.next` pointing to the next action's `temporary_id` (or `null` for the last). `definition.entry_action_id` must equal the temporary_id of the first action.

**Required FlowEmail fields**: `from_email`, `subject_line`. Optional: `from_label`, `reply_to_email`, `preview_text`, `template_id`, `smart_sending_enabled`, `transactional`, `add_tracking_params`, `name`.

### 3. POST it

```python
headers = {
    "Authorization": f"Klaviyo-API-Key {api_key}",
    "revision": "2025-04-15",
    "Accept": "application/json",
    "Content-Type": "application/json",
}
r = requests.post("https://a.klaviyo.com/api/flows/", headers=headers, json=payload)
flow_id = r.json()["data"]["id"]
```

### 4. Handle rate limits

Flow creation is rate-limited to 1/second steady. Add `time.sleep(1.5)` between flow creations. Retry on 429 with backoff.

### 5. Verify

```python
GET /api/flows/<flow_id>/flow-actions/
```

Confirms the action graph is intact (all email/delay nodes returned).

## Common flow patterns

See `PATTERNS.md` (same folder) for full pattern library including conditional branches, update-profile steps, and multi-branch splits.

**Quick reference:**

```
# Simple delay-then-email (cancellation save, browse abandonment)
[time-delay] → [send-email]    entry = delay

# Multi-step welcome
[send-email] → [time-delay] → [send-email] → [time-delay] → [send-email]    entry = first email

# Conditional branch (cancellation with refund vs. retain)
[time-delay] → [conditional-branch] → yes: [send-email A] | no: [send-email B]
```

Conditional branch action shape:

```python
def conditional_branch_action(*, temp_id, next_yes_id, next_no_id, property_key, equals_value):
    return {
        "temporary_id": temp_id,
        "type": "conditional-branch",
        "links": {"yes": next_yes_id, "no": next_no_id},
        "data": {
            "condition": {
                "type": "profile-property",
                "filter": {
                    "type": "equals",
                    "property": property_key,
                    "value": equals_value,
                },
            }
        },
    }
```

For event-based conditions, use `"type": "metric"` with a `metric_id` instead of `"type": "profile-property"`.

## Reference implementation

See `~/dev/gearheadbox/scripts/klaviyo_push_flows.py` — creates 9 flows including the multi-step "Pre-order welcome series" (email → 2-day delay → email).

## Cross-skill links

- `klaviyo-campaign-create` — for one-off campaigns (not flows)
- `klaviyo-calendar-plan` — for planning which flows to build
- `brand-voice-extract` — for the voice that informs each email's content

## Embedded in this skill folder

Scripts (copy to your project's `scripts/` directory and run with `uv run`):
- `scripts/generate_email_templates.py`
- `scripts/klaviyo_push_flows.py`
- `scripts/klaviyo_push_templates.py`

Reference templates / examples (copy or adapt):
- `references/02_preorder_welcome_1.html`

Reference docs:
- `REFERENCE.md` — full schema rules, trigger type table, all action types, tradeoffs
- `PATTERNS.md` — complete flow pattern library with code examples
