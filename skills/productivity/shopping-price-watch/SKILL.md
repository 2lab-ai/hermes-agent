---
name: shopping-price-watch
description: "Use when tracking shopping prices and purchase history."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [shopping, prices, ecommerce, cron, price-history]
    related_skills: [shop-app]
---

# Shopping Price Watch

## Overview

Use this skill to maintain a local JSON shopping list, collect current offers
from shopping sources, record price observations, and report whether the
current price is good against 3-month and 6-month local history. It does not
buy anything and does not assume scraped prices are reliable without source
links.

State lives under `~/.hermes/state/shopping_price_watch/`:

- `items.json` stores active and removed shopping-list items.
- `history.jsonl` stores one observed offer per line.

The deterministic helper script is:

```bash
python3 ~/.hermes/scripts/shopping_price_watch.py --help
```

## When to Use

- The user wants to add, remove, or list tracked shopping items.
- The user asks for current price comparison across Coupang, Naver Shopping,
  Amazon US, official stores, Shop.app, or equivalent purchase/search pages.
- The user wants KRW and USD comparison with explicit links.
- The user wants daily or recurring price monitoring with trend history.
- A cron job needs to record observed prices before producing a Korean brief.

Do not use for investment/stock prices; use a finance skill for that.

## Prerequisites

- Use live `web_search` / `web_extract` tools for current prices. Shopping
  pages are dynamic; prefer direct product pages or official store pages when
  marketplace snippets are ambiguous.
- Use `shop-app` when a US product search across Shopify stores is useful.
- If `digital-research-and-collection` is installed locally, use it as the
  broader research workflow wrapper.
- For currency conversion, use a current USD/KRW rate from a live source in the
  same run. If no rate is available, record the raw currency and say conversion
  is missing.

## How to Run

Use the helper script for deterministic list and history storage, then use live
research tools to collect current offers before recording observations.

State lives under `~/.hermes/state/shopping_price_watch/`, and the installed
script path is `~/.hermes/scripts/shopping_price_watch.py`.

## Quick Reference

```bash
SCRIPT=~/.hermes/scripts/shopping_price_watch.py

python3 "$SCRIPT" add --id airpods-pro-latest \
  --name "AirPods Pro latest revision" \
  --query "AirPods Pro latest revision"

python3 "$SCRIPT" remove airpods-pro-latest
python3 "$SCRIPT" list --active

python3 "$SCRIPT" record --item airpods-pro-latest \
  --source "Amazon US" \
  --title "Apple AirPods Pro latest revision" \
  --url "https://www.amazon.com/..." \
  --price 199.99 --currency USD --usd-krw 1365.20

python3 "$SCRIPT" report
```

## Procedure

### Add Or Remove Items

1. Add each item with a stable ASCII id. Keep the user-facing name close to the
   user's wording, but make the `query` precise enough for search.
2. Remove items with `remove`; this deactivates the item and keeps historical
   observations.
3. Use `list --active` before any daily collection run.

### Current Price Comparison

1. Resolve the current product generation first. Examples:
   - "latest iPhone Pro 256GB" means identify the current Apple iPhone Pro
     generation and storage.
   - "latest Galaxy Ultra 256GB" means identify the current Samsung Galaxy S
     Ultra generation and storage.
   - If the user says "iPod Pro", check whether they likely mean AirPods Pro;
     state the assumption.
2. Search at least these source classes when available:
   - Coupang or Naver Shopping / Naver Store for KRW.
   - Amazon US or Shop.app for USD.
   - Official Apple/Samsung pages as a reliability anchor.
3. For every usable offer, capture source, title, URL, price, currency, and
   timestamp. Record each offer with the script.
4. If a source only exposes a search-results URL or stale snippet, keep the URL
   but mark the price as unverified in the final answer unless the price was
   visible on a page you opened.

### Trend Report

1. Run `python3 "$SCRIPT" report` after recording current observations.
2. Treat `trend_windows.3mo.status == "good"` or `6mo.status == "good"` as a
   highlight-worthy price.
3. If a window says `accumulating`, say local history has fewer than two points
   in that window; do not invent a 3-month or 6-month trend.
4. If the user asks for a 1-year trend before enough local data exists, use
   public historical sources only when directly available and cite them.
   Otherwise say local history starts from the first recorded run.

## Daily Cron Prompt Pattern

Use an agent cron job, not `no_agent=True`, because marketplace research needs
live web tools. The prompt should:

1. Run `python3 ~/.hermes/scripts/shopping_price_watch.py list --active`.
2. Get the current USD/KRW rate from a live source.
3. For each item, search Coupang, Naver Shopping/Store, Amazon US, Shop.app, and
   official stores where relevant.
4. Record each verified offer through `record`.
5. Run `report`.
6. Return a concise Korean report to the originating channel. Emphasize items
   whose 3-month or 6-month status is `good`; otherwise say history is still
   accumulating or price is not exceptional.

## Pitfalls

- Do not treat marketplace search-result snippets as exact checkout prices when
  the page was not opened.
- Do not compare Korean carrier-contract prices against US unlocked prices
  without saying they are different purchase conditions.
- Do not silently fix product names. If the user writes "iPod Pro" and the
  market product appears to be AirPods Pro, state the assumption.
- Do not claim a 3-month, 6-month, or 1-year trend when the local history file
  has too few data points.
- Do not use `.env` for shopping-list data; it is not secret.

## Verification

- `python3 ~/.hermes/scripts/shopping_price_watch.py list --active` returns the
  expected active items.
- `python3 ~/.hermes/scripts/shopping_price_watch.py report` returns JSON with
  `generated_at`, `state_dir`, and an `items` list.
- `~/.hermes/state/shopping_price_watch/history.jsonl` grows after recording
  current offers.
- The cron job uses `deliver: origin` for this channel or a concrete platform
  target configured in Hermes.
