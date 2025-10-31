<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Atom Wiki: The One-File Wonder</title>
    <style>
        :root {
            --bg-primary: #ffffff;
            --bg-secondary: #f6f8fa;
            --text-primary: #24292f;
            --text-secondary: #57606a;
            --border: #d0d7de;
            --accent: #0969da;
            --accent-hover: #0550ae;
        }

        @media (prefers-color-scheme: dark) {
            :root {
                --bg-primary: #0d1117;
                --bg-secondary: #161b22;
                --text-primary: #f0f6fc;
                --text-secondary: #8b949e;
                --border: #30363d;
                --accent: #58a6ff;
                --accent-hover: #79c0ff;
            }
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
            line-height: 1.6;
            color: var(--text-primary);
            background: var(--bg-primary);
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem 1rem;
        }

        header {
            text-align: center;
            margin-bottom: 3rem;
            border-bottom: 1px solid var(--border);
            padding-bottom: 2rem;
        }

        h1 {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
            color: var(--text-primary);
        }

        .tagline {
            font-size: 1.25rem;
            color: var(--text-secondary);
            margin-bottom: 1.5rem;
        }

        .gif-container {
            margin: 2rem 0;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }

        .gif-container img {
            width: 100%;
            height: auto;
            display: block;
        }

        h2 {
            font-size: 1.5rem;
            font-weight: 600;
            margin: 2.5rem 0 1rem 0;
            color: var(--text-primary);
        }

        h3 {
            font-size: 1.25rem;
            font-weight: 600;
            margin: 2rem 0 1rem 0;
            color: var(--text-primary);
        }

        p {
            margin-bottom: 1rem;
            color: var(--text-secondary);
        }

        .tradeoff-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
            margin: 2rem 0;
        }

        @media (max-width: 768px) {
            .tradeoff-grid {
                grid-template-columns: 1fr;
            }
        }

        .tradeoff-column h3 {
            font-size: 1.1rem;
            margin-bottom: 1rem;
        }

        .abandoned, .gained {
            list-style: none;
        }

        .abandoned li, .gained li {
            padding: 0.5rem 0;
            display: flex;
            align-items: center;
        }

        .abandoned li::before {
            content: "❌";
            margin-right: 0.75rem;
            font-size: 0.9rem;
        }

        .gained li::before {
            content: "✅";
            margin-right: 0.75rem;
            font-size: 0.9rem;
        }

        .code-block {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 1.5rem;
            margin: 1.5rem 0;
            overflow-x: auto;
            font-family: 'SFMono-Regular', 'Consolas', 'Liberation Mono', monospace;
            font-size: 0.9rem;
        }

        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin: 2rem 0;
        }

        .feature-item {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 1.5rem;
        }

        .note {
            background: var(--bg-secondary);
            border-left: 4px solid var(--accent);
            padding: 1rem 1.5rem;
            margin: 2rem 0;
            border-radius: 0 6px 6px 0;
        }

        .use-cases {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
            margin: 2rem 0;
        }

        @media (max-width: 768px) {
            .use-cases {
                grid-template-columns: 1fr;
            }
        }

        .perfect-for, .not-for {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 1.5rem;
        }

        .perfect-for h3, .not-for h3 {
            margin-top: 0;
        }

        .perfect-for ul, .not-for ul {
            list-style: none;
            margin-top: 1rem;
        }

        .perfect-for li::before {
            content: "✓";
            color: #1a7f37;
            font-weight: bold;
            margin-right: 0.5rem;
        }

        .not-for li::before {
            content: "✗";
            color: #cf222e;
            font-weight: bold;
            margin-right: 0.5rem;
        }

        .links {
            display: flex;
            gap: 1rem;
            margin: 2rem 0;
            flex-wrap: wrap;
        }

        .link-button {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.75rem 1.5rem;
            background: var(--accent);
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 500;
            transition: background-color 0.2s;
        }

        .link-button:hover {
            background: var(--accent-hover);
        }

        footer {
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 1px solid var(--border);
            text-align: center;
            color: var(--text-secondary);
        }

        .footer-meta {
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin-top: 1rem;
            flex-wrap: wrap;
        }
    </style>
</head>
<body>
    <header>
        <h1>📚 Atom Wiki</h1>
        <p class="tagline">The One-File Wonder</p>
        <blockquote>
            <strong>TLDR:</strong> Tired of organizing digital furniture instead of writing? 
            <code>atom-wiki ./my-notes -o wiki.html</code> turns your markdown folder into one beautiful HTML file. 
            Email it, USB it, server it - it's just a file.
        </blockquote>
        
        <div class="gif-container">
            <img src="https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExMWN2YXowYjEwb3pxcG9nMDV2aTYwcGFrcGt6bHRhMzFiYzZxeWxodyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/1O2BRZcDgIfDsKMTbG/giphy.gif" alt="Coding Magic"/>
        </div>
    </header>

    <section>
        <h2>My Tool Hopping Saga 🤦‍♂️</h2>
        <p>
            I went through more note-taking tools than a digital nomad goes through coffee shops, 
            and here's the realization that hit me: each tool was brilliant at what it did, but 
            maybe a bit too brilliant for my needs.
        </p>
        <p>
            Notion is fantastic for team wikis and databases, but I found myself spending more time 
            designing pretty pages than actually writing content. Obsidian's graph view is pure magic 
            for visual thinkers, but I kept getting lost connecting notes that didn't exist yet. 
            MS Word remains the undisputed champion for formal documents, but I was constantly 
            fighting formatting demons instead of capturing thoughts.
        </p>
        <p>
            Confluence? Absolute powerhouse for enterprise teams - just felt like using a battleship 
            to cross a pond for my personal notes. Hugo and Jekyll are incredible for serious web 
            publishing, but configuration paralysis set in fast when I just wanted to write. 
            Google Docs makes collaboration seamless, though sharing felt like hosting a party 
            where everyone needs ID checks. And Gitbook creates stunning documentation - it's just 
            that another subscription started quietly eating my wallet.
        </p>
        <p>
            All amazing tools, just... not quite right for someone who mainly wants to think, write, 
            and own their words.
        </p>
    </section>

    <section>
        <h2>The Great Trade-Off 🤔</h2>
        <div class="tradeoff-grid">
            <div class="tradeoff-column">
                <h3>What I happily abandoned:</h3>
                <ul class="abandoned">
                    <li>Central server drama</li>
                    <li>Auto-sync anxiety</li>
                    <li>Real-time collaboration FOMO</li>
                </ul>
            </div>
            <div class="tradeoff-column">
                <h3>What I gained:</h3>
                <ul class="gained">
                    <li>Actual writing time</li>
                    <li>True ownership (my files, my rules)</li>
                    <li>Zero subscription guilt</li>
                    <li>The joy of "it just works"</li>
                </ul>
            </div>
        </div>
    </section>

    <section>
        <h2>The Magic Spell ✨</h2>
        <div class="code-block">
            uvx --from "git+https://github.com/manasvi-turing/atom-wiki.git" atom-wiki ./docs -o wiki.html
        </div>
        <p>One command. One beautiful HTML file. Infinite possibilities.</p>
    </section>

    <section>
        <h2>What You Get 🎁</h2>
        <div class="features">
            <div class="feature-item">One self-contained HTML file (no "where are my images?")</div>
            <div class="feature-item">Navigation that doesn't require a map</div>
            <div class="feature-item">Themes that don't hurt your eyes</div>
            <div class="feature-item">Works on your grandma's computer from 2008</div>
            <div class="feature-item">No database to appease, no server to feed</div>
            <div class="feature-item">Files you'll actually own in 2045</div>
        </div>
        
        <div class="note">
            <strong>Current quirk:</strong> Uses CDN magic for fonts/icons (cached after first load). Working on full hermit mode soon!
        </div>
    </section>

    <section>
        <h2>Perfect For Your Needs</h2>
        <div class="use-cases">
            <div class="perfect-for">
                <h3>✅ Perfect for:</h3>
                <ul>
                    <li>Personal knowledge bases</li>
                    <li>Project documentation</li>
                    <li>Recipe collections</li>
                    <li>That novel you've been "meaning to write"</li>
                </ul>
            </div>
            <div class="not-for">
                <h3>❌ Not for:</h3>
                <ul>
                    <li>Real-time collaboration</li>
                    <li>NASA mission control</li>
                    <li>Impressing your VC friends</li>
                </ul>
            </div>
        </div>
    </section>

    <section>
        <h2>Want More Details?</h2>
        <div class="links">
            <a href="./docs/" class="link-button">📖 Full Documentation</a>
            <a href="./docs/README.md" class="link-button">🔧 Technical Guide</a>
        </div>
    </section>

    <footer>
        <p>Made with ❤️ and healthy dose of "why is this so complicated elsewhere?"</p>
        <div class="footer-meta">
            <span><strong>License:</strong> MIT</span>
            <span><strong>Version:</strong> 0.2.0</span>
            <span><strong>Cringe Level:</strong> Moderately proud</span>
        </div>
    </footer>
</body>
</html>