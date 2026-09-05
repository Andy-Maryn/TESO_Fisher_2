# luaParser

**Директория:** `luaParser/`

## Назначение

Парсинг `SavedVariables` аддонов TESO. Код не парсит Lua полноценным Lua-интерпретатором: он выполняет ограниченное
текстовое преобразование Lua-подобной структуры в JSON, после чего использует `json.loads()`.

## `lua_parser.py`

`LuaParser` — базовый loader.

### Источник данных

По умолчанию:

```text
C:\Users\Andrii\Documents\Elder Scrolls Online\live\SavedVariables
```

Файл определяется как `cls._root / cls.lua_file_name`.

### `load_data()`

Подход:

1. прочитать файл целиком;
2. удалить пробелы и переводы строк;
3. заменить несколько Lua-синтаксических конструкций на JSON-подобные;
4. взять текст от первого `{`;
5. вызвать `json.loads()`.

Это хрупкий, но простой parser для конкретного формата SavedVariables.

## `common.py`

Содержит:

- WinAPI-доступ к размерам экрана;
- `XPosition` и `YPosition` для вычисления положения окон;
- `eso_coordinate_to_screen_position()` — маппинг sector в экранную область;
- `search()` — рекурсивный поиск ключа в словаре;
- `set_lua_values()` — перенос значений из словаря в dataclass.

При импорте вызывается `ctypes.windll.user32`, поэтому модуль Windows-only.

## `eso_locate.py`

Dataclass `ESOLocate` содержит:

- `x_position`;
- `y_position`;
- `sector`;
- `sector2`;
- `version`.

Маппинг соответствует структуре `ESOlocate.lua`.

## `eso_locate_parser.py`

`ESOLocateParser` знает, что файл называется `ESOlocate.lua`.

`load_data()` → `get_eso_locate()`.

`get_eso_locate()` ищет ветку `Default`, затем первого account/user и строит словарь `character -> ESOLocate`.

`set_user_property(user)` выбирает персонажа и вычисляет `left/top/right/bottom` окна ESOlocate через
`eso_coordinate_to_screen_position()`.

## `account_wide.py`

Dataclass `AccountWide` описывает общую конфигурацию YetAnotherCompass: position, centered, size, compassStyle, version.

## `yet_another_compass_parser.py`

`YetAnotherCompassParser` читает `YetAnotherCompass.lua`, получает `AccountWide`, затем рассчитывает границы квадратного
окна компаса:

```text
left = x
top = y
right = x + size
bottom = y + size
```

## Тестовое переключение источника

`tests/conftest.py` временно меняет `LuaParser._root` на `tests/lua/`, поэтому тесты используют fixture-файлы, а не
реальный SavedVariables каталог пользователя.
