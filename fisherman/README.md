# fisherman

**Директория:** `fisherman/`

## Назначение

`Fisherman` — координационный слой навигации. Он не хранит собственный state-machine: вместо этого связывает:

- `Gps`;
- `Destination`;
- `ESOLocateCapture`;
- `YetAnotherCompassCapture`;
- `Rotation`.

Основной файл: `fisherman/fisherman.py`.

## Методы

### `set_current_position()`

Если координаты не переданы, вызывает `update_current_position()`, затем записывает результат в `Gps.current_position`.

### `set_destination_point()`

Если destination не передан, вызывает `Destination.get_destination_point()`. Результат записывается в
`Gps.current_destination`.

### `update_current_position()`

Выполняет:

```text
ESOLocateCapture.get_cap()
        ↓
ESOLocateCapture.segmentation()
        ↓
ESOLocateCapture.get_current_position()
```

### `update_current_compas_direction()`

Выполняет:

```text
YetAnotherCompassCapture.get_cap()
        ↓
segmentation()
        ↓
get_cardinal_directions()
        ↓
get_tip()
        ↓
get_compas_direction()
        ↓
Rotation.get_degree((0,0), direction)
```

### `direction_of_view()`

1. Берёт current position и destination.
2. Рассчитывает целевой угол через `Rotation.get_degree()`.
3. Инвертирует ось через `Rotation.x_invert_degree()`.
4. Получает текущий угол компаса.
5. Рассчитывает correction через `Rotation.calibration()`.
6. Двигает мышь.
7. Повторно измеряет компас и рассчитывает residual correction.
8. При выполнении условной ветки может попытаться сделать вторую коррекцию.

### Текущая проблема

Проверка второй коррекции написана как:

```python
if -5 > Rotation.p2d(calibration) > 5:
```

Такое условие не может стать истинным. Вероятно, здесь подразумевался диапазон по модулю.

## Чего здесь пока нет

Нет единого метода уровня `move_to_destination()`, который полностью реализовал бы маршрут:

`set target → rotate → walk → re-read position → correct → check arrival → stop`.

Этот сценарий сейчас существует в основном в `tests/test_moving.py` как runtime/integration logic.
