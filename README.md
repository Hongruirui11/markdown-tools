# Markdown Tools

A Streamlit-based tool for converting Markdown files to Word documents.

## Features

- Convert Markdown to DOCX with proper heading styles mapping
- Web interface powered by Streamlit
- Support for custom Word templates

## Usage

### Web Interface (Streamlit)

```bash
streamlit run app.py
```

Then open http://localhost:8501 in your browser.

### Command Line

```bash
python scripts/markdown_converter.py input.md docx [output.docx]
```

## Heading Style Mapping

The converter maps Markdown headings to Word styles as follows:
- h1 → "Heading 1"
- h2 → "Heading 2"
- h3 → "Heading 3"
- h4 → "Heading 4"
- h5 → "Heading 5"
- h6 → "Heading 6"

## Dependencies

- streamlit
- python-docx
- markdown
- beautifulsoup4
- lxml

## Installation

```bash
pip install -r requirements.txt
```
