# Каталог книг — вариант 2

Практическая работа № 2: управление версиями и изменениями с Git и GitHub.
Требуется Python 3.10 или новее, внешних зависимостей нет.

```powershell
Copy-Item books.json.example books.json
python books.py list
```

Данные — JSON-массив объектов с полями `title`, `author`, `isbn`.
Рабочий `books.json` исключён из Git; пример хранится в репозитории.
Для другого каталога: `python books.py --file other.json list`.

## Команды

```powershell
python books.py add --title "Книга" --author "Автор" --isbn "978-5-17-090630-7"
python books.py search-author "автор"
python books.py export exports-list.json
python -m unittest discover -s tests -v
```

Поиск автора нечувствителен к регистру. Повторный ISBN, пустые поля и
превышение лимита отклоняются. Экспорт записывает отдельный JSON-файл;
его родительский каталог должен существовать. ISBN сравнивается без пробелов
и дефисов; контрольная сумма ISBN не проверяется.

Поиск по ISBN: `python books.py search-isbn "9785170906307"`.

Каталог содержит максимум **500 книг**. При достижении лимита добавление
завершается ошибкой, существующие данные сохраняются.
