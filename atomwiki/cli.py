#!/usr/bin/env python3
"""
Markdown to HTML Converter
Converts a folder of markdown files into a single HTML webpage with inline CSS and JS.
"""

import os
import re
import argparse
from pathlib import Path
import markdown
from markdown.extensions import toc, fenced_code, tables
import yaml
import json

class MarkdownToHTMLConverter:
    def __init__(self, input_folder, output_file="output.html", enable_chat=None, config_file="config.yaml"):
        self.input_folder = Path(input_folder)
        self.output_file = Path(output_file)
        self.markdown_files = []
        self.config_file = Path(config_file)
        
        # Load configuration from YAML file
        self.config = self.load_config()
        
        # Set enable_chat: CLI argument overrides config file
        if enable_chat is not None:
            self.enable_chat = enable_chat
        else:
            self.enable_chat = self.config.get('chat', {}).get('enabled', True)
        
        # Set show_file_titles from config
        self.show_file_titles = self.config.get('features', {}).get('show_file_titles', True)
        
        # Set show_frontmatter from config
        self.show_frontmatter = self.config.get('features', {}).get('show_frontmatter', True)
        
        # Set enable_datatables from config
        self.enable_datatables = self.config.get('features', {}).get('enable_datatables', False)
    
    def load_config(self):
        """Load configuration from YAML file"""
        try:
            # Try user-provided config file path first
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    print(f"📝 Loaded configuration from {self.config_file}")
                    return config if config else {}
            
            # Try path relative to this file (for development/packaged)
            config_path = Path(__file__).parent / 'config.yaml'
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    print(f"📝 Loaded configuration from {config_path}")
                    return config if config else {}
            
            print(f"⚠️  Config file not found. Using defaults.")
            return {}
        except Exception as e:
            print(f"⚠️  Error loading config file: {e}. Using defaults.")
            return {}
        
    def find_markdown_files(self):
        """Find all markdown files in the input folder and subfolders, prioritizing index.md"""
        if not self.input_folder.exists():
            raise FileNotFoundError(f"Folder {self.input_folder} does not exist")
            
        # Find all .md files recursively
        all_md_files = list(self.input_folder.rglob("*.md"))
        
        if not all_md_files:
            raise FileNotFoundError(f"No markdown files found in {self.input_folder}")
        
        # Check for index.md and prioritize it
        index_file = None
        other_files = []
        
        for file in all_md_files:
            if file.name.lower() in ['index.md', 'index.markdown']:
                index_file = file
            else:
                other_files.append(file)
        
        # Sort other files by path (alphabetically)
        other_files.sort(key=lambda x: str(x))
        
        # Validate that index.md exists - REQUIRED
        if not index_file:
            raise ValueError(f"❌ Error: index.md is required but not found in {self.input_folder}\n"
                           f"   Please create an index.md file as the entry point for your documentation.")
        
        # Build final list with index first
        self.markdown_files = [index_file] + other_files
        print(f"Found {len(self.markdown_files)} markdown files (starting with index.md):")
        
        for file in self.markdown_files:
            # Show relative path from input folder
            rel_path = file.relative_to(self.input_folder)
            print(f"  - {rel_path}")
    
    def parse_frontmatter(self, content):
        """Parse YAML frontmatter from markdown content (works for all .md files)"""
        frontmatter = {}
        
        # Check if content starts with --- (YAML frontmatter)
        if content.strip().startswith('---'):
            # Find the closing ---
            lines = content.strip().split('\n')
            if len(lines) > 1:
                # Find the second --- that closes the frontmatter
                end_index = None
                for i in range(1, len(lines)):
                    if lines[i].strip() == '---':
                        end_index = i
                        break
                
                if end_index:
                    # Extract frontmatter section (between the two ---)
                    fm_section = '\n'.join(lines[1:end_index])
                    # Extract the actual markdown content (after closing ---)
                    markdown_content = '\n'.join(lines[end_index + 1:]).strip()
                    
                    # Parse YAML frontmatter
                    try:
                        frontmatter = yaml.safe_load(fm_section) or {}
                    except yaml.YAMLError as e:
                        print(f"Warning: Failed to parse frontmatter YAML: {e}")
                        frontmatter = {}
                    
                    return frontmatter, markdown_content
        
        return {}, content
    
    def read_markdown_file(self, file_path):
        """Read and return the content of a markdown file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return ""
    
    def normalize_code_fence_indentation(self, markdown_content):
        """
        Remove indentation from code fences to ensure they're recognized as fenced code blocks.
        Code fences with indentation are often inside lists, but Python Markdown's fenced_code
        extension doesn't handle indented fences well. We'll de-indent them temporarily for processing.
        """
        import re
        lines = markdown_content.split('\n')
        normalized_lines = []
        in_code_fence = False
        fence_indent = 0
        
        for line in lines:
            # Check if line is a code fence (opening or closing)
            fence_match = re.match(r'^([ ]*)```', line)
            if fence_match:
                indent = len(fence_match.group(1))
                if not in_code_fence:
                    # Opening fence
                    in_code_fence = True
                    fence_indent = indent
                    # Remove indentation from fence line
                    normalized_lines.append(line[indent:])
                else:
                    # Closing fence
                    in_code_fence = False
                    # Remove same indentation from fence line
                    normalized_lines.append(line[fence_indent:] if line.startswith(' ' * fence_indent) else line)
                    fence_indent = 0
            elif in_code_fence:
                # Inside code block - remove the fence indentation but preserve internal indentation
                if line.startswith(' ' * fence_indent):
                    normalized_lines.append(line[fence_indent:])
                else:
                    normalized_lines.append(line)
            else:
                # Not in code block - keep as is
                normalized_lines.append(line)
        
        return '\n'.join(normalized_lines)
    
    def convert_markdown_to_html(self, markdown_content, current_file_index):
        """Convert markdown content to HTML with internal link processing"""
        # Normalize code fence indentation first
        markdown_content = self.normalize_code_fence_indentation(markdown_content)
        
        # Configure markdown extensions
        # Using 'extra' which includes fenced_code, tables, attr_list, and better list handling
        extensions = [
            'extra',  # Includes fenced_code, tables, attr_list, and more
            'toc',
            # Note: nl2br removed - it interferes with nested list parsing
        ]
        
        md = markdown.Markdown(extensions=extensions)
        html_content = md.convert(markdown_content)
        
        # Process internal links to other markdown files
        html_content = self.process_internal_links(html_content, current_file_index)
        
        # Make heading IDs unique by prefixing with section index
        html_content = self.prefix_heading_ids(html_content, current_file_index)
        
        # Wrap tables in a div for better responsive handling
        html_content = self.wrap_tables(html_content)
        
        return html_content
    
    def wrap_tables(self, html_content):
        """Wrap tables in a div with table-wrapper class for responsive scrolling"""
        import re
        # Find all table tags and wrap them
        html_content = re.sub(
            r'<table>',
            r'<div class="table-wrapper"><table>',
            html_content
        )
        html_content = re.sub(
            r'</table>',
            r'</table></div>',
            html_content
        )
        return html_content
    
    def prefix_heading_ids(self, html_content, section_index):
        """Prefix all heading IDs with section index to ensure uniqueness"""
        import re
        
        # Pattern to match heading tags with IDs
        heading_pattern = r'<(h[1-6])\s+id="([^"]+)"'
        
        def replace_id(match):
            tag = match.group(1)
            old_id = match.group(2)
            new_id = f"section-{section_index}-{old_id}"
            return f'<{tag} id="{new_id}"'
        
        return re.sub(heading_pattern, replace_id, html_content)
    
    def generate_navigation(self):
        """Generate hierarchical navigation menu from markdown files with multi-level nesting"""
        # Build a nested folder structure
        folder_tree = {}
        
        for i, file_path in enumerate(self.markdown_files):
            rel_path = file_path.relative_to(self.input_folder)
            
            if rel_path.parent == Path('.'):
                # Root level file
                if 'root' not in folder_tree:
                    folder_tree['root'] = []
                folder_tree['root'].append((i, rel_path.stem))
            else:
                # Nested file - build path hierarchy
                path_parts = rel_path.parts[:-1]  # Exclude filename
                current_level = folder_tree
                
                # Navigate/create the folder structure
                for part in path_parts:
                    if part not in current_level:
                        current_level[part] = {}
                    current_level = current_level[part]
                
                # Add file to the deepest level
                if 'files' not in current_level:
                    current_level['files'] = []
                current_level['files'].append((i, rel_path.stem))
        
        nav_items = []
        
        # Add root files first
        if 'root' in folder_tree:
            for i, filename in folder_tree['root']:
                title = filename.replace('_', ' ').replace('-', ' ').title()
                nav_items.append(f'<li><a href="#" onclick="showSection({i})" class="nav-link" data-section-index="{i}">{title}</a></li>')
        
        # Recursively build navigation for nested folders
        nav_items.append(self._build_folder_navigation(folder_tree, ''))
        
        return '\n'.join(nav_items)
    
    def _build_folder_navigation(self, folder_tree, parent_path):
        """Recursively build navigation for nested folder structure"""
        nav_items = []
        
        for folder_name, folder_content in folder_tree.items():
            if folder_name == 'root':
                continue
                
            if isinstance(folder_content, dict):
                # This is a folder
                clean_folder_name = folder_name.replace('_', ' ').replace('-', ' ').title()
                folder_id = (parent_path + '_' + folder_name if parent_path else folder_name).replace('/', '_').replace('\\', '_')
                
                nav_items.append(f'''
                <li class="folder-item">
                    <div class="folder-header" onclick="toggleFolder('{folder_id}')">
                        <span class="material-symbols-rounded folder-icon" data-fallback="📁">folder</span>
                        <span class="folder-name">{clean_folder_name}</span>
                        <span class="material-symbols-rounded folder-toggle" data-fallback="▶">chevron_right</span>
                    </div>
                    <ul class="folder-contents" id="{folder_id}" style="display: none;">
                ''')
                
                # Add files in this folder
                if 'files' in folder_content:
                    for i, filename in folder_content['files']:
                        title = filename.replace('_', ' ').replace('-', ' ').title()
                        nav_items.append(f'<li><a href="#" onclick="showSection({i})" class="nav-link file-link" data-section-index="{i}" data-parent-folder="{folder_id}">{title}</a></li>')
                
                # Recursively add subfolders
                for subfolder_name, subfolder_content in folder_content.items():
                    if subfolder_name != 'files':
                        nav_items.append(self._build_folder_navigation({subfolder_name: subfolder_content}, folder_id))
                
                nav_items.append('</ul></li>')
        
        return '\n'.join(nav_items)
    
    def generate_toc(self, html_content):
        """Generate table of contents from HTML headings"""
        import re
        
        # Find all headings (h1-h6)
        heading_pattern = r'<h([1-6])[^>]*id="([^"]*)"[^>]*>(.*?)</h[1-6]>'
        headings = re.findall(heading_pattern, html_content)
        
        if not headings:
            return '<div class="toc-empty">No headings found</div>'
        
        toc_items = []
        for level, heading_id, heading_text in headings:
            # Clean heading text (remove HTML tags)
            clean_text = re.sub(r'<[^>]+>', '', heading_text).strip()
            if clean_text:
                indent_class = f"toc-level-{level}"
                # Use event.preventDefault() and return false to prevent default anchor behavior
                toc_items.append(f'<li class="{indent_class}"><a href="#{heading_id}" onclick="event.preventDefault(); scrollToHeading(\'{heading_id}\'); return false;">{clean_text}</a></li>')
        
        return f'<ul class="toc-list">{"".join(toc_items)}</ul>'
    
    def process_internal_links(self, html_content, current_file_index):
        """Process internal links to other markdown files"""
        import re
        
        # Pattern to match links to .md files
        link_pattern = r'<a href="([^"]*\.md)">([^<]*)</a>'
        
        def replace_link(match):
            link_path = match.group(1)
            link_text = match.group(2)
            
            # Find the target file index
            target_index = self.find_file_index_by_path(link_path, current_file_index)
            
            if target_index is not None:
                # Create internal navigation link
                return f'<a href="#" onclick="navigateToSection({target_index}); return false;" class="internal-link">{link_text}</a>'
            else:
                # Keep original link if file not found
                print(f"⚠️  Warning: Could not resolve link '{link_path}' in file index {current_file_index}")
                return match.group(0)
        
        return re.sub(link_pattern, replace_link, html_content)
    
    def find_file_index_by_path(self, link_path, current_file_index):
        """Find the index of a file by resolving relative path from current file"""
        # Get the current file's location
        current_file = self.markdown_files[current_file_index]
        current_file_rel_path = current_file.relative_to(self.input_folder)
        current_dir = current_file_rel_path.parent
        
        # Clean up the link path (remove ./ prefix if present)
        link_path_clean = link_path.lstrip('./')
        
        # Resolve the relative path
        if link_path.startswith('../'):
            # Handle parent directory references
            target_path = (current_dir / link_path).resolve()
        elif link_path.startswith('./'):
            # Handle current directory references
            target_path = (current_dir / link_path_clean).resolve()
        else:
            # Handle direct references (assume current directory)
            target_path = (current_dir / link_path).resolve()
        
        # Make target_path relative to input_folder for comparison
        try:
            target_rel = target_path.relative_to(self.input_folder.resolve())
        except ValueError:
            # Path is outside input folder, try without resolving
            target_rel = Path(str(current_dir / link_path).replace('\\', '/'))
        
        # Find matching file in our list
        for i, file_path in enumerate(self.markdown_files):
            file_rel = file_path.relative_to(self.input_folder)
            # Compare paths (normalize for comparison)
            if str(file_rel).replace('\\', '/') == str(target_rel).replace('\\', '/'):
                return i
        
        # Try alternative matching - just by filename if full path doesn't work
        target_name = Path(link_path).name
        for i, file_path in enumerate(self.markdown_files):
            if file_path.name == target_name:
                return i
        
        return None
    
    def load_css_from_file(self):
        """Load CSS content from static/style.css file and embed it in HTML"""
        # Try local file first (development)
        css_file_path = Path(__file__).parent / 'static' / 'style.css'
        
        if css_file_path.exists():
            try:
                with open(css_file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                print(f"⚠️  Warning: Error reading CSS file: {e}.")
        
        # If static/style.css doesn't exist, return minimal CSS
        # This allows the tool to work even without the CSS file
        print(f"⚠️  Warning: CSS file not found at {css_file_path}. Using minimal inline CSS.")
        return """
        /* Minimal fallback CSS */
        body { font-family: sans-serif; margin: 0; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        h1, h2, h3 { color: #333; }
        a { color: #3498db; text-decoration: none; }
        code { background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }
        """
    
    def generate_theme_css_variables(self):
        """Generate CSS custom properties from theme configuration"""
        themes = self.config.get('themes', {})
        theme_metadata = self.config.get('theme_metadata', [])
        
        if not themes:
            return ""
        
        css_vars = []
        
        # Create a map of theme names to their types
        theme_types = {}
        for meta in theme_metadata:
            if meta.get('type') != 'auto':  # Skip 'system' as it's not a real theme
                theme_types[meta['name']] = meta.get('type', 'light')
        
        # Find the first light theme for :root
        default_light_theme = None
        for theme_name, theme_type in theme_types.items():
            if theme_type == 'light' and theme_name in themes:
                default_light_theme = theme_name
                break
        
        # Generate CSS variables for each theme
        for theme_name, theme_colors in themes.items():
            if theme_name == default_light_theme:
                # First light theme goes in :root (default)
                css_vars.append(":root {")
                for var_name, color_value in theme_colors.items():
                    css_var_name = var_name.replace('_', '-')
                    css_vars.append(f"  --{css_var_name}: {color_value};")
                css_vars.append("}")
            
            # All themes get their own body class
            theme_type = theme_types.get(theme_name, 'light')
            css_vars.append(f"body.theme-{theme_name} {{")
            for var_name, color_value in theme_colors.items():
                css_var_name = var_name.replace('_', '-')
                css_vars.append(f"  --{css_var_name}: {color_value};")
            css_vars.append("}")
        
        return '\n'.join(css_vars)
    
    def get_theme_families(self):
        """Parse theme families from theme names
        
        Returns a dict of families with their display names:
        {
            'default': 'Default',
            'nord': 'Nord',
            'rosepine': 'Rosé Pine',
            ...
        }
        """
        themes = self.config.get('themes', {})
        families = {}
        
        # Add default family if light/dark themes exist
        if 'light' in themes or 'dark' in themes:
            families['default'] = 'Default'
        
        # Parse other theme families from naming convention
        for theme_name in themes.keys():
            if '_' in theme_name and (theme_name.endswith('_light') or theme_name.endswith('_dark')):
                # Extract family name (everything before _light/_dark)
                family_base = theme_name.rsplit('_', 1)[0]
                
                # Generate display name (capitalize and replace underscores)
                if family_base not in families:
                    display_name = family_base.replace('_', ' ').title()
                    families[family_base] = display_name
        
        return dict(sorted(families.items()))
    
    def get_default_theme(self):
        """Get default theme family from config"""
        return self.config.get('styling', {}).get('default_theme', 'default')
    
    def get_default_mode(self):
        """Get default mode (light/dark/system) from config"""
        return self.config.get('styling', {}).get('default_mode', 'system')
    
    def get_theme_config_json(self):
        """Get theme configuration as JSON for JavaScript
        
        Returns:
        {
            'defaultFamily': 'default',
            'defaultMode': 'system',
            'families': {'default': 'Default', 'nord': 'Nord', ...}
        }
        """
        import json
        return json.dumps({
            'defaultFamily': self.get_default_theme(),
            'defaultMode': self.get_default_mode(),
            'families': self.get_theme_families()
        })
    
    def generate_theme_selector(self):
        """Generate theme selector UI (dropdown + mode buttons)"""
        families = self.get_theme_families()
        
        # Generate dropdown options
        options = []
        for family_key, family_name in families.items():
            options.append(f'<option value="{family_key}">{family_name}</option>')
        
        dropdown_html = f'''
                        <div class="theme-selector-group">
                            <label for="theme-family">Theme</label>
                            <select id="theme-family" class="theme-dropdown" onchange="updateTheme()">
                                {chr(10).join(options)}
                            </select>
                        </div>
                        
                        <div class="theme-selector-group">
                            <label>Mode</label>
                            <div class="mode-buttons">
                                <button class="mode-button" data-mode="light" onclick="setMode('light')">
                                    <span class="material-symbols-rounded" data-fallback="☀️">light_mode</span>
                                    <span>Light</span>
                                </button>
                                <button class="mode-button" data-mode="dark" onclick="setMode('dark')">
                                    <span class="material-symbols-rounded" data-fallback="🌙">dark_mode</span>
                                    <span>Dark</span>
                                </button>
                                <button class="mode-button" data-mode="system" onclick="setMode('system')">
                                    <span class="material-symbols-rounded" data-fallback="💻">computer</span>
                                    <span>System</span>
                                </button>
                            </div>
                        </div>'''
        
        return dropdown_html
    
    def get_chat_html(self):
        """Return HTML for chat widget"""
        if not self.enable_chat:
            return ""
        
        return '''
        <button class="chat-toggle" id="chat-toggle" onclick="toggleChat()">
            <span class="material-symbols-rounded" data-fallback="💬">chat</span>
        </button>
        
        <div class="chat-widget" id="chat-widget">
            <div class="chat-header">
                <h4><span class="material-symbols-rounded" data-fallback="💬">chat</span> Document Chat</h4>
                <div class="chat-header-actions">
                    <button class="chat-settings-toggle" onclick="toggleChatSettings()" id="settings-toggle" title="Settings">
                        <span class="material-symbols-rounded" data-fallback="⚙️">settings</span>
                    </button>
                    <button class="chat-close" onclick="toggleChat()" title="Close">✕</button>
                </div>
            </div>
            
            <div class="chat-settings" id="chat-settings">
                <div id="settings-content">
                    <label for="chat-provider">AI Provider:</label>
                    <select id="chat-provider" onchange="updateProviderSettings()">
                        <option value="openai">OpenAI</option>
                        <option value="gemini">Google Gemini</option>
                    </select>
                    
                    <label for="chat-model">Model:</label>
                    <select id="chat-model">
                        <option value="gpt-4o-mini">GPT-4o Mini (Fast & Cheap)</option>
                        <option value="gpt-4o">GPT-4o (Most Capable)</option>
                        <option value="gpt-4-turbo">GPT-4 Turbo</option>
                        <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
                    </select>
                    
                    <label for="api-key">API Key:</label>
                    <input type="password" id="api-key" placeholder="Enter your API key..." />
                    
                    <div id="provider-info" style="font-size: 10px; color: #6c757d; margin-top: 4px;">
                        Your API key is stored locally and never sent to our servers.
                    </div>
                </div>
            </div>
            
            <div class="chat-messages" id="chat-messages">
                <div class="chat-message system">
                    👋 Hi! I can help you understand this document. Ask me anything about the content!
                </div>
            </div>
            
            <div class="typing-indicator" id="typing-indicator">
                AI is thinking...
            </div>
            
            <div class="chat-input-area">
                <textarea class="chat-input" id="chat-input" placeholder="Ask about the document..." rows="2"></textarea>
                <button class="chat-send" id="chat-send" onclick="sendMessage()">Send</button>
            </div>
        </div>
        '''
    
    def get_chat_js(self):
        """Return JavaScript for chat widget"""
        if not self.enable_chat:
            return ""
        
        return '''
        function toggleChat() {
            const chatWidget = document.getElementById('chat-widget');
            const chatToggle = document.getElementById('chat-toggle');
            // Detect mobile: portrait OR landscape with limited height
            const isMobile = window.innerWidth <= 768 || (window.innerWidth <= 1024 && window.innerHeight <= 600);
            
            if (chatWidget.classList.contains('open')) {
                // Hide chat
                chatWidget.classList.remove('open');
                chatToggle.style.display = 'flex';
                
                // Remove mobile fullscreen styles
                if (isMobile) {
                    chatWidget.classList.remove('mobile-fullscreen');
                    document.body.style.overflow = '';
                    
                    // Clear inline styles
                    chatWidget.style.position = '';
                    chatWidget.style.display = '';
                    chatWidget.style.flexDirection = '';
                    chatWidget.style.top = '';
                    chatWidget.style.left = '';
                    chatWidget.style.right = '';
                    chatWidget.style.bottom = '';
                    chatWidget.style.width = '';
                    chatWidget.style.height = '';
                    chatWidget.style.margin = '';
                    chatWidget.style.padding = '';
                    chatWidget.style.transform = '';
                }
            } else {
                // Show chat
                chatWidget.classList.add('open');
                chatToggle.style.display = 'none';
                
                // Apply mobile fullscreen behavior
                if (isMobile) {
                    chatWidget.classList.add('mobile-fullscreen');
                    document.body.style.overflow = 'hidden';
                    
                    // Get actual viewport dimensions
                    const viewportHeight = window.innerHeight;
                    const viewportWidth = window.innerWidth;
                    
                    // Explicitly set dimensions to ensure proper sizing
                    chatWidget.style.position = 'fixed';
                    chatWidget.style.display = 'flex';
                    chatWidget.style.flexDirection = 'column';
                    chatWidget.style.top = '0px';
                    chatWidget.style.left = '0px';
                    chatWidget.style.right = '0px';
                    chatWidget.style.bottom = '0px';
                    chatWidget.style.width = viewportWidth + 'px';
                    chatWidget.style.height = viewportHeight + 'px';
                    chatWidget.style.margin = '0';
                    chatWidget.style.padding = '0';
                    chatWidget.style.transform = 'none';
                    
                    // Let flexbox handle the layout naturally
                    // The CSS flex properties will automatically size the messages area
                }
            }
        }
        
        // Handle window resize while chat is open (throttled)
        let resizeTimeout;
        window.addEventListener('resize', function() {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(() => {
                const chatWidget = document.getElementById('chat-widget');
                if (chatWidget && chatWidget.classList.contains('open')) {
                    // Detect mobile: portrait OR landscape with limited height
                    const isMobile = window.innerWidth <= 768 || (window.innerWidth <= 1024 && window.innerHeight <= 600);
                    
                    if (isMobile) {
                        if (!chatWidget.classList.contains('mobile-fullscreen')) {
                            chatWidget.classList.add('mobile-fullscreen');
                            document.body.style.overflow = 'hidden';
                        }
                        
                        // Recalculate dimensions
                        const viewportHeight = window.innerHeight;
                        const viewportWidth = window.innerWidth;
                        
                        // Explicitly set dimensions to ensure proper sizing
                        chatWidget.style.position = 'fixed';
                        chatWidget.style.display = 'flex';
                        chatWidget.style.flexDirection = 'column';
                        chatWidget.style.top = '0px';
                        chatWidget.style.left = '0px';
                        chatWidget.style.right = '0px';
                        chatWidget.style.bottom = '0px';
                        chatWidget.style.width = viewportWidth + 'px';
                        chatWidget.style.height = viewportHeight + 'px';
                        chatWidget.style.margin = '0';
                        chatWidget.style.padding = '0';
                        chatWidget.style.transform = 'none';
                        
                        // Flexbox will handle layout naturally
                    } else {
                        // Switched to desktop - remove mobile styles
                        chatWidget.classList.remove('mobile-fullscreen');
                        document.body.style.overflow = '';
                        
                        // Clear all inline styles
                        chatWidget.style.position = '';
                        chatWidget.style.display = '';
                        chatWidget.style.flexDirection = '';
                        chatWidget.style.top = '';
                        chatWidget.style.left = '';
                        chatWidget.style.right = '';
                        chatWidget.style.bottom = '';
                        chatWidget.style.width = '';
                        chatWidget.style.height = '';
                        chatWidget.style.margin = '';
                        chatWidget.style.padding = '';
                        chatWidget.style.transform = '';
                    }
                }
            }, 100);
        });
        
        function toggleChatSettings() {
            const chatSettings = document.getElementById('chat-settings');
            chatSettings.classList.toggle('open');
        }
        
        function updateProviderSettings() {
            const provider = document.getElementById('chat-provider').value;
            const modelSelect = document.getElementById('chat-model');
            const info = document.getElementById('provider-info');
            
            if (provider === 'openai') {
                // Show OpenAI models
                modelSelect.innerHTML = `
                    <option value="gpt-4o-mini">GPT-4o Mini (Fast & Cheap)</option>
                    <option value="gpt-4o">GPT-4o (Most Capable)</option>
                    <option value="gpt-4-turbo">GPT-4 Turbo</option>
                    <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
                `;
                info.textContent = 'Get your API key from: https://platform.openai.com/api-keys';
            } else if (provider === 'gemini') {
                // Show Gemini models
                modelSelect.innerHTML = `
                    <option value="gemini-pro">Gemini Pro</option>
                    <option value="gemini-pro-vision">Gemini Pro Vision</option>
                `;
                info.textContent = 'Get your API key from: https://makersuite.google.com/app/apikey';
            }
        }
        
        function getCurrentDocumentContent() {
            const currentSection = document.querySelector('.content-section[style*="block"]');
            if (!currentSection) return '';
            
            // Get all text content from the current section
            const content = currentSection.querySelector('.section-content');
            if (!content) return '';
            
            // Clean up the content
            const text = content.innerText || content.textContent || '';
            return text.trim();
        }
        
        function addMessage(content, type) {
            const messagesContainer = document.getElementById('chat-messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `chat-message ${type}`;
            messageDiv.textContent = content;
            messagesContainer.appendChild(messageDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
        
        function showTyping() {
            document.getElementById('typing-indicator').classList.add('show');
        }
        
        function hideTyping() {
            document.getElementById('typing-indicator').classList.remove('show');
        }
        
        async function sendMessage() {
            const input = document.getElementById('chat-input');
            const message = input.value.trim();
            const apiKey = document.getElementById('api-key').value.trim();
            const provider = document.getElementById('chat-provider').value;
            const model = document.getElementById('chat-model').value;
            
            if (!message) return;
            if (!apiKey) {
                addMessage('Please enter your API key first.', 'system');
                return;
            }
            
            // Add user message
            addMessage(message, 'user');
            input.value = '';
            
            // Disable send button and show typing
            const sendButton = document.getElementById('chat-send');
            sendButton.disabled = true;
            showTyping();
            
            try {
                const documentContent = getCurrentDocumentContent();
                const response = await callAI(provider, apiKey, model, message, documentContent);
                addMessage(response, 'assistant');
            } catch (error) {
                addMessage(`Error: ${error.message}`, 'system');
            } finally {
                sendButton.disabled = false;
                hideTyping();
            }
        }
        
        async function callAI(provider, apiKey, model, question, documentContent) {
            const prompt = `You are a helpful assistant that answers questions about a document. 
            
Document Content:
${documentContent}

Question: ${question}

Please provide a helpful answer based on the document content. If the question cannot be answered from the document, please say so.`;

            if (provider === 'openai') {
                return await callOpenAI(apiKey, model, prompt);
            } else if (provider === 'gemini') {
                return await callGemini(apiKey, model, prompt);
            }
        }
        
        async function callOpenAI(apiKey, model, prompt) {
            const response = await fetch('https://api.openai.com/v1/chat/completions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${apiKey}`
                },
                body: JSON.stringify({
                    model: model,
                    messages: [{
                        role: 'user',
                        content: prompt
                    }],
                    max_tokens: 1000,
                    temperature: 0.7
                })
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error?.message || 'OpenAI API error');
            }
            
            const data = await response.json();
            return data.choices[0].message.content;
        }
        
        async function callGemini(apiKey, model, prompt) {
            const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    contents: [{
                        parts: [{
                            text: prompt
                        }]
                    }],
                    generationConfig: {
                        maxOutputTokens: 1000,
                        temperature: 0.7
                    }
                })
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error?.message || 'Gemini API error');
            }
            
            const data = await response.json();
            return data.candidates[0].content.parts[0].text;
        }
        
        // Add keyboard support for chat
        document.addEventListener('DOMContentLoaded', function() {
            const chatInput = document.getElementById('chat-input');
            if (chatInput) {
                chatInput.addEventListener('keydown', function(e) {
                    if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        sendMessage();
                    }
                });
            }
            
            // Initialize provider settings
            updateProviderSettings();
        });
        '''
    
    def generate_html_content(self):
        """Generate the complete HTML content"""
        # Read and convert all markdown files
        sections = []
        tag_file_map = {}  # Map tags to files: {tag: [{name, index, path}, ...]}
        
        for i, file_path in enumerate(self.markdown_files):
            markdown_content = self.read_markdown_file(file_path)
            if markdown_content.strip():
                # Parse frontmatter for ALL markdown files
                frontmatter, markdown_content = self.parse_frontmatter(markdown_content)
                
                html_content = self.convert_markdown_to_html(markdown_content, i)
                section_id = f"section-{i}"
                
                # Create title from relative path
                rel_path = file_path.relative_to(self.input_folder)
                if rel_path.parent == Path('.'):
                    # File is in root
                    section_title = rel_path.stem.replace('_', ' ').replace('-', ' ').title()
                else:
                    # File is in subfolder
                    folder_name = rel_path.parent.name.replace('_', ' ').replace('-', ' ').title()
                    file_name = rel_path.stem.replace('_', ' ').replace('-', ' ').title()
                    section_title = f"{folder_name} / {file_name}"
                
                # Generate TOC for this section
                toc_content = self.generate_toc(html_content)
                
                # Build tag-to-files mapping and generate tags HTML
                tags_html = ""
                if 'tags' in frontmatter and frontmatter['tags']:
                    tags = frontmatter['tags']
                    # Add this file to tag map for each tag
                    for tag in tags:
                        if tag not in tag_file_map:
                            tag_file_map[tag] = []
                        tag_file_map[tag].append({
                            'name': section_title,
                            'index': i,
                            'path': str(rel_path)
                        })
                    
                    # Generate tags HTML if frontmatter display is enabled
                    if self.show_frontmatter:
                        # Will add count badge after all files are processed
                        tags_items = ''.join([f'<span class="tag" data-tag="{tag}">{tag} <span class="tag-count"></span></span>' for tag in tags])
                        tags_html = f'<div class="frontmatter-tags">{tags_items}</div>'
                
                # Conditionally show section title based on config
                section_header = ""
                if self.show_file_titles:
                    section_header = f'''
                    <div class="section-header">
                        <h1 class="section-title">{section_title}</h1>
                    </div>
                    '''
                
                section_html = f'''
                <div id="{section_id}" class="content-section" style="display: {'block' if i == 0 else 'none'};">
                    {section_header}
                    {tags_html}
                    <div class="section-content">
                        {html_content}
                    </div>
                </div>
                '''
                sections.append(section_html)
        
        # Generate navigation
        navigation = self.generate_navigation()
        
        # Complete HTML template
        # Get folder name for title
        folder_name = self.input_folder.name.replace('_', ' ').replace('-', ' ').title()
        
        # Load CSS from external file
        css_content = self.load_css_from_file()
        
        # Generate theme CSS variables
        theme_css_variables = self.generate_theme_css_variables()
        
        # Get theme config for JavaScript
        theme_config_json = self.get_theme_config_json()
        
        # DataTables CSS and JS sections
        datatables_css = ""
        datatables_js = ""
        datatables_init = ""
        
        if self.enable_datatables:
            datatables_css = """
    <!-- DataTables CSS - Disabled, using custom theme styling -->"""
            
            datatables_js = """
    <!-- DataTables JS -->
    <script src='https://code.jquery.com/jquery-3.7.1.min.js'></script>
    <script src='https://cdn.datatables.net/1.13.7/js/jquery.dataTables.min.js'></script>"""
            
            datatables_init = """
    <script>
        // Initialize DataTables on all tables (with graceful fallback if CDN fails)
        if (typeof jQuery !== 'undefined' && typeof jQuery.fn.DataTable !== 'undefined') {
            $(document).ready(function() {
                $('.section-content table').each(function() {
                    // Skip tables that are too small (less than 3 rows)
                    const rowCount = $(this).find('tbody tr').length;
                    if (rowCount >= 3) {
                        $(this).DataTable({
                            pageLength: 10,
                            lengthMenu: [5, 10, 25, 50, 100],
                            language: {
                                search: "_INPUT_",
                                searchPlaceholder: "Search table..."
                            }
                        });
                    }
                });
            });
        } else {
            console.log('DataTables not available (CDN may have failed to load). Tables will display normally.');
        }
    </script>"""
        
        html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{folder_name}</title>
    
    <!-- Google Fonts - Noto Sans -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet">
    
    <!-- Google Material Symbols Rounded -->
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet">
    
    <!-- Prism.js for Syntax Highlighting -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" rel="stylesheet" />
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/line-numbers/prism-line-numbers.min.css" rel="stylesheet" />
    {datatables_css}
    
    <style>
        /* Theme CSS Variables */
        {theme_css_variables}
        
        /* Base Styles */
        {css_content}
    </style>
    <script>
        // Theme configuration from YAML
        const THEME_CONFIG = {theme_config_json};
        
        // Helper to construct theme name from family and mode
        function constructThemeName(family, mode) {{
            // Determine effective mode (resolve 'system' to 'light' or 'dark')
            let effectiveMode = mode;
            if (mode === 'system') {{
                effectiveMode = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
            }}
            
            // Construct theme name
            let themeName;
            if (family === 'default') {{
                themeName = effectiveMode; // 'light' or 'dark'
            }} else {{
                themeName = family + '_' + effectiveMode; // e.g., 'nord_light'
            }}
            
            return themeName;
        }}
        
        // Initialize theme before page renders to prevent flash
        (function() {{
            const savedFamily = localStorage.getItem('themeFamily') || THEME_CONFIG.defaultFamily;
            const savedMode = localStorage.getItem('themeMode') || THEME_CONFIG.defaultMode;
            const themeName = constructThemeName(savedFamily, savedMode);
            
            // Apply theme class
            document.documentElement.classList.add('theme-' + themeName);
        }})();
    </script>
</head>
<body>
    <div class="container">
        <nav class="sidebar" id="sidebar">
            <button class="sidebar-toggle" id="sidebar-toggle" onclick="toggleSidebar()" title="Collapse Sidebar">
                <span class="material-symbols-rounded" data-fallback="◀">chevron_left</span>
            </button>
            <div class="sidebar-nav">
                <h2><span class="material-symbols-rounded" data-fallback="📖">menu_book</span> {folder_name}</h2>
                <ul>
                    {navigation}
                </ul>
            </div>
            <div class="sidebar-footer">
                <button class="settings-button" onclick="openSettings()" title="Settings">
                    <span class="material-symbols-rounded settings-icon" data-fallback="⚙️">settings</span>
                    <span class="settings-text">Settings</span>
                </button>
            </div>
            <div class="sidebar-resize-handle" id="resize-handle"></div>
        </nav>
        
        <button class="sidebar-open-button" id="sidebar-open-button" onclick="toggleSidebar()" title="Open Sidebar" style="display: none;">
            <span class="material-symbols-rounded" data-fallback="▶">chevron_right</span>
        </button>
        
        <!-- Settings Modal -->
        <div class="settings-modal" id="settings-modal">
            <div class="settings-content">
                <div class="settings-header">
                    <h3><span class="material-symbols-rounded" data-fallback="⚙️">settings</span> Settings</h3>
                    <button class="settings-close" onclick="closeSettings()">✕</button>
                </div>
                <div class="settings-body">
                    <div class="setting-group">
                        <label class="setting-label"><span class="material-symbols-rounded" data-fallback="🎨">palette</span> Theme</label>
                        <div class="theme-selector">{self.generate_theme_selector()}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <main class="main-content">
            {''.join(sections)}
        </main>
        
        <aside class="toc-panel" id="toc-panel">
            <h3>Contents</h3>
            <div id="toc-content">
                <div class="toc-empty">Select a section to view its contents</div>
            </div>
        </aside>
        
        <button class="toc-toggle" id="toc-toggle" onclick="toggleTOC()">
            <span class="material-symbols-rounded" data-fallback="✕">close</span>
        </button>
        
        {self.get_chat_html()}
        
        <!-- Tag popup for showing files with same tag -->
        <div id="tag-popup" class="tag-popup"></div>
    </div>
    
    <script>
        let currentSection = 0;
        let navigationHistory = [{{
            type: 'section',
            sectionIndex: 0,
            scrollY: 0
        }}];
        let historyIndex = 0;
        let isBrowserNavigation = false;
        
        function showSection(index, updateHistory = true) {{
            // Close mobile sidebar when navigating on mobile
            if (window.innerWidth <= 768) {{
                const sidebar = document.getElementById('sidebar');
                sidebar.classList.remove('mobile-open');
                document.body.classList.remove('sidebar-mobile-open');
                document.getElementById('sidebar-open-button').style.display = 'flex';
            }}
            
            // Hide all sections
            const sections = document.querySelectorAll('.content-section');
            sections.forEach(section => {{
                section.style.display = 'none';
            }});
            
            // Show selected section
            const targetSection = document.getElementById(`section-${{index}}`);
            if (targetSection) {{
                targetSection.style.display = 'block';
                targetSection.scrollIntoView({{ behavior: 'smooth' }});
                
                // Update TOC for this section
                updateTOC(targetSection);
            }}
            
            // Update active nav item - use data attribute instead of array index
            const navLinks = document.querySelectorAll('.sidebar a.nav-link');
            navLinks.forEach(link => {{
                link.classList.remove('active');
            }});
            
            // Find the link with matching data-section-index
            const activeLink = document.querySelector(`.sidebar a.nav-link[data-section-index="${{index}}"]`);
            if (activeLink) {{
                activeLink.classList.add('active');
                
                // Auto-expand parent folders if the link is inside a folder
                const parentFolderId = activeLink.getAttribute('data-parent-folder');
                if (parentFolderId) {{
                    expandParentFolders(parentFolderId);
                }}
            }}
            
            // Update navigation buttons
            updateNavigationButtons(index);
            currentSection = index;
            
            // Update browser history if not already handling browser navigation
            if (updateHistory && !isBrowserNavigation) {{
                const state = {{ section: index }};
                const url = `#section-${{index}}`;
                history.pushState(state, '', url);
            }}
        }}
        
        function expandParentFolders(folderId) {{
            // Expand the direct parent folder
            const folder = document.getElementById(folderId);
            if (folder && folder.style.display === 'none') {{
                folder.style.display = 'block';
                
                // Update the toggle icon
                const toggle = document.querySelector(`[onclick="toggleFolder('${{folderId}}')"] .folder-toggle`);
                if (toggle) {{
                    toggle.classList.add('open');
                }}
            }}
            
            // Recursively expand parent folders if this folder is nested
            // Find parent folder by checking if folderId contains underscore (nested structure)
            if (folderId.includes('_')) {{
                const parentId = folderId.substring(0, folderId.lastIndexOf('_'));
                if (parentId) {{
                    expandParentFolders(parentId);
                }}
            }}
        }}
        
        function updateTOC(section) {{
            const tocContent = document.getElementById('toc-content');
            const headings = section.querySelectorAll('h1, h2, h3, h4, h5, h6');
            
            if (headings.length === 0) {{
                tocContent.innerHTML = '<div class="toc-empty">No headings found</div>';
                return;
            }}
            
            let tocHTML = '<ul class="toc-list">';
            headings.forEach(heading => {{
                const level = heading.tagName.charAt(1);
                const id = heading.id || heading.textContent.toLowerCase().replace(/[^a-z0-9]+/g, '-');
                if (!heading.id) heading.id = id;
                
                const text = heading.textContent.trim();
                // Use event.preventDefault() in onclick and return false to prevent default anchor behavior
                tocHTML += `<li class="toc-level-${{level}}"><a href="#${{id}}" onclick="event.preventDefault(); scrollToHeading('${{id}}'); return false;">${{text}}</a></li>`;
            }});
            tocHTML += '</ul>';
            
            tocContent.innerHTML = tocHTML;
            
            // Update active state after a short delay to ensure DOM is ready
            setTimeout(() => {{
                updateActiveHeadingOnScroll();
            }}, 100);
        }}
        
        function scrollToHeading(headingId) {{
            const heading = document.getElementById(headingId);
            if (heading) {{
                // Remove previous highlights
                document.querySelectorAll('.heading-highlight').forEach(el => {{
                    el.classList.remove('heading-highlight');
                }});
                
                // Add highlight to current heading
                heading.classList.add('heading-highlight');
                
                // Update TOC active state
                updateTOCActiveState(headingId);
                
                // Get current scroll position and target position
                const currentScrollY = window.scrollY;
                const targetScrollY = heading.offsetTop - 100; // Offset for better visibility
                
                // Add to navigation history for TOC navigation
                addTOCNavigationToHistory(headingId, currentScrollY);
                
                // Smooth scroll animation
                smoothScrollTo(targetScrollY, 800); // 800ms duration
                
                // Remove highlight after animation
                setTimeout(() => {{
                    heading.classList.remove('heading-highlight');
                }}, 2000);
            }} else {{
                console.error('Heading not found with ID:', headingId);
                console.log('Available heading IDs:', Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6')).map(h => h.id));
            }}
        }}
        
        function updateTOCActiveState(activeHeadingId) {{
            // Remove active class from all TOC links
            document.querySelectorAll('.toc-list a').forEach(link => {{
                link.classList.remove('active');
            }});
            
            // Add active class to current heading link
            const activeLink = document.querySelector(`.toc-list a[href="#${{activeHeadingId}}"]`);
            if (activeLink) {{
                activeLink.classList.add('active');
                
                // Auto-scroll TOC panel to keep active item visible
                const tocPanel = document.querySelector('.toc-panel');
                if (tocPanel) {{
                    const linkRect = activeLink.getBoundingClientRect();
                    const panelRect = tocPanel.getBoundingClientRect();
                    
                    // Check if link is outside visible area
                    const isAboveView = linkRect.top < panelRect.top;
                    const isBelowView = linkRect.bottom > panelRect.bottom;
                    
                    if (isAboveView || isBelowView) {{
                        // Scroll the link into view, centered in the TOC panel
                        const linkOffsetInPanel = activeLink.offsetTop;
                        const panelHeight = tocPanel.clientHeight;
                        const linkHeight = activeLink.offsetHeight;
                        
                        // Calculate scroll position to center the link
                        const scrollTo = linkOffsetInPanel - (panelHeight / 2) + (linkHeight / 2);
                        
                        tocPanel.scrollTo({{
                            top: scrollTo,
                            behavior: 'smooth'
                        }});
                    }}
                }}
            }}
        }}
        
        function updateActiveHeadingOnScroll() {{
            const currentSection = document.querySelector('.content-section[style*="block"]');
            if (!currentSection) return;
            
            const headings = currentSection.querySelectorAll('h1, h2, h3, h4, h5, h6');
            if (headings.length === 0) return;
            
            const scrollPosition = window.scrollY + 150; // Offset for better detection
            let activeHeading = null;
            
            // Find the heading that's currently in view
            for (let i = 0; i < headings.length; i++) {{
                const heading = headings[i];
                const headingTop = heading.offsetTop;
                const headingBottom = headingTop + heading.offsetHeight;
                
                if (scrollPosition >= headingTop && scrollPosition < headingBottom) {{
                    activeHeading = heading;
                    break;
                }} else if (scrollPosition >= headingTop) {{
                    // If we're past this heading, it might be the active one
                    activeHeading = heading;
                }}
            }}
            
            // If no heading is in the exact viewport, find the closest one above
            if (!activeHeading) {{
                for (let i = headings.length - 1; i >= 0; i--) {{
                    const heading = headings[i];
                    if (heading.offsetTop <= scrollPosition) {{
                        activeHeading = heading;
                        break;
                    }}
                }}
            }}
            
            // Update TOC active state
            if (activeHeading && activeHeading.id) {{
                updateTOCActiveState(activeHeading.id);
            }}
        }}
        
        function addTOCNavigationToHistory(headingId, fromScrollY) {{
            // Add TOC navigation to history
            const tocNavEntry = {{
                type: 'toc',
                headingId: headingId,
                fromScrollY: fromScrollY,
                sectionIndex: currentSection
            }};
            
            // Add to history if it's different from the last entry
            const lastEntry = navigationHistory[navigationHistory.length - 1];
            if (!lastEntry || lastEntry.type !== 'toc' || lastEntry.headingId !== headingId) {{
                navigationHistory.push(tocNavEntry);
                historyIndex = navigationHistory.length - 1;
                updateNavigationButtons();
            }}
        }}
        
        function smoothScrollTo(targetY, duration) {{
            const startY = window.scrollY;
            const distance = targetY - startY;
            const startTime = performance.now();
            
            function easeInOutCubic(t) {{
                return t < 0.5 ? 4 * t * t * t : (t - 1) * (2 * t - 2) * (2 * t - 2) + 1;
            }}
            
            function animation(currentTime) {{
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);
                const ease = easeInOutCubic(progress);
                
                window.scrollTo(0, startY + distance * ease);
                
                if (progress < 1) {{
                    requestAnimationFrame(animation);
                }}
            }}
            
            requestAnimationFrame(animation);
        }}
        
        function toggleTOC() {{
            const tocPanel = document.getElementById('toc-panel');
            const toggleButton = document.getElementById('toc-toggle');
            
            if (tocPanel.classList.contains('hidden')) {{
                // Show TOC
                tocPanel.classList.remove('hidden');
                toggleButton.innerHTML = '<span class="material-symbols-rounded" data-fallback="✕">close</span>';
            }} else {{
                // Hide TOC
                tocPanel.classList.add('hidden');
                toggleButton.innerHTML = '<span class="material-symbols-rounded" data-fallback="📑">toc</span>';
            }}
        }}
        
        {self.get_chat_js()}
        
        function toggleFolder(folderId) {{
            const folder = document.getElementById(folderId);
            const toggle = document.querySelector(`[onclick="toggleFolder('${{folderId}}')"] .folder-toggle`);
            
            if (folder.style.display === 'none') {{
                folder.style.display = 'block';
                toggle.classList.add('open');
            }} else {{
                folder.style.display = 'none';
                toggle.classList.remove('open');
            }}
        }}
        
        // Sidebar Toggle Functions
        function toggleSidebar() {{
            const sidebar = document.getElementById('sidebar');
            const openButton = document.getElementById('sidebar-open-button');
            const mainContent = document.querySelector('.main-content');
            const isMobile = window.innerWidth <= 768;
            
            if (isMobile) {{
                // Mobile behavior: toggle mobile-open class and body overlay
                sidebar.classList.toggle('mobile-open');
                document.body.classList.toggle('sidebar-mobile-open');
                
                // Don't save state on mobile
                if (sidebar.classList.contains('mobile-open')) {{
                    openButton.style.display = 'none';
                }} else {{
                    openButton.style.display = 'flex';
                }}
            }} else {{
                // Desktop behavior: toggle collapsed state
                sidebar.classList.toggle('collapsed');
                
                if (sidebar.classList.contains('collapsed')) {{
                    openButton.style.display = 'flex';
                    mainContent.classList.add('sidebar-collapsed');
                    // Remove inline margin styles to let CSS class handle it
                    mainContent.style.marginLeft = '';
                    mainContent.style.marginRight = '';
                    localStorage.setItem('sidebarCollapsed', 'true');
                }} else {{
                    openButton.style.display = 'none';
                    mainContent.classList.remove('sidebar-collapsed');
                    const sidebarWidth = localStorage.getItem('sidebarWidth') || '280px';
                    mainContent.style.marginLeft = sidebarWidth;
                    mainContent.style.marginRight = '20px';
                    localStorage.setItem('sidebarCollapsed', 'false');
                }}
            }}
        }}
        
        // Close mobile sidebar when clicking overlay
        document.addEventListener('click', function(e) {{
            if (window.innerWidth <= 768) {{
                const sidebar = document.getElementById('sidebar');
                const openButton = document.getElementById('sidebar-open-button');
                const clickedOverlay = e.target === document.body && document.body.classList.contains('sidebar-mobile-open');
                const clickedOutside = !sidebar.contains(e.target) && !openButton.contains(e.target) && sidebar.classList.contains('mobile-open');
                
                if (clickedOverlay || clickedOutside) {{
                    sidebar.classList.remove('mobile-open');
                    document.body.classList.remove('sidebar-mobile-open');
                    openButton.style.display = 'flex';
                }}
            }}
        }});
        
        // Handle window resize: cleanup mobile classes on desktop
        window.addEventListener('resize', function() {{
            const sidebar = document.getElementById('sidebar');
            const openButton = document.getElementById('sidebar-open-button');
            const mainContent = document.querySelector('.main-content');
            
            if (window.innerWidth > 768) {{
                // Desktop: remove mobile classes
                sidebar.classList.remove('mobile-open');
                document.body.classList.remove('sidebar-mobile-open');
                
                // Restore desktop state from localStorage
                const isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
                if (isCollapsed) {{
                    sidebar.classList.add('collapsed');
                    openButton.style.display = 'flex';
                    mainContent.classList.add('sidebar-collapsed');
                }} else {{
                    sidebar.classList.remove('collapsed');
                    openButton.style.display = 'none';
                    mainContent.classList.remove('sidebar-collapsed');
                    const sidebarWidth = localStorage.getItem('sidebarWidth') || '280px';
                    mainContent.style.marginLeft = sidebarWidth;
                    mainContent.style.marginRight = '20px';
                }}
            }} else {{
                // Mobile: always show open button, remove desktop classes
                openButton.style.display = 'flex';
                mainContent.style.marginLeft = '';
                mainContent.style.marginRight = '';
                mainContent.classList.remove('sidebar-collapsed');
            }}
        }});
        
        // Sidebar Resize Functions
        function initSidebarResize() {{
            const sidebar = document.getElementById('sidebar');
            const resizeHandle = document.getElementById('resize-handle');
            const mainContent = document.querySelector('.main-content');
            let isResizing = false;
            let startX = 0;
            let startWidth = 0;
            
            // Only apply saved state on desktop
            if (window.innerWidth > 768) {{
                // Load saved width
                const savedWidth = localStorage.getItem('sidebarWidth');
                if (savedWidth) {{
                    sidebar.style.width = savedWidth;
                    mainContent.style.marginLeft = savedWidth;
                }}
                
                // Load collapsed state
                const isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
                if (isCollapsed) {{
                    sidebar.classList.add('collapsed');
                    document.getElementById('sidebar-open-button').style.display = 'flex';
                    mainContent.classList.add('sidebar-collapsed');
                    // Clear inline styles to let CSS class handle margins
                    mainContent.style.marginLeft = '';
                    mainContent.style.marginRight = '';
                }}
            }} else {{
                // Mobile: always show open button
                document.getElementById('sidebar-open-button').style.display = 'flex';
            }}
            
            resizeHandle.addEventListener('mousedown', function(e) {{
                // Don't allow resizing on mobile
                if (window.innerWidth <= 768) return;
                
                isResizing = true;
                startX = e.clientX;
                startWidth = sidebar.offsetWidth;
                resizeHandle.classList.add('resizing');
                document.body.style.cursor = 'ew-resize';
                document.body.style.userSelect = 'none';
            }});
            
            document.addEventListener('mousemove', function(e) {{
                if (!isResizing) return;
                
                const width = startWidth + (e.clientX - startX);
                const minWidth = 200;
                const maxWidth = 600;
                
                if (width >= minWidth && width <= maxWidth) {{
                    sidebar.style.width = width + 'px';
                    mainContent.style.marginLeft = width + 'px';
                }}
            }});
            
            document.addEventListener('mouseup', function() {{
                if (isResizing) {{
                    isResizing = false;
                    resizeHandle.classList.remove('resizing');
                    document.body.style.cursor = '';
                    document.body.style.userSelect = '';
                    localStorage.setItem('sidebarWidth', sidebar.style.width);
                }}
            }});
        }}
        
        // Initialize sidebar resize on load
        document.addEventListener('DOMContentLoaded', function() {{
            initSidebarResize();
        }});
        
        // Settings Modal Functions
        function openSettings() {{
            const modal = document.getElementById('settings-modal');
            modal.classList.add('open');
            
            // Update active theme button
            updateThemeButtons();
        }}
        
        function closeSettings() {{
            const modal = document.getElementById('settings-modal');
            modal.classList.remove('open');
        }}
        
        // Close modal when clicking outside
        document.addEventListener('click', function(e) {{
            const modal = document.getElementById('settings-modal');
            if (e.target === modal) {{
                closeSettings();
            }}
        }});
        
        // Theme Functions
        function updateTheme() {{
            const family = document.getElementById('theme-family').value;
            const mode = getCurrentMode();
            
            // Save preferences
            localStorage.setItem('themeFamily', family);
            localStorage.setItem('themeMode', mode);
            
            // Apply theme
            applyTheme(family, mode);
        }}
        
        function setMode(mode) {{
            // Save mode preference
            localStorage.setItem('themeMode', mode);
            
            // Get current family
            const family = document.getElementById('theme-family').value;
            
            // Apply theme
            applyTheme(family, mode);
            
            // Update UI
            updateModeButtons(mode);
        }}
        
        function getCurrentMode() {{
            // Get active mode button
            const activeButton = document.querySelector('.mode-button.active');
            return activeButton ? activeButton.dataset.mode : 'system';
        }}
        
        function applyTheme(family, mode) {{
            const html = document.documentElement;
            const body = document.body;
            
            // Construct theme name
            const themeName = constructThemeName(family, mode);
            
            // Remove all existing theme classes
            const existingClasses = Array.from(html.classList).filter(cls => cls.startsWith('theme-'));
            existingClasses.forEach(cls => {{
                html.classList.remove(cls);
                body.classList.remove(cls);
            }});
            
            // Apply new theme class
            html.classList.add('theme-' + themeName);
            body.classList.add('theme-' + themeName);
            
            console.log(`Applied theme: ${{themeName}} (family: ${{family}}, mode: ${{mode}})`);
        }}
        
        function updateModeButtons(activeMode) {{
            // Remove active class from all mode buttons
            document.querySelectorAll('.mode-button').forEach(btn => {{
                btn.classList.remove('active');
            }});
            
            // Add active class to current mode button
            const activeButton = document.querySelector(`.mode-button[data-mode="${{activeMode}}"]`);
            if (activeButton) {{
                activeButton.classList.add('active');
            }}
        }}
        
        // Initialize theme on page load
        document.addEventListener('DOMContentLoaded', function() {{
            // Restore saved preferences
            const savedFamily = localStorage.getItem('themeFamily') || THEME_CONFIG.defaultFamily;
            const savedMode = localStorage.getItem('themeMode') || THEME_CONFIG.defaultMode;
            
            // Set dropdown value
            const dropdown = document.getElementById('theme-family');
            if (dropdown) {{
                dropdown.value = savedFamily;
            }}
            
            // Update mode buttons
            updateModeButtons(savedMode);
            
            // Apply theme (already applied in head, but ensure consistency)
            applyTheme(savedFamily, savedMode);
            
            // Listen for system theme changes
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {{
                const currentMode = localStorage.getItem('themeMode') || THEME_CONFIG.defaultMode;
                const currentFamily = localStorage.getItem('themeFamily') || THEME_CONFIG.defaultFamily;
                
                // Only re-apply if in system mode
                if (currentMode === 'system') {{
                    applyTheme(currentFamily, 'system');
                }}
            }});
        }});
        
        function navigateToSection(index) {{
            // Add to internal history if it's a new section
            if (index !== currentSection) {{
                // Remove any forward history if we're navigating to a new section
                navigationHistory = navigationHistory.slice(0, historyIndex + 1);
                
                // Add section navigation entry
                const sectionNavEntry = {{
                    type: 'section',
                    sectionIndex: index,
                    scrollY: window.scrollY
                }};
                
                navigationHistory.push(sectionNavEntry);
                historyIndex = navigationHistory.length - 1;
            }}
            
            showSection(index);
        }}
        
        function goBack() {{
            if (historyIndex > 0) {{
                historyIndex--;
                const historyEntry = navigationHistory[historyIndex];
                navigateToHistoryEntry(historyEntry);
            }} else {{
                // Use browser back if no internal history
                history.back();
            }}
        }}
        
        function goForward() {{
            if (historyIndex < navigationHistory.length - 1) {{
                historyIndex++;
                const historyEntry = navigationHistory[historyIndex];
                navigateToHistoryEntry(historyEntry);
            }} else {{
                // Use browser forward if no internal history
                history.forward();
            }}
        }}
        
        function navigateToHistoryEntry(historyEntry) {{
            if (historyEntry.type === 'section') {{
                // Navigate to a different section
                showSection(historyEntry.sectionIndex, false);
                // Restore scroll position if available
                if (historyEntry.scrollY !== undefined) {{
                    setTimeout(() => {{
                        window.scrollTo(0, historyEntry.scrollY);
                    }}, 100);
                }}
            }} else if (historyEntry.type === 'toc') {{
                // Navigate to a heading within the current section
                // First ensure we're in the right section
                if (historyEntry.sectionIndex !== currentSection) {{
                    showSection(historyEntry.sectionIndex, false);
                }}
                
                // Then scroll to the heading
                setTimeout(() => {{
                    const heading = document.getElementById(historyEntry.headingId);
                    if (heading) {{
                        const targetScrollY = heading.offsetTop - 100;
                        smoothScrollTo(targetScrollY, 600);
                        
                        // Add highlight
                        document.querySelectorAll('.heading-highlight').forEach(el => {{
                            el.classList.remove('heading-highlight');
                        }});
                        heading.classList.add('heading-highlight');
                        setTimeout(() => {{
                            heading.classList.remove('heading-highlight');
                        }}, 2000);
                    }}
                }}, 100);
            }}
        }}
        
        function updateNavigationButtons(index) {{
            const backButtons = document.querySelectorAll('.back-button');
            const forwardButtons = document.querySelectorAll('.forward-button');
            
            // Show/hide back button
            backButtons.forEach(btn => {{
                btn.style.display = historyIndex > 0 ? 'block' : 'block'; // Always show, let browser handle
            }});
            
            // Show/hide forward button
            forwardButtons.forEach(btn => {{
                btn.style.display = historyIndex < navigationHistory.length - 1 ? 'block' : 'block'; // Always show, let browser handle
            }});
        }}
        
        // Handle browser back/forward buttons
        window.addEventListener('popstate', function(event) {{
            isBrowserNavigation = true;
            
            if (event.state && event.state.section !== undefined) {{
                // Navigate to the section from browser history
                showSection(event.state.section, false);
            }} else {{
                // Handle hash-based navigation
                const hash = window.location.hash;
                if (hash) {{
                    const sectionMatch = hash.match(/#section-(\\d+)/);
                    if (sectionMatch) {{
                        const sectionIndex = parseInt(sectionMatch[1]);
                        showSection(sectionIndex, false);
                    }}
                }} else {{
                    // Default to first section
                    showSection(0, false);
                }}
            }}
            
            isBrowserNavigation = false;
        }});
        
        // Add smooth scrolling for anchor links
        document.addEventListener('DOMContentLoaded', function() {{
            const links = document.querySelectorAll('a[href^="#"]');
            links.forEach(link => {{
                link.addEventListener('click', function(e) {{
                    e.preventDefault();
                    const targetId = this.getAttribute('href').substring(1);
                    const targetElement = document.getElementById(targetId);
                    if (targetElement) {{
                        targetElement.scrollIntoView({{ behavior: 'smooth' }});
                    }}
                }});
            }});
            
            // Initialize navigation buttons
            updateNavigationButtons(0);
            
            // Initialize TOC for first section
            const firstSection = document.querySelector('.content-section');
            if (firstSection) {{
                updateTOC(firstSection);
            }}
            
            // Add scroll detection for TOC highlighting
            let scrollTimeout;
            window.addEventListener('scroll', function() {{
                clearTimeout(scrollTimeout);
                scrollTimeout = setTimeout(updateActiveHeadingOnScroll, 100);
            }});
            
            
            // Handle initial page load with hash
            const hash = window.location.hash;
            if (hash) {{
                const sectionMatch = hash.match(/#section-(\\d+)/);
                if (sectionMatch) {{
                    const sectionIndex = parseInt(sectionMatch[1]);
                    showSection(sectionIndex, false);
                }}
            }} else {{
                // Set initial browser history state
                history.replaceState({{ section: 0 }}, '', '#section-0');
            }}
        }});
        
        // Keyboard navigation
        document.addEventListener('keydown', function(e) {{
            if (e.altKey) {{
                if (e.key === 'ArrowLeft') {{
                    e.preventDefault();
                    goBack();
                }} else if (e.key === 'ArrowRight') {{
                    e.preventDefault();
                    goForward();
                }}
            }} else if (e.ctrlKey || e.metaKey) {{
                if (e.key === 't' || e.key === 'T') {{
                    e.preventDefault();
                    toggleTOC();
                }}
            }}
        }});
    </script>
    
    <!-- Prism.js for Syntax Highlighting -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-core.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/line-numbers/prism-line-numbers.min.js"></script>
    
    <script>
        // Configure Prism autoloader
        Prism.plugins.autoloader.languages_path = 'https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/';
        
        // Apply Prism highlighting to all code blocks
        document.addEventListener('DOMContentLoaded', function() {{
            // Add line-numbers class to all pre elements
            document.querySelectorAll('pre').forEach(pre => {{
                pre.classList.add('line-numbers');
            }});
            
            // Re-highlight all code blocks
            Prism.highlightAll();
        }});
        
        // Re-highlight when switching sections
        const originalShowSection = showSection;
        showSection = function(index) {{
            originalShowSection(index);
            setTimeout(() => {{
                Prism.highlightAll();
            }}, 50);
        }};
    </script>
    {datatables_js}
    {datatables_init}
    
    <script>
        // Process task lists - convert markdown syntax to styled checkboxes
        function processTaskLists() {{
            document.querySelectorAll('.section-content li').forEach(li => {{
                const text = li.textContent.trim();
                if (text.startsWith('[x] ') || text.startsWith('[X] ')) {{
                    li.classList.add('task-checked');
                    li.innerHTML = li.innerHTML.replace(/^\[x\]\s*/i, '');
                    li.parentElement.classList.add('task-list');
                }} else if (text.startsWith('[ ] ')) {{
                    li.classList.add('task-unchecked');
                    li.innerHTML = li.innerHTML.replace(/^\[\s\]\s*/, '');
                    li.parentElement.classList.add('task-list');
                }}
            }});
        }}
        
        // Process task lists on page load and section change
        document.addEventListener('DOMContentLoaded', processTaskLists);
        
        const originalShowSection2 = showSection;
        showSection = function(index) {{
            originalShowSection2(index);
            setTimeout(processTaskLists, 50);
        }};
        
        // Tag-to-files mapping for popup functionality
        const TAG_FILE_MAP = {json.dumps(tag_file_map)};
        
        // Populate tag counts and setup hover functionality
        document.addEventListener('DOMContentLoaded', function() {{
            // Populate tag counts
            document.querySelectorAll('.tag').forEach(tag => {{
                const tagName = tag.dataset.tag;
                if (tagName && TAG_FILE_MAP[tagName]) {{
                    const count = TAG_FILE_MAP[tagName].length;
                    const countBadge = tag.querySelector('.tag-count');
                    if (countBadge) {{
                        countBadge.textContent = count;
                    }}
                }}
            }});
            
            // Setup tag hover popup
            const tagPopup = document.getElementById('tag-popup');
            let hideTimeout;
            
            document.querySelectorAll('.tag').forEach(tag => {{
                tag.addEventListener('mouseenter', function(e) {{
                    clearTimeout(hideTimeout);
                    const tagName = this.dataset.tag;
                    const files = TAG_FILE_MAP[tagName] || [];
                    
                    if (files.length === 0) return;
                    
                    // Build popup content
                    let popupHTML = `
                        <div class="tag-popup-header">
                            <span class="material-symbols-rounded" data-fallback="🏷️">sell</span>
                            Files with tag "${{tagName}}" (${{files.length}})
                        </div>
                        <div class="tag-popup-list">
                    `;
                    
                    files.forEach(f => {{
                        popupHTML += `
                            <div class="tag-popup-item" onclick="showSection(${{f.index}}); document.getElementById('tag-popup').style.display='none';">
                                <span class="material-symbols-rounded" data-fallback="📄">description</span>
                                ${{f.name}}
                            </div>
                        `;
                    }});
                    
                    popupHTML += '</div>';
                    tagPopup.innerHTML = popupHTML;
                    
                    // Position popup near tag
                    const rect = this.getBoundingClientRect();
                    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
                    const scrollLeft = window.pageXOffset || document.documentElement.scrollLeft;
                    
                    tagPopup.style.left = (rect.left + scrollLeft) + 'px';
                    tagPopup.style.top = (rect.bottom + scrollTop + 5) + 'px';
                    tagPopup.style.display = 'block';
                }});
                
                tag.addEventListener('mouseleave', function() {{
                    hideTimeout = setTimeout(() => {{
                        if (!tagPopup.matches(':hover')) {{
                            tagPopup.style.display = 'none';
                        }}
                    }}, 200);
                }});
            }});
            
            // Keep popup open when hovering over it
            tagPopup.addEventListener('mouseenter', function() {{
                clearTimeout(hideTimeout);
            }});
            
            tagPopup.addEventListener('mouseleave', function() {{
                hideTimeout = setTimeout(() => {{
                    this.style.display = 'none';
                }}, 200);
            }});
        }});
        
        // Material Icons emoji fallback - replace icon text with emoji when font fails to load
        document.addEventListener('DOMContentLoaded', function() {{
            // Check if Material Icons font loaded after a delay
            setTimeout(function() {{
                // Try to detect if Material Icons is loaded by checking a test element
                const testIcon = document.createElement('span');
                testIcon.className = 'material-symbols-rounded';
                testIcon.textContent = 'settings';
                testIcon.style.position = 'absolute';
                testIcon.style.left = '-9999px';
                testIcon.style.fontSize = '24px';
                document.body.appendChild(testIcon);
                
                // If the element width is very small, the font probably didn't load (showing text)
                const width = testIcon.offsetWidth;
                document.body.removeChild(testIcon);
                
                // Material Icons renders as ~24px icon, plain text would be much wider
                if (width > 30) {{
                    // Font didn't load, use emoji fallbacks
                    document.querySelectorAll('.material-symbols-rounded[data-fallback]').forEach(icon => {{
                        const emoji = icon.getAttribute('data-fallback');
                        if (emoji) {{
                            icon.textContent = emoji;
                        }}
                    }});
                }}
            }}, 500); // Wait 500ms for font to load
        }});
    </script>
    
    <div class="wiki-footer">
        <div class="wiki-footer-content">
            <div class="wiki-footer-text">
                Built with <span class="wiki-footer-emoji">❤️</span> & <span class="wiki-footer-emoji">☕</span> using <a href="https://github.com/manasvi-turing/atom-wiki" target="_blank">Atom Wiki</a>
            </div>
        </div>
    </div>
</body>
</html>'''
        
        return html_template
    
    def convert(self):
        """Main conversion method"""
        print(f"Converting markdown files from {self.input_folder} to {self.output_file}")
        
        # Find markdown files
        self.find_markdown_files()
        
        # Generate HTML content
        html_content = self.generate_html_content()
        
        # Create output directory if it doesn't exist
        output_path = Path(self.output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write to output file
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"✅ Successfully created {self.output_file}")
            print(f"📄 Converted {len(self.markdown_files)} markdown files")
        except Exception as e:
            print(f"❌ Error writing to {self.output_file}: {e}")

def main():
    parser = argparse.ArgumentParser(
        description='Convert markdown files to a single HTML webpage',
        epilog='Configuration can be set in config.yaml or overridden with command-line arguments.'
    )
    parser.add_argument('input_folder', help='Path to folder containing markdown files')
    parser.add_argument('-o', '--output', default=None, help='Output HTML file name (default: from config or wiki_output.html)')
    parser.add_argument('--no-chat', action='store_true', help='Disable AI chat feature (overrides config)')
    parser.add_argument('--enable-chat', action='store_true', help='Enable AI chat feature (overrides config)')
    parser.add_argument('-c', '--config', default='config.yaml', help='Path to config file (default: config.yaml)')
    
    args = parser.parse_args()
    
    try:
        # Determine enable_chat: CLI args override config
        enable_chat = None
        if args.no_chat:
            enable_chat = False
        elif args.enable_chat:
            enable_chat = True
        # If neither flag is set, enable_chat stays None and config will be used
        
        # Determine output file
        output_file = args.output if args.output else 'index.html'
        
        converter = MarkdownToHTMLConverter(
            args.input_folder, 
            output_file, 
            enable_chat=enable_chat,
            config_file=args.config
        )
        converter.convert()
        
        # Show chat status
        chat_status = "✅ Enabled" if converter.enable_chat else "❌ Disabled"
        print(f"💬 AI Chat: {chat_status}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
