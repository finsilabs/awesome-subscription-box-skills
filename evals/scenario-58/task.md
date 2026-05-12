# Local Theme Development Setup Guide — TrailGear Outdoor Subscription

## Problem/Feature Description

TrailGear is an outdoor gear subscription box. They've been running their Shopify store for two years using the built-in code editor, and all their theme customizations exist only on the live store with no local backup or version control. A contractor is about to start making significant changes to the theme — adding new section templates, modifying the layout, and reorganizing the navigation.

Before the contractor begins, the store owner wants a proper local development workflow set up: a copy of the live theme on the developer's laptop, version-controlled with git, so changes can be tracked and reverted if something goes wrong. The contractor should be able to preview changes locally before they touch the live store, and there should be a clear process for when and how to push changes back.

The store URL is `trailgear.myshopify.com`. The Shopify CLI is already installed.

## Output Specification

Produce `theme-setup-guide.md` — a step-by-step guide the developer can follow to:

1. Find out which themes are available on the store and identify the live theme
2. Download the live theme to the current working directory
3. Set up git version control so all theme files are tracked from the start
4. Verify the download succeeded
5. Start a local preview of the theme
6. Push changes back to the store when ready, with clear guidance on any risks

Include every exact command needed at each step. The guide should be ready for a developer who hasn't worked with this store before.
