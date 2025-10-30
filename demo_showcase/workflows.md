"""
tags: [workflows, productivity, tips]
"""

# Workflows

Real-world workflows to maximize productivity.

## 🤖 AI-Powered Documentation

**Use LLMs to write your docs:**

```bash
# Ask Cursor AI
"Write markdown documentation for my Python API"

# Or ChatGPT
"Create a user guide in markdown for feature X"

# Or Claude
"Generate API reference docs in markdown format"
```

**Then:**
```bash
atom-wiki docs -o wiki.html
```

**Result:** Professional documentation in minutes!

---

## 📚 Personal Knowledge Management

### Daily Workflow

```bash
# Morning: Review notes
vim knowledge/daily/2024-01-15.md

# Throughout day: Capture ideas
echo "## New Idea\n..." >> knowledge/ideas.md

# Evening: Generate wiki
atom-wiki knowledge -o my-brain.html

# Sync to cloud
cp my-brain.html ~/Dropbox/
```

### Weekly Review

```bash
# Update index with weekly summary
vim knowledge/index.md

# Reorganize tags
# Find all files with "wip" tag and update

# Rebuild
atom-wiki knowledge -o knowledge-v$(date +%Y%m%d).html
```

---

## 🚀 Project Documentation

### New Project Setup

```bash
# Create docs structure
mkdir -p project/docs/{guides,api,examples}
touch project/docs/index.md
touch project/docs/guides/quickstart.md
touch project/docs/api/reference.md

# Write initial content
cursor project/docs/  # Let AI write docs

# Generate
atom-wiki project/docs -o project-wiki.html

# Commit
git add docs/ project-wiki.html
git commit -m "Add documentation"
```

### Continuous Documentation

```bash
# Pre-commit hook: .git/hooks/pre-commit
#!/bin/bash
if [ -d "docs" ]; then
  atom-wiki docs -o wiki.html
  git add wiki.html
fi
```

### Release Documentation

```bash
# Include in release
VERSION=v1.0.0
atom-wiki docs -o wiki-$VERSION.html

# Package with release
zip release.zip binary wiki-$VERSION.html README.md

# Users get offline docs!
```

---

## 👥 Team Collaboration

### Repository Wiki

```bash
# Setup
git checkout -b wiki
mkdir wiki/
# Team writes content...

# Build
atom-wiki wiki -o index.html

# Deploy to GitHub Pages
git checkout gh-pages
cp wiki.html index.html
git push
```

### Internal Knowledge Base

```bash
# Shared drive workflow
TEAM_DRIVE="/mnt/team-drive/knowledge"

# Everyone contributes
git clone https://github.com/team/knowledge.git
cd knowledge
# Edit files...
git push

# Automated build (CI/CD)
# GitHub Action builds and uploads to shared drive
atom-wiki . -o $TEAM_DRIVE/wiki.html
```

---

## 🎓 Course/Training Materials

### Course Creation

```bash
course/
  ├── index.md              # Course overview
  ├── week1/
  │   ├── lecture1.md
  │   └── exercises.md
  ├── week2/
  │   └── lecture2.md
  └── resources/
      └── references.md

# Build for students
atom-wiki course -o cs101-wiki.html

# Share via LMS or email
```

### Live Updates

```bash
# During semester, update weekly
vim course/week3/lecture3.md

# Rebuild and share
atom-wiki course -o cs101-wiki.html
scp cs101-wiki.html server:/var/www/course/
```

---

## 🔬 Research Notes

### Paper Organization

```bash
research/
  ├── papers/
  │   ├── smith2023.md
  │   └── jones2024.md
  ├── experiments/
  │   └── exp001.md
  └── notes/
      └── ideas.md

# Tag by topic
"""
tags: [machine-learning, nlp, transformers]
"""

# Build personal research wiki
atom-wiki research -o research-notes.html
```

### Collaboration with Advisor

```bash
# Share progress
atom-wiki research -o progress-report.html
# Email to advisor

# Include in thesis
# Appendix: "See attached research-notes.html"
```

---

## 💼 Client Deliverables

### Project Handoff

```bash
# Throughout project
docs/
  ├── setup.md
  ├── architecture.md
  ├── api.md
  └── deployment.md

# End of project
atom-wiki docs -o client-documentation.html

# Package
zip handoff.zip \
  code/ \
  client-documentation.html \
  README.md

# Client gets comprehensive, searchable docs!
```

---

## 🔄 Continuous Integration

### GitHub Actions

```yaml
# .github/workflows/docs.yml
name: Build Documentation

on:
  push:
    paths:
      - 'docs/**'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build wiki
        run: |
          uvx --from git+https://github.com/repo/atom-wiki.git \
            atom-wiki docs -o wiki.html
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: .
          publish_branch: gh-pages
```

---

## 📊 Meeting Notes

### Weekly Meetings

```bash
meetings/
  ├── 2024/
  │   ├── week01.md
  │   ├── week02.md
  │   └── decisions/
  │       └── tech-stack.md
  └── index.md

# After each meeting
vim meetings/2024/week$(date +%V).md

# Regenerate
atom-wiki meetings -o meeting-notes.html

# Share with team
```

---

## 💡 Idea Collection

### Brainstorming Wiki

```bash
ideas/
  ├── products/
  ├── features/
  └── improvements/

# Capture ideas quickly
echo "## New Feature Idea" >> ideas/features/$(date +%F).md

# Review with team
atom-wiki ideas -o brainstorm.html
# Present in meeting
```

---

## Tips for All Workflows

### 1. Use Frontmatter
```markdown
"""
tags: [important, urgent, review]
author: Your Name
date: 2024-01-15
"""
```

### 2. Link Liberally
```markdown
See also: [Related Topic](./other.md)
```

### 3. Organize by Folder
```
Clear hierarchy = Easy navigation
```

### 4. Update Index.md
```markdown
Keep overview fresh with latest links
```

### 5. Version Your Wikis
```bash
wiki-2024-01.html
wiki-2024-02.html
```

---

**Ready to start?** [Quick Start](./quick-start.md)  
**Need ideas?** [Use Cases](./use-cases.md)

