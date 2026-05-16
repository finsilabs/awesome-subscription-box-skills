# Subscription Store Build Runbook with Visual Review Checkpoints

## Problem/Feature Description

A freelance Shopify developer is taking over the second half of a subscription box store build for Driftwood & Tide, a coastal lifestyle subscription box. The first developer completed Phase 0 (scope intake) and Phase 1 (brand vault). The new developer is responsible for all remaining phases: theme scaffold, products, subscriptions config, homepage, supporting pages, navigation, imagery, email automation, and QA.

The agency has had problems on past projects where developers built everything in JSON, pushed it all to the live store at once, and only discovered major visual layout bugs — misaligned tier cards, invisible buttons on mobile, text overlapping images — in production. Several clients were upset about the public-facing broken state. The agency now requires a build runbook that includes mandatory visual review checkpoints during the build process.

Your task is to write a complete build runbook for the remaining phases of the Driftwood & Tide store. The runbook will be handed to the developer and used as a literal checklist during the build.

## Output Specification

Produce the following file:

- `build-runbook.md` — a step-by-step runbook for completing the store build from Phase 2 through Phase 10

The runbook should:
- List each phase as a numbered section with specific steps
- Include explicit checkpoint steps where theme changes must be pushed to a preview/unpublished theme and visually verified before continuing
- Note any commands or flags that differ between preview and live pushes
- Mark which types of visual issues to look for at each checkpoint
