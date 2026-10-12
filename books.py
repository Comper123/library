"""Каталог книг: локальное хранение в JSON."""
import argparse
import json
from pathlib import Path

MAX_BOOKS = 500


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


def normalize_isbn(value):
    return value.replace("-", "").replace(" ", "").upper()


def add_book(books, title, author, isbn):
    title, author, isbn = title.strip(), author.strip(), isbn.strip()
    if not title or not author or not normalize_isbn(isbn):
        raise ValueError("Название, автор и ISBN не должны быть пустыми")
    if len(books) >= MAX_BOOKS:
        raise ValueError(f"Достигнут лимит: {MAX_BOOKS} книг")
    if any(normalize_isbn(book["isbn"]) == normalize_isbn(isbn) for book in books):
        raise ValueError("Книга с таким ISBN уже существует")
    books.append({"title": title, "author": author, "isbn": isbn})


def search_author(books, query):
    return [book for book in books if query.casefold() in book["author"].casefold()]


def search_isbn(books, query):
    return [book for book in books if normalize_isbn(book["isbn"]) == normalize_isbn(query)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", type=Path, default=Path("books.json"))
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list", help="Показать каталог")
    add = commands.add_parser("add", help="Добавить книгу")
    add.add_argument("--title", required=True)
    add.add_argument("--author", required=True)
    add.add_argument("--isbn", required=True)
    author = commands.add_parser("search-author", help="Поиск по части имени автора")
    author.add_argument("query")
    export = commands.add_parser("export", help="Экспортировать список в JSON")
    export.add_argument("output", type=Path)
    isbn = commands.add_parser("search-isbn", help="Поиск по ISBN")
    isbn.add_argument("query")
    args = parser.parse_args()
    try:
        books = load_books(args.file)
        if args.command == "add":
            add_book(books, args.title, args.author, args.isbn)
            save_books(args.file, books)
        result = search_author(books, args.query) if args.command == "search-author" else books
        if args.command == "search-isbn":
            result = search_isbn(books, args.query)
        if args.command == "export":
            if args.output.resolve() == args.file.resolve():
                raise ValueError("Выберите отдельный файл для экспорта")
            save_books(args.output, books)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (OSError, ValueError) as error:
        parser.exit(1, f"Ошибка: {error}\n")


if __name__ == "__main__":
    main()
