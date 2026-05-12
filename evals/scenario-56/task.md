# Add Landing Page to Shopify Navigation — PetalBox Floral Subscription

## Problem/Feature Description

PetalBox is a monthly floral subscription box that sends seasonal flower arrangements to subscribers each month. They recently built a landing page explaining how their subscription works, and the page is live on the store. Now they need this page added to the store's main navigation so visitors can find it.

The page was just created and its Shopify GID is `gid://shopify/OnlineStorePage/82947561023`. The main navigation menu GID is `gid://shopify/Menu/11204857938`. The navigation currently has items for Home, Shop, and About — the developer needs to add the landing page as a new "How It Works" item without breaking the existing items.

The developer also needs to make sure the page handle was chosen well — one that won't need to be changed in a year or two.

## Output Specification

Produce `shopify/navigation-update.md` containing:

1. The exact Shopify GraphQL mutation (with variables) to add the new navigation item to the existing main menu — keep all existing items intact
2. A brief recommendation on whether the page handle is a solid permanent choice for the store URL, and the reasoning behind that assessment
3. The shopify theme push command needed after updating the template, if any template file was updated in this process

The store URL is `petalbox.myshopify.com`. The page handle is `how-it-works`.
