# screenCapture

**Директория:** `screenCapture/`

## Назначение

Низкоуровневое получение изображения с экрана и специализированное выделение областей ESOlocate/YetAnotherCompass.

## `screen_capture.py`

Базовый класс `ScreeCapture`.

### `get_cap(left, top, right, bottom)`

Дважды делает `ImageGrab.grab()` одной и той же областью:

- `start_capture` — первый снимок;
- `capture` — второй снимок.

Это class-level состояние.

### `segmentation(color_error=1)`

Проходит по каждому пикселю и превращает изображение в бинарную матрицу, если RGB близок к `main_color`.

Это очень простой pixel-level segmentation, без OpenCV/морфологии.

## `eso_locate_capture.py`

`ESOLocateCapture` берёт координаты окна из `ESOLocateParser`, делает capture, затем дополнительно вырезает область:

```text
rows 5:18
cols 110:190
```

После segmentation распознаёт цифры по маскам из `eso_locate_masks.json`.

`get_current_position()` возвращает tuple из найденных чисел в формате `float`.

## `yet_another_compass_capture.py`

`YetAnotherCompassCapture` работает с квадратным окном компаса.

### `CardinalDirections`

```text
LEFT / RIGHT / TOP / BOTTOM
```

### `get_cardinal_directions()`

Сравнивает сумму пикселей в четырёх краевых областях и выбирает сторону с максимумом.

### `get_tip()`

По выбранной стороне проходит матрицу в нужном направлении и ищет первый пиксель со значением `1`.

### `get_compas_direction()`

Переносит tip относительно центра изображения и возвращает вектор направления.

## Источники capture

В runtime границы окон определяются через Lua parsers. В тестах границы остаются теми же, но изображение подменяется fixture-файлом.

## Основное ограничение

Capture и segmentation ориентированы на конкретный вид UI аддонов, разрешение и цвет. Изменение темы, размера, позиции или визуального стиля аддона может потребовать новых масок/параметров.
