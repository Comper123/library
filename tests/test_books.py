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
