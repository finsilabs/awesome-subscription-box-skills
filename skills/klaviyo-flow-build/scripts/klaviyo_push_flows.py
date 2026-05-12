# /// script
# requires-python = ">=3.11"
# dependencies = ["requests>=2.31.0", "python-dotenv>=1.0.0"]
# ///
"""Create complete Klaviyo flows with triggers, time-delays, and send-email actions.

Uses Klaviyo's stable Flows API (revision 2025-04-15). Each flow is created with
its full action graph: trigger → optional time-delay → send-email step pointing
at the matching template (auto-cloned by Klaviyo into a flow-private copy).

Idempotent: skips by name. Saves {flow_name: flow_id} to klaviyo/flow_ids.json.

Usage:
    uv run scripts/klaviyo_push_flows.py
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_IDS_FILE = ROOT / "klaviyo" / "template_ids.json"
OUTPUT = ROOT / "klaviyo" / "flow_ids.json"
API_BASE = "https://a.klaviyo.com/api"
REVISION = "2025-04-15"

EMAIL_LIST_ID = "XzpgXM"
WIN_BACK_SEGMENT_ID = "RwujCQ"
METRIC = {
    "placed_order": "R4HMGZ",
    "fulfilled_order": "UDzyHX",
    "cancelled_order": "SR9Fdu",
    "viewed_product": "WmnbT4",
    "checkout_started": "Se8CAR",
}

FROM_EMAIL = "hello@gearheadbox.com"
FROM_LABEL = "Gear Head Box"


def headers(api_key: str) -> dict[str, str]:
    return {
        "Authorization": f"Klaviyo-API-Key {api_key}",
        "revision": REVISION,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


def email_action(
    *,
    temp_id: str,
    next_id: str | None,
    template_id: str,
    subject: str,
    preview: str,
    name: str,
) -> dict[str, Any]:
    return {
        "temporary_id": temp_id,
        "type": "send-email",
        "links": {"next": next_id},
        "data": {
            "message": {
                "from_email": FROM_EMAIL,
                "from_label": FROM_LABEL,
                "reply_to_email": FROM_EMAIL,
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


def delay_action(*, temp_id: str, next_id: str, unit: str, value: int) -> dict[str, Any]:
    return {
        "temporary_id": temp_id,
        "type": "time-delay",
        "links": {"next": next_id},
        "data": {"unit": unit, "value": value, "timezone": "profile"},
    }


def build_flows(template_ids: dict[str, str]) -> list[dict[str, Any]]:
    """Return flow specs with full action graphs ready to POST."""

    def t(name: str) -> str:
        if name not in template_ids:
            raise SystemExit(f"Template not found: {name}")
        return template_ids[name]

    return [
        {
            "name": "GHB · 01 · Newsletter welcome",
            "trigger": {"type": "list", "id": EMAIL_LIST_ID},
            "entry": "e1",
            "actions": [
                email_action(
                    temp_id="e1", next_id=None,
                    template_id=t("GHB · 01 · Newsletter welcome"),
                    subject="Welcome to the inside line.",
                    preview="Monthly emails: spoilers from upcoming boxes, member-only drops, and the occasional rant about manuals dying.",
                    name="Welcome",
                ),
            ],
        },
        {
            "name": "GHB · 02 · Pre-order welcome series",
            "trigger": {"type": "metric", "id": METRIC["placed_order"]},
            "entry": "e1",
            "actions": [
                email_action(
                    temp_id="e1", next_id="d1",
                    template_id=t("GHB · 02 · Pre-order welcome 1 (confirmation)"),
                    subject="You're in. Welcome aboard.",
                    preview="Your subscription is locked in. Here's what happens next, on what dates, and who to email if anything goes sideways.",
                    name="Welcome 1 of 2",
                ),
                delay_action(temp_id="d1", next_id="e2", unit="days", value=2),
                email_action(
                    temp_id="e2", next_id=None,
                    template_id=t("GHB · 03 · Pre-order welcome 2 (curation)"),
                    subject="Behind the curtain: your first box.",
                    preview="A look at how we curate, who picks the items, and what the launch box is shaping up to include.",
                    name="Welcome 2 of 2",
                ),
            ],
        },
        {
            "name": "GHB · 03 · Order confirmation",
            "trigger": {"type": "metric", "id": METRIC["placed_order"]},
            "entry": "d1",
            "actions": [
                delay_action(temp_id="d1", next_id="e1", unit="minutes", value=5),
                email_action(
                    temp_id="e1", next_id=None,
                    template_id=t("GHB · 05 · Order confirmation"),
                    subject="Order confirmed.",
                    preview="Order confirmed. Here are the details and what to expect next.",
                    name="Confirmation",
                ),
            ],
        },
        {
            "name": "GHB · 04 · Box shipped",
            "trigger": {"type": "metric", "id": METRIC["fulfilled_order"]},
            "entry": "e1",
            "actions": [
                email_action(
                    temp_id="e1", next_id=None,
                    template_id=t("GHB · 06 · Box shipped"),
                    subject="Your box just left the warehouse.",
                    preview="Your box is on the way. Tracking inside.",
                    name="Shipped notification",
                ),
            ],
        },
        {
            "name": "GHB · 05 · Browse abandonment",
            "trigger": {"type": "metric", "id": METRIC["viewed_product"]},
            "entry": "d1",
            "actions": [
                delay_action(temp_id="d1", next_id="e1", unit="hours", value=4),
                email_action(
                    temp_id="e1", next_id=None,
                    template_id=t("GHB · 07 · Browse abandonment"),
                    subject="Still thinking it over?",
                    preview="Still thinking? Here's the quick decision guide.",
                    name="Browse reminder",
                ),
            ],
        },
        {
            "name": "GHB · 06 · Checkout abandonment",
            "trigger": {"type": "metric", "id": METRIC["checkout_started"]},
            "entry": "d1",
            "actions": [
                delay_action(temp_id="d1", next_id="e1", unit="hours", value=1),
                email_action(
                    temp_id="e1", next_id=None,
                    template_id=t("GHB · 08 · Checkout abandonment"),
                    subject="Your tier is sitting in the cart.",
                    preview="You left a tier in your cart. Want us to hold it for you?",
                    name="Cart recovery",
                ),
            ],
        },
        {
            "name": "GHB · 07 · Cancellation save",
            "trigger": {"type": "metric", "id": METRIC["cancelled_order"]},
            "entry": "d1",
            "actions": [
                delay_action(temp_id="d1", next_id="e1", unit="minutes", value=30),
                email_action(
                    temp_id="e1", next_id=None,
                    template_id=t("GHB · 09 · Cancellation save"),
                    subject="Did we drop the ball?",
                    preview="Sorry to see you go. If we dropped the ball, we want to know.",
                    name="Save attempt",
                ),
            ],
        },
        {
            "name": "GHB · 08 · Post-purchase feedback",
            "trigger": {"type": "metric", "id": METRIC["fulfilled_order"]},
            "entry": "d1",
            "actions": [
                delay_action(temp_id="d1", next_id="e1", unit="days", value=10),
                email_action(
                    temp_id="e1", next_id=None,
                    template_id=t("GHB · 13 · Post-purchase feedback"),
                    subject="So — what do you think?",
                    preview="Box landed. How'd it feel?",
                    name="Feedback request",
                ),
            ],
        },
        {
            "name": "GHB · 09 · Win-back",
            "trigger": {"type": "segment", "id": WIN_BACK_SEGMENT_ID},
            "entry": "e1",
            "actions": [
                email_action(
                    temp_id="e1", next_id=None,
                    template_id=t("GHB · 10 · Win-back"),
                    subject="The garage misses you.",
                    preview="It's been a minute. Here's what's been in recent boxes.",
                    name="Win-back attempt",
                ),
            ],
        },
    ]


def list_existing(api_key: str) -> dict[str, str]:
    out: dict[str, str] = {}
    url = f"{API_BASE}/flows/"
    while url:
        r = requests.get(url, headers=headers(api_key), timeout=30)
        r.raise_for_status()
        body = r.json()
        for fl in body.get("data", []):
            name = fl["attributes"].get("name")
            if name:
                out[name] = fl["id"]
        url = body.get("links", {}).get("next")
    return out


def create_flow(api_key: str, spec: dict[str, Any], retries: int = 3) -> str:
    payload = {
        "data": {
            "type": "flow",
            "attributes": {
                "name": spec["name"],
                "definition": {
                    "triggers": [spec["trigger"]],
                    "profile_filter": None,
                    "entry_action_id": spec["entry"],
                    "actions": spec["actions"],
                },
            },
        }
    }
    for attempt in range(retries):
        r = requests.post(f"{API_BASE}/flows/", headers=headers(api_key), json=payload, timeout=60)
        if r.status_code == 429:
            time.sleep(3 + attempt * 2)
            continue
        if not r.ok:
            raise RuntimeError(
                f"Create failed for {spec['name']}: HTTP {r.status_code} {r.text[:500]}"
            )
        return r.json()["data"]["id"]
    raise RuntimeError(f"Create failed for {spec['name']} after {retries} retries (rate limited)")


def main() -> int:
    load_dotenv(ROOT / ".env")
    api_key = os.environ.get("KLAVIYO_API_KEY")
    if not api_key:
        print("ERROR: KLAVIYO_API_KEY not in .env", file=sys.stderr)
        return 1
    if not TEMPLATE_IDS_FILE.exists():
        print(f"ERROR: {TEMPLATE_IDS_FILE} not found. Run klaviyo_push_templates.py first.", file=sys.stderr)
        return 1

    template_ids = json.loads(TEMPLATE_IDS_FILE.read_text())
    flows = build_flows(template_ids)

    print("Fetching existing flows...")
    existing = list_existing(api_key)
    print(f"  Found {len(existing)} flows already in Klaviyo.")

    result: dict[str, str] = {}
    for spec in flows:
        if spec["name"] in existing:
            print(f"  EXISTS  {spec['name']}  ({existing[spec['name']]})")
            result[spec["name"]] = existing[spec["name"]]
            continue
        fid = create_flow(api_key, spec)
        n_email = sum(1 for a in spec["actions"] if a["type"] == "send-email")
        n_delay = sum(1 for a in spec["actions"] if a["type"] == "time-delay")
        print(f"  CREATED {spec['name']}  ({fid})  emails={n_email}, delays={n_delay}")
        result[spec["name"]] = fid
        time.sleep(1.5)

    OUTPUT.write_text(json.dumps(result, indent=2))
    print(f"\nWrote {OUTPUT.relative_to(ROOT)} ({len(result)} entries)")
    print("\nAll flows are in DRAFT status. Open each in Klaviyo to review and turn live.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
