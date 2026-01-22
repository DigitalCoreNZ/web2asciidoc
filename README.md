# Web2AsciiDoc Downloader

v0.1.3
© Copyright 2026 DigitalCoreNZ. All rights reserved.

## Introduction

Web2AsciiDoc is an MIT-licensed, specialized Python utility designed to bridge the gap between web content and technical documentation. It allows users to download content from multiple URLs and convert them into a single, well-structured AsciiDoc (`.ad`) file. A key feature of this utility is its robust handling of mathematical formulas (MathML and LaTeX), ensuring that complex technical content is preserved with high fidelity during the conversion process.

## Who Benefits?

- **Technical Writers**: Easily pull research or existing web documentation into an AsciiDoc workflow.
- **Researchers & Academics**: Capture web-based papers and articles containing complex mathematics for offline study or inclusion in larger documents.
- **Developers**: Convert web-based API documentation or tutorials into a format suitable for static site generators like Antora or Asciidoctor.
- **Students**: Compile web resources into a single, searchable, and editable document for study notes.

## How to Download

1. **Prerequisites**: Ensure you have Python 3.x installed on your system.
2. **Clone/Download**:

   - Clone this repository using Git:

     ```bash
     git clone https://github.com/DigitalCoreNZ/web2asciidoc.git
     ```


   - Or download the source code as a ZIP file and extract it to your desired location.
3. **Install Dependencies**: Navigate to the project directory and install the required Python libraries:

   ```bash
   pip install beautifulsoup4 html2text requests
   ```

## How to Use

1. **Launch the Utility**: Open your terminal and run the script:

   ```bash
   python3 web2asciidoc.py
   ```

2. **Provide URLs**:

   - When prompted, paste a URL and press Enter.
   - You can provide multiple URLs, one after another.

3. **Process Results**:

   - Once you have entered all the URLs you want to convert, type `P` (case-insensitive) and press Enter.

4. **Exit**:

   - To exit at any time, type `X` (case-insensitive) or use `CTRL + C`.

5. **Output**:

   - The utility will create a file named `doc_XXX.ad` (where XXX is a sequential number) in the same directory.

## Use Cases

- **Consolidating Documentation**: Pulling multiple related blog posts or documentation pages into a single technical manual.

- **Mathematical Archiving**: Saving web pages with heavy MathML/LaTeX content into a format that remains readable and editable.

- **Content Migration**: Moving content from a CMS or web platform into a version-controlled documentation system using AsciiDoc.

- **Offline Reading**: Creating a single document from various web sources for reading on devices that support text or AsciiDoc formats.

## Full Description

Web2AsciiDoc Downloader (v0.1.3) is a command-line tool built on a refactored foundation of `math4asciidoc.py`. It features an interactive loop for URL collection and a sophisticated processing pipeline:

- **Mathematical Fidelity**: Uses a protection/restoration system for MathML and LaTeX, ensuring symbols and formulas are correctly formatted in the final AsciiDoc output.

- **Structural Integrity**: 
  - Automatically converts Markdown-style hashes (`#`) to AsciiDoc equal signs (`=`).
  - Enforces heading consistency by preventing level jumps (e.g., ensuring a Level 1 heading is followed by a Level 2, not a Level 4).
  - Adjusts all section levels to fit under a single Level 0 document title.

- **Clean Output**: 
  - Removes non-content elements like scripts, styles, and navigation menus.
  - Automatically deletes trailing navigation links or artifacts from each converted page.
- **User-Friendly Interface**: Provides clear prompts, input validation, and a professional splash screen upon exit.

- **Sequential Management**: Automatically detects existing documents to ensure new files are named sequentially (e.g., `doc_001.ad`, `doc_002.ad`).
