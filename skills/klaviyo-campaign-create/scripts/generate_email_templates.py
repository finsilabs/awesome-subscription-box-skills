# /// script
# requires-python = ">=3.11"
# ///
"""Generate brand-consistent Klaviyo email templates for Gear Head Box.

Outputs 10 HTML files into klaviyo/templates/, each ready to upload via
the klaviyo_create_email_template MCP tool.

The shell (header, container, footer, button styles) is defined once in
the `render` function so changes propagate to every email.
"""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "klaviyo" / "templates"

LOGO_URL = "https://cdn.shopify.com/s/files/1/0752/2271/2487/files/gearhead_logo_cropped.png?v=1778111725"
SITE = "https://gearheadbox.myshopify.com"

# Color palette — matches the storefront tire-gray theme
COLORS = {
    "page": "#1F2127",
    "card": "#2A2D34",
    "border": "#3a3d44",
    "text": "#EAEAEA",
    "text_strong": "#F5F5F5",
    "muted": "#888a90",
    "accent": "#E10600",
    "accent_text": "#ffffff",
}


def button(label: str, url: str, secondary: bool = False) -> str:
    bg = "transparent" if secondary else COLORS["accent"]
    border = f"2px solid {COLORS['accent']}" if secondary else "0"
    color = COLORS["accent"] if secondary else COLORS["accent_text"]
    return dedent(f"""
        <table role="presentation" cellspacing="0" cellpadding="0" border="0" style="margin:24px 0;">
          <tr>
            <td style="background:{bg};border:{border};padding:14px 28px;border-radius:2px;">
              <a href="{url}" style="color:{color};text-decoration:none;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;font-size:14px;font-family:Arial,Helvetica,sans-serif;">{label}</a>
            </td>
          </tr>
        </table>
    """).strip()


def render(
    *,
    preview_text: str,
    heading: str,
    body_html: str,
    cta_label: str | None = None,
    cta_url: str | None = None,
    cta_secondary_label: str | None = None,
    cta_secondary_url: str | None = None,
    sign_off: str = "—&nbsp;The Gear Head Box team",
) -> str:
    cta_html = ""
    if cta_label and cta_url:
        cta_html = button(cta_label, cta_url, secondary=False)
    if cta_secondary_label and cta_secondary_url:
        cta_html += button(cta_secondary_label, cta_secondary_url, secondary=True)

    return dedent(f"""\
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width,initial-scale=1">
      <title>Gear Head Box</title>
      <style>
        @media screen and (max-width:620px) {{
          .ghb-container {{ width: 100% !important; }}
          .ghb-cell {{ padding: 24px !important; }}
          .ghb-h1 {{ font-size: 24px !important; }}
        }}
      </style>
    </head>
    <body style="margin:0;padding:0;background:{COLORS['page']};font-family:'Helvetica Neue',Arial,Helvetica,sans-serif;color:{COLORS['text']};">
      <div style="display:none;font-size:1px;color:{COLORS['page']};line-height:1px;max-height:0;max-width:0;opacity:0;overflow:hidden;">{preview_text}</div>
      <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background:{COLORS['page']};">
        <tr>
          <td align="center" style="padding:32px 16px;">
            <table role="presentation" class="ghb-container" width="600" cellspacing="0" cellpadding="0" border="0" style="max-width:600px;width:100%;background:{COLORS['card']};border-radius:2px;overflow:hidden;">
              <tr>
                <td align="center" style="padding:32px 32px 24px;border-bottom:1px solid {COLORS['border']};background:{COLORS['page']};">
                  <a href="{SITE}" style="display:inline-block;text-decoration:none;">
                    <img src="{LOGO_URL}" width="180" alt="Gear Head Box" style="display:block;border:0;height:auto;max-width:180px;">
                  </a>
                </td>
              </tr>
              <tr>
                <td class="ghb-cell" style="padding:40px 36px;">
                  <h1 class="ghb-h1" style="margin:0 0 20px;font-family:'Helvetica Neue',Arial,sans-serif;font-weight:800;font-size:28px;line-height:1.15;color:{COLORS['text_strong']};text-transform:uppercase;letter-spacing:0.02em;">{heading}</h1>
                  <div style="font-size:16px;line-height:1.7;color:{COLORS['text']};">{body_html}</div>
                  {cta_html}
                  <p style="margin:32px 0 0;font-size:14px;color:{COLORS['muted']};">{sign_off}</p>
                </td>
              </tr>
              <tr>
                <td align="center" style="padding:24px 32px 32px;border-top:1px solid {COLORS['border']};font-size:12px;line-height:1.6;color:{COLORS['muted']};">
                  <p style="margin:0 0 8px;">Gear Head Box &middot; Charlotte, NC</p>
                  <p style="margin:0;"><a href="{SITE}" style="color:{COLORS['muted']};text-decoration:underline;">gearheadbox.com</a> &middot; {{% unsubscribe 'Unsubscribe' %}}</p>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </body>
    </html>
    """)


# All 14 email templates as (filename, kwargs) pairs.
EMAILS: list[tuple[str, dict]] = [
    (
        "01_newsletter_welcome.html",
        dict(
            preview_text="Monthly emails: spoilers from upcoming boxes, member-only drops, and the occasional rant about manuals dying.",
            heading="Welcome to the inside line.",
            body_html=(
                "<p>Glad you're here.</p>"
                "<p>You'll get one email a month from us — sometimes two — covering what's coming in the next box, member-only drops, and the occasional rant about manuals dying. No fluff, no daily spam.</p>"
                "<p>Heads up: we're a pre-order box right now. First shipments go out the first week of August. If you want to lock in a tier before the launch list closes, the link below has the three options.</p>"
            ),
            cta_label="See the tiers",
            cta_url=f"{SITE}/collections/tiers",
            cta_secondary_label="How it works",
            cta_secondary_url=f"{SITE}/pages/how-it-works",
        ),
    ),
    (
        "02_preorder_welcome_1.html",
        dict(
            preview_text="Your subscription is locked in. Here's what happens next, on what dates, and who to email if anything goes sideways.",
            heading="You're in. Welcome aboard.",
            body_html=(
                "<p>Hi {{ first_name|default:'gearhead' }},</p>"
                "<p><strong>Your subscription is confirmed</strong> and your tier is locked in. Your card was charged today; you won't be charged again until the next monthly cycle after your first box ships.</p>"
                "<p><strong>Here's the timeline:</strong></p>"
                "<ul style=\"margin:0 0 16px;padding-left:20px;\">"
                "<li style=\"margin:0 0 8px;\"><strong>Now &rarr; July</strong> — we line up brands, items, and packaging for the launch box.</li>"
                "<li style=\"margin:0 0 8px;\"><strong>Late July</strong> — your final preferences (sizes, car platforms, what you already own) get applied to your box.</li>"
                "<li style=\"margin:0 0 8px;\"><strong>First week of August</strong> — your launch box ships. You'll get a tracking email when it leaves the warehouse.</li>"
                "<li style=\"margin:0;\"><strong>15th of every month after that</strong> — regular monthly cadence kicks in.</li>"
                "</ul>"
                "<p>Founding pre-order subscribers (that's you) get a small thank-you item in the launch box and first dibs on limited drops in the first year.</p>"
            ),
            cta_label="Set your preferences",
            cta_url=f"{SITE}/account",
            cta_secondary_label="Read the FAQ",
            cta_secondary_url=f"{SITE}/pages/faq",
        ),
    ),
    (
        "03_preorder_welcome_2.html",
        dict(
            preview_text="A look at how we curate, who picks the items, and what the launch box is shaping up to include.",
            heading="What we're putting in your first box.",
            body_html=(
                "<p>Wanted to share a peek at how the launch box comes together.</p>"
                "<p><strong>Curation is humans-only.</strong> Real people on our team — career mechanics, weekend racers, one ex-OEM product engineer — pick every item. No drop-shipping, no algorithmic filler. We work directly with brands and small-batch automotive artisans, and items get inspected at our warehouse before they ship.</p>"
                "<p><strong>What we're locking in for August:</strong></p>"
                "<ul style=\"margin:0 0 16px;padding-left:20px;\">"
                "<li style=\"margin:0 0 8px;\">A premium microfiber towel and a curated detailing item from a chemist in California who races on weekends</li>"
                "<li style=\"margin:0 0 8px;\">Branded apparel printed by a small shop we've worked with for years (Apex and up)</li>"
                "<li style=\"margin:0 0 8px;\">Tools sourced from a supplier in Greensboro, NC (Apex and up)</li>"
                "<li style=\"margin:0;\">A founding-subscriber thank-you piece &mdash; small but real</li>"
                "</ul>"
                "<p>Every box's items add up to more than what you paid &mdash; that's the deal. If a box ever feels light, our value guarantee covers it: refund, replace, or credit. No hoops.</p>"
            ),
            cta_label="See our value guarantee",
            cta_url=f"{SITE}/policies/refund-policy",
        ),
    ),
    (
        "04_prelaunch_countdown.html",
        dict(
            preview_text="Your launch box ships next week. Here's what's coming, and where to update your address if anything's changed.",
            heading="Your first box ships next week.",
            body_html=(
                "<p>It's almost go time.</p>"
                "<p>The first wave of Gear Head Box launch boxes ships <strong>the first week of August 2026</strong>. Curation is locked, items are at the warehouse, and packing starts in 48 hours.</p>"
                "<p><strong>Two things to check before we ship:</strong></p>"
                "<ol style=\"margin:0 0 16px;padding-left:20px;\">"
                "<li style=\"margin:0 0 8px;\"><strong>Your shipping address</strong> &mdash; if you've moved or want to redirect, update it now from your account dashboard. Once we ship we can't redirect.</li>"
                "<li style=\"margin:0;\"><strong>Your preferences</strong> &mdash; favorite car platforms, sizes, what you already own. We use this to avoid sending you duplicates.</li>"
                "</ol>"
                "<p>You'll get a tracking email the moment your box leaves the warehouse.</p>"
            ),
            cta_label="Update my account",
            cta_url=f"{SITE}/account",
        ),
    ),
    (
        "05_order_confirmation.html",
        dict(
            preview_text="Order confirmed. Here are the details and what to expect next.",
            heading="Order confirmed.",
            body_html=(
                "<p>Hi {{ first_name|default:'gearhead' }},</p>"
                "<p>We got the order. Receipt and details are in a separate email from Shopify. Here's the shape of what happens next:</p>"
                "<table role=\"presentation\" cellspacing=\"0\" cellpadding=\"12\" border=\"0\" style=\"width:100%;background:#1F2127;border-radius:2px;margin:8px 0 16px;\">"
                "<tr><td style=\"font-size:14px;color:#EAEAEA;\">"
                "<strong>Order:</strong> #{{ event.order_id|default:'(see receipt)' }}<br>"
                "<strong>Tier:</strong> {{ event.product_name|default:'Your subscription' }}<br>"
                "<strong>Total today:</strong> {{ event.total|default:'(see receipt)' }}"
                "</td></tr></table>"
                "<p><strong>What's next:</strong> your first box ships <strong>the first week of August 2026</strong>. After that, regular monthly cadence kicks in &mdash; boxes ship on the 15th of every month.</p>"
                "<p>If you want to update preferences (car platforms, sizes), do it from your account before late July.</p>"
            ),
            cta_label="View my account",
            cta_url=f"{SITE}/account",
            cta_secondary_label="Read the FAQ",
            cta_secondary_url=f"{SITE}/pages/faq",
        ),
    ),
    (
        "06_box_shipped.html",
        dict(
            preview_text="Your box is on the way. Tracking inside.",
            heading="Your box is on the way.",
            body_html=(
                "<p>Just left the warehouse.</p>"
                "<p><strong>Tracking number:</strong> {{ event.tracking_number|default:'(see your shipping email)' }}<br>"
                "<strong>Carrier:</strong> {{ event.tracking_company|default:'USPS / UPS / FedEx' }}<br>"
                "<strong>Expected arrival:</strong> 3&ndash;7 business days for US addresses</p>"
                "<p>We'd love to see what's in there once it lands. Tag <strong>@gearheadbox</strong> on Instagram or TikTok in your unboxing &mdash; we repost the good ones and occasionally drop founding subscribers a thank-you item.</p>"
                "<p>If anything in your box arrives damaged or feels off, just reply to this email. Our value guarantee covers it &mdash; we'll refund the box or replace items, your call.</p>"
            ),
            cta_label="Track my box",
            cta_url="{{ event.tracking_url|default:'https://gearheadbox.myshopify.com/account' }}",
        ),
    ),
    (
        "07_browse_abandonment.html",
        dict(
            preview_text="Still thinking? Here's the quick decision guide.",
            heading="Still thinking it over?",
            body_html=(
                "<p>You looked at one of the tiers and didn't pull the trigger. Totally fair &mdash; here's the 30-second decision guide:</p>"
                "<table role=\"presentation\" cellspacing=\"0\" cellpadding=\"14\" border=\"0\" style=\"width:100%;background:#1F2127;border-radius:2px;margin:8px 0 16px;\">"
                "<tr><td style=\"font-size:14px;color:#EAEAEA;line-height:1.7;\">"
                "<strong style=\"color:#F5F5F5;\">PIT STOP &mdash; $54/mo</strong> &middot; Starter. Stickers, towel, tire shine, surprise.<br>"
                "<strong style=\"color:#F5F5F5;\">APEX &mdash; $84/mo</strong> &middot; The sweet spot. Apparel, real tools, premium detailing.<br>"
                "<strong style=\"color:#F5F5F5;\">PODIUM &mdash; $119/mo</strong> &middot; A $60+ retail hero piece every month plus everything in Apex."
                "</td></tr></table>"
                "<p><strong>Cancel anytime. No fees. No fine print.</strong> If a box ever feels light, our value guarantee covers it.</p>"
                "<p>Pre-orders are open right now &mdash; the first wave ships the first week of August.</p>"
            ),
            cta_label="Pick your tier",
            cta_url=f"{SITE}/collections/tiers",
            cta_secondary_label="Compare side-by-side",
            cta_secondary_url=f"{SITE}/pages/how-it-works",
        ),
    ),
    (
        "08_checkout_abandonment.html",
        dict(
            preview_text="You left a tier in your cart. Want us to hold it for you?",
            heading="Your tier is sitting in the cart.",
            body_html=(
                "<p>You started checkout and didn't quite finish. Easy to come back to:</p>"
                "<p>Pre-order capacity is finite for the first wave (we'd rather under-promise than over-pack). If you want a launch box in early August, locking in this week is the right call.</p>"
                "<p>If something stopped you &mdash; a question, a payment hiccup, anything &mdash; just reply to this email. We answer everything within a business day.</p>"
            ),
            cta_label="Finish checkout",
            cta_url="{{ event.checkout_url|default:'https://gearheadbox.myshopify.com/cart' }}",
        ),
    ),
    (
        "09_cancellation_save.html",
        dict(
            preview_text="Sorry to see you go. If we dropped the ball, we want to know.",
            heading="Did we drop the ball?",
            body_html=(
                "<p>Sorry to see you cancel. Genuine question: was it the box itself, the timing, the price, or something else?</p>"
                "<p>If a specific box didn't deliver on the value promise, our guarantee covers it &mdash; we can refund the last box, swap items, or credit your account. Just reply to this email.</p>"
                "<p>If the price is the issue but you'd come back at a lighter tier, you can switch to <strong>Pit Stop ($54/mo)</strong> or <strong>Apex ($84/mo)</strong> from your account in one click.</p>"
                "<p>Whatever the reason, your honest feedback helps us make the box better for the people who stay.</p>"
            ),
            cta_label="Reply with feedback",
            cta_url="mailto:hello@gearheadbox.com?subject=Cancellation%20feedback",
            cta_secondary_label="Switch to Pit Stop",
            cta_secondary_url=f"{SITE}/products/pit-stop",
        ),
    ),
    (
        "10_winback.html",
        dict(
            preview_text="It's been a minute. Here's what's been in recent boxes.",
            heading="The garage misses you.",
            body_html=(
                "<p>It's been about three months since your last box. We've shipped a lot since &mdash; here's the highlight reel:</p>"
                "<ul style=\"margin:0 0 16px;padding-left:20px;\">"
                "<li style=\"margin:0 0 8px;\">A run of leather driving gloves (Podium hero piece, Sept)</li>"
                "<li style=\"margin:0 0 8px;\">Limited-edition track-day apparel collab (Apex, Oct)</li>"
                "<li style=\"margin:0;\">A precision torque wrench from a Greensboro tool maker (Apex+, Nov)</li>"
                "</ul>"
                "<p>If something pulled you away, we'd love to know what would bring you back. Reply to this email &mdash; a real person reads every reply.</p>"
                "<p>If you want to just jump back in, your old account is still there with one-click resubscribe.</p>"
            ),
            cta_label="Resubscribe",
            cta_url=f"{SITE}/collections/tiers",
            cta_secondary_label="Reply with feedback",
            cta_secondary_url="mailto:hello@gearheadbox.com",
        ),
    ),
    (
        "11_subscriber_anniversary.html",
        dict(
            preview_text="One year of boxes. Here's a small thank-you.",
            heading="A year of boxes. Thanks.",
            body_html=(
                "<p>Hi {{ first_name|default:'gearhead' }},</p>"
                "<p>One year ago today, your first Gear Head Box landed at your door. Twelve boxes, dozens of items, somewhere between a few hundred and a few thousand dollars of retail value through your garage.</p>"
                "<p>That's a real commitment, and we appreciate it. As a small thank-you, your <strong>next box has a founding-anniversary item</strong> in it &mdash; a one-year-only piece that doesn't show up in any other box.</p>"
                "<p>Nothing you need to do. It'll just be in there.</p>"
                "<p>If you've got a story or a photo from any of the past twelve boxes, hit reply &mdash; we love seeing where this stuff ends up. The track-day shots are the best ones.</p>"
            ),
            cta_label="See your subscription",
            cta_url=f"{SITE}/account",
            cta_secondary_label="Tell us a story",
            cta_secondary_url="mailto:hello@gearheadbox.com?subject=Year%20one%20story",
        ),
    ),
    (
        "12_monthly_cycle_reminder.html",
        dict(
            preview_text="This month's box ships in 5 days. Address current?",
            heading="This month's box ships in 5 days.",
            body_html=(
                "<p>Quick heads-up: we ship the next round of boxes on the 15th. Five days out.</p>"
                "<p><strong>Two things to confirm:</strong></p>"
                "<ul style=\"margin:0 0 16px;padding-left:20px;\">"
                "<li style=\"margin:0 0 8px;\"><strong>Address</strong> — if you've moved or are spending the month somewhere different, update it now from your account.</li>"
                "<li style=\"margin:0;\"><strong>Tier or skip</strong> — want to swap tiers, skip the month, or pause? All one click in your account.</li>"
                "</ul>"
                "<p>Otherwise we're packing your box this weekend and shipping it Tuesday.</p>"
            ),
            cta_label="Manage subscription",
            cta_url=f"{SITE}/account",
            cta_secondary_label="Skip this month",
            cta_secondary_url=f"{SITE}/account",
        ),
    ),
    (
        "13_post_purchase_feedback.html",
        dict(
            preview_text="Box landed. How'd it feel?",
            heading="So &mdash; what do you think?",
            body_html=(
                "<p>Your box should be a few days into its new home by now. We'd love to know what you thought.</p>"
                "<p><strong>Three quick things:</strong></p>"
                "<ol style=\"margin:0 0 16px;padding-left:20px;\">"
                "<li style=\"margin:0 0 8px;\">Was there a favorite item? (We use this to inform future boxes.)</li>"
                "<li style=\"margin:0 0 8px;\">Was there anything you'd skip? (Same reason &mdash; honest answers help.)</li>"
                "<li style=\"margin:0;\">Did the box feel worth the money?</li>"
                "</ol>"
                "<p>Just reply to this email with whatever you've got. One word, three sentences, a photo &mdash; whatever's easy. A real person on our team reads every reply.</p>"
                "<p>If anything was off, our value guarantee covers it: refund, replace, or credit. Just say the word.</p>"
            ),
            cta_label="Reply with feedback",
            cta_url="mailto:hello@gearheadbox.com?subject=This%20month%27s%20box",
        ),
    ),
    (
        "14_launch_announcement.html",
        dict(
            preview_text="The launch box is live. First boxes ship this week.",
            heading="The garage doors are open.",
            body_html=(
                "<p>Today's the day.</p>"
                "<p>The first wave of Gear Head Box launch boxes <strong>ships this week</strong>. After months of pre-order, sourcing, and packing, the boxes are leaving the warehouse.</p>"
                "<p>If you're a founding subscriber: your tracking email lands in the next 48&ndash;72 hours.</p>"
                "<p>If you're <strong>not</strong> a subscriber yet: the launch box is officially closed, but new subscriptions starting today get the September 15th box. Same value guarantee, same hand-curated approach &mdash; just a 30-day wait instead of an immediate ship.</p>"
                "<p>Real talk on what's in the launch box: a premium microfiber towel, a curated detailing item, a small surprise drop for everyone, and tier-specific apparel + tools for Apex and Podium. Pictures coming once people start unboxing &mdash; we don't want to spoil the surprise.</p>"
                "<p>Thanks for being here from the start.</p>"
            ),
            cta_label="Subscribe for September",
            cta_url=f"{SITE}/collections/tiers",
            cta_secondary_label="See the FAQ",
            cta_secondary_url=f"{SITE}/pages/faq",
        ),
    ),
]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for filename, kwargs in EMAILS:
        html = render(**kwargs)
        (OUT / filename).write_text(html)
        print(f"Wrote {filename} ({len(html)} bytes)")
    print(f"\n{len(EMAILS)} templates written to {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
