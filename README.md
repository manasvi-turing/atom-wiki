# 📚 Atom Wiki

> **Turn your markdown folder into one HTML file. Share it on a USB stick. Email it. Put it on a server. It's just a file.**

## My Journey (The Short Version)

I kept trying different tools:
- **Notion** - Loved it, but spent more time organizing pages than writing
- **Obsidian** - Beautiful graphs, but I got lost connecting notes instead of creating them
- **MS Word** - Familiar, but I didn't want to waste time on fonts and spacing
- **Confluence** - Great for teams, but $10/user/month felt steep for my notes
- **Hugo/Jekyll** - Powerful, but I just wanted to write, not configure Ruby/Node
- **Google Docs** - Simple, but sharing meant endless permission requests
- **ReadTheDocs** - Professional, but seemed overkill for personal docs
- **Gitbook** - Beautiful, but another subscription I didn't need

I realized: I wasn't building knowledge. I was building *furniture for knowledge that never moved in.*

**What I gave up (and why I'm okay with it):**
- ❌ Central server? Don't need it. My knowledge lives in files I can backup however I want.
- ❌ Auto-sync between devices? I'll manage. Git, Dropbox, or a USB stick work fine.
- ❌ Real-time collaboration? Rarely needed. I focus on thinking deeply, then share when ready.

**What I gained:**
- ✅ FOSS philosophy - Open source, inspect the code, modify it, own it completely.
- ✅ No vendor lock-in - My files are mine. Forever. No export, no migration needed.
- ✅ Simple workflow - Write markdown anywhere (even WhatsApp), polish later, build when ready.

The ideas matter more than the sync. The ownership matters more than the convenience.

So I built this:

```bash
atom-wiki ./my-docs -o wiki.html
```

**One command. One HTML file. Done.**

Now I write in Markdown (in VimWiki, like a civilized person), run one command, and get a beautiful wiki I can:
- Drop on a USB stick
- Email to anyone
- Put on any server
- Open in 2045 and it still works

No subscriptions. No "please upgrade" popups. No vendor lock-in. Just files.

## Quick Start

```bash
# Install
uvx --from "git+https://github.com/manasvi-turing/atom-wiki.git" atom-wiki

# Run
atom-wiki ./your-docs -o wiki.html

# Share (literally any way you want)
cp wiki.html /Volumes/USB/
```

## What You Get

✅ **One self-contained HTML file** with all your docs  
✅ **Beautiful navigation** (hierarchical sidebar + floating TOC)  
✅ **Dark/light/system themes** that actually look good  
✅ **Works everywhere** (desktop, tablet, phone)  
✅ **No database** to migrate, no server to maintain  
✅ **Yours forever** - just a file you own

**Current caveat:** Uses CDNs for fonts/icons/syntax highlighting (cached after first load). Optional DataTables for interactive tables. Working on fully embedded mode soon!

## Want More Details?

📖 **[Full Documentation](./docs/index.md)** - Features, use cases, workflows, FAQ  
🔧 **[Technical Details](#technical-details)** - Installation, configuration, API  

---

## Technical Details

### Installation Options

```bash
# Option 1: Run with uvx (no install needed)
uvx --from "git+https://github.com/manasvi-turing/atom-wiki.git" atom-wiki ./docs -o wiki.html

# Option 2: Install globally
uv tool install "git+https://github.com/manasvi-turing/atom-wiki.git"
atom-wiki ./docs -o wiki.html

# Option 3: Local development
git clone https://github.com/manasvi-turing/atom-wiki.git
cd atom-wiki
uv sync
uv run atom-wiki ./docs -o wiki.html
```

### Command-Line Options

```bash
atom-wiki <input_folder> [OPTIONS]

Options:
  -o, --output FILE     Output HTML file (default: output.html)
  --config FILE         Custom config YAML file
  --no-chat             Disable AI chat feature
  --enable-chat         Enable AI chat feature
  -h, --help            Show help
```

### Requirements

- **Python 3.11+**
- **uv package manager** - [Install uv](https://docs.astral.sh/uv/)
- Dependencies: `markdown>=3.9`, `pyyaml>=6.0.3`

### Configuration

Create a `config.yaml`:

```yaml
# Output Settings
output:
  default_filename: "output.html"
  table_of_contents: true

# Styling & Theming
styling:
  default_theme: "system"  # light, dark, or system

# AI Chat (optional)
chat:
  enabled: false
  default_provider: "openai"
```

See [docs/](./docs/) for full configuration options and examples.

### External Dependencies (CDN)

**Always Loaded:**
- **Google Fonts** (Noto Sans) - Typography
- **Material Icons** - UI icons
- **Prism.js** - Code syntax highlighting

**Optional (Config-based):**
- **DataTables** - Interactive, searchable, sortable tables
  - Enable with `enable_datatables: true` in `config.yaml`
  - Features: global search, column sorting, pagination
  - ~150KB (cached after first load)
  - Only applied to tables with 3+ rows

**Note:** All resources are cached by the browser after first load for offline use.

---

## Roadmap

### 🚀 Coming Soon
- **Fully Embedded Mode** - Zero external dependencies, works 100% offline
- **Mermaid Diagrams** - Auto-detected, conditionally embedded
- **Math Rendering** - KaTeX support
- **Custom Themes** - Easy theme creation

### 🔮 Future Ideas
- Excalidraw support
- Export to PDF
- Better mobile navigation
- Plugin system

---

## Contributing

Contributions welcome! 

1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Test with `uv run atom-wiki ./docs -o test.html`
5. Submit a PR

---

## License

MIT License - Use it, modify it, share it. It's yours.

---

## Links

- **GitHub:** https://github.com/manasvi-turing/atom-wiki
- **Issues:** https://github.com/manasvi-turing/atom-wiki/issues
- **Full Docs:** [./docs/](./docs/)

---

**Current Version:** 0.2.0

Made with ❤️ and a healthy disrespect for over-engineered solutions.
