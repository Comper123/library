"""Каталог книг: локальное хранение в JSON."""
import argparse
import json
from pathlib import Path

MAX_BOOKS = 50


def load_books(path):
    if not path.exists():
        return []
    books = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(books, list) or any(
        not isinstance(book, dict) or
        any(not isinstance(book.get(key), str) for key in ("title", "author", "isbn"))
        for book in books
    ):
        raise ValueError("Некорректный формат каталога")
    return books


def save_books(path, books):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(books, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", type=Path, default=Path("books.json"))
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list", help="Показать каталог")
    args = parser.parse_args()
    try:
        books = load_books(args.file)
        result = books
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (OSError, ValueError) as error:
        parser.exit(1, f"Ошибка: {error}\n")


if __name__ == "__main__":
    main()
