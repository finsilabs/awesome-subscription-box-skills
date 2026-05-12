# Corporate and Individual Gift Landing Page — NorthBrew Coffee Subscription

## Problem/Feature Description

NorthBrew is a specialty coffee subscription box — a new curated selection of single-origin roasts ships to subscribers each month. They've had success with individual gift subscriptions for birthdays and holidays, and are now seeing interest from companies that want to send coffee boxes as client gifts and employee appreciation packages.

The team wants a dedicated gift landing page at `/pages/gift` that serves both individual buyers and corporate buyers in one place. The page needs to feel premium — this is a gifted product, not a standard subscription signup. It should present the gifting options clearly, explain the gifting process in a simple step-by-step format, and give corporate buyers an easy path to reach the team.

The developer has the Shopify Page record already created. They now need the custom JSON template for the gift landing page. No real image files are available yet — use shopify://shop_images/ paths for all image references. The page should render at `/pages/gift` using the theme's custom template system.

## Output Specification

Produce `templates/page.gift.json` — a Dawn-compatible JSON template for the gift landing page. The template should contain multiple sections that together serve both individual and corporate gift buyers, structured appropriately for a premium gift experience.

Also produce `gift-page-notes.md` explaining which Dawn sections were used and in what order, and why the color scheme choices suit a gifting context.
