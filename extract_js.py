#!/usr/bin/env python3
import argparse
import os
import re
import sys

# Pattern to match <script>…</script>, non-greedy, across newlines, case-insensitive
SCRIPT_RE = re.compile(r'<script\b[^>]*>(.*?)</script>', re.S | re.I)

def extract_with_regex(html):
    """Return concatenated contents of all <script> tags in the given HTML."""
    return "\n".join(match.group(1) for match in SCRIPT_RE.finditer(html))

def extract_scripts_from_dir(input_dir, output_dir):
    """Extract JS from each HTML file in input_dir into .js files under output_dir."""
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if not filename.lower().endswith('.html'):
            continue

        in_path  = os.path.join(input_dir, filename)
        out_name = os.path.splitext(filename)[0] + '.js'
        out_path = os.path.join(output_dir, out_name)

        # Read the HTML file, ignoring undecodable bytes
        with open(in_path, 'r', encoding='utf-8', errors='ignore') as f:
            html_content = f.read()

        # Extract and write the JS
        js_code = extract_with_regex(html_content)
        if js_code.strip():
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(js_code)
            print(f"Extracted JS from {filename} -- > {out_name}")
        else:
            print(f"No <script> tags found in {filename}")

def main():
    parser = argparse.ArgumentParser(
        description="Extract JS snippets from all .html files in a directory"
    )
    parser.add_argument(
        "--input_dir", required=True,
        help="Directory containing input HTML files"
    )
    parser.add_argument(
        "--output_dir", required=True,
        help="Directory where extracted JS files will be written"
    )
    args = parser.parse_args()

    extract_scripts_from_dir(args.input_dir, args.output_dir)

if __name__ == "__main__":
    main()
