# tests/data_screen_capture/locate

**Директория:** `tests/data_screen_capture/locate/`

## Назначение

Fixture-изображения ESOlocate.

Имена файлов кодируют ожидаемые координаты, например `4669_7987.jpeg` соответствует примерно `(46.69, 79.87)`.

## Как используются

Fixture `eso_locate_capture` в `tests/conftest.py`:

1. открывает изображение;
2. обрезает область ESOlocate по координатам parser;
3. дополнительно вырезает область цифр `[5:18, 110:190]`;
4. делает segmentation с `color_error=20`.

Далее `ESOLocateCapture.get_current_position()` распознаёт цифры по маскам.

## Важная практика

При изменении шрифта/масштаба/позиции ESOlocate нужно заново создавать fixtures и проверять `eso_locate_masks.json`.
