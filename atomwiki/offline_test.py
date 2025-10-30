#!/usr/bin/env python3
"""
Create offline test version of wiki HTML file.
Breaks all CDN links to simulate complete offline mode.
"""

import sys
import re
import argparse
from pathlib import Path


def create_offline_version(input_file, output_file=None):
    """Create an offline test version by breaking CDN links."""
    
    input_path = Path(input_file)
    
    if not input_path.exists():
        print(f"❌ Error: File '{input_file}' not found")
        sys.exit(1)
    
    # Default output filename
    if output_file is None:
        output_file = input_path.stem + "_offline.html"
    
    output_path = Path(output_file)
    
    print(f"📖 Reading: {input_path}")
    
    # Read the HTML file
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Break all CDN links
    replacements = [
        # Google Fonts
        (r'https://fonts\.googleapis\.com', 'https://fonts.googleapis.com/BROKEN'),
        (r'https://fonts\.gstatic\.com', 'https://fonts.gstatic.com/BROKEN'),
        # Prism.js
        (r'https://cdnjs\.cloudflare\.com/ajax/libs/prism', 'https://cdnjs.cloudflare.com/BROKEN/prism'),
        # jQuery
        (r'https://code\.jquery\.com/jquery-[0-9.]+\.min\.js', 'https://code.jquery.com/BROKEN_jquery.js'),
        # DataTables
        (r'https://cdn\.datatables\.net/[0-9.]+/js/jquery\.dataTables\.min\.js', 'https://cdn.datatables.net/BROKEN_datatables.js'),
    ]
    
    broken_count = 0
    for pattern, replacement in replacements:
        matches = len(re.findall(pattern, content))
        if matches > 0:
            content = re.sub(pattern, replacement, content)
            broken_count += matches
    
    # Write the offline version
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Created: {output_path}")
    print(f"🔗 Broke {broken_count} CDN links")
    print()
    print("🧪 Test it:")
    print(f"   open {output_path}")
    print()
    print("📋 Compare:")
    print(f"   open {input_path} {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Create offline test version by breaking all CDN links',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  aw-offline test.html
  aw-offline wiki.html -o wiki_offline.html
  aw-offline output.html --output test_offline.html

This creates a test version with all CDN links broken to simulate
complete offline mode (no internet access).
        '''
    )
    
    parser.add_argument('input', help='Input HTML file')
    parser.add_argument('-o', '--output', help='Output HTML file (default: input_offline.html)')
    
    args = parser.parse_args()
    
    create_offline_version(args.input, args.output)


if __name__ == "__main__":
    main()

