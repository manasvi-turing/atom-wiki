# Atom Wiki - Technical Guide

Complete technical documentation for installation, configuration, and usage.

---

## Table of Contents

- [Installation](#installation)
- [Command-Line Reference](#command-line-reference)
- [Requirements](#requirements)
- [Configuration](#configuration)
- [External Dependencies](#external-dependencies)
- [Testing Offline Mode](#testing-offline-mode)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

---

## Installation

### Option 1: Quick Start (No Installation)

```bash
# Run directly with uvx (requires Python and uv)
uvx --from "git+https://github.com/manasvi-turing/atom-wiki.git" atom-wiki ./docs -o wiki.html
```

### Option 2: Global Installation

```bash
# Install globally with uv
uv tool install "git+https://github.com/manasvi-turing/atom-wiki.git"

# Use anywhere
atom-wiki ./docs -o wiki.html
```

### Option 3: Local Development

```bash
# Clone and setup
git clone https://github.com/manasvi-turing/atom-wiki.git
cd atom-wiki
uv sync

# Run locally
uv run atom-wiki ./docs -o wiki.html
```

---

## Command-Line Reference

### Build Wiki

```bash
atom-wiki <input_folder> [OPTIONS]

Options:
  -o, --output FILE     Output HTML file (default: output.html)
  --config FILE         Custom config YAML file
  --no-chat             Disable AI chat feature
  --enable-chat         Enable AI chat feature
  -h, --help            Show help

# Examples
atom-wiki ./docs                    # Output to output.html
atom-wiki ./docs -o wiki.html       # Custom output name
atom-wiki ./docs --no-chat          # Disable AI chat
```

### Test Offline Mode

```bash
aw-offline <input_html> [OPTIONS]

Options:
  -o, --output FILE     Output HTML file (default: input_offline.html)
  -h, --help            Show help

# Example workflow
aw ./docs -o wiki.html            # Build wiki
aw-offline wiki.html              # Create offline test version
open wiki.html wiki_offline.html  # Compare both
```

This creates a test version with all CDN links broken to simulate complete offline mode. Perfect for verifying graceful degradation and testing the standalone file philosophy.

---

## Requirements

- **Python 3.11+**
- **uv package manager** - [Install uv](https://docs.astral.sh/uv/)
- **Dependencies:** `markdown>=3.9`, `pyyaml>=6.0.3`

---

## Configuration

Create a `config.yaml` in your project root or specify with `--config`:

```yaml
# Output Settings
output:
  default_filename: "output.html"
  table_of_contents: true

# Styling & Theming
styling:
  default_theme: "system"          # Options: light, dark, system
  default_family: "nord"           # Theme family (nord, rose_pine, catppuccin, solarized)

# Features
features:
  enable_datatables: true          # Interactive tables with search/sort

# AI Chat (optional)
chat:
  enabled: false
  default_provider: "openai"
  api_key: ""                      # Or use environment variable
```

### Available Themes

**Families:** `nord`, `rose_pine`, `catppuccin`, `solarized`, `default`  
**Modes:** `light`, `dark`, `system`

All themes support proper contrast, beautiful colors, and automatic dark mode switching.

---

## External Dependencies (CDN)

Atom Wiki uses the following CDN resources for enhanced functionality:

### Always Loaded

- **Google Fonts** (Noto Sans) - Typography
- **Material Icons** - UI icons with emoji fallback when offline
- **Prism.js** - Code syntax highlighting

### Optional (Config-based)

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

### Caching & Offline Behavior

All external resources are cached by the browser after first load, making subsequent visits work offline. If opened without internet on first load:
- Tables display as regular HTML tables
- Material Icons fall back to emojis
- Code blocks display as plain monospace
- Content remains 100% readable

---

## Testing Offline Mode

Want to see how your wiki looks without internet? Use the `aw-offline` command!

### Purpose

- **Verify graceful degradation** - See that content remains 100% readable
- **Test offline behavior** - Confirm no errors or broken functionality
- **Demo standalone philosophy** - Show it works without internet
- **Compare visual differences** - See what enhancements are CDN-dependent

### Usage

```bash
# Build your wiki
aw ./docs -o wiki.html

# Create offline test version
aw-offline wiki.html -o wiki_offline.html

# Compare both versions
open wiki.html wiki_offline.html
```

### What Changes in Offline Mode

- ⚠️ **Fonts** → System default (Arial, Helvetica)
- ⚠️ **Icons** → Emojis (automatically substituted)
- ⚠️ **Code highlighting** → Plain monospace text
- ⚠️ **DataTables** → Regular HTML tables

### What Stays the Same

- ✅ **100% of content readable**
- ✅ **All navigation works**
- ✅ **Theme switching works**
- ✅ **Tables display normally**
- ✅ **Zero functionality lost**

---

## Roadmap

### 🚀 Coming Soon

- **Fully Embedded Mode** - Zero external dependencies, works 100% offline
- **Mermaid Diagrams** - Auto-detected, conditionally embedded
- **Math Rendering** - KaTeX support for LaTeX equations
- **Custom Themes** - Easy theme creation and customization

### 🔮 Future Ideas

- Excalidraw support for hand-drawn diagrams
- Export to PDF functionality
- Better mobile navigation and responsive design
- Plugin system for extensibility
- Search across all content
- Version history and git integration

---

## Contributing

Contributions welcome! Whether it's bug fixes, new features, documentation, or themes.

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes**
4. **Test thoroughly** (`uv run atom-wiki ./docs -o test.html`)
5. **Commit your changes** (`git commit -m 'Add amazing feature'`)
6. **Push to branch** (`git push origin feature/amazing-feature`)
7. **Submit a Pull Request**

### Development Setup

```bash
git clone https://github.com/manasvi-turing/atom-wiki.git
cd atom-wiki
uv sync
uv run atom-wiki ./docs -o test.html
```

### Testing

```bash
# Build test wiki
uv run aw ./docs -o test.html

# Test offline mode
uv run aw-offline test.html

# Open and verify
open test.html test_offline.html
```

---

## License

**MIT License**

Copyright (c) 2024 Atom Wiki

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

**TL;DR:** Use it, modify it, share it. It's yours.

---

## Additional Documentation

- **[Features](./features.md)** - Complete feature list
- **[Use Cases](./use-cases.md)** - Real-world scenarios
- **[Workflows](./workflows.md)** - Productivity tips
- **[Quick Start](./quick-start.md)** - Step-by-step guide
- **[FAQ](./faq.md)** - Common questions
- **[Index](./index.md)** - Documentation overview

---

## Links

- **GitHub:** https://github.com/manasvi-turing/atom-wiki
- **Issues:** https://github.com/manasvi-turing/atom-wiki/issues
- **Discussions:** https://github.com/manasvi-turing/atom-wiki/discussions

---

**Current Version:** 0.2.0  
**Last Updated:** 2024

Built with ❤️ and a healthy disrespect for over-engineered solutions.

