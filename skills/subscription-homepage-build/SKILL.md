---
name: subscription-homepage-build
description: Use this skill when the user wants to build a homepage optimized for a subscription-box business — phrases like "build a subscription homepage", "subscription main page", "homepage for monthly box", "subscription tier picker page". Generates a Dawn-compatible templates/index.json with hero → how-it-works → tier picker → recent drops → testimonials → FAQ → email capture, with tier images and brand-aligned copy.
---

# Subscription homepage build

Generate `templates/index.json` for a subscription-box homepage on a Dawn-based theme. The structure drives the visitor from emotional hook → mechanic explanation → tier choice → social proof → objection handling → email capture.

## Prerequisites

- Dawn-based Shopify theme with `templates/`, `sections/`, `config/` present
- Store is a subscription box with 1–4 tiers; tier product handles exist or will exist
- **Brand voice vault** at `~/.claude/brand-voice-vault/<brand>/` helpful but not required

## Section order

```
1. Hero (image-banner)               — emotional hook + 2 CTAs
2. Anchor 