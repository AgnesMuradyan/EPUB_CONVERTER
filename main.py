from pathlib import Path
import argparse

from pdf_to_epub.converter import pdf_to_epub
from html_to_epub.converter import html_to_epub


def main():
    parser = argparse.ArgumentParser(description="Convert PDF or HTML to EPUB")
    parser.add_argument("input_file", type=str)
    parser.add_argument("-o", "--output", type=str)
    parser.add_argument("-t", "--title", type=str)
    parser.add_argument("-a", "--author", type=str)
    parser.add_argument(
        "-l",
        "--lang",
        type=str,
        default="en",
        help="EPUB language code, e.g. 'en', 'hy', 'hy-AM'",
    )

    args = parser.parse_args()
    path = Path(args.input_file)

    if not path.exists():
        raise SystemExit(f"File not found: {path}")

    if path.suffix.lower() == ".pdf":
        result = pdf_to_epub(
            pdf_path=str(path),
            output_path=args.output,
            title=args.title,
            author=args.author,
            language=args.lang,
        )

    elif path.suffix.lower() in (".html", ".htm"):
        result = html_to_epub(
            html_path=str(path),
            output_path=args.output,
            title=args.title,
            author=args.author,
            language=args.lang,
        )

    else:
        raise SystemExit("Supported formats: PDF, HTML")

    print("EPUB created:", result)


if __name__ == "__main__":
    main()
