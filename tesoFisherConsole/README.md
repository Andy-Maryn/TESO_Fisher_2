# tesoFisherConsole

**Директория:** `tesoFisherConsole/`

## Назначение

Это текущая реализация самого простого рабочего рыболовного цикла: отслеживание уровня аудиовыхода и отправка `E` при превышении порога.

Файл: `tesoFisherConsole/teso_fisher_console.py`.

## Основные константы

```python
DEVICE_NAME = "Динамики (Realtek(R) Audio)"
MIN_PEAK_VOLUME = 0.45
```

Обратите внимание: CLI параметр `--min_peak_volume` ожидает шкалу 0..99 и переводит её в 0..1.

## Выбор аудиоустройства

`get_list_of_devices()` перебирает `pyWinCoreAudio.AudioDevices` и берёт render endpoints только с form factor `Headphones` или `Speakers`.

`get_device_by_name()` и `get_device_by_id()` возвращают endpoint.

## Детектор события

`get_peak_value(dev)` просто возвращает:

```python
dev.volume.peak_meter.peak_value
```

Никакого фильтра, debounce, edge detection или усреднения сейчас нет.

## `action()`

Действие на обнаруженное событие:

```text
E
wait 1 sec
E
```

Это используется как универсальное действие для текущего прототипа — код не различает «заброс» и «подсечку» на уровне состояния.

## `loop()`

Бесконечный loop:

```text
read peak
  |
  +-- >= min_pv --> log + action()
  |
  +-- < min_pv  --> continue
```

## CLI

Модуль можно запускать как standalone script. `parser()` поддерживает:

- `--device_name`;
- `--device_id`;
- `--min_peak_volume`;
- `--log`.

## Связь с GUI

GUI импортирует:

- `get_list_of_devices`;
- `get_peak_value`;
- `action`;
- `get_device_by_name`;
- `DEVICE_NAME`.

Однако сам GUI не использует `loop()` — он создаёт собственный `multiprocessing.Process` (`UI.Fisher`) с почти той же логикой.

## Будущая точка интеграции

Историческое ТЗ предполагает image-based state machine. Этот модуль логично оставить низкоуровневым драйвером «нажать клавишу»/«получить audio signal», а decision logic перенести в отдельный state machine, когда она будет реализована.
