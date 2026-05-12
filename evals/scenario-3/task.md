# Brand Vault Setup for a New Client — Crunchyroll Crate

## Problem/Feature Description

Your agency runs a marketing automation stack where every downstream tool — landing page generators, email campaign builders, and Shopify theme creators — all pull brand configuration from a shared, centralized location on each operator's machine. This means every brand vault must land in the same predictable place so those tools can find it automatically; a vault tucked away in the current project directory simply won't be discovered.

You've just onboarded Crunchyroll Crate (https://www.crunchyroll.com/crunchyroll-crate) as a new client. Before the first campaign goes out, you need to research and document their brand identity. The deliverable is a fully populated brand vault following your team's standard structure: voice, visual, color, principles, audience, source quotes, and metadata. Once it's created, any team member running a downstream skill on this machine will automatically pick up the brand reference without needing to know where you put it.

## Output Specification

Produce a complete brand vault for Crunchyroll Crate with all standard vault files. The folder must be named using the brand's computer-friendly slug form.

The vault should include:
- Voice and tone guide with vocabulary and sample copy
- Visual identity guide (typography, photo style, iconography)
- Color palette as a structured data file
- Brand principles document
- Audience profile
- Verbatim quotes from the website in an examples subfolder
- Metadata file recording sources and fetch date

After writing the vault, provide a brief confirmation note (saved as `vault_confirmation.txt`) stating the exact path where the vault was written and a one-line summary of each file created.
