import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
import books


class CatalogTests(unittest.TestCase):
    def test_add(self):
        catalog = []
        books.add_book(catalog, "Title", "Author", "978-5-17-090630-7")
        self.assertEqual(catalog[0]["title"], "Title")
        with self.assertRaises(ValueError):
            books.add_book(catalog, "Other", "Other", "9785170906307")
        with self.assertRaises(ValueError):
            books.add_book([], " ", "Author", "123")

    def test_limit(self):
        catalog = [{"title": "A", "author": "B", "isbn": str(i)}
                   for i in range(books.MAX_BOOKS)]
        with self.assertRaises(ValueError):
            books.add_book(catalog, "T", "A", "unique")
        catalog.pop()
        books.add_book(catalog, "T", "A", "unique")
        self.assertEqual(len(catalog), books.MAX_BOOKS)

    def test_author_search(self):
        catalog = [{"title": "T", "author": "Михаил Булгаков", "isbn": "1"}]
        self.assertEqual(books.search_author(catalog, "БУЛГАКОВ"), catalog)
        self.assertEqual(books.search_author(catalog, "Пушкин"), [])

    def test_export_cli(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "books.json"
            target = Path(directory) / "export.json"
            catalog = [{"title": "Книга", "author": "Автор", "isbn": "1"}]
            books.save_books(source, catalog)
            result = subprocess.run([sys.executable, "books.py", "--file", str(source),
                                     "export", str(target)], capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(books.load_books(target), catalog)
