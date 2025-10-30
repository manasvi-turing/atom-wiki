# 📚 Atom Wiki

> **Wiki generator for the offline world. One HTML file, share via USB, email, or carrier pigeon. No servers, no internet, no BS.**

---

## 🌍 For Users: Why This Exists

### The Problem
Your documentation lives in:
- 💸 SaaS platforms that charge per seat
- ☁️ Cloud services that go down when you need them
- 🔒 Proprietary formats that trap your data
- 🌐 Web apps that stop working when the internet dies

**Your knowledge is hostage. We're here to free it.**

### The Solution
```bash
atom-wiki ./docs -o wiki.html
```

**Boom.** One HTML file. That's it.

### What You Get

#### 💾 **It's Just a File**
- Drop it on a USB stick
- Email it to your team
- Put it on a shared drive
- Archive it for 20 years
- Open it in 2045 and it **still works**

#### 🔌 **Works Offline, Always**
- Internet down? Who cares.
- On a plane? Perfect.
- In a basement? Ideal.
- Apocalypse? You're the only one with docs.

#### 🎨 **Beautiful By Default**
- Hierarchical navigation (folders work like folders!)
- Table of contents that follows you
- Dark mode, light mode, system mode
- Looks good on phone, tablet, desktop
- No JavaScript frameworks that'll be deprecated in 6 months

#### 🆓 **Truly Free**
- No "free tier" that expires
- No "premium features" locked away
- No "per user" pricing
- No credit card required
- No account to create
- No tracking, analytics, or telemetry

### The Philosophy

**Own your files.** Your docs shouldn't live on someone else's server, tied to someone else's business model, dependent on someone else's infrastructure staying up.

**Share peer-to-peer.** USB sticks. Email attachments. File shares. The way files were meant to be shared.

**Build for permanence.** That wiki you generate today? It should work in 10 years. No updates required. No "end of support" notices. Just HTML and CSS doing what they've done since 1993.

**Zero dependencies.** The minute you depend on external services, CDNs, or API keys, your "documentation" becomes someone else's product. Not here.

### Who This Is For

- 📝 **Developers** who want to document projects without npm installing the internet
- 🏢 **Teams** tired of paying per-seat for a place to store markdown
- 🎓 **Students** archiving knowledge that'll outlive their .edu email
- 🔬 **Researchers** who need docs that work in 20 years when their grant is long gone
- 🏠 **Hobbyists** building personal knowledge bases without subscriptions
- 🌐 **Anyone** who believes files should be files

### Quick Start

```bash
# Install
uvx --from "git+https://github.com/manasvi-turing/atom-wiki.git" atom-wiki

# Run
atom-wiki ./your-docs -o wiki.html

# Share (literally any way)
cp wiki.html /Volumes/USB/
# or
email wiki.html to your team
# or
scp wiki.html yourserver:/var/www/
# or
carrier pigeon if you're feeling medieval
```

**That's it. You're done. You now have a file. A file you own. Forever.**

---

## 🛠️ For Developers: Technical Details

### Installation

#### **Option 1: Run with uvx (Recommended)**
```bash
uvx --from "git+https://github.com/manasvi-turing/atom-wiki.git" atom-wiki ./docs -o output.html
```

#### **Option 2: Install Globally**
```bash
uv tool install "git+https://github.com/manasvi-turing/atom-wiki.git"
atom-wiki ./docs -o output.html
```

#### **Option 3: Local Development**
```bash
git clone https://github.com/manasvi-turing/atom-wiki.git
cd atom-wiki
uv sync
uv run atom-wiki ./docs -o output.html
```

### Command-Line Options

```bash
atom-wiki <input_folder> [OPTIONS]

Arguments:
  input_folder              Path to folder containing markdown files

Options:
  -o, --output FILE         Output HTML file (default: output.html)
  --config FILE             Custom config YAML file
  --no-chat                 Disable AI chat feature
  --enable-chat             Enable AI chat feature (overrides config)
  -h, --help               Show help message
```

### Usage Examples

```bash
# Basic usage
atom-wiki ./docs -o wiki.html

# Custom config
atom-wiki ./docs -o wiki.html --config my-config.yaml

# Disable AI chat (smaller file)
atom-wiki ./docs -o wiki.html --no-chat

# Using Python module
python -m atomwiki ./docs -o output.html
```

### Features

#### 🎨 **Modern Design**
- Live theme switching (Light, Dark, Nord)
- Material Design icons
- Responsive layout (desktop, tablet, mobile)
- Self-contained (all CSS/JS embedded)

#### 📖 **Smart Navigation**
- Hierarchical sidebar with collapsible folders
- Floating table of contents
- Internal linking between markdown files
- Active section highlighting
- Browser history support

#### 🎯 **Content Processing**
- Recursive folder support
- Index prioritization (`index.md` first)
- Frontmatter support (tags, metadata)
- Code syntax highlighting
- Relative link resolution (`../`, `./`)

#### 🤖 **AI Chat (Optional)**
- Document Q&A using OpenAI or Google Gemini
- Bring your own API key
- Client-side processing (no data sent to servers)
- Toggle on/off via config

#### ⚙️ **Customization**
- YAML configuration for all settings
- Multiple theme support
- CSS variables for easy styling
- Font customization

### Configuration

Create a `config.yaml`:

```yaml
# AI Chat Feature (optional)
chat:
  enabled: false               # Enable/disable AI chat widget
  default_provider: "openai"   # openai or gemini
  default_model: "gpt-4o-mini"

# Output Settings
output:
  default_filename: "output.html"
  table_of_contents: true
  navigation_sidebar: true
  folder_navigation: true

# Styling & Theming
styling:
  default_theme: "system"      # light, dark, or system
  custom_css_path: "static/style.css"

# Theme Color Schemes
themes:
  light:
    bg_primary: "#ffffff"
    text_primary: "#333333"
    accent_primary: "#3498db"
  
  dark:
    bg_primary: "#0d1117"
    text_primary: "#c9d1d9"
    accent_primary: "#58a6ff"
```

### Adding Custom Themes

1. Define theme metadata:
```yaml
theme_metadata:
  - name: "dracula"
    display_name: "Dracula"
    icon: "nightlight"
    type: "dark"
```

2. Add color scheme:
```yaml
themes:
  dracula:
    bg_primary: "#282a36"
    bg_secondary: "#44475a"
    text_primary: "#f8f8f2"
    accent_primary: "#bd93f9"
```

3. Rebuild - theme appears automatically!

### Project Structure

```
atomwiki/
├── __init__.py          # Package metadata
├── __main__.py          # CLI entry point
├── cli.py               # Main converter code
├── config.yaml          # Default configuration
└── static/
    └── style.css        # All CSS styles
```

### Requirements

- **Python 3.11+**
- **uv package manager** - [Install uv](https://docs.astral.sh/uv/)
- **Dependencies:**
  - `markdown>=3.9` - Markdown to HTML conversion
  - `pyyaml>=6.0.3` - YAML configuration parsing

### Output File Details

The generated HTML includes:
- ✅ Left Sidebar - Hierarchical navigation
- ✅ Main Content - Rendered markdown
- ✅ Right TOC - Floating table of contents
- ✅ Settings Modal - Theme switcher
- ✅ All Assets Embedded - Fonts, icons, CSS, JS

**File size:** ~185KB (without chat) or ~200KB (with chat)

### Contributing

Contributions welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with `uv run atom-wiki ./test_nested -o test.html`
5. Submit a pull request

---

## 📄 License

MIT License - Feel free to use, modify, and distribute.

---

## 🔗 Links

- **GitHub:** https://github.com/manasvi-turing/atom-wiki
- **Issues:** https://github.com/manasvi-turing/atom-wiki/issues

---

## 🎯 Version

**Current Version:** 0.2.0

### Changelog

**v0.2.0** (Latest)
- ✨ Converted to proper package structure
- ✨ Live theme switching with CSS variables
- ✨ Material Design icons throughout
- ✨ Multiple theme support (Light, Dark, Nord variants)
- ✨ YAML configuration system
- ✨ Improved package data handling
- 🐛 Fixed CSS embedding for uvx installations

**v0.1.x**
- Initial release with basic features
- Hierarchical navigation
- TOC support
- AI chat integration

---

**Remember:** The best documentation is documentation you can still open in 10 years. Make files, not dependencies.
