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
