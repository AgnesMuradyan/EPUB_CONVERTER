from pathlib import Path
from typing import List, Optional

from pypdf import PdfReader
from ebooklib import epub
from bs4 import BeautifulSoup


def normalize_multiline_text(text: str) -> str:
    """Join non-heading lines separated by newlines into continuous text."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    normalized = []

    for line in lines:
        if line.isupper() or line.endswith(":"):
            normalized.append("\n" + line + "\n")
        else:
            if normalized and not normalized[-1].endswith("\n"):
                normalized[-1] += " " + line
            else:
                normalized.append(line)

    return "\n".join(l.strip() for l in normalized if l.strip())


def extract_text_from_pdf(pdf_path: Path) -> List[str]:
    """Extract and normalize per-page text."""
    reader = PdfReader(str(pdf_path))
    pages = []

    for page in reader.pages:
        raw = page.extract_text() or ""
        cleaned = normalize_multiline_text(raw)
        pages.append(cleaned)

    return pages


def build_html(title: str, text: str) -> str:
    """Create valid XHTML 1.1 content for Kindle."""

    soup = BeautifulSoup("", "lxml")

    html = soup.new_tag("html", xmlns="http://www.w3.org/1999/xhtml")

    head = soup.new_tag("head")
    meta = soup.new_tag("meta", charset="utf-8")
    head.append(meta)
    title_tag = soup.new_tag("title")
    title_tag.string = title
    head.append(title_tag)

    body = soup.new_tag("body")

    h1 = soup.new_tag("h1")
    h1.string = title
    body.append(h1)

    for block in text.split("\n"):
        block = block.strip()
        if not block:
            continue
        p = soup.new_tag("p")
        p.string = block.replace("\n", " ")
        body.append(p)

    html.append(head)
    html.append(body)
    soup.append(html)

    return str(soup)



def pdf_to_epub(
    pdf_path: str,
    output_path: Optional[str] = None,
    title: Optional[str] = None,
    author: Optional[str] = None,
    language: str = "en",
) -> str:

    pdf = Path(pdf_path)
    if not pdf.exists():
        raise FileNotFoundError(pdf)

    if output_path is None:
        out = pdf.with_suffix(".epub")
    else:
        out = Path(output_path)

    book_title = title or pdf.stem

    pages = extract_text_from_pdf(pdf)

    book = epub.EpubBook()
    book.set_identifier(pdf.stem)
    book.set_title(book_title)
    book.set_language(language)

    if author:
        book.add_author(author)

    chapters = []

    for i, text in enumerate(pages, start=1):
        chapter_title = f"{book_title} – Page {i}"
        html = build_html(chapter_title, text)

        chap = epub.EpubHtml(
            title=chapter_title,
            file_name=f"chap_{i}.xhtml",
            lang="en"
        )
        chap.content = html

        book.add_item(chap)
        chapters.append(chap)

    book.toc = tuple(chapters)
    book.spine = ["nav"] + chapters

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    epub.write_epub(str(out), book)
    return str(out)
