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

## Critical schema notes

The Klaviyo Flows API has nuance that's easy to get wrong:

- **Stable revision**: `2025-04-15` (verified working with full action graphs)
- **The send-email action data is nested**: `data.message.template_id`, NOT `data.template_id`. Many published examples and AI-generated code get this wrong.
- **Required FlowEmail fields**: `from_email`, `subject_line`. Optional: `from_label`, `reply_to_email`, `preview_text`, `template_id`, `smart_sending_enabled`, `transactional`, `add_tracking_params`, `name`.
- **Action chaining**: Each action has `temporary_id` and `links.next` pointing to the next action's `temporary_id` (or `null` for the last).
- **Entry**: `definition.entry_action_id` must equal the temporary_id of the first action.
- **Flows can't be PATCHed for definition** — to change action graph, delete + recreate.
- **Date-based triggers (`type: date-based`) NOT supported via API** — date-anchored flows must be built in UI.
- **Klaviyo auto-clones the template** when attached to a flow's send-email action — the flow gets its own private copy.

## Trigger types supported via API

| Trigger | Type field | id field |
|---|---|---|
| Metric (event) | `"metric"` | metric_id (e.g., R4HMGZ for Placed Order) |
| List subscription | `"list"` | list_id |
| Segment membership | `"segment"` | segment_id |
| Date-based | `"date-based"` | ❌ NOT supported via API |

## Action types in the spec

From the OpenAPI: 18 action types. Common ones:

| Action | Use for |
|---|---|
| `send-email` | The email step. Wraps a `FlowEmail` message. |
| `time-delay` | Wait between actions. Units: `minutes` / `hours` / `days`. Timezone: `profile` (recipient's TZ) or specific TZ. |
| `conditional-branch` | Yes/no split based on profile properties or events |
| `multi-branch-split` / `action-output-split` | Multi-way split |
| `update-profile` | Set a profile property (e.g., tag as "Founding subscriber") |
| `list-update` | Add/remove from a list |
| `send-sms` | SMS step (same shape as email) |
| `send-webhook` | Fire a webhook to an external URL |
| `ab-test` | Built-in A/B testing |
| `code` | JS code action (gated) |

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

## Composing common flow patterns

**Simple delay-then-email** (cancellation save, browse abandonment):
```
[time-delay] → [send-email]
entry = delay
```

**Multi-step welcome** (welcome series):
```
[send-email] → [time-delay] → [send-email] → [time-delay] → [send-email]
entry = first email
```

**Conditional branch** (cancellation with refund vs. retain):
```
[time-delay] → [conditional-branch] → split A: [send-email A] | split B: [send-email B]
```

(Conditional branches need `ConditionalBranchActionData` — see OpenAPI spec for filter conditions.)

**Update profile property as part of flow** (tag founding subscribers):
```
[send-email] → [update-profile { property: "founding_subscriber", value: true }] → [time-delay] → [send-email]
```

## Reference implementation

See `~/dev/gearheadbox/scripts/klaviyo_push_flows.py` — creates 9 flows including the multi-step "Pre-order welcome series" (email → 2-day delay → email).

## Common gotchas

- **Empty `data: {}` returns 500** instead of a clear error. Don't send empty data — always include the FlowEmail object.
- **`data.template_id` (without `.message`) returns "field not valid"** — that's the symptom. The fix is `data.message.template_id`.
- **Time delays under 1 minute fail silently** — Klaviyo enforces a minimum of 1 minute.
- **Subject line is required**, even on the email's later steps. If you don't set it, it errors out.
- **`from_email` must be a verified sender** — flow create succeeds either way, but the flow can't be lived without verification.

## Cross-skill links

- `klaviyo-campaign-create` — for one-off campaigns (not flows)
- `klaviyo-calendar-plan` — for planning which flows to build
- `brand-voice-extract` — for the voice that informs each email's content

## Tradeoffs

- **API vs. UI for flows** — API gets you to 95% in seconds. The remaining 5% (visual flow-builder review, complex conditional logic, A/B testing setup) is sometimes faster in UI. Use API for the bulk; tweak in UI.
- **Multiple flows on same trigger** — totally fine. Klaviyo lets multiple flows fire on `Placed Order`. Use profile filters to scope each one.
- **Auto-cloned templates** — if you re-push the source template via `klaviyo_push_templates.py`, flows keep their cloned copies. Either re-sync each flow's email step in UI, or delete + recreate the flow with the new template_id.

## Embedded in this skill folder

Scripts (copy to your project's `scripts/` directory and run with `uv run`):
- `scripts/generate_email_templates.py`
- `scripts/klaviyo_push_flows.py`
- `scripts/klaviyo_push_templates.py`

Reference templates / examples (copy or adapt):
- `examples/02_preorder_welcome_1.html`
