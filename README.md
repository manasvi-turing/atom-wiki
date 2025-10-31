# 📚 Atom Wiki: The One-File Wonder

<div align="center" style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size: 1.1em; line-height: 1.6; color: #555; padding: 20px; max-width: 800px; margin: 0 auto;">
  <strong>TLDR:</strong> Tired of organizing digital furniture instead of writing? <code style="background: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-size: 0.9em;">atom-wiki ./my-notes -o wiki.html</code> turns your markdown folder into one beautiful HTML file. Email it, USB it, server it - it's just a file.
</div>

<div align="center">
  <img src="https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExMWN2YXowYjEwb3pxcG9nMDV2aTYwcGFrcGt6bHRhMzFiYzZxeWxodyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/1O2BRZcDgIfDsKMTbG/giphy.gif" width="600" alt="Coding Magic"/>
</div>


## My Tool Hopping Saga

I went through more note-taking tools than a digital nomad goes through coffee shops, and here's the realization that hit me: each tool was brilliant at what it did, but maybe a bit too brilliant for my needs.

Notion is fantastic for team wikis and databases, but I found myself spending more time designing pretty pages than actually writing content. Obsidian's graph view is pure magic for visual thinkers, but I kept getting lost connecting notes that didn't exist yet. MS Word remains the undisputed champion for formal documents, but I was constantly fighting formatting demons instead of capturing thoughts.

Confluence? Absolute powerhouse for enterprise teams - just felt like using a battleship to cross a pond for my personal notes. Hugo and Jekyll are incredible for serious web publishing, but configuration paralysis set in fast when I just wanted to write. Google Docs makes collaboration seamless, though sharing felt like hosting a party where everyone needs ID checks. And Gitbook creates stunning documentation - it's just that another subscription started quietly eating my wallet.

All amazing tools, just... not quite right for someone who mainly wants to think, write, and own their words.

## The Great Trade-Off

**What I happily abandoned:**
- ❌ Central server drama
- ❌ Auto-sync anxiety  
- ❌ Real-time collaboration FOMO

**What I gained:**
- ✅ Actual writing time
- ✅ True ownership (my files, my rules)
- ✅ Zero subscription guilt
- ✅ The joy of "it just works"

## The Magic Spell

```bash
uvx --from "git+https://github.com/manasvi-turing/atom-wiki.git" atom-wiki ./docs -o wiki.html
```

One command. One beautiful HTML file. Infinite possibilities.

## What You Get

✅ One self-contained HTML file (no "where are my images?")  
✅ Navigation that doesn't require a map  
✅ Themes that don't hurt your eyes  
✅ Works on your grandma's computer from 2008  
✅ No database to appease, no server to feed  
✅ Files you'll actually own in 2045

> *Current quirk:* Uses CDN magic for fonts/icons (cached after first load). Working on full hermit mode soon!

**Perfect for:** Personal knowledge bases, project documentation, recipe collections, or that novel you've been "meaning to write"

**Not for:** Real-time collaboration, NASA mission control, or impressing your VC friends

---

## Want More Details?

📖 **[Full Documentation](./docs/)** - Features, use cases, workflows, FAQ  
🔧 **[Technical Guide](./docs/README.md)** - Installation, configuration, commands, roadmap

---

Made with ❤️ and healthy dose of "why is this so complicated elsewhere?"

---

**License:** MIT | **Version:** 0.2.0 | **Cringe Level:** Moderately proud

---