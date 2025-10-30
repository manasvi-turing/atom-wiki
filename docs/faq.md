---
tags: [faq, help, troubleshooting]
---

# Frequently Asked Questions

## General Questions

### What makes this different from other documentation tools?

**One file. That's it.**
- No hosting required
- No build dependencies
- No framework lock-in
- Share via email, USB, cloud

Compare to alternatives:
- ❌ MkDocs → Needs hosting
- ❌ Docusaurus → Complex setup
- ❌ Jekyll → Ruby dependencies
- ✅ **This tool** → Single HTML file

### Do I need to know HTML/CSS/JavaScript?

**No!** Just write markdown:
```markdown
# My Heading
Some text with **bold** and *italic*.
```

Tool handles everything else.

### Can I use this commercially?

**Yes!** Use for:
- Internal company docs
- Client deliverables
- Product documentation
- Training materials

### Is it really just one file?

**Yes!** One HTML file with:
- ✅ All your content (fully embedded)
- ✅ All CSS styles (fully embedded)
- ✅ All JavaScript (fully embedded)
- ✅ Navigation logic (fully embedded)
- ⚠️ Fonts & icons (from CDN, cached after first load)
- ⚠️ Syntax highlighting (from CDN, cached after first load)

Result: ~200KB typical size (your content + embedded code)

**Note:** We're working on fully embedded mode (no CDNs) - coming soon!

---

## Features & Usage

### Can I customize the theme?

**Yes!** Edit `config.yaml`:
```yaml
styling:
  default_theme: "nord"
  default_mode: "dark"
```

Available themes: default, nord, rosepine, catppuccin, solarized

### How do internal links work?

**Automatically!** Just link to `.md` files:
```markdown
See [User Guide](./guides/user.md)
```

Tool converts to JavaScript navigation.

### Can I have images?

**Yes!** Two options:

**Option 1: Relative paths**
```markdown
![Logo](./images/logo.png)
```

**Option 2: URLs**
```markdown
![Logo](https://example.com/logo.png)
```

### Do code blocks support syntax highlighting?

**Yes!** Powered by Prism.js:
````markdown
```python
def hello():
    print("Hello!")
```
````

50+ languages supported.

### Can I disable features?

**Yes!** In `config.yaml`:
```yaml
features:
  show_file_titles: false
  show_frontmatter: false
  table_of_contents: false
```

---

## Technical Questions

### What's the file size limit?

**No hard limit**, but recommended:
- ✅ Up to 100 markdown files: Fast
- ⚠️ 100-500 files: Still works
- ❌ 1000+ files: Consider splitting

Typical wiki: 20-50 files = 100-300KB

### Does it work offline?

**Mostly!** Here's the reality:

✅ **Works offline:**
- All your content
- Navigation & TOC
- Theme switching
- Everything except fonts/icons/syntax highlighting

⚠️ **Needs internet on first load:**
- Google Fonts (cached by browser after first load)
- Material Icons (cached by browser after first load)
- Prism.js for code syntax highlighting (cached by browser)

**After first load:** Everything is cached, works offline!

**Future:** We're building fully embedded mode with zero CDN dependencies.

### Can I host on GitHub Pages?

**Absolutely!**
```bash
# Rename to index.html
mv wiki.html index.html

# Push to gh-pages branch
git checkout -b gh-pages
git add index.html
git commit -m "Deploy"
git push origin gh-pages
```

Your wiki: `https://username.github.io/repo/`

### Does it work on mobile?

**Yes!** Fully responsive:
- Touch-friendly navigation
- Collapsible sidebar
- Readable fonts
- Portrait & landscape

### What browsers are supported?

**Modern browsers:**
- ✅ Chrome/Edge (latest 2 versions)
- ✅ Firefox (latest 2 versions)
- ✅ Safari (latest 2 versions)
- ✅ Mobile browsers

IE11: Not supported.

---

## Troubleshooting

### Links don't work?

**Check:**
1. Use `.md` extension: `[Link](./file.md)`
2. Use relative paths: `./folder/file.md` or `../file.md`
3. File exists in your markdown folder

### Theme not applying?

**Solutions:**
1. Check `config.yaml` syntax
2. Verify theme name spelling
3. Try default theme first
4. Clear browser cache

### Sidebar not showing?

**Check:**
1. Browser JavaScript enabled?
2. No console errors? (F12 → Console)
3. File size too large? (>5MB?)

### Generated file too large?

**Reduce size:**
1. Optimize images
2. Remove unused files
3. Split into multiple wikis
4. Disable AI chat feature

### Can't build on Windows?

**Try:**
```powershell
# Use WSL
wsl
cd /mnt/c/your/folder
atom-wiki docs -o wiki.html
```

Or:
```powershell
# Windows native
python -m atomwiki docs -o wiki.html
```

---

## Best Practices

### How to structure content?

**Recommended:**
```
docs/
  ├── index.md          # Start here
  ├── getting-started/  # Onboarding
  ├── guides/           # How-tos
  ├── reference/        # API/Details
  └── about.md          # Meta
```

### Should I use Git?

**Yes!** Benefits:
- Version history
- Collaboration
- Backup
- CI/CD automation

### How often to rebuild?

**Options:**
1. **Manual**: When content changes
2. **Git hooks**: Pre-commit
3. **CI/CD**: On push
4. **Scheduled**: Daily/weekly

### How to handle large projects?

**Strategies:**
1. Split by topic/module
2. Use tags for cross-reference
3. Multiple wikis
4. Archive old content

---

## Comparison

| Feature | Atom Wiki | Notion | Confluence | MkDocs | Google Docs |
|---------|-----------|--------|------------|---------|-------------|
| **Cost** | Free | $8-15/user/mo | $5-10/user/mo | Free | Free |
| **Offline** | ⚠️ Mostly* | ❌ No | ❌ No | ❌ Needs server | ⚠️ Limited |
| **One File** | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ No |
| **Version Control** | ✅ Git | ⚠️ History | ⚠️ Limited | ✅ Git | ⚠️ History |
| **Setup Time** | < 1 min | 10-30 min | 30+ min | 10-30 min | < 1 min |
| **Hosting** | ❌ Not needed | ☁️ Cloud only | ☁️ Cloud/Self | 🖥️ Required | ☁️ Cloud only |
| **Sharing** | USB/Email/File | 🔗 Link only | 🔗 Link only | 🔗 Link only | 🔗 Link only |
| **Real-time Collab** | ❌ No | ✅ Yes | ✅ Yes | ❌ No | ✅ Yes |
| **Database Features** | ❌ No | ✅ Yes | ✅ Yes | ❌ No | ⚠️ Limited |
| **Markdown** | ✅ Native | ⚠️ Export only | ⚠️ Limited | ✅ Native | ❌ No |
| **Beautiful Output** | ✅ Yes | ✅ Yes | ⚠️ OK | ✅ Yes | ⚠️ OK |
| **Vendor Lock-in** | ❌ None | ⚠️ High | ⚠️ High | ❌ None | ⚠️ Medium |

\* *Needs internet on first load for fonts/icons (cached after). Working on fully embedded mode!*

### When to Choose What?

**Choose Atom Wiki if you want:**
- 📁 Files you own forever
- 📤 Share via USB/email/file servers
- 🚀 Zero setup time
- 💰 Zero cost
- 🔧 Git-based workflow

**Choose Notion/Confluence if you need:**
- 👥 Real-time collaboration
- 🗃️ Database features
- 📊 Project management
- 👤 User permissions

**Choose MkDocs/Docusaurus if you need:**
- 🔌 Extensive plugins
- 🎨 Complete customization
- 🌐 Public documentation sites

**Choose Google Docs if you need:**
- ✍️ Real-time co-editing
- 💬 Comment threads
- 📱 Mobile-first editing

---

## Getting Help

### Where to report bugs?

GitHub Issues: https://github.com/manasvi-turing/atom-wiki/issues

### How to contribute?

1. Fork repository
2. Create feature branch
3. Submit pull request

### Can I request features?

**Yes!** Open GitHub Issue with:
- Use case description
- Expected behavior
- Example if possible

---

**Still have questions?** Check [Features](./features.md) or [Workflows](./workflows.md)!

