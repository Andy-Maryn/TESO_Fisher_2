# moving

**Директория:** `moving/`

## Назначение

Содержит низкоуровневые функции управления положением персонажа:

- `gps.py` — координаты, расстояние и проверка достижения;
- `walking.py` — клавиша движения;
- `rotation/` — расчёт и управление поворотом.

## `Gps`

Class-level state:

```python
Gps.current_position
Gps.current_destination
Gps.error
```

`get_current_position()` повторно снимает ESOlocate в течение указанного `wait`, пока не получит непустой результат.

`get_distance()` использует `math.hypot()`.

`is_it_destination_point(d=0.05)` возвращает `True`, если расстояние меньше `d`.

## `Walking`

Очень тонкая обёртка над `keyboard`:

- `start()` → `keyboard.press('w')`;
- `stop()` → `keyboard.release('w')`.

Здесь нет логики курса, столкновений или проверки того, что персонаж реально движется.

## `rotation/`

См. `moving/rotation/README.md`.

## Runtime-сценарий

Полный пример движения сейчас находится в `tests/test_moving.py`, а не в production class.
