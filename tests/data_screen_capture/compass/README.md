# tests/data_screen_capture/compass

**Директория:** `tests/data_screen_capture/compass/`

## Назначение

Fixture-изображения окна YetAnotherCompass для проверки распознавания направления.

## Файлы

- `top_3.jpeg`
- `bottom_3.jpeg`
- `left_3.jpeg`
- `right_3.jpeg`
- `left_top_3.jpeg`
- `left_bottom_3.jpeg`
- `right_top_3.jpeg`
- `right_bottom_3.jpeg`

Имя файла кодирует ожидаемое грубое направление наконечника.

## Как используются

`tests/conftest.py::yet_another_compass_capture`:

1. открывает fixture;
2. вырезает область по координатам parser;
3. сохраняет в `YetAnotherCompassCapture.capture`;
4. выполняет segmentation с `color_error=13`.

`tests/test_screen_capture.py` затем независимо проверяет:

- cardinal direction;
- tip coordinate;
- compass vector.
