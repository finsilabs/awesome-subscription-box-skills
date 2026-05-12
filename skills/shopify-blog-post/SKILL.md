---
name: shopify-blog-post
description: Use this skill when the user wants to create a blog post for their Shopify shop — phrases like "write a blog post", "publish to the shop blog", "create an article for the store". Drafts brand-voice-aligned post content (hooked, scannable, on-message), generates a hero image, and publishes to Shopify via the Articles API.
---

# Shopify blog post creation

Draft a blog post in the brand's voice, generate a hero image, and publish to a Shopify blog. Posts go from idea → draft → published in one pass.

## When to use

- The brand has a blog set up in Shopify (default is "News" blog)
- User wants long-form content (e.g., behind-the-scenes, product story, how-to guide)
- Editorial / SEO content as part of a content calendar

## Prerequisites

- Shopify MCP with article write access (`mcp__<shopify>__graphql_mutation`)
- `GOOGLE_API_KEY` for hero image generation (Nano Banana)
- Brand voice vault at `~/.claude/brand-voice-vault/<brand>/` strongly recommended

## Steps

### 1. Confirm topic and angle

Ask the user:
- Topic / title / angle (e.g., "Why we picked the K&N intake for September's box")
- Audience temperature (existing subscribers vs. cold visitors)
- Length target (default 600-900 words; long-form 1200-1800)
- Whether to publish or save as draft

### 2. Read brand vault

If `~/.claude/brand-voice-vault/<brand>/` exists, load:
- `voice.md` for tone, vocabulary
- `principles.md` for the brand position
- `audience.md` for who you're writing to
- `examples/source-quotes.md` for phrasing patterns

### 3. Outline + draft

Skeleton that works for most brand blog posts:

```
1. Hook (1 paragraph, 2-3 sentences)
2. The problem / context (2-3 paragraphs)
3. The product/decision/principle being explained (3-5 paragraphs, with sub-headings if >300 words)
4. Concrete example or evidence
5. What it means for the reader
6. Soft CTA (1 paragraph)
```

Voice rules:
- No "in today's fast-paced world" intros. Start with a concrete moment.
- Match the brand's reading level — masculine direct copy is shorter sentences than lifestyle copy.

### 4. Generate the hero image

Aspect ratio `16:9`, use Nano Banana with a prompt that fits the post's subject. See `shopify-product-with-images` skill for the generation pattern.

Save to `generated/blog/<slug>_hero.png` and upload to Shopify CDN via `stagedUploadsCreate` + `fileCreate`.

**Image upload error handling:**
- If `stagedUploadsCreate` returns errors, check that the file MIME type and size are within Shopify limits (images: ≤20 MB, JPEG/PNG/WEBP).
- After `fileCreate`, poll the file status until it is `READY` before using the CDN URL. If status stays `FAILED`, re-upload the source file.
- Do not proceed to article creation until a valid CDN URL is confirmed.

### 5. Find the blog ID

```graphql
query { blogs(first: 10) { nodes { id handle title } } }
```

Default blog is usually `News` with handle `news`.

### 6. Create the article

```graphql
mutation ArticleCreate($article: ArticleCreateInput!) {
  articleCreate(article: $article) {
    article { id handle title onlineStoreUrl }
    userErrors { field message }
  }
}
```

Variables:
```json
{
  "article": {
    "blogId": "gid://shopify/Blog/<id>",
    "title": "<title>",
    "handle": "<slug>",
    "body": "<HTML content>",
    "summary": "<150-char excerpt for OG/listing>",
    "tags": ["<tag1>", "<tag2>"],
    "isPublished": true,
    "image": {
      "altText": "<descriptive>",
      "originalSource": "<CDN URL>"
    }
  }
}
```

**Mutation validation:**
- Check the `userErrors` array first. If any errors are present, do not treat the mutation as successful — report the `field` and `message` values to the user and stop.
- Confirm the returned `onlineStoreUrl` is non-null. If it is null and `isPublished` was true, the article may have been saved as draft — verify the article status via a follow-up query.
- If the mutation itself fails (network/MCP error), retry once. If it fails again, save the HTML draft locally and report the failure to the user.

### 7. Verify and link

After a successful mutation:
1. Confirm `userErrors` is empty.
2. Output the `onlineStoreUrl` to the user.
3. If the user asked for it, link from the homepage's Featured Blog section or footer menu.

## Conventions and SEO

See `shopify-blog-conventions.md` for HTML body conventions (heading levels, internal link patterns, pull quotes, mid-article image uploads) and SEO guidelines (title length, slug format, summary character counts, tag style).

## Cross-skill links

- `brand-voice-extract` → populate the vault before writing
- `klaviyo-campaign-create` → if the post should drive an email blast
- `klaviyo-calendar-plan` → schedule blog publishing alongside email cadence
