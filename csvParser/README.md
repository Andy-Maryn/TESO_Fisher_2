# csvParser

**Директория:** `csvParser/`

## Назначение

Небольшой слой загрузки CSV-файлов в Python-структуры.

## `csv_parser.py`

`CsvParser` — базовый parser.

### Механизм

`load_data()`:

- открывает `cls.path` с UTF-8;
- использует `csv.reader` с разделителем `|`;
- первая строка становится `headers`;
- остальные строки превращаются в `dict[str, str]`.

`path` строится как `cls._root / cls.csv_file_name`. По умолчанию `_root = ROOT_DIR / doc`.

## `adjacency_matrix.py`

`AdjacencyMatrixParser` наследует `CsvParser`, но переопределяет root на `matrix/`.

После загрузки формирует:

- `destination_points`: `index -> (x, y)`;
- `map_destination`: список строк матрицы смежности;
- `is_destination`: `index -> bool`.

`destination_point` сейчас разбирается через `eval()`. Это означает, что CSV считается доверенным входом.

## `requirements_parser.py`

`RequirementsParser` читает `doc/requirements.csv` и записывает описания в dataclass `Requirements` только для полей,
существующих в `Requirements.__annotations__`.

### Важное ограничение

Dataclass сейчас содержит только:

- `FRS_TESO_FISHER_010000`
- `FRS_TESO_FISHER_010100`
- `FRS_TESO_FISHER_010101`
- `FRS_TESO_FISHER_010102`
- `FRS_TESO_FISHER_010103`

Поэтому остальные requirements физически читаются из CSV, но не становятся атрибутами `Requirements`.

## Где используется

- `AdjacencyMatrixParser` → `matrix.Destination`.
- `RequirementsParser` → pytest marker output в `tests/conftest.py`.
- `CsvParser` → общий базовый механизм.
