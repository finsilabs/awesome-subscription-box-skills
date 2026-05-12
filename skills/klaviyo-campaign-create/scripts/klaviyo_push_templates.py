# /// script
# requires-python = ">=3.11"
# dependencies = ["requests>=2.31.0", "python-dotenv>=1.0.0"]
# ///
"""Push all email templates in klaviyo/templates/ to Klaviyo as code-mode templates.

Idempotent: lists existing templates, updates by name if found, creates if not.
Writes the resulting {template_name: template_id} map to klaviyo/template_ids.json.

Usage:
    uv run scripts/klaviyo_push_templates.py
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT / "klaviyo" / "templates"
OUTPUT = ROOT / "klaviyo" / "template_ids.json"
API_BASE = "https://a.klaviyo.com/api"
REVISION = "2025-04-15"

# Filename → template name in Klaviyo. Order matches the FLOW_GUIDE table.
NAMES: dict[str, str] = {
    "01_newsletter_welcome.html": "GHB · 01 · Newsletter welcome",
    "02_preorder_welcome_1.html": "GHB · 02 · Pre-order welcome 1 (confirmation)",
    "03_preorder_welcome_2.html": "GHB · 03 · Pre-order welcome 2 (curation)",
    "04_prelaunch_countdown.html": "GHB · 04 · Pre-launch countdown",
    "05_order_confirmation.html": "GHB · 05 · Order confirmation",
    "06_box_shipped.html": "GHB · 06 · Box shipped",
    "07_browse_abandonment.html": "GHB · 07 · Browse abandonment",
    "08_checkout_abandonment.html": "GHB · 08 · Checkout abandonment",
    "09_cancellation_save.html": "GHB · 09 · Cancellation save",
    "10_winback.html": "GHB · 10 · Win-back",
    "11_subscriber_anniversary.html": "GHB · 11 · Subscriber anniversary",
    "12_monthly_cycle_reminder.html": "GHB · 12 · Monthly cycle reminder",
    "13_post_purchase_feedback.html": "GHB · 13 · Post-purchase feedback",
    "14_launch_announcement.html": "GHB · 14 · Launch announcement",
}


def headers(api_key: str) -> dict[str, str]:
    return {
        "Authorization": f"Klaviyo-API-Key {api_key}",
        "revision": REVISION,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


def list_existing(api_key: str) -> dict[str, str]:
    """Return {template_name: template_id} for all existing templates."""
    out: dict[str, str] = {}
    url = f"{API_BASE}/templates/"
    while url:
        r = requests.get(url, headers=headers(api_key), timeout=30)
        r.raise_for_status()
        body = r.json()
        for tpl in body.get("data", []):
            name = tpl["attributes"].get("name")
            if name:
                out[name] = tpl["id"]
        url = body.get("links", {}).get("next")
    return out


def create_template(api_key: str, name: str, html: str) -> str:
    payload = {
        "data": {
            "type": "template",
            "attributes": {
                "name": name,
                "editor_type": "CODE",
                "html": html,
            },
        }
    }
    r = requests.post(f"{API_BASE}/templates/", headers=headers(api_key), json=payload, timeout=30)
    if not r.ok:
        raise RuntimeError(f"Create failed for {name}: HTTP {r.status_code} {r.text[:300]}")
    return r.json()["data"]["id"]


def update_template(api_key: str, template_id: str, name: str, html: str) -> None:
    payload = {
        "data": {
            "type": "template",
            "id": template_id,
            "attributes": {
                "name": name,
                "html": html,
            },
        }
    }
    r = requests.patch(
        f"{API_BASE}/templates/{template_id}/",
        headers=headers(api_key),
        json=payload,
        timeout=30,
    )
    if not r.ok:
        raise RuntimeError(f"Update failed for {name}: HTTP {r.status_code} {r.text[:300]}")


def main() -> int:
    load_dotenv(ROOT / ".env")
    api_key = os.environ.get("KLAVIYO_API_KEY")
    if not api_key:
        print("ERROR: KLAVIYO_API_KEY not in .env", file=sys.stderr)
        return 1

    if not TEMPLATES_DIR.is_dir():
        print(f"ERROR: {TEMPLATES_DIR} not found", file=sys.stderr)
        return 1

    print("Fetching existing templates...")
    existing = list_existing(api_key)
    print(f"  Found {len(existing)} templates already in Klaviyo.")

    result: dict[str, str] = {}
    for filename, name in NAMES.items():
        path = TEMPLATES_DIR / filename
        if not path.exists():
            print(f"  SKIP (file missing): {filename}", file=sys.stderr)
            continue
        html = path.read_text()
        if name in existing:
            tid = existing[name]
            update_template(api_key, tid, name, html)
            print(f"  UPDATED  {name}  ({tid})")
        else:
            tid = create_template(api_key, name, html)
            print(f"  CREATED  {name}  ({tid})")
        result[name] = tid

    OUTPUT.write_text(json.dumps(result, indent=2))
    print(f"\nWrote {OUTPUT.relative_to(ROOT)} ({len(result)} entries)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
