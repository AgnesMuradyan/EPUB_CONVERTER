from pathlib import Path
from typing import Optional

from ebooklib import epub
from bs4 import BeautifulSoup


def normalize_html(html: str, title: str) -> str:
    """Make HTML Kindle-compatible XHTML."""

    soup = BeautifulSoup(html, "lxml")

    new = BeautifulSoup("", "lxml")
    html_tag = new.new_tag("html", xmlns="http://www.w3.org/1999/xhtml")
    head = new.new_tag("head")
    meta = new.new_tag("meta", charset="utf-8")
    head.append(meta)
    title_tag = new.new_tag("title")
    title_tag.string = title
    head.append(title_tag)

    body = new.new_tag("body")

    h1 = new.new_tag("h1")
    h1.string = title
    body.append(h1)

    for el in soup.body or soup.contents:
        body.append(el)

    html_tag.append(head)
    html_tag.append(body)
    new.append(html_tag)
    return str(new)


def html_to_epub(
    html_path: str,
    output_path: Optional[str] = None,
    title: Optional[str] = None,
    author: Optional[str] = None,
    language: str = "en",
) -> str:

    html_file = Path(html_path)
    if not html_file.exists():
        raise FileNotFoundError(html_file)

    if output_path is None:
        out = html_file.with_suffix(".epub")
    else:
        out = Path(output_path)

    book_title = title or html_file.stem

    raw = html_file.read_text(encoding="utf-8", errors="ignore")
    cleaned_html = normalize_html(raw, title=book_title)

    book = epub.EpubBook()
    book.set_identifier(html_file.stem)
    book.set_title(book_title)
    book.set_language(language)

    if author:
        book.add_author(author)

    chapter = epub.EpubHtml(
        title=book_title,
        file_name="chapter.xhtml",
        lang="en",
    )
    chapter.content = cleaned_html

    book.add_item(chapter)
    book.toc = (chapter,)
    book.spine = ["nav", chapter]

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    epub.write_epub(str(out), book)
    return str(out)
