---
name: shopify-product-with-images
description: Use this skill to create or update Shopify products with AI-generated imagery — phrases like "create a product with images", "add product with photos", "generate product photos and upload to Shopify", "build a PDP". Generates images via Google Nano Banana (gemini-2.5-flash-image), uploads to Shopify CDN via stagedUploadsCreate + fileCreate, attaches them to the product, and creates/applies a custom product template (PDP).
---

# Shopify product + AI imagery

End-to-end product creation: generate brand-consistent imagery via Nano Banana → upload to Shopify CDN → attach to product → optionally apply a custom PDP template.

## When to use

- Creating a new product (subscription tier, physical SKU, gift card)
- Adding/replacing imagery on an existing product
- Building a custom Product Detail Page template

## Prerequisites

- `GOOGLE_API_KEY` in `.env` (for Nano Banana image generation)
- Shopify MCP connected with product write scope
- `uv` available for Python script execution
- Brand voice vault helpful but not required

## Steps

### 1. Gather product inputs

Ask user for what's not provided:
- **Title** (slug-able, e.g., "Pit Stop")
- **Price** in USD
- **Description** — 1-3 paragraphs, brand-voice if vault exists
- **Tags** — array of slug strings
- **SKU** — `<BRAND>-<HANDLE>-<VARIANT>` convention works
- **Tier vs. one-off** — affects whether subscription template applies
- **Image count** — typically 1 hero + 2-4 lifestyle/detail shots

### 2. Generate images via Nano Banana

Use a Python script following this pattern (see canonical at `~/dev/gearheadbox/scripts/generate_images.py`):

```python
# /// script
# requires-python = ">=3.11"
# dependencies = ["google-genai>=0.3.0", "python-dotenv>=1.0.0"]
# ///
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os, json
from pathlib import Path

load_dotenv()
client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

prompt = "..."
config = types.GenerateContentConfig(
    response_modalities=["IMAGE"],
    image_config=types.ImageConfig(aspect_ratio="1:1"),
)
response = client.models.generate_content(model="gemini-2.5-flash-image", contents=prompt, config=config)
for part in response.candidates[0].content.parts:
    if part.inline_data and part.inline_data.data:
        Path("generated/product.png").write_bytes(part.inline_data.data)
```

**Aspect ratios** for product images:
- `1:1` square — primary product card, gallery default
- `4:5` portrait — works on PDP gallery
- `16:9` wide — hero/lifestyle banner

**Prompt patterns that work for product photography:**

```
Product photograph of [item description] on [surface]. [Lighting:
"Soft directional studio light from upper left, dramatic shadows on right"].
Mood: [editorial e-commerce / lifestyle / minimalist]. No people. No
readable text or logos beyond the product's own. [Aspect] format.
```

For a tier subscription box (concrete example from gearheadbox):
```
Product photograph of a small subscription box on a polished concrete surface.
The box is matte kraft cardboard with a single vibrant racing-red wraparound band,
stamp-style sans serif text on the band reads 'PIT STOP'. Lid open at angle showing
contents arranged inside: a microfiber towel folded, a small enamel pin and sticker
pack on top, a small spray bottle of tire shine. Soft directional studio light, dark
gradient background. High-end e-commerce product photography. Square format.
```

### 3. Upload to Shopify CDN (3-step staged upload)

Shopify's product/file API requires public HTTPS URLs. Use `stagedUploadsCreate` → POST binary → `fileCreate`:

```python
# Pattern (full example at ~/dev/gearheadbox/scripts/upload_staged.py)
# 1. POST /api/graphql.json: stagedUploadsCreate with [{ resource: IMAGE, filename, mimeType, httpMethod }]
# 2. POST each binary to the returned GCS URL (multipart/form-data with the parameters)
# 3. POST: fileCreate with [{ originalSource, alt, contentType: IMAGE }]
# 4. Query the file by ID until fileStatus == READY; the response.image.url is the CDN URL
```

The Shopify MCP exposes:
- `mcp__<shopify>__graphql_mutation` for stagedUploadsCreate / fileCreate
- `mcp__<shopify>__graphql_query` to poll file status
- `mcp__<shopify>__create-product` / `update-product` for attaching the CDN URL

### 4. Create or update the product

For a new product:
```
mcp__<shopify>__create-product(
  title="Pit Stop",
  vendor="<Brand>",
  productType="Subscription Box",
  status="ACTIVE",
  tags=["subscription", "monthly-box", "tier-pit-stop"],
  descriptionHtml="...",
  options=["Title"],
  variants=[{
    "price": "54.00",
    "sku": "GHB-PITSTOP-MO",
    "optionValues": [{"optionName": "Title", "name": "Default Title"}],
    "inventoryItem": {"tracked": false}
  }]
)
```

Then attach images:
```
mcp__<shopify>__update-product(
  id="gid://shopify/Product/<id>",
  images=[{"url": "<CDN URL from step 3>", "altText": "..."}]
)
```

### 5. Apply a custom PDP template (optional)

For tier products or any product needing a non-standard layout:

1. Create `templates/product.<suffix>.json` in the theme (see canonical: `~/dev/gearheadbox/templates/product.subscription.json`).
2. Set the product's templateSuffix via:
```
mcp__<shopify>__graphql_mutation(
  query: "mutation($id: ID!) { productUpdate(input: { id: $id, templateSuffix: \"subscription\" }) { product { id templateSuffix } userErrors { field message } } }",
  variables: { "id": "gid://shopify/Product/<id>" }
)
```

The template suffix matches the filename: `product.subscription.json` ↔ `templateSuffix: "subscription"`.

### 6. Verify everything

```
mcp__<shopify>__graphql_query(query: "{ product(id: \"<gid>\") { handle title featuredImage { url } templateSuffix } }")
```

## Key files this skill creates

```
generated/<product>_*.png            — local AI-generated images
scripts/generate_<product>_images.py — re-runnable generator
templates/product.<suffix>.json      — custom PDP layout (if not default)
```

## Tradeoffs

- **AI-generated vs. real photography** — AI is fast (seconds per image) and consistent (same brand prompt = same look). Real photography wins on unique product detail and trust signals. For pre-launch / placeholder, AI is great. For long-term, replace with real shots.
- **Aspect ratio enforcement** — Nano Banana sometimes drifts from the requested aspect by ~5-10%. Don't rely on pixel-perfect ratios — crop with PIL post-generation if needed.
- **Color fidelity** — Nano Banana doesn't honor exact hex codes well. If the product needs a specific brand red (e.g., `#E10600`), generate on a neutral background and chroma-key in post (see `~/dev/gearheadbox/scripts/remove_background.py`).

## Common follow-ups

- Reduce or change a generated image — re-run with different prompt
- Make logo/product image transparent — invoke `remove_background.py` pattern
- Composite multiple images (e.g., 3 tier boxes side-by-side) — see `~/dev/gearheadbox/scripts/composite_tier_lineup.py`

## Reference example

The full pipeline ran for `~/dev/gearheadbox`:
- 9 brand images generated (hero, 3 tier boxes, 3 recent drops, 2 logos)
- Uploaded via stagedUploadsCreate
- 3 tier products created with featured images attached
- Custom `product.subscription.json` PDP template applied

## Embedded in this skill folder

Scripts (copy to your project's `scripts/` directory and run with `uv run`):
- `scripts/composite_images.py`
- `scripts/generate_images.py`
- `scripts/remove_background.py`
- `scripts/upload_staged.py`

Reference templates / examples (copy or adapt):
- `examples/product.subscription.json`
