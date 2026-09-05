# tests/lua

**Директория:** `tests/lua/`

## Назначение

Минимальные SavedVariables-файлы, используемые вместо реального ESO профиля в тестах.

- `ESOlocate.lua`
- `YetAnotherCompass.lua`

Они нужны для deterministic parser tests и не должны содержать секреты пользователя.

## Связь с production

В production `LuaParser._root` указывает на системный каталог SavedVariables. В тестах `conftest.py` временно
переключает root на эту директорию.
