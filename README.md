# awesome-subscription-box-skills

A collection of [Claude](https://claude.com/claude-code) skills for running a subscription-box business end-to-end — from extracting a brand's voice to launching paid campaigns, building a Shopify storefront, sending Klaviyo emails, and analyzing the customer journey.

Each skill is a self-contained `SKILL.md` under `skills/<name>/`, packaged as a Tessl tile (`tile.json`) for distribution and evaluation.

## Skills

### Brand foundation

| Skill | What it does |
|---|---|
| [brand-voice-extract](skills/brand-voice-extract/SKILL.md) | Crawl a brand's website and produce a reusable voice/visual/audience vault at `~/.claude/brand-voice-vault/<brand>/` that the other skills read from. |

### Shopify storefront

| Skill | What it does |
|---|---|
| [shopify-theme-create](skills/shopify-theme-create/SKILL.md) | Scaffold a new Horizon-based Shopify theme with brand styling applied. |
| [shopify-theme-clone](skills/shopify-theme-clone/SKILL.md) | Pull an existing live or unpublished theme from a Shopify store and initialize git. |
| [subscription-homepage-build](skills/subscription-homepage-build/SKILL.md) | Generate a Horizon `templates/index.json` for a subscription-box homepage (hero → tiers → testimonials → FAQ → capture). |
| [shopify-landing-page](skills/shopify-landing-page/SKILL.md) | Create a campaign-specific landing page (Black Friday, gifting, how-it-works, etc.) with a custom Liquid/JSON template. |
| [shopify-product-with-images](skills/shopify-product-with-images/SKILL.md) | Create/update a Shopify product with AI-generated imagery (Gemini Nano Banana) and a custom PDP template. |
| [shopify-blog-post](skills/shopify-blog-post/SKILL.md) | Draft and publish a brand-voiced blog article (with hero image) via the Shopify Articles API. |
| [page-critical-review](skills/page-critical-review/SKILL.md) | Senior-eye UX/conversion review of a homepage, PDP, or landing page — P0/P1/P2 issues with concrete fixes. |

### Paid ads (Meta)

| Skill | What it does |
|---|---|
| [ads-calendar-plan](skills/ads-calendar-plan/SKILL.md) | Plan a full year of paid spend — budget by funnel stage, creative cadence, seasonal flights. Coordinates with `klaviyo-calendar-plan`. |
| [ads-brief-create](skills/ads-brief-create/SKILL.md) | Generate a structured creative brief (objective, audience, hooks, copy variants, asset specs). |
| [ads-campaign-create](skills/ads-campaign-create/SKILL.md) | Create the campaign + ad sets + ads in Meta via MCP, with Nano-Banana-generated creative. |
| [ads-performance-analysis](skills/ads-performance-analysis/SKILL.md) | Pull Meta metrics, compare to benchmarks, output a prioritized recommendation list. |

### Klaviyo (email/SMS)

| Skill | What it does |
|---|---|
| [klaviyo-calendar-plan](skills/klaviyo-calendar-plan/SKILL.md) | Plan an annual or quarterly campaign calendar with cadence by lifecycle stage. |
| [klaviyo-campaign-create](skills/klaviyo-campaign-create/SKILL.md) | Build a single email campaign (template + draft) via the Klaviyo API. |
| [klaviyo-flow-build](skills/klaviyo-flow-build/SKILL.md) | Create multi-step flows (welcome series, abandoned cart, post-purchase) with the Flows API. |

### Analytics (Shopify journey)

| Skill | What it does |
|---|---|
| [shopify-journey-acquisition](skills/shopify-journey-acquisition/SKILL.md) | Channel scoreboard — sessions / conv / AOV / revenue per source, where to invest. |
| [shopify-journey-funnel](skills/shopify-journey-funnel/SKILL.md) | Session-to-order funnel, biggest leak identification, device/geo segments. |
| [shopify-journey-cohort-retention](skills/shopify-journey-cohort-retention/SKILL.md) | Acquisition-month cohort table, repeat % at 30/60/90d, LTV per cohort. |
| [shopify-journey-product-path](skills/shopify-journey-product-path/SKILL.md) | Entry products, repeat-drivers, dead-ends, and cross-sell affinity pairs. |
| [shopify-journey-segments](skills/shopify-journey-segments/SKILL.md) | Define named segments (VIP, lapsed, dormant…) ready to push to Klaviyo or ads. |

## How the skills fit together

```
brand-voice-extract  ──┐
                       ├──▶  every other skill reads ~/.claude/brand-voice-vault/<brand>/
                       │
shopify-theme-create  ─┤
shopify-theme-clone    │     ┌── subscription-homepage-build
                       └──▶  ├── shopify-landing-page
                             ├── shopify-product-with-images
                             ├── shopify-blog-post
                             └── page-critical-review

ads-calendar-plan  ──▶  ads-brief-create  ──▶  ads-campaign-create  ──▶  ads-performance-analysis
                   ╲                                                    ╱
                    ╲────── coordinates with ──────╲                   ╱
                                                    ▶ klaviyo-calendar-plan ──▶ klaviyo-campaign-create + klaviyo-flow-build

shopify-journey-* ──▶  feeds segments back into klaviyo + ads
```

## Requirements

The skills assume the following MCP servers / CLIs are connected:

- **Shopify** MCP (`mcp__9bf46487-…`) — product, theme, order, GraphQL access
- **Klaviyo** MCP (`mcp__4c43da2b-…`) — campaigns, flows, templates, segments
- **Meta Ads** MCP (`mcp__4ef1b68b-…`) — campaign / ad set / ad management, insights
- **Shopify CLI** — theme pull/push/dev
- **`uv`** + Gemini API key — image generation (`gemini-2.5-flash-image`)
- **`gh`** / **`git`** — theme version control

## Working with this tile

```bash
# Lint the tile
tessl skill lint

# Generate eval scenarios for a skill
tessl scenario generate . -n 10

# Run all evals in ./evals/
tessl eval run .

# Review and auto-optimize a SKILL.md
tessl skill review --optimize skills/<name>/

# Publish to the registry
tessl skill publish
```

The repo currently has **59 generated eval scenarios** in [evals/](evals/) covering all 20 skills (see [tile.json](tile.json)).

## Layout

```
.
├── tile.json              # tessl tile manifest (lists all 20 skills)
├── tessl.json             # tessl workspace config
├── skills/
│   └── <skill-name>/
│       ├── SKILL.md       # the skill itself (frontmatter + body)
│       └── ...            # optional reference files, scripts
└── evals/
    └── scenario-<n>/      # generated eval scenarios with checklists
```
