# Product Journey Analysis for CraftKit

## Problem/Feature Description

CraftKit is a monthly art supplies subscription box that offers a range of starter kits and add-on products. The merchandising team is preparing for the next quarterly product review and wants to understand which products are genuinely driving the business versus which are just selling lots of one-off units to customers who never return.

They have two concerns: first, the Kids Craft Explorer Box has been their second-highest unit-volume seller, but the team suspects it may attract a different type of buyer who doesn't convert well to repeat subscription behavior. Second, they wonder if there are any lower-volume products that have an outsized positive impact on customer lifetime value.

The analytics team has prepared two data files in `inputs/`: a revenue baseline by product, and an order history dataset showing the first and second orders for a sample of 40 customers. Use these to produce the product journey analysis.

## Output Specification

Using the data in `inputs/`, produce a product path report at `journey-reports/product-path-2026-05-12.md`. The report should help the team answer:

- Which products bring in the most new customers (entry products)?
- Which entry products lead to the most repeat purchases (repeat drivers)?
- Which products have high entry rates but poor repeat conversion (dead ends)?
- Which products are underrated but strongly correlate with repeat buying (hidden gems)?
- What does a typical customer buy on their second order after each major entry product?
- What immediate merchandising or marketing decisions should the team make?
