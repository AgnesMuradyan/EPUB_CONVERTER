# PDF and HTML to EPUB Converter
This project provides a command-line tool for converting PDF and HTML documents into EPUB format. It includes separate internal converters for PDF and HTML input, unified through a single entry point (main.py). The generated EPUB files follow EPUB 3.3 requirements and support custom metadata such as title, author, and language.

## Installation
This project uses uv for environment and dependency management.

### Install uv on macOS
brew install uv

Or using pipx:
pipx install uv

### Install all project dependencies
Run the following command in the project root (where pyproject.toml exists):
uv sync

This installs all required packages:
- pypdf
- ebooklib
- beautifulsoup4
- lxml

## Usage
Use uv run to execute everything inside the uv-managed environment.

### Convert a PDF
uv run main.py input.pdf

Convert a PDF with a custom output file:
uv run main.py input.pdf -o output.epub

Convert a PDF with metadata:
uv run main.py input.pdf -t "Title" -a "Author" -l hy

### Convert an HTML file
uv run main.py input.html

Convert HTML with metadata:
uv run main.py input.html -t "Title" -l en

## Command-Line Arguments
-o, --output    Output EPUB file path  
-t, --title     EPUB title  
-a, --author    EPUB author  
-l, --lang      EPUB language code (examples: en, hy, hy-AM)

## EPUB Validation (optional)
Download EPUBCheck from https://github.com/w3c/epubcheck  
Unzip it, then navigate into the folder (example: epubcheck-5.3.0):
cd epubcheck-5.3.0

Validate the EPUB file:
java -jar epubcheck.jar ../path/to/file.epub
