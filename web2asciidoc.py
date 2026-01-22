"""
web2asciidoc.py v0.1.3
Description: A utility to download web content and convert it to AsciiDoc format,
with specialized support for MathML and LaTeX formulas.
© Copyright 2026 DigitalCoreNZ. All rights reserved.
"""

import os
import sys
import re
import requests
from bs4 import BeautifulSoup
import html2text # type: ignore

class Web2AsciiDoc:
    """
    A utility to download web content and convert it to AsciiDoc format,
    with specialized support for MathML and LaTeX formulas.
    """
    
    def __init__(self):
        self.url_list = []
        # Greek letters, mathematical symbols, and other symbols for MathML/LaTeX
        self.greek_list = [
            # Lowercase Greek
            'α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'σ', 'τ', 'υ', 'φ', 'χ', 'ψ', 'ω',
            # Uppercase Greek
            'Α', 'Β', 'Γ', 'Δ', 'Ε', 'Ζ', 'Η', 'Θ', 'Ι', 'Κ', 'Λ', 'Μ', 'Ν', 'Ξ', 'Ο', 'Π', 'Ρ', 'Σ', 'Τ', 'Υ', 'Φ', 'Χ', 'Ψ', 'Ω',
            # Mathematical Symbols
            '∑', '∏', '∫', '∂', '∇', '∆', '∞', '≈', '≠', '≡', '≤', '≥', '±', '×', '÷', '√', '∝', '∠', '∧', '∨', '∩', '∪', '⊂', '⊃', '⊆', '⊇', '∈', '∉', '∀', '∃', '¬', '⊕', '⊗', '⊥', '⋅', '∗', '∘', '∼'
        ]
        
        # Markers for protecting content during conversion (from math4asciidoc.py)
        self.backslash_marker = "UNIQUE_BACKSLASH_MARKER"
        self.block_start_marker = "BLOCK_MATH_START"
        self.block_end_marker = "BLOCK_MATH_END"
        self.inline_start_marker = "STEM_INLINE_START"
        self.inline_end_marker = "STEM_INLINE_END"
        
        self.artifact_patterns = [
            r'\bBigl\b', r'\bBigr\b', r'\bigl\b', r'\bigr\b',
            r'\bleft\b', r'\bright\b',
            r'(?<![a-zA-Z])igl(?![a-zA-Z])',
            r'(?<![a-zA-Z])igr(?![a-zA-Z])',
            r'(?<!r)ight\b',
            r'\\?ight', r'\\?left', r'\\?igl', r'\\?igr',
            r'\\?Bigl', r'\\?Bigr'
        ]

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_splash(self):
        self.clear_screen()
        splash = """
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃       The Web to AsciiDoc Download Utility (web2asciidoc.py) v0.1.3      ┃
┠──────────────────────────────────────────────────────────────────────────┨
┃                                MIT License                               ┃
┃──────────────────────────────────────────────────────────────────────────┨
┃           © Copyright 2026 DigitalCoreNZ. All rights reserved.           ┃
┃                                                                          ┃
┃        Permission is hereby granted, free of charge, to any person       ┃
┃      obtaining a copy of this software, and associated documentation     ┃
┃    files (the "Software"), to deal in the Software without restriction,  ┃
┃   including without limitation, the rights to use, copy, modify, merge,  ┃
┃    publish, distribute, sublicense, and/or sell copies of the Software,  ┃
┃      and to permit persons to whom the Software is furnished to do so,   ┃
┃                   subject to the following conditions:                   ┃
┃                                                                          ┃
┃          THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF           ┃
┃       ANY KIND, EXPRESS OR IMPLIED, INCLUDING, BUT NOT LIMITED TO,       ┃
┃       THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR        ┃
┃      PURPOSE, AND NONINFRINGEMENT. IN NO EVENT SHALL THE DEVELOPERS,     ┃
┃        OR COPYRIGHT HOLDERS, BE LIABLE FOR ANY CLAIM, DAMAGES OR         ┃
┃        OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR        ┃
┃        OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION WITH, THE       ┃
┃          SOFTWARE, OR THE USE, OR OTHER DEALINGS IN THE SOFTWARE.        ┃
┃                                                                          ┃
┃              The above notice shall be included in all copies,           ┃
┃                  or substantial portions, of the Software.               ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"""
        print(splash)

    def get_next_filename(self):
        """Determines the next sequential filename for output (doc_XXX.ad)."""
        pattern = re.compile(r'doc_(\d{3})\.ad')
        max_num = 0
        for f in os.listdir('.'):
            match = pattern.match(f)
            if match:
                num = int(match.group(1))
                if num > max_num:
                    max_num = num
        return f"doc_{max_num + 1:03d}.ad"

    def protect_math(self, soup):
        """Identifies math tags and replaces them with protected markers."""
        for i, math_tag in enumerate(soup.find_all('math')):
            annotation = math_tag.find('annotation', encoding='application/x-tex')
            math_content = annotation.get_text().strip() if annotation else str(math_tag).strip()
            math_content = math_content.replace('\\sim', '~')
            protected_content = math_content.replace('\\', self.backslash_marker)
            
            is_block = 'display="block"' in str(math_tag)
            if is_block:
                markup = f"{self.block_start_marker}{protected_content}{self.block_end_marker}"
            else:
                markup = f"{self.inline_start_marker}{protected_content}{self.inline_end_marker}"
                
            target = math_tag
            if target.parent and target.parent.name == 'span' and 'katex' in str(target.parent.get('class', [])):
                target = target.parent
            target.replace_with(markup)

    def clean_html(self, soup):
        """Removes non-content elements."""
        for container in soup.find_all(['span', 'div'], class_=lambda x: x and any(k in x for k in ['katex-html', 'MathJax_Display', 'MathJax_Preview'])):
            container.decompose()
        for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
            tag.decompose()

    def convert_to_text(self, soup):
        """Converts cleaned HTML to structured text using html2text."""
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.body_width = 0
        h.protect_links = True
        h.unicode_snob = True
        h.escape_snob = False 
        return h.handle(str(soup))

    def restore_and_format_math(self, content):
        """Restores protected math and applies final formatting."""
        content = re.sub(f'{self.block_start_marker}(.*?){self.block_end_marker}', 
                         r'\n\n[stem]\n++++\n\1\n++++\n\n', content, flags=re.DOTALL)
        content = content.replace(self.inline_start_marker, ' stem:[')
        content = content.replace(self.inline_end_marker, '] ')
        content = content.replace(self.backslash_marker, '\\')
        content = content.replace(r'\-', '-').replace(r'\_', '_').replace(r'\*', '*')
        
        for _ in range(10):
            content = re.sub(r'(stem:\[.*?\])\s*([pθqxALISCLIPPPOCISPODRO0-9\u0370-\u03FF\u2100-\u214F\u2200-\u22FF\u2A00-\u2AFF]{1,10})(?=\s|$|\.|\,)', r'\1', content)

        for pattern in self.artifact_patterns:
            content = re.sub(pattern, '', content)
        
        content = content.replace('xsimpθ', 'x ~ p_\\theta').replace('xsimq', 'x ~ q')
        content = re.sub(r'(?<![a-zA-Z])\\b(?![a-zA-Z])', '[', content)
        content = re.sub(r'(?<![a-zA-Z])\\B(?![a-zA-Z])', ']', content)
        content = content.replace(r'\[', '[').replace(r'\]', ']').replace(r'\(', '(').replace(r'\)', ')')
        content = content.replace('[[A(x)[]', '[A(x)]').replace('\\B]', ']')
        content = re.sub(r'\bight\b', '', content)
        content = re.sub(r'\bleft\b', '', content)
        
        return content

    def adjust_levels(self, content):
        """Adjusts section levels: Level 0 (=) becomes Level 1 (==), etc.
        Also converts Markdown-style hashes (#) to AsciiDoc equals (=).
        Ensures heading consistency (no jumps like Level 1 to Level 3)."""
        lines = content.split('\n')
        processed_lines = []
        
        # First pass: Convert hashes to equals
        for line in lines:
            if line.startswith('#'):
                match = re.match(r'^(#+)\s', line)
                if match:
                    hashes = match.group(1)
                    line = '=' * len(hashes) + line[len(hashes):]
            processed_lines.append(line)
            
        # Second pass: Ensure consistency and increment levels
        final_lines = []
        current_max_level = 0 # Level 0 is the document title
        
        for line in processed_lines:
            if line.startswith('='):
                match = re.match(r'^(=+)\s', line)
                if match:
                    level = len(match.group(1))
                    # Adjust level if it jumps too far
                    if level > current_max_level + 1:
                        level = current_max_level + 1
                    
                    current_max_level = level
                    # Increment level by 1 for the final document
                    final_lines.append('=' * (level + 1) + line[len(match.group(1)):])
                else:
                    final_lines.append(line)
            else:
                final_lines.append(line)
                
        return '\n'.join(final_lines)

    def run(self):
        try:
            self.clear_screen()
            prompt = "This is the Web2AsciiDoc Downloader. Provide a URL, or type 'X' to exit this utility: "
            
            while True:
                user_input = input(prompt).strip()
                
                if user_input.upper() == 'X':
                    self.display_splash()
                    sys.exit(0)
                elif user_input.upper() == 'P':
                    if not self.url_list:
                        print("No URLs to process.")
                        prompt = "Provide a URL, or type 'X' to exit this utility: "
                        continue
                    break
                elif user_input.startswith('http'):
                    self.url_list.append(user_input)
                    prompt = "Provide another URL, type 'P' to process the results, or type 'X' to exit this utility: "
                else:
                    self.clear_screen()
                    prompt = "INVALID INPUT!! Provide a URL, or type 'X' to exit this utility: "

            # Process URLs
            self.clear_screen()
            output_filename = self.get_next_filename()
            doc_title = os.path.splitext(output_filename)[0]
            
            # Deduplicate URLs
            unique_urls = []
            for url in self.url_list:
                if url not in unique_urls:
                    unique_urls.append(url)
            
            final_content = f"= {doc_title}\n:stem:\n\n"
            
            for url in unique_urls:
                try:
                    print(f"Downloading and converting: {url}")
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.text, 'html.parser')
                    self.clean_html(soup)
                    self.protect_math(soup)
                    
                    content = self.convert_to_text(soup)
                    content = self.restore_and_format_math(content)
                    
                    # Delete the last line (navigation links/artifacts)
                    lines = content.strip().split('\n')
                    if lines:
                        lines = lines[:-1]
                    content = '\n'.join(lines)
                    
                    # Adjust levels, convert # to =, and ensure consistency
                    content = self.adjust_levels(content)
                    
                    final_content += content + "\n\n"
                except Exception as e:
                    print(f"Error processing {url}: {e}")

            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(final_content)
            
            print(f"\nSuccessfully created {output_filename}")
            self.display_splash()
            sys.exit(0)

        except KeyboardInterrupt:
            self.display_splash()
            sys.exit(0)

if __name__ == "__main__":
    downloader = Web2AsciiDoc()
    downloader.run()
