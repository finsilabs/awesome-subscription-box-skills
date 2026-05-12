# Building a Brand Reference Library — KiwiCo

## Problem/Feature Description

Your consultancy advises subscription box founders, and you've started maintaining an internal brand reference library — a growing collection of well-documented brand profiles for leading players in the space. When a founder asks "how does KiwiCo talk to parents?", you want to be able to pull up a file and answer immediately rather than re-researching from scratch.

KiwiCo (https://www.kiwico.com) is a STEM-focused subscription box for kids and is a good starting point for the library. You need to document their brand in a structured way so that any team member can quickly understand how to research and reference it, see when it was captured, and trace any quotes or phrases back to the actual page they came from.

The library entry should be machine-readable where possible (JSON for metadata) so it can be indexed later, and should include actual verbatim language pulled from their website to give a feel for their voice. The quotes should be short enough to be clearly fair use — no long passages.

Once the research is done, write a brief snapshot of the brand's identity — a compact overview that gives any newcomer an instant grasp of the brand: who they are, the archetype they embody, who they sell to, their signature color, and their dominant tone of voice.

## Output Specification

Produce:
- A structured brand folder named after the brand (in a computer-friendly format)
- A machine-readable metadata file tracking: the brand name, the folder slug, when this research was done (in a standard date format), the list of pages that were fetched, and brief notes about the brand
- A quotes file containing short verbatim phrases from the site, each credited with its source URL
- A brief brand snapshot document (a short overview covering: the brand name, its archetype, its audience, its dominant color, and its dominant tone)
