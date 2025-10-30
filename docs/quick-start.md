---
tags: [getting-started, tutorial, guide]
---

# Quick Start

Get your first wiki up and running in **2 minutes**.

## Installation

```bash
# Using uvx (recommended)
uvx --from "git+https://github.com/manasvi-turing/atom-wiki.git" atom-wiki

# Or clone and install
git clone https://github.com/manasvi-turing/atom-wiki.git
cd atom-wiki
uv pip install -e .
```

## Your First Wiki

### Step 1: Create Content

```bash
mkdir my-docs
cd my-docs
```

Create `index.md`:
```markdown
# My Documentation

Welcome to my wiki!

## Quick Links
- [Guide](./guide.md)
- [FAQ](./faq.md)
```

Create `guide.md`:
```markdown
# User Guide

## Getting Started
Your content here...
```

### Step 2: Generate

```bash
atom-wiki my-docs -o wiki.html
```

### Step 3: Open

```bash
open wiki.html  # Mac
# or
xdg-open wiki.html  # Linux
# or
start wiki.html  # Windows
```

**Done! 🎉**

---

## Add Frontmatter (Optional)

Enhance any markdown file:

```markdown
---
title: My Page
tags: [guide, tutorial, beginner]
author: Your Name
---

# Content starts here
```

**Benefits:**
- Tags appear as clickable badges
- Organize content by topic
- Hover tags to see related pages

---

## Organize with Folders

```
docs/
  ├── index.md
  ├── guides/
  │   ├── beginner.md
  │   └── advanced.md
  ├── api/
  │   └── reference.md
  └── about.md
```

**Tool automatically creates:**
- ✅ Hierarchical navigation
- ✅ Collapsible folders
- ✅ Clean URLs

---

## Configuration

Create `config.yaml` (optional):

```yaml
# Feature Flags
features:
  show_file_titles: true      # Show file names in content
  show_frontmatter: true      # Display tags
  table_of_contents: true     # TOC panel
  
# Styling
styling:
  default_theme: "nord"       # Theme family
  default_mode: "system"      # light/dark/system
  
# Chat (optional)
chat:
  enabled: false              # AI chat widget
```

---

## Common Commands

```bash
# Basic build
atom-wiki ./docs -o output.html

# Custom config
atom-wiki ./docs -o wiki.html -c my-config.yaml

# Disable chat
atom-wiki ./docs -o wiki.html --no-chat

# Enable chat
atom-wiki ./docs -o wiki.html --enable-chat
```

---

## Tips & Tricks

### ✨ Linking Between Pages

```markdown
See [User Guide](./guides/user.md)
Check [API Docs](./api/reference.md)
```

Links automatically work in generated wiki!

### 🎨 Themes

Available themes:
- `default` - Clean blue
- `nord` - Nordic palette
- `rosepine` - Warm tones
- `catppuccin` - Pastel colors
- `solarized` - Classic

### 📱 Mobile-Friendly

Generated wiki works perfectly on:
- 📱 Phones
- 📱 Tablets
- 💻 Laptops
- 🖥️ Desktops

### 🌐 Deployment Options

**Option 1: Email**
```bash
# Just attach wiki.html
```

**Option 2: Cloud Storage**
```bash
# Upload to Drive/Dropbox
# Share link
```

**Option 3: GitHub Pages**
```bash
# Rename to index.html
mv wiki.html index.html
# Push to gh-pages branch
git checkout -b gh-pages
git add index.html
git commit -m "Deploy wiki"
git push origin gh-pages
```

**Option 4: Company Intranet**
```bash
# Upload to internal server
```

---

## Next Steps

- Explore [Use Cases](./use-cases.md) for inspiration
- Check [Features](./features.md) for full capabilities
- Try [Workflows](./workflows.md) for efficiency

---

**Questions? Issues? Check the [FAQ](./faq.md)!**

