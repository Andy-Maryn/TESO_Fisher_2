# tests

**Директория:** `tests/`

## Назначение

Pytest suite для unit, image-based и runtime/integration проверок.

## Структура

- `conftest.py` — fixtures, переключение источников данных, HTML extras, проверка TESO process.
- `common.py` — общие импорты и константы путей.
- `test_destination.py` — выбор destination и переходы графа.
- `test_gps.py` — расстояние/проверки GPS.
- `test_lua_parser.py` — парсеры SavedVariables.
- `test_screen_capture.py` — распознавание координат и компаса по сохранённым изображениям.
- `test_rotation.py` — геометрия углов и runtime calibration.
- `test_moving.py` — реальные runtime/integration сценарии движения.
- `main.py` — старый пример ручного исполнения цепочки.

## Как тесты подставляют данные

Fixture `data_path` временно устанавливает:

```text
LuaParser._root = tests/lua
AdjacencyMatrixParser._root = tests/matrix
```

После тестовой сессии Lua root восстанавливается к Windows SavedVariables path.

`load_test_data` загружает:

- ESOlocate parser;
- конкретного пользователя `BendreTolstyy`;
- YetAnotherCompass parser;
- adjacency matrix;
- Destination graph.

## `TESO_RUNNING`

`conftest.py` проверяет процесс `eso64.exe` через `psutil`.

Runtime тесты помечены `skipif` и запускаются только если TESO уже работает.

## Image fixtures

`tests/data_screen_capture/` содержит реальные снимки GUI аддонов, поэтому image tests не требуют запуска игры.

## HTML report

В тестах используются `pytest_html.extras` для прикрепления исходных и сегментированных изображений.

## Что считать «хорошим» тестом здесь

Для parser/capture модулей полезны fixture-driven tests с детерминированным результатом.

Для keyboard/mouse/navigation нужны integration tests, которые явно помечены как требующие запущенной игры.

Для будущего fishing state machine нужно добавить тесты без зависимости от реального аудиоустройства и клавиатуры — через mock/stub event source.
