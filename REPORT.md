# Отчёт — вариант 2

Дата: 12 октября 2026 года.
Тема: каталог книг.
Репозиторий: https://github.com/Comper123/library

## 1. Создание репозитория

В папке library создал репозиторий командой `git init -b main`.
Настроил имя Ilia и почту ibarishnikov07@mail.ru для этого репозитория.
Сделал три начальных коммита: .gitignore, books.py, затем README.md и books.json.example.
Рабочий books.json, временные файлы и кеш Python добавил в .gitignore.

## 2. Добавление функций

Добавил книгу, поиск по автору и экспорт списка в JSON.
Каждую функцию сохранил отдельным коммитом. Сначала написал тесты,
затем добавил код и проверил результат. Инструкцию по запуску сохранил отдельно.
Перед коммитами смотрел изменения через `git diff` и `git diff --staged`.
Опечатку в последнем сообщении исправил командой:

```powershell
git commit --amend -m "docs: describe catalog commands"
```

## 3. Поиск по ISBN

Создал ветку feature/isbn-search. Сделал два коммита:
сначала добавил функцию поиска, затем команду запуска и описание в README.
При поиске пробелы и дефисы в ISBN не учитываются.
После проверки объединил ветку с main и удалил её:

```powershell
git merge --no-ff feature/isbn-search -m "merge: add ISBN search"
git branch -d feature/isbn-search
git log --graph --oneline --decorate --all
```

## 4. Конфликт при слиянии

От одной точки создал ветки change/a и change/b.
В первой изменил MAX_BOOKS с 50 на 100, во второй — с 50 на 500.
Сначала объединил main с change/a, затем с change/b.
При втором слиянии возник конфликт: обе ветки меняли одну строку.
Убрал маркеры конфликта и оставил MAX_BOOKS = 500.
В README написал, что можно хранить не больше 500 книг.
Проверил тестами: при 499 книгах добавление работает, при 500 — выдаёт ошибку.
После проверки завершил слияние коммитом.

## 5. GitHub и восстановление файла

Подключил GitHub и отправил main, change/a, change/b и recovery-demo.
Создал аннотированную метку v0.5.0 и тоже отправил её:

```powershell
git remote add origin https://github.com/Comper123/library.git
git push -u origin main change/a change/b recovery-demo
git tag -a v0.5.0 -m "Educational book catalog release 0.5.0"
git push origin v0.5.0
```

В ветке recovery-demo временно изменил MAX_BOOKS с 500 на 1, без коммита.
Через `git status --short` и `git diff` посмотрел изменение.
Выполнил `git restore books.py`. Лимит снова стал 500,
а `git diff` перестал показывать изменения файла.
Использовал git restore для отмены изменения, которое ещё не попало в коммит.
История коммитов осталась прежней. После проверки вернулся в main.

## Результат

Все 5 тестов прошли:

```powershell
python -m unittest discover -s tests -v
```

Команды, граф коммитов и вывод при конфликте записаны в COMMANDS.md.
