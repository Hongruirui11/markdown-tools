---
name: markdown-processing
description: Edits and converts Markdown files. Use when the user needs to edit Markdown headings, manage numbering, or convert Markdown to HTML/DOCX/txt formats.
---

# Markdown Processing

## Quick Start

### Markdown Editing
```bash
# Upgrade headings by one level
uv run python scripts/markdown_editor.py document.md upgrade

# Convert to DOCX format
uv run python scripts/markdown_converter.py document.md docx
```

## Core Capabilities

### Markdown Editing (markdown_editor.py)
- **Heading Operations**: Upgrade/downgrade heading levels while preserving content structure
- **Numbering Management**: Add structured numbering (Chinese bidding, technical, academic styles) or remove existing numbering
- **Formatting Preservation**: Maintain consistent formatting during all edits

### Format Conversion (markdown_converter.py)
- **DOCX**: Create Word documents with preserved formatting and styling
- **HTML**: Convert to HTML with embedded CSS styling options
- **Plain Text**: Extract clean text content without Markdown formatting
- **Planned**: PDF conversion support

## Script Usage

### markdown_editor.py

**Required Dependencies:**
```bash
# No additional dependencies required - uses only standard library
```

**Actions:**
- `upgrade` - Increase heading levels by one (h2 → h1, h3 → h2, etc.)
- `downgrade` - Decrease heading levels by one (h1 → h2, h2 → h3, etc.)
- `remove_numbers` - Remove all numbering prefixes from headings
- `add_numbers` - Add structured numbering to headings (requires --style)

**Options:**
- `-o, --output` - Specify output file path (default: overwrite input file)
- `--style` - Numbering style for `add_numbers` action (chinese_bidding, technical, academic)

**Examples:**
```bash
# Add Chinese bidding document style numbering
uv run python scripts/markdown_editor.py document.md add_numbers --style chinese_bidding -o numbered_document.md

# Remove all numbering from headings
uv run python scripts/markdown_editor.py document.md remove_numbers

# Downgrade headings and save to new file
uv run python scripts/markdown_editor.py document.md downgrade -o downgraded.md
```

### markdown_converter.py

**Required Dependencies:**
```bash
pip install python-docx markdown beautifulsoup4
```

**Supported Formats:**
- `docx` - Microsoft Word document format
- `html` - Hypertext Markup Language with styling
- `txt` - Plain text format

**Options:**
- `-o, --output` - Specify output file path (default: input filename with new extension)

**Examples:**
```bash
# Convert Markdown to DOCX (output: document.docx)
uv run python scripts/markdown_converter.py document.md docx

# Convert to HTML with custom output filename
uv run python scripts/markdown_converter.py document.md html -o output.html

# Convert to plain text
uv run python scripts/markdown_converter.py document.md txt
```

## Resources

- **scripts/**: Core Python scripts for Markdown operations
- **references/**: Markdown syntax documentation and best practices
- **assets/**: Templates and styling resources for conversion

---

For detailed API reference and advanced usage examples, see the documentation in the `references/` directory.