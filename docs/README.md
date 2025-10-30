# Atom Wiki Documentation

This folder contains the **complete documentation** for Atom Wiki.

## What's Inside

- **index.md** - Overview and introduction
- **use-cases.md** - Real-world scenarios and workflows
- **quick-start.md** - Step-by-step getting started guide
- **features.md** - Complete feature list
- **workflows.md** - Productivity workflows and tips
- **faq.md** - Common questions and troubleshooting

## Try It Yourself

```bash
# Generate this documentation as a wiki
atom-wiki docs -o atom-wiki-docs.html

# Open in browser
open atom-wiki-docs.html
```

## Purpose

This demo showcases:
- **Simple structure** - Easy to navigate
- **Clear content** - Explains tool value
- **Real examples** - Practical use cases
- **Professional look** - Beautiful output

## Use This As

1. **Template** - Start your own documentation
2. **Reference** - See markdown examples
3. **Demo** - Show others what's possible
4. **Inspiration** - Ideas for your wiki

## Customize It

Feel free to:
- Copy this structure
- Modify the content
- Add your own pages
- Change frontmatter tags
- Adjust for your needs

---

## External Dependencies (CDN)

Atom Wiki uses the following CDN resources for enhanced functionality:

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
    - Pagination with customizable page size (5, 10, 25, 50, 100 rows)
    - Fully styled to match your theme (light/dark modes)
    - Headers and hover effects consistent with normal tables
  - Includes jQuery + DataTables core
  - ~150KB total (cached after first load)
  - Only applied to tables with 3+ rows
  - No default DataTables CSS loaded - uses custom theme styling
  - **Graceful fallback:** If CDN fails (no internet), tables display normally without errors

**Note:** All external resources are cached by the browser after first load, making subsequent visits work offline (except on first load). If opened without internet on first load, tables will display as regular HTML tables.

---

## Testing Offline Mode

Want to see how your wiki looks without internet? Use the `aw-offline` command!

### What

Creates a test version of your HTML file with all CDN links broken, simulating complete offline mode.

### Why

- **Verify graceful degradation** - See that content remains 100% readable
- **Test offline behavior** - Confirm no errors or broken functionality
- **Demo standalone philosophy** - Show it works without internet
- **Compare visual differences** - See what enhancements are CDN-dependent

### How

```bash
# Build your wiki
aw ./docs -o wiki.html

# Create offline test version
aw-offline wiki.html

# Compare both versions
open wiki.html wiki_offline.html
```

**What changes:**

- ⚠️ Fonts → System default (Arial, Helvetica)
- ⚠️ Icons → Placeholder boxes
- ⚠️ Code highlighting → Plain monospace text
- ⚠️ DataTables → Regular HTML tables

**What stays the same:**

- ✅ 100% of content readable
- ✅ All navigation works
- ✅ Theme switching works
- ✅ Tables display normally
- ✅ Zero functionality lost

---

**Generated Wiki:** See `demo.html` in parent folder!

