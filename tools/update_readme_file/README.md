# tools/update_readme_file

**Директория:** `tools/update_readme_file/`

## Назначение

Исторический script для автоматической вставки содержимого `doc/requirements.csv` и `doc/test_cases.csv` в секцию корневого README.

## `update_readme_file.py`

Скрипт:

1. читает `doc/requirements.csv`;
2. читает `doc/test_cases.csv`;
3. читает root `README.md`;
4. находит секцию между `### 3.2 Тестовая спецификация` и `___`;
5. заменяет её CSV-текстом;
6. записывает README обратно.

## Почему сейчас осторожно

Этот механизм синхронизирует только старую статическую документацию. Он не сопоставляет requirements с pytest-кодом и не знает фактического статуса реализации.

Для будущего проекта лучше перейти к трассировке:

```text
Requirement ID -> source code -> pytest test -> status
```

и генерировать documentation из единого структурированного источника.
