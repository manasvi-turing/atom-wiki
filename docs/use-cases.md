---
tags: [use-cases, examples, workflows]
---

# Use Cases

## 1. 📚 Personal Knowledge Base

**The Problem:** Scattered notes across tools, hard to navigate, slow to share.

**The Solution:**
```
knowledge/
  ├── index.md (overview)
  ├── coding/
  │   ├── python.md
  │   └── javascript.md
  ├── books/
  │   └── summaries.md
  └── ideas/
      └── project-ideas.md
```

Generate once → Share anywhere → Update anytime

---

## 2. 🚀 Project Documentation

**Scenario:** GitHub repo needs documentation.

**Workflow:**
1. Write markdown in `docs/` folder
2. Use AI (Cursor, ChatGPT) to generate content
3. Build wiki: `atom-wiki docs -o wiki.html`
4. Commit `wiki.html` to repo
5. Enable GitHub Pages → Instant documentation site

**Bonus:** Include in releases for offline docs!

---

## 3. 👥 Team Knowledge Sharing

**The Problem:** Onboarding new team members takes weeks.

**The Solution:**
```
team-wiki/
  ├── index.md (welcome)
  ├── onboarding/
  │   ├── day-1.md
  │   └── tools-setup.md
  ├── processes/
  │   └── deployment.md
  └── architecture/
      └── system-design.md
```

**Share:** Upload to company drive, everyone gets the same beautiful wiki.

---

## 4. 📖 Course Materials

**For Educators:**
- Write lectures in markdown
- Include code examples
- Add images and diagrams
- Tag by topic
- Share single HTML file with students

**Students get:**
- Searchable content
- Table of contents
- Dark mode for night study
- Works on any device

---

## 5. 🔧 API Documentation

**Replace Postman/Swagger exports:**

```markdown
# API Reference

## Authentication
POST /api/auth/login

## Users API
GET /api/users
POST /api/users
...
```

Generate → Share with partners → No hosting needed!

---

## 6. 📝 Meeting Notes & Decisions

**Instead of Google Docs:**
```
meetings/
  ├── 2024-01-week1.md
  ├── 2024-01-week2.md
  └── decisions/
      └── architecture.md
```

**Benefits:**
- Version control in Git
- Easy to search
- Beautiful presentation
- One file to archive

---

## 7. 🎓 Research Notes

**For Students/Researchers:**
- Organize papers and notes
- Tag by subject
- Cross-reference easily
- Share with advisor
- Include in thesis appendix

---

## 8. 🏢 Company Handbook

**Replace PDF handbooks:**
- Policies
- Benefits
- Contact info
- FAQs
- Emergency procedures

**Update easily, redistribute instantly.**

---

## 9. 💡 Brainstorming & Ideas

**Creative teams:**
- Collect ideas in markdown
- Tag by category
- Review together
- Export as presentation

---

## 10. 🌐 Simple Website Alternative

**Need a quick site?**
- No hosting
- No build tools
- No frameworks
- Just markdown → HTML → Deploy anywhere

---

## Common Workflows

### Workflow 1: Solo Writer
```bash
write in vim/VSCode → build → share via Dropbox
```

### Workflow 2: Team Collaboration
```bash
Git repo → everyone writes markdown → build → host on intranet
```

### Workflow 3: AI-Assisted
```bash
Ask Cursor/ChatGPT to write docs → review → build → publish
```

### Workflow 4: Archive & Share
```bash
Project finished → generate wiki → include in ZIP → send to client
```

---

**See [Quick Start](./quick-start.md) to try it yourself!**

