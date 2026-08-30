# tools/draw_graph

**Директория:** `tools/draw_graph/`

## Назначение

Эксперименты с визуализацией графа маршрутов.

## Файлы

### `draw_graph.py`

Задуман для загрузки adjacency data и отображения `networkx.DiGraph` через matplotlib.

В текущем файле есть несогласованность путей/форматов загрузки: сначала формируется путь к CSV, а затем используется `np.load()` с тем же CSV path как будто это NPZ. Поэтому это скорее исторический эксперимент, чем надёжный production tool.

### `reload_map.py`

Содержит hard-coded пример `map_destination` и `destination_points`, а затем сохраняет их в:

```text
adjacency_matrix.npz
```

## `adjacency_matrix.npz`

Бинарный артефакт с сохранёнными numpy-массивами.

## Практическое использование

Если нужно изменить маршрутную карту, сначала редактируйте production `matrix/adjacency_matrix.csv`, затем при необходимости используйте tool для визуализации/генерации производных данных.
