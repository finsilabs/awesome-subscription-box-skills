# /// script
# requires-python = ">=3.11"
# dependencies = ["requests>=2.31.0", "python-dotenv>=1.0.0"]
# ///
"""Create Klaviyo campaigns (one-off email sends) with templates attached.

Idempotent: skips a campaign if one with the same name already exists.
Saves the resulting {campaign_name: campaign_id} map to klaviyo/campaign_ids.json.

Campaigns are created in DRAFT state. They do NOT auto-send — review in the
Klaviyo UI and click Send (or schedule) when ready.

Usage:
    uv run scripts/klaviyo_push_campaigns.py
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_IDS = ROOT / "klaviyo" / "template_ids.json"
OUTPUT = ROOT / "klaviyo" / "campaign_ids.json"
API_BASE = "https://a.klaviyo.com/api"
REVISION = "2025-10-15"

EMAIL_LIST_ID = "XzpgXM"

# Each campaign: name, audience, message content, scheduled time (or None for unscheduled draft).
# `template_name` references the key in template_ids.json — script looks up the actual template_id.
CAMPAIGNS: list[dict] = [
    {
        "name": "GHB · Launch announcement",
        "template_name": "GHB · 14 · Launch announcement",
        "subject": "The garage doors are open.",
        "preview_text": "The launch box is live. First boxes ship this week.",
        "from_email": "hello@gearheadbox.com",
        "from_label": "Gear Head Box",
        "audience_included": [EMAIL_LIST_ID],
        "audience_excluded": [],
        # Send time placeholder: Aug 4 2026 9am Eastern. The campaign is created in
        # DRAFT status; you can adjust the time in the Klaviyo UI before sending.
        "schedule_at_iso": "2026-08-04T13:00:00+00:00",
    },
]


def headers(api_key: str) -> dict[str, str]:
    return {
        "Authorization": f"Klaviyo-API-Key {api_key}",
        "revision": REVISION,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


def list_existing_campaigns(api_key: str) -> dict[str, str]:
    out: dict[str, str] = {}
    url = f"{API_BASE}/campaigns/?filter=equals(messages.channel,'email')"
    while url:
        r = requests.get(url, headers=headers(api_key), timeout=30)
        r.raise_for_status()
        body = r.json()
        for c in body.get("data", []):
            name = c["attributes"].get("name")
            if name:
                out[name] = c["id"]
        url = body.get("links", {}).get("next")
    return out


def create_campaign(api_key: str, spec: dict, template_id: str) -> str:
    """Create the campaign with one email message. Returns campaign_id."""
    payload = {
        "data": {
            "type": "campaign",
            "attributes": {
                "name": spec["name"],
                "audiences": {
                    "included": spec["audience_included"],
                    "excluded": spec["audience_excluded"],
                },
                "send_strategy": {
                    "method": "static",
                    "datetime": spec["schedule_at_iso"] or "2099-12-31T23:59:59+00:00",
                },
                "send_options": {
                    "use_smart_sending": True,
                },
                "tracking_options": {
                    "add_tracking_params": True,
                    "is_tracking_clicks": True,
                    "is_tracking_opens": True,
                },
                "campaign-messages": {
                    "data": [
                        {
                            "type": "campaign-message",
                            "attributes": {
                                "definition": {
                                    "channel": "email",
                                    "label": spec["name"],
                                    "content": {
                                        "subject": spec["subject"],
                                        "preview_text": spec["preview_text"],
                                        "from_email": spec["from_email"],
                                        "from_label": spec["from_label"],
                                    },
                                },
                            },
                        }
                    ]
                },
            },
        }
    }
    r = requests.post(f"{API_BASE}/campaigns/", headers=headers(api_key), json=payload, timeout=30)
    if not r.ok:
        raise RuntimeError(
            f"Create campaign failed for {spec['name']}: HTTP {r.status_code} {r.text[:500]}"
        )
    body = r.json()
    campaign_id = body["data"]["id"]
    # The campaign-message id is included in the response's relationships
    msg_id = body["data"]["relationships"]["campaign-messages"]["data"][0]["id"]
    return campaign_id, msg_id


def assign_template(api_key: str, message_id: str, template_id: str) -> None:
    payload = {
        "data": {
            "type": "campaign-message",
            "id": message_id,
            "relationships": {
                "template": {
                    "data": {"type": "template", "id": template_id}
                }
            },
        }
    }
    r = requests.post(
        f"{API_BASE}/campaign-message-assign-template/",
        headers=headers(api_key),
        json=payload,
        timeout=30,
    )
    if not r.ok:
        raise RuntimeError(
            f"Assign template failed for message {message_id}: HTTP {r.status_code} {r.text[:300]}"
        )


def main() -> int:
    load_dotenv(ROOT / ".env")
    api_key = os.environ.get("KLAVIYO_API_KEY")
    if not api_key:
        print("ERROR: KLAVIYO_API_KEY not in .env", file=sys.stderr)
        return 1
    if not TEMPLATE_IDS.exists():
        print(f"ERROR: {TEMPLATE_IDS} not found. Run klaviyo_push_templates.py first.", file=sys.stderr)
        return 1

    template_ids = json.loads(TEMPLATE_IDS.read_text())
    print(f"Loaded {len(template_ids)} template IDs.")

    print("Fetching existing campaigns...")
    existing = list_existing_campaigns(api_key)
    print(f"  Found {len(existing)} email campaigns already in Klaviyo.")

    result: dict[str, str] = {}
    for spec in CAMPAIGNS:
        name = spec["name"]
        if name in existing:
            print(f"  EXISTS  {name}  ({existing[name]})")
            result[name] = existing[name]
            continue
        template_id = template_ids.get(spec["template_name"])
        if not template_id:
            print(f"  SKIP    {name} (template '{spec['template_name']}' not found)", file=sys.stderr)
            continue
        cid, msg_id = create_campaign(api_key, spec, template_id)
        time.sleep(1.0)
        assign_template(api_key, msg_id, template_id)
        print(f"  CREATED {name}  campaign={cid}  message={msg_id}  template={template_id}")
        result[name] = cid
        time.sleep(1.5)

    OUTPUT.write_text(json.dumps(result, indent=2))
    print(f"\nWrote {OUTPUT.relative_to(ROOT)} ({len(result)} entries)")
    print("\nNext step: open each campaign in Klaviyo UI.")
    print("Review audience, preview the email, then schedule or click Send.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
