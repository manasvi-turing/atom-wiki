---
title: List Formatting Test
tags: [testing, formatting]
---

# List with Bold/Italic Formatting

## Regular List
- Item one
- Item two
- Item three

## List with Bold
- **Bold item** - Description
- **Another bold** - More text
- **Third bold** - Even more

## List with Italic
- *Italic item* - Description
- _Underscore italic_ - More text
- *Third italic* - Even more

## List with Mixed
- **Bold** and *italic* together
- This has __double underscore bold__
- This has _single underscore italic_
- **Bold** with (parentheses)
- **Multiple** *formats* __in__ _one_ line

## Nested with Bold
- **Parent item** - Has bold
  - **Nested bold** - Description
  - Regular nested
  - **Another bold nested**
- **Second parent**
  - Child item
  - **Bold child**

## Complex CDN-style List
**Always Loaded:**

- **Google Fonts** (Noto Sans) - Typography
- **Material Icons** - UI icons
- **Prism.js** - Code syntax highlighting

**Optional (Config-based):**

- **DataTables** - Interactive, searchable, sortable tables
  - Enable with `enable_datatables: true` in `config.yaml`
  - **Features:**
    - Global search across all columns
    - Sort by clicking column headers
  - Includes jQuery + DataTables core
  - ~150KB total (cached after first load)

## With Code Blocks

- **Command:** `npm install`
- **Usage:** Run `atom-wiki ./docs`
- **Config:** Set `enable: true` in config

