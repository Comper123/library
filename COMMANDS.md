# Журнал выполнения варианта 2

Первоначальные коммиты: .gitignore, books.py, README.md + books.json.example.

```text
$ python -m unittest discover -s tests -v
test_add (test_books.CatalogTests.test_add) ... ok
test_author_search (test_books.CatalogTests.test_author_search) ... ERROR
test_limit (test_books.CatalogTests.test_limit) ... ok

======================================================================
ERROR: test_author_search (test_books.CatalogTests.test_author_search)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\Admin\Desktop\Учеба\4 курс\ВиПКС\2\library\tests\test_books.py", line 31, in test_author_search
    self.assertEqual(books.search_author(catalog, "БУЛГАКОВ"), catalog)
                     ^^^^^^^^^^^^^^^^^^^
AttributeError: module 'books' has no attribute 'search_author'

----------------------------------------------------------------------
Ran 3 tests in 0.074s

FAILED (errors=1)

$ python -m unittest discover -s tests -v
test_add (test_books.CatalogTests.test_add) ... ok
test_author_search (test_books.CatalogTests.test_author_search) ... ok
test_limit (test_books.CatalogTests.test_limit) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.001s

OK

$ git diff
diff --git a/books.py b/books.py
index 2730d6f..0b4c50d 100644
--- a/books.py
+++ b/books.py
@@ -40,6 +40,10 @@ def add_book(books, title, author, isbn):
     books.append({"title": title, "author": author, "isbn": isbn})
 
 
+def search_author(books, query):
+    return [book for book in books if query.casefold() in book["author"].casefold()]
+
+
 def main():
     parser = argparse.ArgumentParser(description=__doc__)
     parser.add_argument("--file", type=Path, default=Path("books.json"))
@@ -49,13 +53,15 @@ def main():
     add.add_argument("--title", required=True)
     add.add_argument("--author", required=True)
     add.add_argument("--isbn", required=True)
+    author = commands.add_parser("search-author", help="Поиск по части имени автора")
+    author.add_argument("query")
     args = parser.parse_args()
     try:
         books = load_books(args.file)
         if args.command == "add":
             add_book(books, args.title, args.author, args.isbn)
             save_books(args.file, books)
-        result = books
+        result = search_author(books, args.query) if args.command == "search-author" else books
         print(json.dumps(result, ensure_ascii=False, indent=2))
     except (OSError, ValueError) as error:
         parser.exit(1, f"Ошибка: {error}\n")
diff --git a/tests/test_books.py b/tests/test_books.py
index 138663a..8b6b23c 100644
--- a/tests/test_books.py
+++ b/tests/test_books.py
@@ -25,3 +25,8 @@ class CatalogTests(unittest.TestCase):
         catalog.pop()
         books.add_book(catalog, "T", "A", "unique")
         self.assertEqual(len(catalog), books.MAX_BOOKS)
+
+    def test_author_search(self):
+        catalog = [{"title": "T", "author": "Михаил Булгаков", "isbn": "1"}]
+        self.assertEqual(books.search_author(catalog, "БУЛГАКОВ"), catalog)
+        self.assertEqual(books.search_author(catalog, "Пушкин"), [])

$ git add books.py tests

$ git diff --staged
diff --git a/books.py b/books.py
index 2730d6f..0b4c50d 100644
--- a/books.py
+++ b/books.py
@@ -40,6 +40,10 @@ def add_book(books, title, author, isbn):
     books.append({"title": title, "author": author, "isbn": isbn})
 
 
+def search_author(books, query):
+    return [book for book in books if query.casefold() in book["author"].casefold()]
+
+
 def main():
     parser = argparse.ArgumentParser(description=__doc__)
     parser.add_argument("--file", type=Path, default=Path("books.json"))
@@ -49,13 +53,15 @@ def main():
     add.add_argument("--title", required=True)
     add.add_argument("--author", required=True)
     add.add_argument("--isbn", required=True)
+    author = commands.add_parser("search-author", help="Поиск по части имени автора")
+    author.add_argument("query")
     args = parser.parse_args()
     try:
         books = load_books(args.file)
         if args.command == "add":
             add_book(books, args.title, args.author, args.isbn)
             save_books(args.file, books)
-        result = books
+        result = search_author(books, args.query) if args.command == "search-author" else books
         print(json.dumps(result, ensure_ascii=False, indent=2))
     except (OSError, ValueError) as error:
         parser.exit(1, f"Ошибка: {error}\n")
diff --git a/tests/test_books.py b/tests/test_books.py
index 138663a..8b6b23c 100644
--- a/tests/test_books.py
+++ b/tests/test_books.py
@@ -25,3 +25,8 @@ class CatalogTests(unittest.TestCase):
         catalog.pop()
         books.add_book(catalog, "T", "A", "unique")
         self.assertEqual(len(catalog), books.MAX_BOOKS)
+
+    def test_author_search(self):
+        catalog = [{"title": "T", "author": "Михаил Булгаков", "isbn": "1"}]
+        self.assertEqual(books.search_author(catalog, "БУЛГАКОВ"), catalog)
+        self.assertEqual(books.search_author(catalog, "Пушкин"), [])

$ git commit -m feat: search catalog by author
[main d9864f4] feat: search catalog by author
 2 files changed, 12 insertions(+), 1 deletion(-)

$ python -m unittest discover -s tests -v
test_add (test_books.CatalogTests.test_add) ... ok
test_author_search (test_books.CatalogTests.test_author_search) ... ok
test_export_cli (test_books.CatalogTests.test_export_cli) ... FAIL
test_limit (test_books.CatalogTests.test_limit) ... ok

======================================================================
FAIL: test_export_cli (test_books.CatalogTests.test_export_cli)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\Admin\Desktop\Учеба\4 курс\ВиПКС\2\library\tests\test_books.py", line 42, in test_export_cli
    self.assertEqual(result.returncode, 0, result.stderr)
AssertionError: 2 != 0 : b"usage: books.py [-h] [--file FILE] {list,add,search-author} ...\r\nbooks.py: error: argument command: invalid choice: 'export' (choose from list, add, search-author)\r\n"

----------------------------------------------------------------------
Ran 4 tests in 0.287s

FAILED (failures=1)

$ python -m unittest discover -s tests -v
test_add (test_books.CatalogTests.test_add) ... ok
test_author_search (test_books.CatalogTests.test_author_search) ... ok
test_export_cli (test_books.CatalogTests.test_export_cli) ... ok
test_limit (test_books.CatalogTests.test_limit) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.253s

OK

$ git diff
diff --git a/books.py b/books.py
index 0b4c50d..16e31c7 100644
--- a/books.py
+++ b/books.py
@@ -55,6 +55,8 @@ def main():
     add.add_argument("--isbn", required=True)
     author = commands.add_parser("search-author", help="Поиск по части имени автора")
     author.add_argument("query")
+    export = commands.add_parser("export", help="Экспортировать список в JSON")
+    export.add_argument("output", type=Path)
     args = parser.parse_args()
     try:
         books = load_books(args.file)
@@ -62,6 +64,10 @@ def main():
             add_book(books, args.title, args.author, args.isbn)
             save_books(args.file, books)
         result = search_author(books, args.query) if args.command == "search-author" else books
+        if args.command == "export":
+            if args.output.resolve() == args.file.resolve():
+                raise ValueError("Выберите отдельный файл для экспорта")
+            save_books(args.output, books)
         print(json.dumps(result, ensure_ascii=False, indent=2))
     except (OSError, ValueError) as error:
         parser.exit(1, f"Ошибка: {error}\n")
diff --git a/tests/test_books.py b/tests/test_books.py
index 8b6b23c..e991b15 100644
--- a/tests/test_books.py
+++ b/tests/test_books.py
@@ -30,3 +30,14 @@ class CatalogTests(unittest.TestCase):
         catalog = [{"title": "T", "author": "Михаил Булгаков", "isbn": "1"}]
         self.assertEqual(books.search_author(catalog, "БУЛГАКОВ"), catalog)
         self.assertEqual(books.search_author(catalog, "Пушкин"), [])
+
+    def test_export_cli(self):
+        with tempfile.TemporaryDirectory() as directory:
+            source = Path(directory) / "books.json"
+            target = Path(directory) / "export.json"
+            catalog = [{"title": "Книга", "author": "Автор", "isbn": "1"}]
+            books.save_books(source, catalog)
+            result = subprocess.run([sys.executable, "books.py", "--file", str(source),
+                                     "export", str(target)], capture_output=True)
+            self.assertEqual(result.returncode, 0, result.stderr)
+            self.assertEqual(books.load_books(target), catalog)

$ git add books.py tests

$ git diff --staged
diff --git a/books.py b/books.py
index 0b4c50d..16e31c7 100644
--- a/books.py
+++ b/books.py
@@ -55,6 +55,8 @@ def main():
     add.add_argument("--isbn", required=True)
     author = commands.add_parser("search-author", help="Поиск по части имени автора")
     author.add_argument("query")
+    export = commands.add_parser("export", help="Экспортировать список в JSON")
+    export.add_argument("output", type=Path)
     args = parser.parse_args()
     try:
         books = load_books(args.file)
@@ -62,6 +64,10 @@ def main():
             add_book(books, args.title, args.author, args.isbn)
             save_books(args.file, books)
         result = search_author(books, args.query) if args.command == "search-author" else books
+        if args.command == "export":
+            if args.output.resolve() == args.file.resolve():
+                raise ValueError("Выберите отдельный файл для экспорта")
+            save_books(args.output, books)
         print(json.dumps(result, ensure_ascii=False, indent=2))
     except (OSError, ValueError) as error:
         parser.exit(1, f"Ошибка: {error}\n")
diff --git a/tests/test_books.py b/tests/test_books.py
index 8b6b23c..e991b15 100644
--- a/tests/test_books.py
+++ b/tests/test_books.py
@@ -30,3 +30,14 @@ class CatalogTests(unittest.TestCase):
         catalog = [{"title": "T", "author": "Михаил Булгаков", "isbn": "1"}]
         self.assertEqual(books.search_author(catalog, "БУЛГАКОВ"), catalog)
         self.assertEqual(books.search_author(catalog, "Пушкин"), [])
+
+    def test_export_cli(self):
+        with tempfile.TemporaryDirectory() as directory:
+            source = Path(directory) / "books.json"
+            target = Path(directory) / "export.json"
+            catalog = [{"title": "Книга", "author": "Автор", "isbn": "1"}]
+            books.save_books(source, catalog)
+            result = subprocess.run([sys.executable, "books.py", "--file", str(source),
+                                     "export", str(target)], capture_output=True)
+            self.assertEqual(result.returncode, 0, result.stderr)
+            self.assertEqual(books.load_books(target), catalog)

$ git commit -m feat: export book list to JSON
[main b129caa] feat: export book list to JSON
 2 files changed, 17 insertions(+)

$ git diff
diff --git a/README.md b/README.md
index a753551..1be5c6c 100644
--- a/README.md
+++ b/README.md
@@ -11,3 +11,17 @@ python books.py list
 Данные — JSON-массив объектов с полями `title`, `author`, `isbn`.
 Рабочий `books.json` исключён из Git; пример хранится в репозитории.
 Для другого каталога: `python books.py --file other.json list`.
+
+## Команды
+
+```powershell
+python books.py add --title "Книга" --author "Автор" --isbn "978-5-17-090630-7"
+python books.py search-author "автор"
+python books.py export exports-list.json
+python -m unittest discover -s tests -v
+```
+
+Поиск автора нечувствителен к регистру. Повторный ISBN, пустые поля и
+превышение лимита отклоняются. Экспорт записывает отдельный JSON-файл;
+его родительский каталог должен существовать. ISBN сравнивается без пробелов
+и дефисов; контрольная сумма ISBN не проверяется.
warning: in the working copy of 'README.md', LF will be replaced by CRLF the next time Git touches it

$ git add README.md
warning: in the working copy of 'README.md', LF will be replaced by CRLF the next time Git touches it

$ git diff --staged
diff --git a/README.md b/README.md
index a753551..1be5c6c 100644
--- a/README.md
+++ b/README.md
@@ -11,3 +11,17 @@ python books.py list
 Данные — JSON-массив объектов с полями `title`, `author`, `isbn`.
 Рабочий `books.json` исключён из Git; пример хранится в репозитории.
 Для другого каталога: `python books.py --file other.json list`.
+
+## Команды
+
+```powershell
+python books.py add --title "Книга" --author "Автор" --isbn "978-5-17-090630-7"
+python books.py search-author "автор"
+python books.py export exports-list.json
+python -m unittest discover -s tests -v
+```
+
+Поиск автора нечувствителен к регистру. Повторный ISBN, пустые поля и
+превышение лимита отклоняются. Экспорт записывает отдельный JSON-файл;
+его родительский каталог должен существовать. ISBN сравнивается без пробелов
+и дефисов; контрольная сумма ISBN не проверяется.

$ git commit -m docs: describe catalog comands
[main 078a153] docs: describe catalog comands
 1 file changed, 14 insertions(+)

$ git commit --amend -m docs: describe catalog commands
[main b78735e] docs: describe catalog commands
 Date: Mon Oct 12 15:44:28 2026 +0300
 1 file changed, 14 insertions(+)

$ git switch -c feature/isbn-search
Switched to a new branch 'feature/isbn-search'

$ python -m unittest discover -s tests -v
test_add (test_books.CatalogTests.test_add) ... ok
test_author_search (test_books.CatalogTests.test_author_search) ... ok
test_export_cli (test_books.CatalogTests.test_export_cli) ... ok
test_isbn_search (test_books.CatalogTests.test_isbn_search) ... ERROR
test_limit (test_books.CatalogTests.test_limit) ... ok

======================================================================
ERROR: test_isbn_search (test_books.CatalogTests.test_isbn_search)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\Admin\Desktop\Учеба\4 курс\ВиПКС\2\library\tests\test_books.py", line 47, in test_isbn_search
    self.assertEqual(books.search_isbn(catalog, "9785170906307"), catalog)
                     ^^^^^^^^^^^^^^^^^
AttributeError: module 'books' has no attribute 'search_isbn'

----------------------------------------------------------------------
Ran 5 tests in 0.294s

FAILED (errors=1)

$ git diff
diff --git a/books.py b/books.py
index 16e31c7..b244faa 100644
--- a/books.py
+++ b/books.py
@@ -44,6 +44,10 @@ def search_author(books, query):
     return [book for book in books if query.casefold() in book["author"].casefold()]
 
 
+def search_isbn(books, query):
+    return [book for book in books if normalize_isbn(book["isbn"]) == normalize_isbn(query)]
+
+
 def main():
     parser = argparse.ArgumentParser(description=__doc__)
     parser.add_argument("--file", type=Path, default=Path("books.json"))
diff --git a/tests/test_books.py b/tests/test_books.py
index e991b15..19fe73b 100644
--- a/tests/test_books.py
+++ b/tests/test_books.py
@@ -41,3 +41,8 @@ class CatalogTests(unittest.TestCase):
                                      "export", str(target)], capture_output=True)
             self.assertEqual(result.returncode, 0, result.stderr)
             self.assertEqual(books.load_books(target), catalog)
+
+    def test_isbn_search(self):
+        catalog = [{"title": "T", "author": "A", "isbn": "978-5-17-090630-7"}]
+        self.assertEqual(books.search_isbn(catalog, "9785170906307"), catalog)
+        self.assertEqual(books.search_isbn(catalog, "missing"), [])

$ git add books.py tests

$ git diff --staged
diff --git a/books.py b/books.py
index 16e31c7..b244faa 100644
--- a/books.py
+++ b/books.py
@@ -44,6 +44,10 @@ def search_author(books, query):
     return [book for book in books if query.casefold() in book["author"].casefold()]
 
 
+def search_isbn(books, query):
+    return [book for book in books if normalize_isbn(book["isbn"]) == normalize_isbn(query)]
+
+
 def main():
     parser = argparse.ArgumentParser(description=__doc__)
     parser.add_argument("--file", type=Path, default=Path("books.json"))
diff --git a/tests/test_books.py b/tests/test_books.py
index e991b15..19fe73b 100644
--- a/tests/test_books.py
+++ b/tests/test_books.py
@@ -41,3 +41,8 @@ class CatalogTests(unittest.TestCase):
                                      "export", str(target)], capture_output=True)
             self.assertEqual(result.returncode, 0, result.stderr)
             self.assertEqual(books.load_books(target), catalog)
+
+    def test_isbn_search(self):
+        catalog = [{"title": "T", "author": "A", "isbn": "978-5-17-090630-7"}]
+        self.assertEqual(books.search_isbn(catalog, "9785170906307"), catalog)
+        self.assertEqual(books.search_isbn(catalog, "missing"), [])

$ git commit -m feat: implement normalized ISBN lookup
[feature/isbn-search c02c3b7] feat: implement normalized ISBN lookup
 2 files changed, 9 insertions(+)

$ python -m unittest discover -s tests -v
test_add (test_books.CatalogTests.test_add) ... ok
test_author_search (test_books.CatalogTests.test_author_search) ... ok
test_export_cli (test_books.CatalogTests.test_export_cli) ... ok
test_isbn_search (test_books.CatalogTests.test_isbn_search) ... ok
test_limit (test_books.CatalogTests.test_limit) ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.270s

OK

$ git diff
diff --git a/README.md b/README.md
index 1be5c6c..9ebaf7b 100644
--- a/README.md
+++ b/README.md
@@ -25,3 +25,5 @@ python -m unittest discover -s tests -v
 превышение лимита отклоняются. Экспорт записывает отдельный JSON-файл;
 его родительский каталог должен существовать. ISBN сравнивается без пробелов
 и дефисов; контрольная сумма ISBN не проверяется.
+
+Поиск по ISBN: `python books.py search-isbn "9785170906307"`.
diff --git a/books.py b/books.py
index b244faa..5659a15 100644
--- a/books.py
+++ b/books.py
@@ -61,6 +61,8 @@ def main():
     author.add_argument("query")
     export = commands.add_parser("export", help="Экспортировать список в JSON")
     export.add_argument("output", type=Path)
+    isbn = commands.add_parser("search-isbn", help="Поиск по ISBN")
+    isbn.add_argument("query")
     args = parser.parse_args()
     try:
         books = load_books(args.file)
@@ -68,6 +70,8 @@ def main():
             add_book(books, args.title, args.author, args.isbn)
             save_books(args.file, books)
         result = search_author(books, args.query) if args.command == "search-author" else books
+        if args.command == "search-isbn":
+            result = search_isbn(books, args.query)
         if args.command == "export":
             if args.output.resolve() == args.file.resolve():
                 raise ValueError("Выберите отдельный файл для экспорта")
warning: in the working copy of 'README.md', LF will be replaced by CRLF the next time Git touches it

$ git add books.py README.md
warning: in the working copy of 'README.md', LF will be replaced by CRLF the next time Git touches it

$ git diff --staged
diff --git a/README.md b/README.md
index 1be5c6c..9ebaf7b 100644
--- a/README.md
+++ b/README.md
@@ -25,3 +25,5 @@ python -m unittest discover -s tests -v
 превышение лимита отклоняются. Экспорт записывает отдельный JSON-файл;
 его родительский каталог должен существовать. ISBN сравнивается без пробелов
 и дефисов; контрольная сумма ISBN не проверяется.
+
+Поиск по ISBN: `python books.py search-isbn "9785170906307"`.
diff --git a/books.py b/books.py
index b244faa..5659a15 100644
--- a/books.py
+++ b/books.py
@@ -61,6 +61,8 @@ def main():
     author.add_argument("query")
     export = commands.add_parser("export", help="Экспортировать список в JSON")
     export.add_argument("output", type=Path)
+    isbn = commands.add_parser("search-isbn", help="Поиск по ISBN")
+    isbn.add_argument("query")
     args = parser.parse_args()
     try:
         books = load_books(args.file)
@@ -68,6 +70,8 @@ def main():
             add_book(books, args.title, args.author, args.isbn)
             save_books(args.file, books)
         result = search_author(books, args.query) if args.command == "search-author" else books
+        if args.command == "search-isbn":
+            result = search_isbn(books, args.query)
         if args.command == "export":
             if args.output.resolve() == args.file.resolve():
                 raise ValueError("Выберите отдельный файл для экспорта")

$ git commit -m feat: expose ISBN search command and usage
[feature/isbn-search d6b4c1b] feat: expose ISBN search command and usage
 2 files changed, 6 insertions(+)

$ git switch main
Switched to branch 'main'

$ git merge --no-ff feature/isbn-search -m merge: add ISBN search
Merge made by the 'ort' strategy.
 README.md           | 2 ++
 books.py            | 8 ++++++++
 tests/test_books.py | 5 +++++
 3 files changed, 15 insertions(+)

$ git branch -d feature/isbn-search
Deleted branch feature/isbn-search (was d6b4c1b).

$ git log --graph --oneline --decorate --all
*   7f71c80 (HEAD -> main) merge: add ISBN search
|\  
| * d6b4c1b feat: expose ISBN search command and usage
| * c02c3b7 feat: implement normalized ISBN lookup
|/  
* b78735e docs: describe catalog commands
* b129caa feat: export book list to JSON
* d9864f4 feat: search catalog by author
* 5b71829 feat: add books with duplicate and capacity validation
* 1f83538 docs: describe startup and catalog format
* 61c4ec9 feat: initialize JSON book catalog
* 993155c chore: add ignore rules

$ git switch -c change/a
Switched to a new branch 'change/a'

$ git diff
diff --git a/books.py b/books.py
index 5659a15..c59d8c1 100644
--- a/books.py
+++ b/books.py
@@ -3,7 +3,7 @@ import argparse
 import json
 from pathlib import Path
 
-MAX_BOOKS = 50
+MAX_BOOKS = 100
 
 
 def load_books(path):

$ git add books.py

$ git diff --staged
diff --git a/books.py b/books.py
index 5659a15..c59d8c1 100644
--- a/books.py
+++ b/books.py
@@ -3,7 +3,7 @@ import argparse
 import json
 from pathlib import Path
 
-MAX_BOOKS = 50
+MAX_BOOKS = 100
 
 
 def load_books(path):

$ git commit -m config: limit catalog to 100 books
[change/a fa6f96b] config: limit catalog to 100 books
 1 file changed, 1 insertion(+), 1 deletion(-)

$ git switch main
Switched to branch 'main'

$ git switch -c change/b
Switched to a new branch 'change/b'

$ git diff
diff --git a/books.py b/books.py
index 5659a15..e7c94a9 100644
--- a/books.py
+++ b/books.py
@@ -3,7 +3,7 @@ import argparse
 import json
 from pathlib import Path
 
-MAX_BOOKS = 50
+MAX_BOOKS = 500
 
 
 def load_books(path):

$ git add books.py

$ git diff --staged
diff --git a/books.py b/books.py
index 5659a15..e7c94a9 100644
--- a/books.py
+++ b/books.py
@@ -3,7 +3,7 @@ import argparse
 import json
 from pathlib import Path
 
-MAX_BOOKS = 50
+MAX_BOOKS = 500
 
 
 def load_books(path):

$ git commit -m config: limit catalog to 500 books
[change/b b89cf71] config: limit catalog to 500 books
 1 file changed, 1 insertion(+), 1 deletion(-)

$ git switch main
Switched to branch 'main'

$ git merge change/a
Updating 7f71c80..fa6f96b
Fast-forward
 books.py | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)

$ git merge change/b
Auto-merging books.py
CONFLICT (content): Merge conflict in books.py
Automatic merge failed; fix conflicts and then commit the result.

$ git status
On branch main
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)
	both modified:   books.py

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	COMMANDS.md

no changes added to commit (use "git add" and/or "git commit -a")

$ git diff
diff --cc books.py
index c59d8c1,e7c94a9..0000000
--- a/books.py
+++ b/books.py
@@@ -3,7 -3,7 +3,11 @@@ import argpars
  import json
  from pathlib import Path
  
++<<<<<<< HEAD
 +MAX_BOOKS = 100
++=======
+ MAX_BOOKS = 500
++>>>>>>> change/b
  
  
  def load_books(path):

$ python -m unittest discover -s tests -v
test_add (test_books.CatalogTests.test_add) ... ok
test_author_search (test_books.CatalogTests.test_author_search) ... ok
test_export_cli (test_books.CatalogTests.test_export_cli) ... ok
test_isbn_search (test_books.CatalogTests.test_isbn_search) ... ok
test_limit (test_books.CatalogTests.test_limit) ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.283s

OK

$ git diff
diff --cc books.py
index c59d8c1,e7c94a9..0000000
--- a/books.py
+++ b/books.py
diff --git a/README.md b/README.md
index 9ebaf7b..c7ade42 100644
--- a/README.md
+++ b/README.md
@@ -27,3 +27,6 @@ python -m unittest discover -s tests -v
 и дефисов; контрольная сумма ISBN не проверяется.
 
 Поиск по ISBN: `python books.py search-isbn "9785170906307"`.
+
+Каталог содержит максимум **500 книг**. При достижении лимита добавление
+завершается ошибкой, существующие данные сохраняются.

$ git add books.py README.md

$ git diff --staged
diff --git a/README.md b/README.md
index 9ebaf7b..c7ade42 100644
--- a/README.md
+++ b/README.md
@@ -27,3 +27,6 @@ python -m unittest discover -s tests -v
 и дефисов; контрольная сумма ISBN не проверяется.
 
 Поиск по ISBN: `python books.py search-isbn "9785170906307"`.
+
+Каталог содержит максимум **500 книг**. При достижении лимита добавление
+завершается ошибкой, существующие данные сохраняются.
diff --git a/books.py b/books.py
index c59d8c1..e7c94a9 100644
--- a/books.py
+++ b/books.py
@@ -3,7 +3,7 @@ import argparse
 import json
 from pathlib import Path
 
-MAX_BOOKS = 100
+MAX_BOOKS = 500
 
 
 def load_books(path):

$ git commit -m merge: resolve catalog limit to 500 books
[main dec8a5b] merge: resolve catalog limit to 500 books

$ git switch -c recovery-demo
Switched to a new branch 'recovery-demo'

$ git status --short
 M books.py
?? COMMANDS.md

$ git diff
diff --git a/books.py b/books.py
index e7c94a9..b1bcd48 100644
--- a/books.py
+++ b/books.py
@@ -3,7 +3,7 @@ import argparse
 import json
 from pathlib import Path
 
-MAX_BOOKS = 500
+MAX_BOOKS = 1
 
 
 def load_books(path):

$ git restore books.py

$ git status --short
?? COMMANDS.md

$ git diff

$ python -m unittest discover -s tests -v
test_add (test_books.CatalogTests.test_add) ... ok
test_author_search (test_books.CatalogTests.test_author_search) ... ok
test_export_cli (test_books.CatalogTests.test_export_cli) ... ok
test_isbn_search (test_books.CatalogTests.test_isbn_search) ... ok
test_limit (test_books.CatalogTests.test_limit) ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.220s

OK

$ git switch main
Switched to branch 'main'

```
